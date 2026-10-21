# UniXNU-PHY120

把 [UniXNU](https://github.com/UniXNU/UniXNU) 移植到
**OPPO Find X7 Ultra（卫星通信版，型号 PHY120，SoC SM8650）** 的设备仓库。

[English](README.md) | 简体中文

## 一键编译

```sh
git clone https://github.com/peiyuesheng666/UniXNU-PHY120
cd UniXNU-PHY120
./setup.sh /path/to/IMAGES/uefi.elf
```

`uefi.elf` 取自官方固件包 `PHY120domestic_11_16.0.7.200CN01_*/IMAGES/`。
脚本会依次完成五件事：

1. 克隆基础固件树（`UniXNU/uefi-sheng`，`sheng` 分支）
2. 铺入 `uefi/Platforms/OPPO/PHY120Pkg` 和 `uefi/Resources/Configs/PHY120.toml`
3. 从 `uefi.elf` 中抽出手机**自己的** DXE 驱动，写入 `Binaries/PHY120`
4. 用 EDK II 编译固件
5. 打包 `boot.img` 与 `vendor_boot.img`

仓库里**不存放任何专有二进制**：厂商驱动始终由使用者从自己的固件镜像现抽。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `board.toml` | 设备描述（所有数值均为实机实测） |
| `configs/PHY120_defconfig` | 内核配置，派生自 sheng |
| `uefi/Platforms/OPPO/PHY120Pkg/` | Mu-Silicium 平台包（DSC/FDF/includes/库） |
| `uefi/Resources/Configs/PHY120.toml` | `[uefi_fd] base 0xA7100000 size 0x300000` |
| `uefi/Resources/DTBs/lanai-oppo-phy120.dtb` | 从手机 `vendor_boot.img` 抽出的设备树 |
| `package/unixnu.toml` | 我们自己的启动菜单项 |
| `tools/` | FV/FFS/LZMA/gzip 解析、boot 镜像与 vendor_boot 打包工具 |
| `docs/PHY120-STATUS.md` | bring-up 记录与待解决的问题 |

## 硬件事实

| 项目 | 数值 |
| --- | --- |
| SoC | SM8650（`ro.board.platform=pineapple`） |
| DDR 基址 | `0x80000000` |
| UEFI 固件卷加载地址 | `0xA7000000`，大小 `0x300000`（原厂 `uefi.elf` 的 PT_LOAD） |
| splash_region | `0xD5100000` + `0x2B00000` |
| 串口 | `qupv3_0@ac0000 / qup_uart@a94000`，115200 8N1 |
| 面板 | `AA545_P_1_A0006` / `AA545_P_3_A0005`，1440×3168，DSC command 模式，120/90/60 Hz |
| 触控 | `goodix-berlin` 与 `synaptics_tcm`（S3910）两套同时存在 |
| UFS | `ufshc@1d84000` |
| SMEM / IMEM | `0x81D00000` + `0x200000` / `0x14680000` |
| `boot_a` | LUN 4，起始扇区 `121734`，49152 × 4096 |
| `vendor_boot_a` | LUN 4，起始扇区 `315974`，49152 × 4096 |
| `userdata` | LUN 0，起始扇区 `4555500`（`0x4582EC`） |

## 原厂 ABL 能接受的启动镜像格式

总长 `201326592` 字节（49152 × 4096），header v4，`signature_size = 0`；
`0x1000` 处的 kernel 字段是一份**未压缩**的 arm64 Image，其中
`text_offset = 0`、`flags = 0xa`、`image_size = 0x220AA00`；
`0x220C000` 处的 `vbmeta` 块从原厂镜像**逐字节复制**；
kernel 偏移 0 处的 BootShim 负责把固件卷搬到 `0xA7000000`。

`BootShim.S` 在拷贝**之前**必须对目标区间做一遍 `dc ivac`：
否则某个更早阶段遗留的脏缓存行会被写回，覆盖刚拷好的固件卷，
SEC 随即以 `Decompress Failed - Invalid Parameter` 失败。

## 踩得最深的一个坑

`vendor_boot.img` 保持原厂的总大小与所有偏移不变，**只替换 `vendor_ramdisk` 区间的字节**
（payload 补零到原始的 18494345 字节），因为 bootloader 依赖 DTB 段正好落在 `0x11A5000`。

## 当前状态

UniXNU 启动管理器已在设备上运行并显示菜单。
