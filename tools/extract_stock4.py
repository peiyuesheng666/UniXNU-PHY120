#!/usr/bin/env python3
"""Replace Binaries/PHY120 .efi payloads with PHY120's own, located by FILE_GUID.

The inner volumes have no usable FV header at offset 0 (FvLength reads as garbage),
so instead of walking the volume we search the decompressed blobs for each INF's
16-byte FILE_GUID and parse the FFS header in place:
  name[16] integrity[2] type[1] attributes[1] size[3] state[1]
Sections use the original layout Size[3] then Type.
"""
import gzip
import pathlib
import struct
import uuid

IMAGES = pathlib.Path("/mnt/e/6/玩机资源/OPPOFindX7Ultra卫星通信版刷机资源/"
                      "PHY120domestic_11_16.0.7.200CN01_2026051621160102/IMAGES")
W = pathlib.Path("/root/phy120-w1")


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
        ssize = u24(body, p)
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


def main():
    elf = (IMAGES / "uefi.elf").read_bytes()
    blobs = []
    for base, size in ((0x52118, 1315150), (0x193268, 1359912)):
        body = elf[base + 24:base + size]
        sec_size = u24(body, 0)
        data_off = int.from_bytes(body[20:22], "little")
        inner = gzip.decompress(body[data_off:sec_size])
        blobs.append(inner)
        print(f"inner blob @0x{base:x}: {len(inner)} B")

    root = W / "Binaries/PHY120"
    infs = sorted(root.rglob("*.inf"))
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
                if pos + 24 <= len(blob):
                    ftype = blob[pos + 18]
                    fsize = u24(blob, pos + 20)
                    if 0x01 <= ftype <= 0x0C and 24 <= fsize <= len(blob) - pos:
                        pe = extract_pe(blob, pos, fsize)
                        if pe:
                            found = pe
                            break
                pos = blob.find(raw, pos + 1)
            if found:
                break
        if found:
            inf.with_suffix(".efi").write_bytes(found)
            done += 1
        else:
            miss.append(inf.relative_to(root).as_posix())

    print(f"\nINFs: {len(infs)}   replaced with PHY120's own: {done}   still giulia: {len(miss)}")
    for m in miss[:12]:
        print(f"   miss {m}")


if __name__ == "__main__":
    main()
