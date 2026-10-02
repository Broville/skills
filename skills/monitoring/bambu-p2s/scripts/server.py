#!/usr/bin/env python3
"""Bounded MCP stdio server. No listeners, discovery, installation or startup network."""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from core import MAX_JSON, Refused, Service, VERSION, exact, load_registry, strict_json


def schema(properties=None, required=()):
    return {'type': 'object', 'properties': properties or {}, 'required': list(required),
            'additionalProperties': False}


STRING = {'type': 'string', 'maxLength': 240}
TOOLS = [
    {'name': 'p2s_capabilities', 'description': 'Offline capability and blocker report; no printer access.', 'inputSchema': schema()},
    {'name': 'p2s_list_devices', 'description': 'List locally enrolled aliases only; no network discovery or secrets.', 'inputSchema': schema()},
    {'name': 'p2s_status', 'description': 'Demo status or explicitly approved read-only pinned TLS LAN subscription. Experimental, unqualified on P2S firmware.', 'inputSchema': schema({'device_id': STRING}, ('device_id',))},
    {'name': 'p2s_inspect_artifact', 'description': 'Bounded local 3MF/G-code inspection under an operator-selected artifact root. Does not establish print safety.', 'inputSchema': schema({'artifact': STRING}, ('artifact',))},
    {'name': 'p2s_preview_action', 'description': 'Preview a blocked action for owner review. Never uploads, streams or controls a printer; never grants approval.',
     'inputSchema': schema({'device_id': STRING, 'action': {'type': 'string', 'enum': ['upload','start','pause','resume','cancel','camera']},
                            'artifact': STRING, 'settings': schema({'plate': {'type':'integer','minimum':1,'maximum':999},
                            **{n:{'type':'boolean'} for n in ('bed_leveling','flow_calibration','vibration_calibration','timelapse','use_ams')},
                            'ams_mapping': {'type':'array','minItems':1,'maxItems':4,'items':{'type':'integer','minimum':0,'maximum':3}}})}, ('device_id','action'))},
]
for tool in TOOLS:
    tool['annotations'] = {'readOnlyHint': True, 'destructiveHint': False,
                           'idempotentHint': True, 'openWorldHint': tool['name'] == 'p2s_status'}


def invoke(service, name, args):
    if name == 'p2s_capabilities':
        exact(args, ())
        return service.capabilities()
    if name == 'p2s_list_devices':
        exact(args, ())
        return service.list_devices()
    if name == 'p2s_status':
        exact(args, ('device_id',))
        return service.status(args['device_id'])
    if name == 'p2s_inspect_artifact':
        from core import inspect_artifact
        exact(args, ('artifact',))
        return inspect_artifact(service.artifact_root, args['artifact'])
    if name == 'p2s_preview_action':
        exact(args, ('device_id','action'), ('artifact','settings'))
        return service.preview(args['device_id'], args['action'], args.get('artifact'), args.get('settings'))
    raise Refused('Unknown tool.')


def error(id, code, message):
    return {'jsonrpc': '2.0', 'id': id, 'error': {'code': code, 'message': message}}


def serve(service, input_stream=None, output_stream=None):
    input_stream = input_stream or sys.stdin.buffer
    output_stream = output_stream or sys.stdout
    initialized = False
    ready = False
    while True:
        line = input_stream.readline(MAX_JSON + 2)
        if not line:
            return
        if len(line) > MAX_JSON:
            output_stream.write(json.dumps(error(None, -32700, 'Message size limit exceeded.'))+'\n')
            output_stream.flush()
            return  # close rather than desynchronize framing
        id = None
        try:
            try:
                request = strict_json(line)
            except Refused:
                output_stream.write(json.dumps(error(None, -32700, 'Invalid JSON.'))+'\n')
                output_stream.flush()
                continue
            exact(request, ('jsonrpc','method'), ('id','params'))
            if request['jsonrpc'] != '2.0' or not isinstance(request['method'], str):
                raise Refused('Invalid JSON-RPC request.')
            candidate_id = request.get('id')
            if 'id' in request and (candidate_id is None or type(candidate_id) not in (str,int) or isinstance(candidate_id,str) and len(candidate_id)>128):
                raise Refused('Invalid request ID.')
            id = candidate_id
            method = request['method']
            params = request.get('params', {})
            if not isinstance(params, dict):
                raise Refused('Invalid parameters.')
            if 'id' not in request:
                if method == 'notifications/initialized' and initialized:
                    ready = True
                continue
            if method == 'initialize':
                if initialized:
                    raise Refused('Session already initialized.')
                exact(params, ('protocolVersion','capabilities','clientInfo'), ('_meta',))
                if not isinstance(params['protocolVersion'], str) or not isinstance(params['capabilities'],dict) or not isinstance(params['clientInfo'],dict):
                    raise Refused('Invalid initialization.')
                version = params['protocolVersion']
                if version not in ('2024-11-05','2025-03-26','2025-06-18','2025-11-25'):
                    version = '2025-11-25'
                initialized = True
                result = {'protocolVersion': version, 'capabilities': {'tools': {'listChanged': False}},
                          'serverInfo': {'name': 'broville-bambu-p2s', 'version': VERSION},
                          'instructions': 'Offline-first draft; inspect capabilities before use. Live controls are blocked.'}
            elif method == 'ping':
                result = {}
            elif not ready:
                raise Refused('Initialize the session before tool use.')
            elif method == 'tools/list':
                exact(params, (), ('cursor','_meta'))
                if params.get('cursor') is not None:
                    raise Refused('Pagination is not supported.')
                result = {'tools': TOOLS}
            elif method == 'tools/call':
                exact(params, ('name',), ('arguments','_meta'))
                try:
                    value = invoke(service, params['name'], params.get('arguments', {}))
                    result = {'content':[{'type':'text','text':json.dumps(value,allow_nan=False)}], 'isError':False}
                except Refused as exc:
                    result = {'content':[{'type':'text','text':str(exc)}], 'isError':True}
                except Exception:
                    # Device filenames, certificate paths, credentials and incoming text never echo.
                    result = {'content':[{'type':'text','text':'Operation failed safely.'}], 'isError':True}
            else:
                response = error(id, -32601, 'Method not found.')
                output_stream.write(json.dumps(response)+'\n')
                output_stream.flush()
                continue
            response = {'jsonrpc':'2.0','id':id,'result':result}
        except Refused as exc:
            response = error(id, -32602, str(exc))
        except Exception:
            response = error(id, -32603, 'Request failed safely.')
        output_stream.write(json.dumps(response,allow_nan=False)+'\n')
        output_stream.flush()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', help='Synthetic offline devices; never connects to network')
    parser.add_argument('--check-registry', type=Path, help='Validate a local enrollment file without reading secrets or connecting')
    args = parser.parse_args()
    if args.check_registry:
        try:
            devices = load_registry(args.check_registry)
            print(json.dumps({'valid':True,'devices':len(devices),'network_access':False}))
            return 0
        except Exception:
            print('Enrollment validation failed; no device was contacted.',file=sys.stderr)
            return 2
    try:
        path = os.environ.get('BAMBUP2S_REGISTRY')
        devices = load_registry(Path(path)) if path and not args.demo else {}
        root = os.environ.get('BAMBUP2S_FILE_ROOT')
        service = Service(devices, Path(root) if root else None, args.demo)
        serve(service)
        return 0
    except Exception:
        print('P2S server configuration failed safely.',file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
