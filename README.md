# UniXNU-PHY120

Device port of [UniXNU](https://github.com/UniXNU/UniXNU) to the
**OPPO Find X7 Ultra** (satellite edition, model **PHY120**, SoC **SM8650**).

[English](README.md) | [简体中文](README.zh-CN.md)

## One-shot build

```sh
git clone https://github.com/peiyuesheng666/UniXNU-PHY120
cd UniXNU-PHY120
./setup.sh /path/to/IMAGES/uefi.elf
```

`uefi.elf` comes from the official firmware package
`PHY120domestic_11_16.0.7.200CN01_*/IMAGES/`. The script:

1. clones the base firmware tree (`UniXNU/uefi-sheng`, branch `sheng`)
2. drops `uefi/Platforms/OPPO/PHY120Pkg` and `uefi/Resources/Configs/PHY120.toml` in
3. imports the phone's **own** DXE drivers out of `uefi.elf` into `Binaries/PHY120`
4. builds the firmware with EDK II
5. packs `boot.img` and `vendor_boot.img`

Nothing proprietary is stored here: the vendor binaries are always regenerated
from the user's own firmware image.

## Layout

| Path | Content |
| --- | --- |
| `board.toml` | device descriptor (every value measured on hardware) |
| `configs/PHY120_defconfig` | kernel config, derived from sheng |
| `uefi/Platforms/OPPO/PHY120Pkg/` | Mu-Silicium platform package (DSC/FDF/includes/libs) |
| `uefi/Resources/Configs/PHY120.toml` | `[uefi_fd] base 0xA7100000 size 0x300000` |
| `uefi/Resources/DTBs/lanai-oppo-phy120.dtb` | device tree from the phone's `vendor_boot.img` |
| `package/unixnu.toml` | our boot menu entry |
| `tools/` | FV/FFS/LZMA/gzip dissection, boot image and vendor_boot packers |
| `docs/PHY120-STATUS.md` | bring-up log and open issues |

## Hardware facts

| Item | Value |
| --- | --- |
| SoC | SM8650 (`ro.board.platform=pineapple`) |
| DDR base | `0x80000000` |
| UEFI FD load address | `0xA7000000`, `0x300000` (stock `uefi.elf` PT_LOAD) |
| splash_region | `0xD5100000` + `0x2B00000` |
| UART | `qupv3_0@ac0000 / qup_uart@a94000`, 115200 8N1 |
| Panel | `AA545_P_1_A0006` / `AA545_P_3_A0005`, 1440x3168 DSC cmd, 120/90/60 Hz |
| Touch | `goodix-berlin` and `synaptics_tcm` (S3910) both present |
| UFS | `ufshc@1d84000` |
| SMEM / IMEM | `0x81D00000` + `0x200000` / `0x14680000` |
| boot_a | LUN 4, sector `121734`, 49152 x 4096 |
| vendor_boot_a | LUN 4, sector `315974`, 49152 x 4096 |
| userdata | LUN 0, sector `4555500` (`0x4582EC`) |

## Boot image layout the stock ABL accepts

`201326592` bytes (49152 x 4096), header v4, `signature_size = 0`;
kernel field at `0x1000` is an uncompressed arm64 Image with
`text_offset = 0`, `flags = 0xa`, `image_size = 0x220AA00`;
`vbmeta` at `0x220C000` copied verbatim from stock; BootShim at kernel offset 0
relocates the firmware volume to `0xA7000000`.

`BootShim.S` needs a `dc ivac` pass over the destination **before** the copy:
without it a stale dirty cache line is written back over the fresh volume and SEC
fails with `Decompress Failed - Invalid Parameter`.

## Favourite failure so far

`vendor_boot.img` keeps the stock size and offsets; only the `vendor_ramdisk`
bytes are replaced (payload padded to the original 18494345 bytes), because the
bootloader relies on the DTB section sitting at `0x11A5000`.

## Status

The UniXNU boot manager runs on the device and shows its menu.
