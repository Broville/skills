"""Original offline contracts from pinned public vendor facts; no transport or effects."""
from __future__ import annotations

import hashlib
import ipaddress
import re
import time
from urllib.parse import urlsplit

from core import HEX, Refused, strict_json, text_match

VENDOR_REVISION = 'da8b44ee34dd349f2ae0df3f1cbae366df482354'
JOB_STATES = ('IDLE', 'SLICING', 'PREPARE', 'STARTING', 'RUNNING', 'PAUSE',
              'PAUSING', 'RESUMING', 'FINISH', 'FAILED', 'FINISHING', 'STOPPING')
CONTROL_NAMES = {'pause': 'pause', 'resume': 'resume', 'cancel': 'stop'}


def job_identity(value):
    # Vendor job IDs are numeric; neither a job name nor an untrusted string is identity.
    if type(value) is int and 0 <= value <= 2**63 - 1:
        return str(value)
    if isinstance(value, str) and re.fullmatch(r'[0-9]{1,19}', value):
        if int(value) <= 2**63 - 1:
            return str(int(value))
    raise Refused('A bounded numeric job identity is required.')


def job_binding(value):
    return hashlib.sha256(('p2s-job:' + job_identity(value)).encode()).hexdigest()


def report_job(print_object):
    """Whitelist state and opaque binding; never echo raw job or advertised camera URL."""
    result = {}
    job = print_object.get('job')
    if isinstance(job, dict):
        state = job.get('job_state')
        if type(state) is int and 0 <= state < len(JOB_STATES):
            result['job_state'] = JOB_STATES[state]
    value = print_object.get('job_id')
    if value is not None:
        try:
            if job_identity(value) != '0':
                result['job_binding'] = job_binding(value)
        except Refused:
            pass
    ipcam = print_object.get('ipcam')
    if isinstance(ipcam, dict):
        liveview = ipcam.get('liveview')
        value = liveview.get('local') if isinstance(liveview, dict) else None
        result['camera_protocol'] = value if value in ('none', 'disabled', 'local', 'rtsps', 'rtsp') else 'unknown'
    return result


def state_gate(action, snapshot, observed_monotonic, now=None):
    """Preview readiness only. Report provenance is internal to the service, not a tool argument."""
    now = time.monotonic() if now is None else now
    if action not in ('start', 'pause', 'resume', 'cancel'):
        return {'checked': False, 'ready': False, 'reason': 'No qualified operation state contract.'}
    if snapshot is None or observed_monotonic is None or not 0 <= now - observed_monotonic <= 10:
        return {'checked': False, 'ready': False, 'reason': 'Fresh status is required before physical-action review.'}
    state = snapshot.get('job_state', snapshot.get('state', 'UNKNOWN'))
    legacy = snapshot.get('state', 'UNKNOWN')
    if legacy != 'UNKNOWN' and state in ('IDLE', 'RUNNING', 'PAUSE', 'FINISH', 'FAILED', 'PREPARE') and legacy != state:
        return {'checked': True, 'ready': False, 'reason': 'Conflicting job-state evidence.'}
    allowed = {'start': ('IDLE', 'FINISH'), 'pause': ('RUNNING',),
               'resume': ('PAUSE',), 'cancel': ('RUNNING', 'PAUSE')}
    if state not in allowed[action]:
        return {'checked': True, 'ready': False, 'state': state,
                'reason': 'State is incompatible or transitional; native safety checks remain required.'}
    if action != 'start' and 'job_binding' not in snapshot:
        return {'checked': True, 'ready': False, 'state': state,
                'reason': 'Current job identity is unknown.'}
    return {'checked': True, 'ready': True, 'state': state,
            'job_binding': snapshot.get('job_binding'), 'physical_safety_verified': False,
            'reason': 'Offline preview precondition only; authorization and live qualification still absent.'}


def task_request(action, sequence_id, job_id):
    """Pure wire-shape fixture builder. Not connected to any publisher or MCP execution tool."""
    if action not in CONTROL_NAMES or type(sequence_id) is not int or not 1 <= sequence_id <= 2**31 - 1:
        raise Refused('Only bounded pause/resume/cancel fixture requests are supported.')
    job = job_identity(job_id)
    if job == '0':
        raise Refused('An active job identity is required.')
    payload = {'command': CONTROL_NAMES[action], 'param': '', 'sequence_id': str(sequence_id)}
    if action == 'cancel':
        payload['job_id'] = job
    return {'print': payload}


def acknowledgement(payload, action, sequence_id, expected_job):
    """A matching ack is not proof of a completed physical action. Unknown results stay uncertain."""
    request = task_request(action, sequence_id, expected_job)['print']
    value = strict_json(payload)
    response = value.get('print') if isinstance(value, dict) else None
    if not isinstance(response, dict):
        raise Refused('Invalid control acknowledgement.')
    if response.get('sequence_id') != request['sequence_id'] or response.get('command') != request['command']:
        raise Refused('Control acknowledgement correlation mismatch.')
    if 'job_id' in response and job_identity(response['job_id']) != job_identity(expected_job):
        raise Refused('Control acknowledgement job mismatch.')
    result = response.get('result')
    if not isinstance(result, str):
        result = ''
    outcome = 'rejected' if result.lower() == 'fail' else 'matched-ack-unconfirmed'
    return {'outcome': outcome, 'completed': False, 'retry_allowed': False,
            'state_reconciliation_required': True}


def private_ipv4(value):
    if not isinstance(value, str):
        raise Refused('A fixed enrolled private IPv4 address is required.')
    try:
        address = ipaddress.IPv4Address(value)
    except ValueError:
        raise Refused('A fixed enrolled private IPv4 address is required.') from None
    if not any(address in ipaddress.ip_network(net) for net in
               ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')):
        raise Refused('A fixed enrolled private IPv4 address is required.')
    return str(address)


def passive_target(reply, enrolled_address):
    """Validate FTP passive negotiation offline; never trust a broker-selected endpoint."""
    address = private_ipv4(enrolled_address)
    if not isinstance(reply, str) or len(reply) > 256 or any(not 32 <= ord(c) <= 126 for c in reply):
        raise Refused('Invalid passive reply.')
    extended = re.fullmatch(r'229[^()]*\(\|\|\|([0-9]{1,5})\|\)[^()]*', reply)
    standard = re.fullmatch(r'227[^()]*\(([0-9]{1,3}(?:,[0-9]{1,3}){5})\)[^()]*', reply)
    if extended:
        port = int(extended[1])
    elif standard:
        values = [int(v) for v in standard[1].split(',')]
        if any(v > 255 for v in values) or '.'.join(str(v) for v in values[:4]) != address:
            raise Refused('Passive endpoint differs from the enrolled printer.')
        port = values[4] * 256 + values[5]
    else:
        raise Refused('Unsupported passive reply.')
    if not 50000 <= port <= 50100:
        raise Refused('Passive port is outside the vendor-documented range.')
    return {'address': address, 'port': port, 'data_tls_required': True,
            'independent_identity_check_required': True}


def upload_contract(digest, size, kind):
    text_match(digest, HEX)
    if type(size) is not int or not 0 < size <= 128 * 1024 * 1024 or kind not in ('3mf', 'gcode'):
        raise Refused('Invalid transfer snapshot.')
    return {'snapshot_sha256': digest, 'bytes': size,
            'candidate_basename': digest + ('.gcode.3mf' if kind == '3mf' else '.gcode'),
            'control_tls_required': True, 'data_tls_required': True,
            'remote_directory_qualified': False, 'digest_reconciliation_required': True,
            'executable': False, 'resume_or_overwrite_allowed': False,
            'note': 'A byte count or transfer acknowledgement cannot verify remote contents.'}


def camera_endpoint(candidate, enrolled_address, approved_path):
    """Pure inspection of an untrusted hint against an operator-chosen exact endpoint."""
    address = private_ipv4(enrolled_address)
    if (not isinstance(candidate, str) or len(candidate) > 512
            or any(ord(c) < 33 or ord(c) == 127 for c in candidate)
            or not isinstance(approved_path, str) or not re.fullmatch(r'/[A-Za-z0-9_/-]{1,128}', approved_path)
            or any(p in ('', '.', '..') for p in approved_path[1:].split('/'))):
        raise Refused('Invalid camera endpoint policy.')
    try:
        parts = urlsplit(candidate)
        valid = (parts.scheme == 'rtsps' and parts.hostname == address and parts.port == 322
                 and parts.netloc == address + ':322' and parts.path == approved_path
                 and parts.username is None and parts.password is None
                 and not parts.query and not parts.fragment)
    except ValueError:
        valid = False
    if not valid:
        raise Refused('Camera hint differs from the approved secure endpoint.')
    return {'protocol': 'rtsps', 'port': 322, 'credentials_in_uri': False,
            'service_identity_qualification_required': True, 'stream_approval_required': True,
            'executable': False}
