#!/usr/bin/env python3
"""Populate Binaries/PHY120 from the phone's own firmware image.

Scaffolding (INF / depex / panel xml) is taken from Binaries/giulia of the cloned
firmware tree - same SM8650 SoC, metadata only. Every .efi payload is replaced by
the driver carrying the same FILE_GUID inside the stock uefi.elf:

    outer FV -> FFS(FV_IMAGE) -> GUID_DEFINED 1D301FE9-BE79-4353-91C2-D23BC959AE0C
             -> gzip -> inner volume -> FFS -> PE32

Usage:
    python3 tools/import_binaries.py --tree <uefi tree> --stock-elf <IMAGES/uefi.elf>
"""
import argparse
import gzip
import pathlib
import shutil
import struct
import uuid

GZIP_GUID = struct.pack("<IHH", 0x1D301FE9, 0xBE79, 0x4353) + bytes.fromhex("91C2D23BC959AE0C")


def u24(b, o):
    return b[o] | (b[o + 1] << 8) | (b[o + 2] << 16)


def pe_body(pe):
    if pe[:2] != b"MZ":
        return None
    try:
        e = struct.unpack_from("<I", pe, 0x3C)[0]
        if pe[e:e + 4] != b"PE\0\0":
            return None
        coff = e + 4
        nsect = struct.unpack_from("<H", pe, coff + 2)[0]
        optsize = struct.unpack_from("<H", pe, coff + 16)[0]
        opt = coff + 20
        align = struct.unpack_from("<I", pe, opt + 36)[0] or 0x200
        sect = opt + optsize
        end = 0
        for k in range(nsect):
            s = sect + k * 40
            rs = struct.unpack_from("<I", pe, s + 16)[0]
            rp = struct.unpack_from("<I", pe, s + 20)[0]
            if rs and rp:
                end = max(end, rp + rs)
        return pe[:(end + align - 1) // align * align] if end else None
    except Exception:
        return None


def extract_pe(blob, off, fsize):
    body = blob[off + 24:off + fsize]
    p = 0
    while p + 4 <= len(body):
        ssize = u24(body, p)          # this firmware stores Size[3] then Type
        st = body[p + 3]
        if st in (0xFF, 0x00) or ssize < 4 or p + ssize > len(body):
            break
        if st in (0x10, 0x11, 0x12):
            pe = pe_body(body[p + 4:p + ssize])
            if pe:
                return pe
        p = (p + ssize + 3) & ~3
    k = body.find(b"MZ")
    return pe_body(body[k:]) if k >= 0 else None


def inner_volumes(elf):
    out = []
    pos = 0
    while True:
        i = elf.find(GZIP_GUID, pos)
        if i < 0:
            return out
        sec = i - 4                     # Size[3] + Type
        sec_size = u24(elf, sec)
        data_off = struct.unpack_from("<H", elf, i + 16)[0]
        payload = elf[sec + data_off: sec + sec_size]
        if payload[:2] == b"\x1f\x8b":
            try:
                out.append(gzip.decompress(payload))
            except OSError:
                pass
        pos = i + 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True, help="cloned firmware tree")
    ap.add_argument("--stock-elf", required=True, help="stock IMAGES/uefi.elf")
    a = ap.parse_args()

    tree = pathlib.Path(a.tree)
    src = tree / "Binaries/giulia"
    dst = tree / "Binaries/PHY120"
    if not src.is_dir():
        raise SystemExit(f"{src} missing (expected the giulia scaffolding in the tree)")

    # scaffold: metadata only, no payloads
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for f in dst.rglob("*.efi"):
        f.unlink()
    print(f"scaffolding: {src} -> {dst} (payloads removed)")

    elf = pathlib.Path(a.stock_elf).read_bytes()
    blobs = inner_volumes(elf)
    print(f"inner volumes from the stock image: {[len(b) for b in blobs]}")
    if not blobs:
        raise SystemExit("no gzip inner volume found - is this the right uefi.elf?")

    infs = sorted(dst.rglob("*.inf"))
    done, miss = 0, []
    for inf in infs:
        guid = None
        for line in inf.read_text(errors="replace").splitlines():
            if line.strip().upper().startswith("FILE_GUID"):
                guid = line.split("=", 1)[1].strip().split()[0].upper()
                break
        if not guid:
            continue
        try:
            raw = uuid.UUID(guid).bytes_le
        except ValueError:
            continue
        found = None
        for blob in blobs:
            pos = blob.find(raw)
            while pos != -1:
                ftype = blob[pos + 18]
                fsize = u24(blob, pos + 20)
                if 0x01 <= ftype <= 0x0C and 24 <= fsize <= len(blob) - pos:
                    found = extract_pe(blob, pos, fsize)
                    if found:
                        break
                pos = blob.find(raw, pos + 1)
            if found:
                break
        if found:
            inf.with_suffix(".efi").write_bytes(found)
            done += 1
        else:
            miss.append(inf.relative_to(dst).as_posix())

    print(f"drivers replaced with the phone's own: {done} / {len(infs)}")
    if miss:
        print("still without payload (not present in the stock image):")
        for m in miss[:10]:
            print(f"  {m}")


if __name__ == "__main__":
    main()
