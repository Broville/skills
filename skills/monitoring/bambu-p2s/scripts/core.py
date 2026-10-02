"""Original, bounded offline preparation and opt-in read-only LAN monitoring."""
from __future__ import annotations

import hashlib
import ipaddress
import json
import os
import re
import socket
import ssl
import stat
import struct
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

VERSION = '0.1.0'
MAX_JSON = 256 * 1024
MAX_FILE = 128 * 1024 * 1024
MAX_INFLATED = 512 * 1024 * 1024
MAX_MEMBER = 128 * 1024 * 1024
MAX_ENTRIES = 2048
MAX_RATIO = 100
ID = re.compile(r'[a-z][a-z0-9-]{0,47}\Z')
SERIAL = re.compile(r'[A-Za-z0-9]{6,32}\Z')
HEX = re.compile(r'[0-9a-f]{64}\Z')
ACTIONS = ('upload', 'start', 'pause', 'resume', 'cancel', 'camera')
BLOCKER = 'No qualified P2S control/upload/camera adapter; no device action was sent.'


class Refused(Exception):
    """Fixed public message; never attach network errors or input values."""


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Refused('Duplicate JSON keys refused.')
            result[key] = value
        return result
    if len(data) > MAX_JSON:
        raise Refused('JSON size limit exceeded.')
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        raise Refused('Invalid JSON.') from None


def exact(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise Refused('Invalid fields.')


def text_match(value, pattern):
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise Refused('Invalid identifier.')
    return value


@dataclass(frozen=True)
class Device:
    id: str
    serial: str = field(repr=False)
    address: str = field(repr=False)
    tls_name: str = field(repr=False)
    ca_file: Path = field(repr=False)
    pin: str = field(repr=False)
    secret_env: str = field(repr=False)
    firmware: str
    monitor_approved: bool

    @classmethod
    def parse(cls, data, config_dir):
        exact(data, ('id', 'model', 'serial', 'address', 'tls_name', 'ca_file',
                     'certificate_sha256', 'secret_env', 'firmware', 'monitor_approved'))
        name = text_match(data['id'], ID)
        if data['model'] != 'P2S' or type(data['monitor_approved']) is not bool:
            raise Refused('Only explicit P2S enrollment is supported.')
        serial = text_match(data['serial'], SERIAL)
        if not isinstance(data['address'], str):
            raise Refused('A fixed private IPv4 address is required.')
        try:
            address = ipaddress.IPv4Address(data['address'])
        except (ValueError, TypeError, ipaddress.AddressValueError):
            raise Refused('A fixed private IPv4 address is required.') from None
        if not any(address in ipaddress.ip_network(net) for net in
                   ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')):
            raise Refused('A fixed private IPv4 address is required.')
        tls_name = text_match(data['tls_name'], re.compile(r'[A-Za-z0-9][A-Za-z0-9.-]{0,252}\Z'))
        ca_name = text_match(data['ca_file'], re.compile(r'[A-Za-z0-9_-]{1,64}\.crt\Z'))
        ca_file = config_dir / ca_name
        if ca_file.is_symlink() or not ca_file.is_file() or ca_file.stat().st_size > MAX_JSON:
            raise Refused('A bounded locally supplied trust certificate is required.')
        pin = text_match(data['certificate_sha256'], HEX)
        env = text_match(data['secret_env'], re.compile(r'BAMBUP2S_SECRET_[A-Z0-9_]{1,48}\Z'))
        firmware = text_match(data['firmware'], re.compile(r'[0-9]{2}(?:\.[0-9]{2}){3}\Z'))
        return cls(name, serial, str(address), tls_name, ca_file, pin, env,
                   firmware, data['monitor_approved'])


def load_registry(path):
    if path.is_symlink() or path.stat().st_size > MAX_JSON:
        raise Refused('Invalid registry file.')
    data = strict_json(path.read_bytes())
    exact(data, ('version', 'devices'))
    if type(data['version']) is not int or data['version'] != 1 or not isinstance(data['devices'], list) or len(data['devices']) > 32:
        raise Refused('Invalid registry version or device count.')
    result = {}
    serials, addresses, pins, secrets = set(), set(), set(), set()
    for entry in data['devices']:
        device = Device.parse(entry, path.parent)
        if (device.id in result or device.serial in serials or device.address in addresses
                or device.pin in pins or device.secret_env in secrets):
            raise Refused('Enrollment identities, endpoints, pins and secrets must be unique.')
        result[device.id] = device
        serials.add(device.serial)
        addresses.add(device.address)
        pins.add(device.pin)
        secrets.add(device.secret_env)
    return result


def relative_parts(value):
    if not isinstance(value, str) or len(value) > 240 or '\\' in value or ':' in value or '\x00' in value:
        raise Refused('Use a relative artifact path.')
    parts = value.split('/')
    if any(part in ('', '.', '..') for part in parts) or value.startswith('/'):
        raise Refused('Use a contained relative artifact path.')
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise Refused('Control characters in paths refused.')
    return parts


def open_artifact(root, value):
    """POSIX directory-relative opens prevent symlink and rename escape."""
    parts = relative_parts(value)
    if os.name != 'posix' or not hasattr(os, 'O_NOFOLLOW'):
        raise Refused('Secure artifact inspection currently requires a POSIX host.')
    if root is None or root.is_symlink() or not root.is_dir():
        raise Refused('Operator must select an artifact root before file access.')
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_FILE:
            os.close(descriptor)
            raise Refused('Artifact must be a bounded, nonempty regular file.')
        return os.fdopen(descriptor, 'rb')
    finally:
        os.close(directory)


def inspect_artifact(root, value):
    if not isinstance(value, str) or not value.lower().endswith(('.3mf', '.gcode')):
        raise Refused('Only 3MF and G-code artifacts can be inspected.')
    try:
        with open_artifact(root, value) as stream:
            # Snapshot within a hard cap; this exact snapshot is hashed and inspected.
            raw = stream.read(MAX_FILE + 1)
            if len(raw) > MAX_FILE:
                raise Refused('Artifact size limit exceeded.')
        if not raw:
            raise Refused('Artifact is empty.')
        digest = hashlib.sha256(raw).hexdigest()
        if value.lower().endswith('.gcode'):
            return {'sha256': digest, 'bytes': len(raw), 'kind': 'gcode',
                    'printable_verified': False, 'note': 'Content is never executed or returned.'}
        import io
        # Bound central-directory allocation before ZipFile constructs ZipInfo objects.
        end = raw.rfind(b'PK\x05\x06', max(0, len(raw) - 65557))
        if end < 0 or end + 22 > len(raw):
            raise Refused('Missing ZIP directory.')
        _, disk, directory_disk, local_count, count, directory_size, offset, comment = struct.unpack_from('<4s4H2LH', raw, end)
        if (disk or directory_disk or local_count != count or not 0 < count <= MAX_ENTRIES
                or directory_size > 2 * 1024 * 1024 or offset + directory_size > end
                or end + 22 + comment != len(raw) or count == 65535):
            raise Refused('Unsupported or oversized ZIP directory; ZIP64 is not accepted.')
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if not 0 < len(entries) <= MAX_ENTRIES:
                raise Refused('Archive entry limit exceeded.')
            total = 0
            names = set()
            plates = []
            for member in entries:
                name = member.filename
                relative_parts(name[:-1] if name.endswith('/') else name)
                if name.casefold() in names:
                    raise Refused('Duplicate archive paths refused.')
                names.add(name.casefold())
                if (member.flag_bits & 1 or stat.S_ISLNK(member.external_attr >> 16)
                        or member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)):
                    raise Refused('Encrypted, linked or unsupported archive members refused.')
                if member.file_size > MAX_MEMBER or member.file_size > max(1, member.compress_size) * MAX_RATIO:
                    raise Refused('Archive inflation limit exceeded.')
                total += member.file_size
                if total > MAX_INFLATED:
                    raise Refused('Archive total inflation limit exceeded.')
                match = re.fullmatch(r'Metadata/plate_([1-9][0-9]{0,2})\.gcode', name)
                if match:
                    plates.append(int(match[1]))
            # Read incrementally for CRC and actual limits; never extract or parse XML.
            actual_total = 0
            for member in entries:
                actual = 0
                with archive.open(member) as source:
                    while chunk := source.read(64 * 1024):
                        actual += len(chunk)
                        actual_total += len(chunk)
                        if actual > MAX_MEMBER or actual_total > MAX_INFLATED:
                            raise Refused('Archive actual inflation limit exceeded.')
                if actual != member.file_size:
                    raise Refused('Archive member size mismatch.')
        return {'sha256': digest, 'bytes': len(raw), 'kind': '3mf',
                'entries': len(entries), 'inflated_bytes': actual_total,
                'candidate_plates': sorted(plates), 'printable_verified': False,
                'note': 'Container validation cannot establish P2S slicing or physical print safety.'}
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, EOFError, NotImplementedError):
        raise Refused('Artifact cannot be safely inspected.') from None


def normalize_status(payload):
    data = strict_json(payload)
    if not isinstance(data, dict) or not isinstance(data.get('print'), dict):
        raise Refused('Status report has no print object.')
    source = data['print']
    result = {}
    state = source.get('gcode_state')
    result['state'] = state if state in ('IDLE', 'RUNNING', 'PAUSE', 'FINISH', 'FAILED', 'PREPARE') else 'UNKNOWN'
    for field_name, output, maximum in (
        ('mc_percent', 'progress_percent', 100), ('mc_remaining_time', 'remaining_minutes', 100000),
        ('layer_num', 'layer', 100000), ('total_layer_num', 'total_layers', 100000),
        ('nozzle_temper', 'nozzle_c', 400), ('bed_temper', 'bed_c', 150),
        ('print_error', 'error_code', 2**32 - 1)):
        number = source.get(field_name)
        if type(number) in (int, float) and 0 <= number <= maximum:
            result[output] = number
    hms = source.get('hms', [])
    if isinstance(hms, list):
        result['hms'] = [{k: v for k, v in item.items() if k in ('attr', 'code')
                          and type(v) is int and 0 <= v <= 2**32 - 1}
                         for item in hms[:32] if isinstance(item, dict)]
    return result


def mqtt_string(value):
    raw = value.encode('utf-8')
    if len(raw) > 65535 or '\x00' in value:
        raise Refused('Invalid MQTT string.')
    return struct.pack('!H', len(raw)) + raw


def packet(kind, body):
    length = len(body)
    digits = bytearray()
    while True:
        byte = length % 128
        length //= 128
        digits.append(byte | (128 if length else 0))
        if not length:
            return bytes([kind]) + digits + body


def read_exact(stream, size, deadline):
    result = bytearray()
    while len(result) < size:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Refused('Status deadline exceeded.')
        stream.settimeout(remaining)
        chunk = stream.recv(size - len(result))
        if not chunk:
            raise Refused('Status connection closed.')
        result.extend(chunk)
    return bytes(result)


def read_packet(stream, deadline):
    kind = read_exact(stream, 1, deadline)[0]
    size = 0
    for index in range(4):
        digit = read_exact(stream, 1, deadline)[0]
        size += (digit & 127) * 128**index
        if size > MAX_JSON:
            raise Refused('MQTT packet limit exceeded.')
        if not digit & 128:
            return kind, read_exact(stream, size, deadline)
    raise Refused('Invalid MQTT packet length.')


def monitor(device):
    """Never publish. Verify certificate chain, name and enrolled pin before credentials."""
    if not device.monitor_approved:
        raise Refused('Read-only network monitoring needs explicit operator enrollment approval.')
    deadline = time.monotonic() + 10
    try:
        context = ssl.create_default_context(cafile=str(device.ca_file))
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.keylog_filename = None  # Never inherit SSLKEYLOGFILE credential-bearing traffic logs.
        with socket.create_connection((device.address, 8883), timeout=5) as raw:
            with context.wrap_socket(raw, server_hostname=device.tls_name) as stream:
                peer = hashlib.sha256(stream.getpeercert(binary_form=True)).hexdigest()
                if peer != device.pin:
                    raise Refused('Enrolled certificate mismatch; re-enrollment requires owner review.')
                secret = os.environ.get(device.secret_env, '')
                if not re.fullmatch(r'[A-Za-z0-9]{8}', secret):
                    raise Refused('Operator-supplied access code unavailable or invalid.')
                body = (mqtt_string('MQTT') + bytes([4, 0xC2]) + struct.pack('!H', 15)
                        + mqtt_string('broville-' + os.urandom(8).hex())
                        + mqtt_string('bblp') + mqtt_string(secret))
                stream.sendall(packet(0x10, body))
                kind, response = read_packet(stream, deadline)
                if kind != 0x20 or response != b'\x00\x00':
                    raise Refused('MQTT authentication failed.')
                topic = ('device/' + device.serial + '/report').encode()
                stream.sendall(packet(0x82, b'\x00\x01' + mqtt_string(topic.decode()) + b'\x00'))
                subscribed = False
                for _ in range(64):
                    kind, message = read_packet(stream, deadline)
                    if kind == 0x90:
                        if message != b'\x00\x01\x00':
                            raise Refused('MQTT subscription refused.')
                        subscribed = True
                    elif kind & 0xF0 == 0x30:
                        # QoS 0 only, fresh non-retained report; no cached state claims.
                        if kind != 0x30 or not subscribed or len(message) < 2:
                            raise Refused('Unsupported or stale MQTT report.')
                        size = struct.unpack('!H', message[:2])[0]
                        if size != len(topic) or message[2:2+size] != topic:
                            raise Refused('MQTT device topic mismatch.')
                        return normalize_status(message[2+size:])
                    else:
                        raise Refused('Unexpected MQTT packet.')
                raise Refused('Status report limit exceeded.')
    except (OSError, ssl.SSLError, ValueError):
        raise Refused('Secure status connection failed; no insecure fallback is available.') from None


class Service:
    def __init__(self, devices=None, artifact_root=None, demo=False):
        self.devices = devices or {}
        self.artifact_root = artifact_root
        self.demo = demo

    def device(self, id):
        text_match(id, ID)
        if self.demo and id in ('demo-p2s-a', 'demo-p2s-b'):
            return None
        if id not in self.devices:
            raise Refused('Select an explicitly enrolled device ID.')
        return self.devices[id]

    def capabilities(self):
        return {'version': VERSION, 'mode': 'demo' if self.demo else 'offline-first',
                'network_on_startup': False, 'live_controls': False,
                'status': 'opt-in TLS MQTT subscription; P2S live qualification pending',
                'artifact_inspection': 'POSIX only', 'actions': {a: 'preview only; blocked' for a in ACTIONS},
                'excluded': ['arbitrary-gcode', 'manual-heat', 'manual-motion', 'firmware',
                             'cloud-login', 'security-settings', 'network-discovery'],
                'blocker': BLOCKER}

    def list_devices(self):
        if self.demo:
            return {'source': 'demo', 'devices': [{'id': n, 'model': 'P2S', 'monitor_approved': False}
                                                for n in ('demo-p2s-a', 'demo-p2s-b')]}
        return {'source': 'local-enrollment', 'devices': [
            {'id': d.id, 'model': 'P2S', 'firmware': d.firmware, 'monitor_approved': d.monitor_approved}
            for d in self.devices.values()]}

    def status(self, id):
        device = self.device(id)
        if self.demo:
            value = {'print': {'gcode_state': 'RUNNING' if id.endswith('a') else 'IDLE',
                               'mc_percent': 42 if id.endswith('a') else 0, 'print_error': 0}}
            return {'device_id': id, 'source': 'demo', 'live_verified': False,
                    'status': normalize_status(json.dumps(value))}
        return {'device_id': id, 'source': 'enrolled-lan', 'received_at_unix': int(time.time()),
                'live_verified': False, 'qualification': 'experimental subscription; firmware unqualified',
                'status': monitor(device)}

    def preview(self, id, action, artifact=None, settings=None):
        device = self.device(id)
        if action not in ACTIONS:
            raise Refused('Unsupported action; arbitrary G-code, heat and motion are excluded.')
        settings = {} if settings is None else settings
        exact(settings, (), ('plate', 'bed_leveling', 'flow_calibration', 'vibration_calibration',
                             'timelapse', 'use_ams', 'ams_mapping'))
        for name, value in settings.items():
            if name == 'plate':
                if type(value) is not int or not 1 <= value <= 999:
                    raise Refused('Invalid plate selection.')
            elif name == 'ams_mapping':
                if (not isinstance(value, list) or not 1 <= len(value) <= 4
                        or any(type(v) is not int or not 0 <= v <= 3 for v in value)):
                    raise Refused('Only explicit four-slot AMS intent is supported.')
            elif type(value) is not bool:
                raise Refused('Preparation toggles must be booleans.')
        if action not in ('start', 'upload') and (artifact is not None or settings):
            raise Refused('This action does not accept an artifact or preparation settings.')
        if action == 'upload' and settings:
            raise Refused('Upload does not accept print settings.')
        if settings.get('ams_mapping') is not None and settings.get('use_ams') is not True:
            raise Refused('AMS mapping requires explicit AMS intent.')
        if action in ('start', 'upload') and artifact is None:
            raise Refused('Start/upload preview requires an inspected artifact.')
        inspected = inspect_artifact(self.artifact_root, artifact) if artifact is not None else None
        if action == 'start' and inspected['kind'] == '3mf':
            if 'plate' not in settings or settings['plate'] not in inspected['candidate_plates']:
                raise Refused('Select a candidate sliced plate explicitly.')
        plan = {'device_id': id, 'action': action, 'artifact': inspected, 'settings': settings,
                'identity_binding': hashlib.sha256((device.serial + device.pin).encode()).hexdigest()
                if device else 'DEMO-NO-DEVICE'}
        digest = hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        return {'source': 'demo' if self.demo else 'local-preview', 'plan': plan, 'plan_sha256': digest,
                'approval_required': True, 'executable': False, 'blocker': BLOCKER,
                'approval_contract': 'Owner must approve exact device, file hash, settings and action. '
                'This preview is not an authorization token and no execution tool exists.'}
