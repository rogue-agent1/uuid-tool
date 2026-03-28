#!/usr/bin/env python3
"""UUID tool — generate v1/v4/v5, validate, parse."""
import sys, uuid
def parse(u):
    u = uuid.UUID(u)
    return {"uuid": str(u), "version": u.version, "variant": str(u.variant),
            "hex": u.hex, "int": u.int, "bytes": len(u.bytes)}
def cli():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "v4"
    if cmd == "v1": print(uuid.uuid1())
    elif cmd == "v4": print(uuid.uuid4())
    elif cmd == "v5":
        ns = uuid.NAMESPACE_DNS; name = sys.argv[2] if len(sys.argv)>2 else "example.com"
        print(uuid.uuid5(ns, name))
    elif cmd == "parse":
        for k, v in parse(sys.argv[2]).items(): print(f"  {k}: {v}")
    elif cmd == "batch":
        n = int(sys.argv[2]) if len(sys.argv)>2 else 5
        for _ in range(n): print(uuid.uuid4())
    elif cmd == "validate":
        try: uuid.UUID(sys.argv[2]); print("Valid ✓")
        except: print("Invalid ✗")
if __name__ == "__main__": cli()
