#!/usr/bin/env python3
"""Dump reserved-memory / chosen nodes from the PHY120 device tree.

The vendor_boot dtb section holds 8 concatenated FDTs (first one at 0x11a5000);
we parse the first and print every reserved-memory entry with its label and reg,
so the SMEM/IMEM addresses can be compared with the values inherited from giulia.
"""
import pathlib
import struct

IMAGES = pathlib.Path("/mnt/e/6/玩机资源/OPPOFindX7Ultra卫星通信版刷机资源/"
                      "PHY120domestic_11_16.0.7.200CN01_2026051621160102/IMAGES")
OUT = pathlib.Path("/root/phy120-w1/out")


class FDT:
    def __init__(self, blob):
        (self.magic, self.total, off_struct, off_strings, _rsv, _ver,
         _last, _cpu, size_strings, size_struct) = struct.unpack_from(">10I", blob, 0)
        assert self.magic == 0xD00DFEED, "bad fdt magic"
        self.blob = blob
        self.struct = blob[off_struct:off_struct + size_struct]
        self.strings = blob[off_strings:off_strings + size_strings]

    def _s(self, off):
        end = self.strings.index(b"\x00", off)
        return self.strings[off:end].decode("utf-8", "replace")

    def walk(self, visit):
        pos, path = 0, []
        while pos + 4 <= len(self.struct):
            tok = struct.unpack_from(">I", self.struct, pos)[0]
            pos += 4
            if tok == 1:
                end = self.struct.index(b"\x00", pos)
                name = self.struct[pos:end].decode("utf-8", "replace")
                pos = (end + 4) & ~3
                path.append(name)
                visit("/" + "/".join(p for p in path if p), None, None)
            elif tok == 2:
                if path:
                    path.pop()
            elif tok == 3:
                length, nameoff = struct.unpack_from(">II", self.struct, pos)
                pos += 8
                val = self.struct[pos:pos + length]
                pos = (pos + length + 3) & ~3
                visit("/" + "/".join(p for p in path if p), self._s(nameoff), val)
            elif tok == 4:
                continue
            elif tok == 9:
                break


def cells(val, n=2):
    if len(val) % 4:
        return None
    ints = struct.unpack(">%dI" % (len(val) // 4), val)
    out = []
    for i in range(0, len(ints), n):
        pair = ints[i:i + n]
        if len(pair) == 2:
            out.append((pair[0] << 32) | pair[1])
        else:
            out.append(pair[0])
    return out


def main():
    vb = (IMAGES / "vendor_boot.img").read_bytes()
    base = vb.find(b"\xd0\x0d\xfe\xed", 0x100000)
    print(f"first FDT in vendor_boot at 0x{base:x}")
    blob = vb[base:]
    fdt = FDT(blob)
    nodes = []
    fdt.walk(lambda p, n, v: nodes.append((p, n, v)))

    # reserved-memory children: group props by path
    props = {}
    order = []
    for path, name, val in nodes:
        if path not in props:
            props[path] = {}
            order.append(path)
        if name:
            props[path][name] = val

    print("\n=== /reserved-memory entries (label + reg) ===")
    for path in order:
        if "/reserved-memory/" not in path:
            continue
        d = props[path]
        label = d.get("label", b"").rstrip(b"\x00").decode("latin-1", "replace")
        reg = d.get("reg")
        size = d.get("size")
        range_ = cells(reg) if reg else None
        sz = cells(size, 2) if size else None
        txt = ""
        if range_:
            txt = " reg=" + ",".join(f"0x{v:x}" for v in range_)
        elif sz:
            txt = " size=" + ",".join(f"0x{v:x}" for v in sz)
        name = path.rsplit("/", 1)[-1]
        print(f"  {name:44s}{(' label=' + label) if label else ''}{txt}")

    print("\n=== anything smem / imem ===")
    for path, name, val in nodes:
        low = path.lower() + (name or "").lower()
        if "smem" in low or "imem" in low:
            if name is None:
                print(f"  node {path}")
            elif name in ("reg", "size", "label"):
                c = cells(val)
                print(f"  {path} {name} = " + ((",".join(f"0x{v:x}" for v in c)) if c else val.hex()))

    # save the raw dtb for later use in the FV
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / "lanai-oppo-phy120.dtb"
    dst.write_bytes(blob[:fdt.total])
    print(f"\nsaved {dst} ({fdt.total} bytes)")


if __name__ == "__main__":
    main()
