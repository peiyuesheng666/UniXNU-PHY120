#!/usr/bin/env python3
"""Overlay the UniXNU payload onto the STOCK vendor_boot.img, keeping it byte-identical elsewhere.

The stock image is the template: same total size, same header, same vendor_ramdisk_size
(18,494,345), same dtb section at 0x11A5000. Only the bytes inside the vendor_ramdisk
region change: our FAT volume goes at its start and the rest is zero padding.

That keeps every offset the bootloader relies on untouched.
"""
import pathlib
import struct
import subprocess

IMAGES = pathlib.Path("/mnt/e/6/玩机资源/OPPOFindX7Ultra卫星通信版刷机资源/"
                      "PHY120domestic_11_16.0.7.200CN01_2026051621160102/IMAGES")
W = pathlib.Path("/root/phy120-w1")
STOCK = IMAGES / "vendor_boot.img"
OUT = W / "out/vendor_boot-PHY120.img"
VOL_MIB = 16

UNIXNU_TOML = """version = 1

[boot]
timeout = 3
default = "xnu"

[[entry]]
id = "xnu"
title = "OPPO Find X7 Ultra - Darwin XNU"
type = "xnu"
path = "Payloads/kernel.macho"

[[entry]]
id = "exit"
title = "Return to firmware"
type = "action"
action = "exit"
"""


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit(f"failed: {cmd}")


def build_volume():
    stage = OUT.parent / "payloadstage"
    if stage.exists():
        sh(f"rm -rf {stage}")
    (stage / "EFI/UniXNU/Payloads").mkdir(parents=True, exist_ok=True)
    (stage / "EFI/UniXNU/unixnu.toml").write_text(UNIXNU_TOML)
    (stage / "EFI/UniXNU/Payloads/README.txt").write_text(
        "Put kernel.macho, kernel.macho.adt and kernel.macho.trustcache here.\n"
        "Only this vendor_ramdisk needs repacking; the firmware and boot.img stay as they are.\n")
    img = OUT.parent / "payload-PHY120.img"
    if img.exists():
        img.unlink()
    sh(f"mformat -C -i {img} -T $(({VOL_MIB}*2048)) -v PHY120ESP ::")
    sh(f"mcopy -s -i {img} {stage}/EFI ::")
    print(f"payload FAT volume: {img.stat().st_size} B ({VOL_MIB} MiB)")
    return img


def main():
    stock = bytearray(STOCK.read_bytes())
    pay = build_volume().read_bytes()

    page = struct.unpack_from("<I", stock, 12)[0]
    rd_size = struct.unpack_from("<I", stock, 24)[0]
    header_size = struct.unpack_from("<I", stock, 2096)[0]
    dtb_size = struct.unpack_from("<I", stock, 2100)[0]
    rd_off = (header_size + page - 1) // page * page

    print(f"stock: {len(stock)} B, page={page}, rd_off=0x{rd_off:x}, "
          f"vendor_ramdisk_size={rd_size}, dtb_size={dtb_size} @0x{rd_off+((rd_size+page-1)//page*page):x}")

    if len(pay) > rd_size:
        raise SystemExit(f"payload {len(pay)} B does not fit in the stock ramdisk {rd_size} B")

    out = bytearray(stock)
    region = pay + b"\x00" * (rd_size - len(pay))
    out[rd_off:rd_off + rd_size] = region

    OUT.write_bytes(out)

    # verification: everything outside the ramdisk region must be identical
    def outside(a, b):
        bad = 0
        for i in range(0, len(a), 4096):
            if rd_off <= i < rd_off + rd_size:
                continue
            if a[i:i + 4096] != b[i:i + 4096]:
                bad += 1
        return bad

    print(f"\nwritten {OUT} ({len(out)} B)  same size as stock: {len(out) == len(stock)}")
    print(f"  bytes changed only inside [0x{rd_off:x}, 0x{rd_off+rd_size:x})")
    print(f"  4 KiB blocks differing OUTSIDE the ramdisk: {outside(out, stock)}")
    print(f"  header fields identical: {out[0:2128] == stock[0:2128]}")
    print(f"  dtb section identical:   {out[rd_off+((rd_size+page-1)//page*page):][:dtb_size] == stock[rd_off+((rd_size+page-1)//page*page):][:dtb_size]}")
    print(f"  partition 49152*4096 = {49152*4096} -> fits: {len(out) == 49152*4096}")


if __name__ == "__main__":
    main()
