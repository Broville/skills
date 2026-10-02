"""Security regression tests, with synthetic files and an offline fake TLS MQTT printer."""
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import zipfile

import core
from core import Device, Refused, Service, inspect_artifact, load_registry, monitor, normalize_status, packet, read_packet
from server import serve

HERE = Path(__file__).resolve().parent


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.service = Service(artifact_root=self.root, demo=True)

    def tearDown(self):
        self.temp.cleanup()

    def archive(self, members, name='job.3mf'):
        path = self.root / name
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            for member, data in members.items():
                z.writestr(member, data)
        return path

    def test_bounded_inspection_and_binding(self):
        if os.name != 'posix':
            self.skipTest('Secure artifact access currently supports POSIX only')
        self.archive({'Metadata/plate_1.gcode': 'G28\n', '[Content_Types].xml': '<Types/>'})
        inspected = inspect_artifact(self.root, 'job.3mf')
        self.assertEqual(inspected['candidate_plates'], [1])
        self.assertFalse(inspected['printable_verified'])
        a = self.service.preview('demo-p2s-a','start','job.3mf',{'plate':1,'use_ams':True,'ams_mapping':[0,1]})
        b = self.service.preview('demo-p2s-b','start','job.3mf',{'plate':1,'use_ams':True,'ams_mapping':[0,1]})
        self.assertNotEqual(a['plan_sha256'],b['plan_sha256'])
        self.assertFalse(a['executable'])
        self.assertTrue(a['approval_required'])
        self.archive({'Metadata/plate_1.gcode':'G28\nG1 X10\n'})
        c=self.service.preview('demo-p2s-a','start','job.3mf',{'plate':1,'use_ams':True,'ams_mapping':[0,1]})
        self.assertNotEqual(a['plan_sha256'],c['plan_sha256'])

    def test_path_traversal_and_missing_root(self):
        for name in ('../secret.3mf','/etc/passwd.3mf','C:/secret.3mf','x\\secret.3mf','x//y.3mf','x/./y.3mf','x\n.3mf'):
            with self.subTest(name=name),self.assertRaises(Refused):
                inspect_artifact(self.root,name)
        with self.assertRaises(Refused):
            inspect_artifact(None,'job.3mf')

    @unittest.skipUnless(os.name=='posix','POSIX secure open')
    def test_symlink_and_fifo_refused(self):
        (self.root/'outside.gcode').write_text('G28\n')
        (self.root/'link.gcode').symlink_to(self.root/'outside.gcode')
        with self.assertRaises(Refused):inspect_artifact(self.root,'link.gcode')
        (self.root/'directory').mkdir()
        (self.root/'linkdir').symlink_to(self.root/'directory',target_is_directory=True)
        with self.assertRaises(Refused):inspect_artifact(self.root,'linkdir/job.3mf')
        os.mkfifo(self.root/'pipe.gcode')
        with self.assertRaises(Refused):inspect_artifact(self.root,'pipe.gcode')

    @unittest.skipUnless(os.name=='posix','POSIX secure open')
    def test_archive_traversal_bomb_and_links(self):
        for members in ({'../escape':'x'},{'/absolute':'x'}, {'Metadata/plate_1.gcode':'0'*100000}, {'a':'x','A':'y'}):
            self.archive(members)
            with self.assertRaises(Refused):inspect_artifact(self.root,'job.3mf')
        info=zipfile.ZipInfo('link');info.external_attr=0o120777<<16
        with zipfile.ZipFile(self.root/'job.3mf','w') as z:z.writestr(info,'target')
        with self.assertRaises(Refused):inspect_artifact(self.root,'job.3mf')
        self.archive({'a':'abc','b':'abc'})
        with patch.object(core,'MAX_ENTRIES',1),self.assertRaises(Refused):inspect_artifact(self.root,'job.3mf')
        with patch.object(core,'MAX_INFLATED',1),self.assertRaises(Refused):inspect_artifact(self.root,'job.3mf')
        with patch.object(core,'MAX_MEMBER',1),self.assertRaises(Refused):inspect_artifact(self.root,'job.3mf')

    def test_no_control_or_auto_enrollment(self):
        with patch('core.socket.create_connection',side_effect=AssertionError('Network forbidden')):
            self.service.status('demo-p2s-a')
            for action in ('pause','resume','cancel','camera'):
                self.assertFalse(self.service.preview('demo-p2s-a',action)['executable'])
            for action in ('gcode','heat','motion','firmware','enable-developer-mode'):
                with self.assertRaises(Refused):self.service.preview('demo-p2s-a',action)
        for action in ('start','upload'):
            with self.assertRaises(Refused):self.service.preview('demo-p2s-a',action)
        with self.assertRaises(Refused):self.service.status('invented-device')
        with self.assertRaises(Refused):self.service.preview('demo-p2s-a','pause',settings={'approved':True})
        with self.assertRaises(Refused):self.service.preview('demo-p2s-a','start','job.3mf',{'plate':True})
        with self.assertRaises(Refused):self.service.preview('demo-p2s-a','start','job.3mf',{'ams_mapping':[4]})

    def test_reports_redact_untrusted_text_and_numbers(self):
        report={'print':{'gcode_state':'SECRET','mc_percent':True,'nozzle_temper':-10,'hms':[{'code':1,'message':'SECRET'}], 'access_code':'SECRET','filename':'SECRET'}}
        result=normalize_status(json.dumps(report))
        self.assertNotIn('SECRET',json.dumps(result))
        self.assertEqual(result['state'],'UNKNOWN')
        self.assertNotIn('progress_percent',result)
        self.assertEqual(result['hms'],[{'code':1}])
        for raw in ('{"print":{},"print":{}}','{"print":{"mc_percent":NaN}}'):
            with self.assertRaises(Refused):normalize_status(raw)

    def entry(self):
        (self.root/'trust.crt').write_text('synthetic placeholder for validation only')
        return {'id':'printer-a','model':'P2S','serial':'SYNTHETICA','address':'192.168.10.50',
                'tls_name':'printer.test','ca_file':'trust.crt','certificate_sha256':'a'*64,
                'secret_env':'BAMBUP2S_SECRET_A','firmware':'01.02.00.00','monitor_approved':False}

    def registry(self,entries):
        path=self.root/'devices.json';path.write_text(json.dumps({'version':1,'devices':entries}))
        return path

    def test_endpoint_and_identity_enrollment(self):
        entry=self.entry()
        self.assertEqual(list(load_registry(self.registry([entry]))),['printer-a'])
        for key,value in (('address','example.com'),('address','127.0.0.1'),('address','169.254.1.1'),('address','8.8.8.8'),('address','::1'),('address',3232235570),('ca_file','../trust.crt'),('model','P1S'),('monitor_approved','true'),('secret_env','PATH'),('serial','x/#'),('certificate_sha256','bad')):
            altered=dict(entry);altered[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(Refused):load_registry(self.registry([altered]))
        for key in ('serial','id','address','certificate_sha256','secret_env'):
            b=dict(entry,id='printer-b',serial='SYNTHETICB',address='192.168.10.51',certificate_sha256='b'*64,secret_env='BAMBUP2S_SECRET_B');b[key]=entry[key]
            with self.subTest(key=key),self.assertRaises(Refused):load_registry(self.registry([entry,b]))
        device=Device.parse(entry,self.root)
        with patch('core.socket.create_connection',side_effect=AssertionError('must not connect')),self.assertRaises(Refused):monitor(device)
        self.assertNotIn('192.168',repr(device))
        self.assertNotIn('SYNTHETIC',json.dumps(Service({'printer-a':device}).list_devices()))

    def test_mcp_real_subprocess_startup_discovery_call(self):
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'offline-test','version':'1'}}},
                  {'jsonrpc':'2.0','method':'notifications/initialized'},
                  {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{'_meta':{'test':'standard-host-metadata'}}},
                  {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'p2s_capabilities','arguments':{}}},
                  {'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'p2s_status','arguments':{'device_id':'demo-p2s-b'}}},
                  {'jsonrpc':'2.0','id':5,'method':'tools/call','params':{'name':'p2s_status','arguments':{'device_id':'demo-p2s-a','host':'ATTACKER','access_code':'SECRET'}}}]
        result=subprocess.run([sys.executable,'-B',str(HERE/'server.py'),'--demo'],input=''.join(json.dumps(x)+'\n' for x in messages),text=True,capture_output=True,timeout=10,check=True)
        replies=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(replies),5)
        self.assertEqual(len(replies[1]['result']['tools']),5)
        self.assertFalse(json.loads(replies[2]['result']['content'][0]['text'])['live_controls'])
        self.assertEqual(json.loads(replies[3]['result']['content'][0]['text'])['source'],'demo')
        self.assertTrue(replies[4]['result']['isError'])
        self.assertNotIn('SECRET',result.stdout+result.stderr)
        self.assertNotIn('ATTACKER',result.stdout+result.stderr)
        self.assertEqual(result.stderr,'')

    def test_mcp_order_and_bounds(self):
        output=io.StringIO()
        serve(self.service,io.BytesIO(b'{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n'),output)
        self.assertIn('error',json.loads(output.getvalue()))
        output=io.StringIO();serve(self.service,io.BytesIO(b'x'*(core.MAX_JSON+3)),output)
        self.assertEqual(json.loads(output.getvalue())['error']['code'],-32700)
        output=io.StringIO();serve(self.service,io.BytesIO(b'[]\n{"jsonrpc":"2.0","id":[],"method":"ping"}\n'),output)
        self.assertTrue(all('error' in json.loads(x) for x in output.getvalue().splitlines()))


class FakeTLSPrinterTests(unittest.TestCase):
    """TLS over socketpair: no network interface, printer or LAN access."""
    @classmethod
    def setUpClass(cls):
        if os.name!='posix':raise unittest.SkipTest('Unix socketpair fixture')
        cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
        cls.cert=cls.root/'trust.crt';cls.key=cls.root/'test.key'
        subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(cls.key),'-out',str(cls.cert),'-days','1','-subj','/CN=printer.test','-addext','subjectAltName=DNS:printer.test'],check=True,capture_output=True)
        der=ssl.PEM_cert_to_DER_cert(cls.cert.read_text());cls.pin=hashlib.sha256(der).hexdigest()

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def exchange(self,pin=None,tls_name='printer.test',trust=None,topic='device/SYNTHETICA/report',retained=False,huge=False):
        client,server=socket.socketpair()
        server.settimeout(5)
        observed=[];errors=[]
        def fake():
            context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);context.load_cert_chain(self.cert,self.key)
            try:
                with server,context.wrap_socket(server,server_side=True) as stream:
                    deadline=time.monotonic()+5
                    kind,body=read_packet(stream,deadline);observed.append((kind,body))
                    stream.sendall(packet(0x20,b'\x00\x00'))
                    kind,body=read_packet(stream,deadline);observed.append((kind,body))
                    stream.sendall(packet(0x90,b'\x00\x01\x00'))
                    payload=json.dumps({'print':{'gcode_state':'RUNNING','mc_percent':50,'filename':'DO-NOT-ECHO'}}).encode()
                    body=core.mqtt_string(topic)+payload
                    if huge:stream.sendall(bytes([0x30,0xff,0xff,0xff,0x7f]))
                    else:stream.sendall(packet(0x31 if retained else 0x30,body))
            except (OSError,Refused) as exc:errors.append(type(exc).__name__)
        thread=threading.Thread(target=fake);thread.start()
        device=Device('printer-a','SYNTHETICA','192.168.10.50',tls_name,trust or self.cert,pin or self.pin,'BAMBUP2S_SECRET_A','01.02.00.00',True)
        try:
            with patch('core.socket.create_connection',return_value=client) as dial,patch.dict(os.environ,{'BAMBUP2S_SECRET_A':'Ab12Cd34'}):
                result=monitor(device)
            self.assertEqual(dial.call_args.args[0],('192.168.10.50',8883))
            return result,observed
        except Refused:
            self.assertFalse(any(b'Ab12Cd34' in body for _,body in observed)) if pin is not None or tls_name!='printer.test' or trust else None
            raise
        finally:
            client.close();thread.join(6)
            self.assertFalse(thread.is_alive())

    def test_keylog_environment_does_not_record_tls_secrets(self):
        log=self.root/'traffic.log'
        with patch.dict(os.environ,{'SSLKEYLOGFILE':str(log)}):
            self.exchange()
        if log.exists():
            self.assertNotIn('TRAFFIC_SECRET',log.read_text())
            self.assertNotIn('CLIENT_RANDOM',log.read_text())

    def test_verified_tls_and_only_read_packets(self):
        result,observed=self.exchange()
        self.assertEqual(result['progress_percent'],50)
        self.assertEqual([kind for kind,_ in observed],[0x10,0x82])
        self.assertNotIn('DO-NOT-ECHO',json.dumps(result))

    def test_mismatch_sends_no_credentials(self):
        with self.assertRaises(Refused):self.exchange(pin='f'*64)
        with self.assertRaises(Refused):self.exchange(tls_name='wrong.test')
        with self.assertRaises(Refused):self.exchange(trust=Path('/missing-synthetic-ca.crt'))

    def test_wrong_device_retained_and_oversized_reports(self):
        for kwargs in ({'topic':'device/SYNTHETICB/report'},{'retained':True},{'huge':True}):
            with self.subTest(kwargs=kwargs),self.assertRaises(Refused):self.exchange(**kwargs)


class ProtocolContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures=json.loads((HERE.parent/'templates/protocol-fixtures.json').read_text())

    def test_vendor_request_shapes_have_no_arbitrary_commands(self):
        from protocol_contracts import task_request
        for action,expected in self.fixtures['requests'].items():
            self.assertEqual(task_request(action,17,'101'),expected)
        for args in (('heat',17,'101'),('gcode',17,'101'),('resume',True,'101'),('cancel',17,'0'),('cancel',17,'101\nM104 S300')):
            with self.subTest(args=args),self.assertRaises(Refused):task_request(*args)

    def test_ack_is_correlated_and_never_completion_or_retry_permission(self):
        from protocol_contracts import acknowledgement
        reply={'print':{'command':'stop','sequence_id':'17','job_id':'101','result':'success','message':'SECRET'}}
        result=acknowledgement(json.dumps(reply),'cancel',17,'101')
        self.assertFalse(result['completed']);self.assertFalse(result['retry_allowed'])
        self.assertNotIn('SECRET',json.dumps(result))
        for key,value in (('command','resume'),('sequence_id','18'),('job_id','102')):
            changed=json.loads(json.dumps(reply));changed['print'][key]=value
            with self.subTest(key=key),self.assertRaises(Refused):acknowledgement(json.dumps(changed),'cancel',17,'101')
        reply['print']['result']='FAIL'
        self.assertEqual(acknowledgement(json.dumps(reply),'cancel',17,'101')['outcome'],'rejected')

    def test_job_and_camera_hints_are_whitelisted(self):
        report=normalize_status(json.dumps(self.fixtures['status']['running']))
        self.assertEqual(report['job_state'],'RUNNING')
        self.assertEqual(report['camera_protocol'],'rtsps')
        self.assertNotIn('job_id',report)
        self.assertNotIn('DO-NOT-RETURN',json.dumps(report))
        self.assertRegex(report['job_binding'],r'^[0-9a-f]{64}$')
        other=normalize_status('{"print":{"job_id":"101\\nPROMPT","job":{"job_state":true}}}')
        self.assertNotIn('job_binding',other);self.assertNotIn('job_state',other)
        idle=normalize_status(json.dumps(self.fixtures['status']['idle']))
        self.assertNotIn('job_binding',idle)

    def test_fresh_job_state_and_transition_gates(self):
        from protocol_contracts import state_gate
        running=normalize_status(json.dumps(self.fixtures['status']['running']))
        paused=normalize_status(json.dumps(self.fixtures['status']['paused']))
        pausing=normalize_status(json.dumps(self.fixtures['status']['pausing']))
        self.assertTrue(state_gate('pause',running,10,now=11)['ready'])
        self.assertTrue(state_gate('resume',paused,10,now=11)['ready'])
        for action,report,observed,now in (('resume',running,10,11),('cancel',pausing,10,11),('pause',running,10,21),('pause',running,10,9),('pause',None,None,11)):
            with self.subTest(action=action,observed=observed,now=now):self.assertFalse(state_gate(action,report,observed,now=now)['ready'])
        conflict=dict(running,state='PAUSE')
        self.assertFalse(state_gate('pause',conflict,10,now=11)['ready'])
        missing_job=normalize_status('{"print":{"gcode_state":"RUNNING","job_id":0}}')
        self.assertFalse(state_gate('pause',missing_job,10,now=11)['ready'])

    def test_failed_status_invalidates_earlier_job_evidence(self):
        device=Device('printer-a','SYNTHETICA','192.168.10.50','printer.test',Path('/synthetic.crt'),'a'*64,'BAMBUP2S_SECRET_A','01.02.00.00',True)
        service=Service({'printer-a':device})
        running=normalize_status(json.dumps(self.fixtures['status']['running']))
        with patch('core.monitor',return_value=running):service.status('printer-a')
        self.assertTrue(service.preview('printer-a','pause')['plan']['state_precondition']['ready'])
        with patch('core.monitor',side_effect=Refused('Synthetic failure.')),self.assertRaises(Refused):service.status('printer-a')
        self.assertFalse(service.preview('printer-a','pause')['plan']['state_precondition']['ready'])

    def test_preview_uses_internal_status_and_stays_nonexecutable(self):
        service=Service(demo=True)
        before=service.preview('demo-p2s-a','pause')
        self.assertFalse(before['plan']['state_precondition']['ready'])
        with patch('core.socket.create_connection',side_effect=AssertionError('network forbidden')):
            service.status('demo-p2s-a')
            after=service.preview('demo-p2s-a','pause')
        self.assertTrue(after['plan']['state_precondition']['ready'])
        self.assertFalse(after['executable']);self.assertTrue(after['approval_required'])
        self.assertNotEqual(before['plan_sha256'],after['plan_sha256'])
        service.snapshots['demo-p2s-a']=(service.snapshots['demo-p2s-a'][0],time.monotonic()-11)
        self.assertFalse(service.preview('demo-p2s-a','pause')['plan']['state_precondition']['ready'])

    def test_upload_contract_is_snapshot_bound_and_cannot_overwrite(self):
        from protocol_contracts import upload_contract
        result=upload_contract('a'*64,4096,'3mf')
        self.assertEqual(result['candidate_basename'],'a'*64+'.gcode.3mf')
        self.assertTrue(result['data_tls_required'])
        self.assertFalse(result['resume_or_overwrite_allowed'])
        self.assertFalse(result['executable'])
        for args in (('not-a-digest',4096,'3mf'),('a'*64,True,'3mf'),('a'*64,0,'3mf'),('a'*64,4096,'shell')):
            with self.assertRaises(Refused):upload_contract(*args)

    def test_passive_data_endpoint_cannot_redirect_credentials_or_content(self):
        from protocol_contracts import passive_target
        for reply in self.fixtures['passive'].values():
            result=passive_target(reply,'192.168.10.50')
            self.assertEqual(result['address'],'192.168.10.50');self.assertEqual(result['port'],50000)
            self.assertTrue(result['independent_identity_check_required'])
        for reply in ('227 Passive (8,8,8,8,195,80)','227 Passive (192,168,10,51,195,80)','229 Passive (|||22|)','229 Passive (|||50101|)','227 Passive (999,168,10,50,195,80)','229 Passive (|||50000|)\nSECRET'):
            with self.subTest(reply=reply),self.assertRaises(Refused):passive_target(reply,'192.168.10.50')

    def test_camera_hint_is_not_authority_and_never_contains_credentials(self):
        from protocol_contracts import camera_endpoint
        value=self.fixtures['camera'];good=value['candidate'];path=value['approved_path']
        result=camera_endpoint(good,'192.168.10.50',path)
        self.assertFalse(result['executable']);self.assertTrue(result['stream_approval_required'])
        for candidate in (good.replace('rtsps','rtsp'),good.replace('192.168.10.50','8.8.8.8'),good.replace(':322',':554'),good+'?token=SECRET',good+'#SECRET',good.replace('://','://user:SECRET@'),good.replace('://','://@'),good.replace(path,'/other'),good+'\nSECRET'):
            with self.subTest(candidate=candidate),self.assertRaises(Refused):camera_endpoint(candidate,'192.168.10.50',path)


if __name__=='__main__':
    unittest.main(verbosity=2)
