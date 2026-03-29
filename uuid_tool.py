#!/usr/bin/env python3
"""uuid_tool - Generate and parse UUIDs."""
import sys, argparse, json, uuid, time

def parse_uuid(s):
    u = uuid.UUID(s)
    info = {"uuid": str(u), "version": u.version, "variant": str(u.variant), "hex": u.hex, "int": u.int, "bytes": len(u.bytes)}
    if u.version == 1:
        ts = (u.time - 0x01b21dd213814000) / 1e7
        info["timestamp"] = ts
        info["node"] = hex(u.node)
    return info

def main():
    p = argparse.ArgumentParser(description="UUID tool")
    sub = p.add_subparsers(dest="cmd")
    g = sub.add_parser("generate"); g.add_argument("-v", type=int, default=4, choices=[1,3,4,5])
    g.add_argument("-n", type=int, default=1); g.add_argument("--name", default="")
    g.add_argument("--namespace", default="dns", choices=["dns","url","oid","x500"])
    pr = sub.add_parser("parse"); pr.add_argument("uuid")
    args = p.parse_args()
    ns_map = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL, "oid": uuid.NAMESPACE_OID, "x500": uuid.NAMESPACE_X500}
    if args.cmd == "generate":
        uuids = []
        for _ in range(args.n):
            if args.v == 1: u = uuid.uuid1()
            elif args.v == 3: u = uuid.uuid3(ns_map[args.namespace], args.name)
            elif args.v == 4: u = uuid.uuid4()
            elif args.v == 5: u = uuid.uuid5(ns_map[args.namespace], args.name)
            uuids.append(str(u))
        print(json.dumps({"version": args.v, "uuids": uuids}))
    elif args.cmd == "parse":
        print(json.dumps(parse_uuid(args.uuid), indent=2))
    else: p.print_help()

if __name__ == "__main__": main()
