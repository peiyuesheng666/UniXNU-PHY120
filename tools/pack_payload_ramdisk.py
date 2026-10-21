#!/usr/bin/env python3
"""Build the UniXNU payload FAT volume and pack it into the boot image ramdisk.

Layout of the produced boot image (matches the stock one, only the kernel field
shrinks to make room for the ramdisk before the vbmeta block at 0x220C000):

  0x0000              header v4 (kernel_size / ramdisk_size updated)
  0x1000              kernel = BootShim + firmware volume (page padded)
  kernel_end (page)   ramdisk = FAT volume with EFI/UniXNU/unixnu.toml + payloads
  0x220C000           vbmeta block, untouched
  ...                 zeros to 49152 * 4096

The payload volume carries our own menu entries, so once kernel.macho exists it is
only a file replacement - no firmware rebuild.
"""
import pathlib
import struct
import subprocess
import sys

W = pathlib.Path("/root/phy120-w1")
OUT = W / "out"
STOCK = pathlib.Path("/mnt/e/6/玩机资源/OPPOFindX7Ultra卫星通信版刷机资源/"
                     "PHY120domestic_11_16.0.7.200CN01_2026051621160102/IMAGES/boot.img")
SHIM = W / "Build/PHY120Pkg/DEBUG_CLANGPDB/FV/SILICIUM_UEFI.fd-bootshim"
PART_SIZE = 49152 * 4096
KERNEL_OFF = 0x1000
VBMETA_OFF = 0x220C000
VOL_MIB = 24

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
id = "probe"
title = "PHY120 boot diagnostics"
type = "efi"
path = "Payloads/BootDiag.efi"

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
    return r.stdout


def build_volume():
    stage = OUT / "payloadstage"
    if stage.exists():
        sh(f"rm -rf {stage}")
    (stage / "EFI/UniXNU/Payloads").mkdir(parents=True, exist_ok=True)
    (stage / "EFI/UniXNU/unixnu.toml").write_text(UNIXNU_TOML)

    # placeholder so the menu item exists before the kernel is built
    (stage / "EFI/UniXNU/Payloads/README.txt").write_text(
        "Drop kernel.macho, kernel.macho.adt and kernel.macho.trustcache here.\n"
        "No firmware rebuild is needed: only this ramdisk is replaced.\n")

    img = OUT / "payload-PHY120.img"
    if img.exists():
        img.unlink()
    mb = VOL_MIB
    # mformat -T counts 512-byte sectors
    sh(f"mformat -C -i {img} -T $(({mb}*2048)) -v PHY120ESP ::")
    sh(f"mcopy -s -i {img} {stage}/EFI ::")
    print(f"payload volume: {img} ({img.stat().st_size} B, label PHY120ESP)")
    print(mdir_cmd := sh(f"mdir -i {img} -/ ::"))
    return img


def pack(vol: pathlib.Path):
    stock = bytearray(STOCK.read_bytes())
    shim = SHIM.read_bytes()
    kernel = bytearray(shim)
    kernel += b"\x00" * ((-len(kernel)) % 4096)

    rd = vol.read_bytes()
    rd_padded = bytearray(rd)
    rd_padded += b"\x00" * ((-len(rd_padded)) % 4096)

    kernel_off = KERNEL_OFF
    rd_off = kernel_off + len(kernel)
    end = rd_off + len(rd_padded)
    if end > VBMETA_OFF:
        raise SystemExit(f"ramdisk does not fit: needs to end before 0x{VBMETA_OFF:x}, got 0x{end:x}")

    out = bytearray(stock)
    struct.pack_into("<I", out, 8, len(kernel))          # kernel_size
    struct.pack_into("<I", out, 12, len(rd_padded))      # ramdisk_size
    out[kernel_off:kernel_off + len(kernel)] = kernel
    out[rd_off:rd_off + len(rd_padded)] = rd_padded

    # arm64 image header inside the kernel field
    struct.pack_into("<Q", out, kernel_off + 0x08, 0)          # text_offset
    struct.pack_into("<Q", out, kernel_off + 0x10, len(kernel))  # image_size
    struct.pack_into("<Q", out, kernel_off + 0x18, 0xA)         # flags
    if out[kernel_off + 0x38:kernel_off + 0x3C] != b"ARM\x64":
        raise SystemExit("kernel field does not carry the arm64 Image magic")

    dst = OUT / "boot-PHY120-M2-payload.img"
    dst.write_bytes(out)

    print(f"\n{dst} ({dst.stat().st_size} B)")
    print(f"  kernel   @0x{kernel_off:x} size={len(kernel)}")
    print(f"  ramdisk  @0x{rd_off:x} size={len(rd_padded)}")
    print(f"  vbmeta   @0x{VBMETA_OFF:x} untouched: "
          f"{bytes(out[VBMETA_OFF:VBMETA_OFF+0x1000]) == bytes(stock[VBMETA_OFF:VBMETA_OFF+0x1000])}")
    print(f"  text_offset=0x{struct.unpack_from('<Q', out, kernel_off+0x08)[0]:x} "
          f"flags=0x{struct.unpack_from('<Q', out, kernel_off+0x18)[0]:x}")
    return dst


if __name__ == "__main__":
    pack(build_volume())
