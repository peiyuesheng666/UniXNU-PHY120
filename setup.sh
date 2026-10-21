#!/bin/bash
# One-shot build for the PHY120 (OPPO Find X7 Ultra, SM8650) UniXNU port.
#
#   ./setup.sh /path/to/IMAGES/uefi.elf
#
# Clones the base firmware tree, drops this port into it, imports the phone's own
# DXE drivers out of the stock firmware image, builds the firmware and packs both
# boot images. Nothing else has to be arranged by hand.
set -eu

STOCK_ELF="${1:-}"
PORT=$(cd "$(dirname "$0")" && pwd)
WORK="${WORK:-$PWD/phy120-build}"

if [ -z "$STOCK_ELF" ]; then
  echo "usage: $0 <path to IMAGES/uefi.elf from the PHY120 firmware package>" >&2
  echo "       (PHY120domestic_11_16.0.7.200CN01_*/IMAGES/uefi.elf)" >&2
  exit 2
fi
[ -f "$STOCK_ELF" ] || { echo "not found: $STOCK_ELF" >&2; exit 2; }

echo "== 1/6 base firmware tree =="
mkdir -p "$WORK"
cd "$WORK"
if [ ! -d uefi ]; then
  git clone --depth 1 -q -b sheng https://github.com/UniXNU/uefi-sheng.git uefi
fi
cd uefi

echo "== 2/6 platform package =="
mkdir -p Platforms/OPPO Resources/Configs Resources/DTBs
rm -rf Platforms/OPPO/PHY120Pkg
cp -a "$PORT/platform/PHY120Pkg" Platforms/OPPO/PHY120Pkg
cp "$PORT/platform/Resources/Configs/PHY120.toml" Resources/Configs/PHY120.toml
cp "$PORT/platform/Resources/DTBs/lanai-oppo-phy120.dtb" Resources/DTBs/

echo "== 3/6 device tree into the platform package =="
mkdir -p Platforms/OPPO/PHY120Pkg/FdtBlob
cp "$PORT/platform/Resources/DTBs/lanai-oppo-phy120.dtb" \
   Platforms/OPPO/PHY120Pkg/FdtBlob/lanai-oppo-phy120.dtb

echo "== 4/6 import the phone's own DXE drivers =="
python3 "$PORT/tools/import_binaries.py" --tree . --stock-elf "$STOCK_ELF"

echo "== 5/6 build firmware =="
python3 build_uefi.py -d PHY120 -r DEBUG

echo "== 6/6 pack boot images =="
python3 "$PORT/tools/pack_boot.py" --tree . --out ../out
python3 "$PORT/tools/mk_vendor_boot2.py" --tree . --stock "$(dirname "$STOCK_ELF")/vendor_boot.img" --out ../out \
  || echo "  (vendor_boot packing skipped: needs the stock vendor_boot.img next to uefi.elf)"

cat <<EOF

Done.
  firmware volume : $WORK/uefi/Build/PHY120Pkg/DEBUG_CLANGPDB/FV/SILICIUM_UEFI.fd
  boot image      : $WORK/out/boot-PHY120.img
  vendor_boot     : $WORK/out/vendor_boot-PHY120.img

Flash with EDL (fastboot is disabled on this device):
  boot_a        LUN 4, start_sector 121734, 49152 x 4096
  vendor_boot_a LUN 4, start_sector 315974, 49152 x 4096

The kernel (kernel.macho) still has to be built on macOS with Xcode; put it in
EFI/UniXNU/Payloads/ of the payload volume.
EOF
