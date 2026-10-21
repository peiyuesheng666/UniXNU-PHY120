# PHY120 移植进度（当前状态）

## 已经确认成立的

| 项 | 证据 |
| --- | --- |
| FD 基址 `0xA7000000` | 原厂 `uefi.elf` 的 ELF `PT_LOAD`：`paddr=0xa7000000 filesz=0x300000`；实机已跑起来 |
| 启动镜像布局 | 与原厂 `boot.img` 逐字节同构：4 KiB 头 + `vbmeta@0x220C000` 全同，只有 kernel 字段变 |
| `text_offset=0`、`flags=0xa`、`image_size=0x220AA00` | ABL 能接受，BootShim 得以执行 |
| 面板 1440×3168 | 屏幕文字清晰、位置正确 |
| SMBIOS | 屏幕打印 `Project Silicium for OPPO Find X7 Ultra` |
| SEC / PrePi / MMU | `MMU: 37 regions`、`HOBs 85/89`、四个 constructor 全过 |
| 内层 FV 与引导段 | 7,483,400 B / 1,193,814 B，离线 `.lzma alone` 与 **EDK2 自身解码器源码**均解压成功 |

## 当前唯一卡点

SEC 解压内层 FV 时 `LzmaDecode` 返回 `SZ_ERROR_DATA`：

```
PHY120LZ: srcSize=1193814 decoded=7483400 encoded=1193801
PHY120LZ: result=1 status=0 remainDecoded=794207 remainEncoded=5
```

产出 6,689,193 / 7,483,400 字节后失败。

## 已排除的原因

| 假设 | 排除方式 |
| --- | --- |
| 压缩流损坏/截断 | 按**声明长度**离线解码：`eof=True`，正好 7,483,400 B |
| 段不自包含 | 同上（不需要段外字节） |
| scratch 只有 64 KiB 装不下 16 MiB 字典 | 单次 `LzmaDecode` 只用 16,256 B 概率表，**不分配字典**（字典=目标缓冲区）；且已把常量放大到 17 MiB 验证无用 |
| 缓冲区未初始化 | host 用 0xAA 填满 scratch/dest 仍成功 |
| Parallel LZMA GUID 不匹配 | `gParallelLzmaCustomDecompressGuid`=`bd9921ea…`；SEC 链的是标准 `LzmaCustomDecompressLib`（`SiliciumPkg dsc.inc:385`） |
| shim 缺 cache 维护 | `BootShim.S` 有 `dc cvac` 全区间 clean + `ic iallu` |

## 结论

解码器、数据、长度、缓冲区全部正常 ⇒ **RAM 里 `0xA7000000` 那份 FV 与镜像字节不一致**。
FV 头/FFS 头/LZMA 头（前 0x10030 字节）都对，错误发生在约 1 MB 之后 —— 指向
「搬运只对了一部分」或「有东西写了 0xA7xxxxxx」。

## 下一步（按优先级）

1. **在 SEC 里校验 RAM 副本**：对 FV 前 N 字节做累加/CRC 并打印，与离线值比对。
   一致 ⇒ 排除搬运；不一致 ⇒ 定位到第一个差异偏移，直接指认元凶。
2. **放开 RELEASE**：`SiliciumPkg/Sec/Sec.c` 里 `BaseDebugLibSerialPortConstructor()`
   的调用要加 `#ifndef MDEPKG_NDEBUG` 守卫，否则 RELEASE 链接失败
   （`undefined symbol: BaseDebugLibSerialPortConstructor`）。RELEASE 的 FV 更小，
   可验证是否与尺寸相关。
3. 若确认是搬运问题：改 shim（分块拷贝 + 每块 clean），或换 FD 落点重试。

## 更新：LZMA 已解决（M5/M6）

**根因**：`BootShim` 在 MMU 关闭时把 FV 写进 `0xA7000000`（非缓存写直达 DRAM），
随后用 `dc cvac`（clean+invalidate）扫目标区间——把上一阶段遗留的**脏缓存行写回 DRAM**，
覆盖了刚写好的数据。校验和证据：压缩载荷**只有第一个 256 KiB 块**与镜像不一致，其余三段逐字节相同。

**修复**：拷贝**之前**先对目标区间做 `dc ivac`（丢弃旧行，绝不写回）。

**结果**（实机验证）：

```
PHY120CK: 0 262144 83E0DCDE      <- 与离线期望值一致
PHY120LZ: result=0 status=4      <- SZ_OK
SEC: FV decompressed (Success)
SEC: Loading DXE core
...
Successfully Enabled UFS Cache Coherency
```

SEC 关卡通过，DXE 完整加载（PcdDxe、IortDxe、UFS、EnvDxeEnhanced）。

**下一个卡点**：`ASSERT [AutoGen.c:649]`，属 `MdeModulePkg/Application/BootManagerMenuApp`
（BDS 的启动管理器 UI）。原因：卷里没有可启动项、也没有 HII 数据库。
M6 已把 `PcdBootManagerMenuFile` 清零（`SiliciumPkg.dsc.inc:91`），让 BDS 跳过该应用。

**再下一步**：把 `UniXNU.efi` + `DarwinBoot` 集成进固件卷，才是真正的 UniXNU 菜单。
（另：`Binaries/PHY120` 仍是 giulia 占位；原厂驱动压缩存放，需先解压抽取。）

## 更新 2：当前卡点 = SmemDxe

SEC 之后 DXE 正常加载，实机日志末尾：

```
Loading driver ... IortDtDxe.efi
Successfully Enabled UFS Cache Coherency
... PcdDxe / ReportStatusCodeRouter / StatusCodeHandler / RuntimeDxe /
    ArmCpuDxe / ArmGicDxe / MetronomeDxe / ArmTimerDxe / SmemDxe
ASSERT_EFI_ERROR (Status = Not Found)
ERROR: C90000002:V03000007 10 F541D663-4A48-40AA-AABF-FF158CCAE34C
ASSERT AutoGen.c:392: !EFI_ERROR (Status)
```

- `SmemDxe.inf` 的 `FILE_GUID` = `F541D663-4A48-40AA-AABF-FF158CCAE34C`，**与 assert 里的 GUID 完全一致** → 元凶确定是 `SmemDxe`（giulia 的预编译二进制）
- 它的 `.depex` 只有 `06 08`（TRUE, END）→ **不依赖任何协议**，是无条件启动后内部失败
- 设备树假设已排除：giulia 自己的 `fdf` 里 DTB 那行也是注释掉的，而它的 `SmemDxe` 工作正常

因此怀疑它按固定地址/配置查找 SMEM 结构，而我们用的是 **giulia 的 `ConfigurationMapLib` 与 `MemoryMapLib`**：

| 键 | giulia 的值 | 备注 |
| --- | --- | --- |
| `SharedIMEMBaseAddr` | `0x14680000` | SM8650 IMEM，PHY120 需核对 |
| 内存表 `SMEM` 项 | `0x81D00000` + `0x200000` | 需与 PHY120 自己的 DTB 核对 |
| `DloadCookieAddr` | `0x01FD9000` | 同上 |
| `DRAM_CLK_PERIOD_ADDR` | `0x240BA050` | 同上 |

### 下一步（按优先级）

1. **核对 SMEM/IMEM 地址**：从 `vendor_boot` 的 dtb 段（`0x11a5000` 起 8 个 FDT）抽出我们的 `reserved-memory`，
   与上表逐项比对，修正 `Platforms/OPPO/PHY120Pkg/Library/{MemoryMapLib,ConfigurationMapLib}`。
2. 若仍失败：临时摘掉 `SmemDxe` 及其下游（`CmdDbDxe`/`PwrUtilsDxe`/`RpmhDxe`/`NpaDxe`/`ULogDxe`/`VcsDxe`/`ClockDxe`），
   先冲到 BDS，验证「固件全流程可用」。
3. 根治：解压原厂 `uefi.elf` 的内层 FV，按 `BASE_NAME` 换成 PHY120 自己的驱动（当前 `Binaries/PHY120` 是 giulia 占位）。

## 更新 3：原厂固件结构与「BDS 已跑通」

### 实机进展

去掉全部 53 个厂商驱动后（只留 30 个通用 EDK2 驱动），**BDS 成功起来**：

```
... HiiDatabase.efi / BdsDxe.efi / Fat.efi / UsbBus / UsbKb / UsbMassStorage
SimpleFbDxe.efi / SimpleTextInOutSerial.efi / ConPlatform / ConSplitter / GraphicsConsole
BdsDxe: PrepareForProtection: Failed to Locate SCM Protocol! Status = Not Found   (非致命)
RamManagerDxe.efi -> Failed to Locate RAM Partition Protocol!
ASSERT [RamManagerDxe] AutoGen.c(364)
```

即：SEC → DXE → BDS 全链路可跑。最后一个 assert 是因为我连**提供 RAM Partition Protocol 的厂商驱动**也一起摘了。

### 逐个 assert 的归因

| 驱动 | 现象 | 原因 |
| --- | --- | --- |
| `EnvDxeEnhanced` | `AutoGen.c:648 !EFI_ERROR` | 一加预编译二进制，需要我们没有的环境 |
| `SmemDxe` | GUID `F541D663-4A48-40AA-AABF-FF158CCAE34C` | 二进制里含 `SMEM is not initialized by Boot.` / `SMEM base addr=…memory mapping failed.` → 这条启动路径下 bootloader 没初始化 SMEM 分区表；地址本身是对的（PHY120 DTB 里 `smem_region@81d00000`、IMEM `0x14680000` 与 giulia 表一致） |
| `DALSYSDxe` | GUID `8E9BD160-B184-11DF-94E2-0800200C9A66` | 同样依赖 SMEM/OEM 环境 |
| `RamManagerDxe` | `Failed to Locate RAM Partition Protocol!` | 提供者被我一起摘掉了 |

### 原厂 `uefi.elf` 的真实结构（重要）

```
ELF PT_LOAD: paddr=0xa7000000 filesz=0x300000
FV @0x1000, attr=0xcfeff (ERASE_POLARITY=1, READ_LOCK), hdrlen=0x48
  @0x1fe8   SEC        323608
  @0x51000  FREEFORM     4376
  @0x52118  FV_IMAGE  1315150   GUID 1D301FE9-BE79-4353-91C2-D23BC959AE0C
  @0x193268 FV_IMAGE  1359912   同上 GUID
```

- **段头布局是 `[Size(3)][Type(1)]`**（老式 PI 顺序），不是 `[Type][Size3]`。这一条对写解析器是决定性的。
- 两个 `FV_IMAGE` 里都是 **GUID_DEFINED 段**，其 GUID = `1D301FE9-BE79-4353-91C2-D23BC959AE0C`，
  `DataOffset=0x18`，payload 开头 `1f 8b 08 00` → **gzip**（高通自定义压缩 GUID）。
- `gzip.decompress` 后得到内层 FV：3,903,496 B 与 3,907,592 B。

### 下一步（明确）

1. **内层 FV 的 FFS 遍历还差一层**：现在只解出 9 和 6 个 PE（应上百个）。内层卷里可能还有嵌套 `FV_IMAGE`，
   或 FFS 头需要同类擦除态/对齐处理。修好后即可把 `Binaries/PHY120` 里 107 个 `.efi`
   按 `FILE_GUID` 全部换成 PHY120 原厂载荷。
2. 换完后把 `DXE.inc` 里被注释的 53 个厂商驱动**恢复启用**（`tools/drop_all_vendor.py` 的反操作），重编。
3. 之后 `SmemDxe`/`DALSYSDxe`/`RamManagerDxe` 应当都不再 assert —— 因为它们就是原厂配套的那一套。

工具：`tools/extract_stock3.py`（gzip + FV 解析）、`tools/dump_nested.py`（段结构）、
`tools/identify_guid.py`（GUID 识别）、`tools/drop_all_vendor.py`（批量停用厂商驱动）。

## 工作区

- 构建树：`/root/phy120-w1`（干净树，`Build/PHY120Pkg/DEBUG_CLANGPDB/FV/`）
- 原始树未改动：`/root/phy120-fw`、`/root/phy120-out`、`/root/unixnu`
- 产物：`out/boot-PHY120-M1*.img`、`M2-scratch`、`M3-lzdbg`
- 工具：`tools/*.py`、`tools/*.sh`（离线解码、FV 解析、打包、插桩）
- 刷机几何：**LUN 4 / start_sector 121734 / 49152 扇区 × 4096 B**
