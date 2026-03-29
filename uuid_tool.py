import uuid, argparse, time

def main():
    p = argparse.ArgumentParser(description="UUID generator and parser")
    sub = p.add_subparsers(dest="cmd")
    g = sub.add_parser("gen")
    g.add_argument("-v", "--version", type=int, default=4, choices=[1,4,5])
    g.add_argument("-n", "--count", type=int, default=1)
    g.add_argument("--name", default="")
    sub.add_parser("parse").add_argument("uuid")
    sub.add_parser("nil")
    args = p.parse_args()
    if args.cmd == "gen":
        for _ in range(args.count):
            if args.version == 1: print(uuid.uuid1())
            elif args.version == 5: print(uuid.uuid5(uuid.NAMESPACE_DNS, args.name))
            else: print(uuid.uuid4())
    elif args.cmd == "parse":
        u = uuid.UUID(args.uuid)
        print(f"version={u.version} variant={u.variant} hex={u.hex}")
        print(f"int={u.int} urn={u.urn}")
        if u.version == 1:
            ts = (u.time - 0x01b21dd213814000) / 1e7
            print(f"timestamp={ts} node={u.node:012x}")
    elif args.cmd == "nil":
        print("00000000-0000-0000-0000-000000000000")
    else:
        print(uuid.uuid4())

if __name__ == "__main__":
    main()
