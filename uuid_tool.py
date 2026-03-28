#!/usr/bin/env python3
"""uuid_tool — Generate, validate, and inspect UUIDs.

Usage:
    uuid_tool.py gen
    uuid_tool.py gen --version 4 --count 5
    uuid_tool.py gen --version 1
    uuid_tool.py inspect 550e8400-e29b-41d4-a716-446655440000
    uuid_tool.py validate 550e8400-e29b-41d4-a716-446655440000
    uuid_tool.py batch 100 --format bare
"""

import sys
import uuid
import json
import time
import argparse
from datetime import datetime, timezone


def inspect_uuid(u):
    info = {
        'uuid': str(u),
        'version': u.version,
        'variant': str(u.variant),
        'hex': u.hex,
        'int': u.int,
        'urn': u.urn,
        'bytes': len(u.bytes),
        'fields': {
            'time_low': f'{u.time_low:#010x}',
            'time_mid': f'{u.time_mid:#06x}',
            'time_hi_version': f'{u.time_hi_version:#06x}',
            'clock_seq_hi_variant': f'{u.clock_seq_hi_variant:#04x}',
            'clock_seq_low': f'{u.clock_seq_low:#04x}',
            'node': f'{u.node:#014x}',
        },
    }
    if u.version == 1:
        # Extract timestamp (100-ns intervals since Oct 15, 1582)
        timestamp = u.time
        epoch_diff = 122192928000000000  # diff between UUID epoch and Unix epoch
        unix_ts = (timestamp - epoch_diff) / 1e7
        try:
            dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
            info['timestamp'] = dt.isoformat()
        except (OSError, ValueError):
            pass
        info['clock_seq'] = u.clock_seq
        info['node_mac'] = ':'.join(f'{u.node >> (8*i) & 0xff:02x}' for i in range(5, -1, -1))
    return info


def cmd_gen(args):
    for _ in range(args.count):
        if args.version == 1:
            u = uuid.uuid1()
        elif args.version == 3 and args.name:
            ns = uuid.NAMESPACE_DNS if args.namespace == 'dns' else uuid.NAMESPACE_URL
            u = uuid.uuid3(ns, args.name)
        elif args.version == 5 and args.name:
            ns = uuid.NAMESPACE_DNS if args.namespace == 'dns' else uuid.NAMESPACE_URL
            u = uuid.uuid5(ns, args.name)
        else:
            u = uuid.uuid4()

        if args.format == 'bare':
            print(u.hex)
        elif args.format == 'upper':
            print(str(u).upper())
        elif args.format == 'braces':
            print(f'{{{u}}}')
        elif args.format == 'urn':
            print(u.urn)
        else:
            print(u)


def cmd_inspect(args):
    try:
        u = uuid.UUID(args.uuid)
    except ValueError as e:
        print(f'Invalid UUID: {e}')
        sys.exit(1)

    info = inspect_uuid(u)
    if args.json:
        print(json.dumps(info, indent=2, default=str))
    else:
        for k, v in info.items():
            if isinstance(v, dict):
                print(f'{k}:')
                for fk, fv in v.items():
                    print(f'  {fk}: {fv}')
            else:
                print(f'{k}: {v}')


def cmd_validate(args):
    for s in args.uuids:
        try:
            u = uuid.UUID(s)
            print(f'✓ {s} (v{u.version})')
        except ValueError:
            print(f'✗ {s} (invalid)')


def cmd_batch(args):
    for _ in range(args.count):
        u = uuid.uuid4()
        if args.format == 'bare':
            print(u.hex)
        elif args.format == 'upper':
            print(str(u).upper())
        else:
            print(u)


def cmd_nil(args):
    print('00000000-0000-0000-0000-000000000000')


def main():
    p = argparse.ArgumentParser(description='UUID generator and inspector')
    p.add_argument('--json', action='store_true')
    sub = p.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('gen', help='Generate UUIDs')
    s.add_argument('--version', '-v', type=int, default=4, choices=[1, 3, 4, 5])
    s.add_argument('--count', '-n', type=int, default=1)
    s.add_argument('--format', '-f', choices=['standard', 'bare', 'upper', 'braces', 'urn'], default='standard')
    s.add_argument('--name', help='Name for v3/v5')
    s.add_argument('--namespace', choices=['dns', 'url'], default='dns')
    s.set_defaults(func=cmd_gen)

    s = sub.add_parser('inspect', help='Inspect UUID details')
    s.add_argument('uuid')
    s.set_defaults(func=cmd_inspect)

    s = sub.add_parser('validate', help='Validate UUIDs')
    s.add_argument('uuids', nargs='+')
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser('batch', help='Generate many UUIDs fast')
    s.add_argument('count', type=int)
    s.add_argument('--format', choices=['standard', 'bare', 'upper'], default='standard')
    s.set_defaults(func=cmd_batch)

    sub.add_parser('nil', help='Print nil UUID').set_defaults(func=cmd_nil)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
