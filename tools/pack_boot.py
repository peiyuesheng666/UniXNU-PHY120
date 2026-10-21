#!/usr/bin/env python3
"""Pack the boot image exactly like the stock OPPO one, with our shim+FV in the kernel field.

Layout (from the stock IMAGES/boot.img, measured):
  0x0000           header v4, 1584 B, signature_size = 0
  0x1000           kernel field, kernel_size 0x220AA00, uncompressed
  0x220C000        vbmeta block (hash + RSA4096 signature + HASH descriptor)
  ...              zeros up to 49152 * 4096 = 201326592

Our change: the kernel field holds BootShim + firmware volume instead of the Android
kernel, and the arm64 Image header is patched to text_offset = 0, flags = 0xa,
image_size = 0x220AA00 (as the stock image does). ABL then loads it as a Linux-style
Image at DDR base and the shim relocates the 3 MiB volume to FD_BASE.
"""
import pathlib
import struct
import sys

W = pathlib.Path("/root/phy120-w1")
STOCK = pathlib.Path("/mnt/e/6/玩机资源/OPPOFindX7Ultra卫星通信版刷机资源/"
                     "PHY120domestic_11_16.0.7.200CN01_2026051621160102/IMAGES/boot.img")
SHIM = W / "Build/PHY120Pkg/DEBUG_CLANGPDB/FV/SILICIUM_UEFI.fd-bootshim"
OUT = W / "out/boot-PHY120-M1.img"

PART_SIZE = 49152 * 4096          # 201326592
KERNEL_OFF = 0x1000
VBMETA_OFF = 0x220C000
IMAGE_MAGIC_OFF = 0x38


def main():
    stock = bytearray(STOCK.read_bytes())
    shim = SHIM.read_bytes()
    print(f"stock boot.img : {len(stock)} B")
    print(f"shim+FV payload: {len(shim)} B")

    kernel_size = struct.unpack_from("<I", stock, 8)[0]
    print(f"stock kernel_size = 0x{kernel_size:x} ({kernel_size})")

    if len(shim) > kernel_size:
        sys.exit("payload larger than the kernel field")

    payload = bytearray(shim)
    # arm64 Image header inside the payload
    magic = payload[IMAGE_MAGIC_OFF:IMAGE_MAGIC_OFF + 4]
    print(f"payload header: text_offset=0x{struct.unpack_from('<Q', payload, 0x08)[0]:x} "
          f"image_size=0x{struct.unpack_from('<Q', payload, 0x10)[0]:x} "
          f"flags=0x{struct.unpack_from('<Q', payload, 0x18)[0]:x} magic={magic!r}")
    if magic != b"ARM\x64":
        sys.exit("payload does not carry an arm64 Image header at 0x38")

    struct.pack_into("<Q", payload, 0x08, 0)            # text_offset
    struct.pack_into("<Q", payload, 0x10, kernel_size)  # image_size
    struct.pack_into("<Q", payload, 0x18, 0xA)          # flags
    payload += b"\x00" * (kernel_size - len(payload))

    out = bytearray(stock)                    # header + vbmeta + zeros stay byte-identical
    out[KERNEL_OFF:KERNEL_OFF + kernel_size] = payload

    assert len(out) == PART_SIZE, len(out)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(out)

    # verification
    stock_b = STOCK.read_bytes()
    diff = [i for i in range(0, len(out), 1) if out[i] != stock_b[i]]
    head_diff = [i for i in diff if i < KERNEL_OFF]
    vb_diff = [i for i in diff if VBMETA_OFF - 0x40 <= i < VBMETA_OFF + 0x1000]
    print(f"\nwritten {OUT}  ({OUT.stat().st_size} B)")
    print(f"  header bytes differing from stock : {len(head_diff)}")
    print(f"  vbmeta-area bytes differing       : {len(vb_diff)}")
    print(f"  changed bytes start at offset     : 0x{min(diff):x}" if diff else "  no diff")
    print(f"  changed bytes end at offset       : 0x{max(diff):x}")

    hdr = bytes(out[:KERNEL_OFF])
    print(f"  4 KiB header identical to stock   : {hdr == stock_b[:KERNEL_OFF]}")
    print(f"  vbmeta block identical            : "
          f"{bytes(out[VBMETA_OFF:VBMETA_OFF + 0x10000]) == stock_b[VBMETA_OFF:VBMETA_OFF + 0x10000]}")
    print(f"  patched: text_offset=0x{struct.unpack_from('<Q', out, KERNEL_OFF+0x08)[0]:x} "
          f"image_size=0x{struct.unpack_from('<Q', out, KERNEL_OFF+0x10)[0]:x} "
          f"flags=0x{struct.unpack_from('<Q', out, KERNEL_OFF+0x18)[0]:x}")
    print(f"  flash geometry: LUN 4, start_sector 121734, 49152 sectors x 4096 B")


if __name__ == "__main__":
    main()
