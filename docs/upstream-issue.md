# 提交给上游 UniXNU 的 issue（告知式）

> 用途：按 `UniXNU/UniXNU` 的 CONTRIBUTING 约定，告知维护者「已有新设备成功引导 UniXNU」，
> 以便把 PHY120 加入文档的设备列表。
>
> 提交地址：https://github.com/UniXNU/UniXNU/issues/new

## 标题

```
在 OPPO Find X7 Ultra（PHY120 / SM8650）上成功启动 UniXNU
```

## 正文

按 CONTRIBUTING 里说的方式报个到：已经在一台非 Apple、且不在现有支持列表里的机型上
成功引导了 UniXNU，仓库已开源，希望能加入文档的设备列表。

### 设备

| 项 | 值 |
| --- | --- |
| 机型 | OPPO Find X7 Ultra（卫星通信版），型号 PHY120 |
| SoC | SM8650 |
| 面板 | 1440×3168，DSC command，120/90/60 Hz |
| boot_a | LUN 4，起始扇区 `121734`，49152 × 4096 |
| vendor_boot_a | LUN 4，起始扇区 `315974`，49152 × 4096 |
| 刷写方式 | 该机型 `fastboot` 被禁用，全程用 EDL（9008）写 `boot_a` / `vendor_boot_a` |

### 仓库

https://github.com/peiyuesheng666/UniXNU-PHY120

`./setup.sh <IMAGES/uefi.elf>` 一条命令完成：拉基础固件树、铺平台包、从手机自己的
`uefi.elf` 里抽出原厂 DXE 驱动、编固件、打 `boot.img` 与 `vendor_boot.img`。
仓库里不放任何专有二进制。设备树也是从手机自己的 `vendor_boot.img` 里抽的。

### 当前状态

UniXNU 启动管理器已在设备上运行并显示菜单。

### 移植过程中几个可能对别人有用的点

1. **固件卷加载地址不要猜**：直接用原厂 `uefi.elf` 的 ELF `PT_LOAD`
   （我们这里是 `paddr = 0xA7000000`、`filesz = 0x300000`），比照抄同 SoC 机型的配置可靠。
2. **启动镜像必须和原厂同格式**：这台机器只接受总长 192 MiB、header v4、
   `text_offset = 0`、`flags = 0xa`、`vbmeta` 块固定在 `0x220C000` 的镜像，
   kernel 字段放未压缩的 shim + 固件卷。
3. **一个很隐蔽的坑**：`BootShim` 在 MMU 关闭时把固件卷写到 `FD_BASE`，之后用
   `dc cvac` clean 目标区间。这一步会把更早阶段遗留的脏缓存行写回 DRAM，
   覆盖掉刚拷好的几个 cache line。症状是 FV 头、FFS 头、LZMA 头全部正确，
   但 SEC 报 `Decompress Failed - Invalid Parameter`，`LzmaDecode` 解到约 89% 返回
   `SZ_ERROR_DATA`；分段校验和比对显示只有第一个 256 KiB 块与镜像不一致。
   修复是在拷贝**之前**先对目标区间做一遍 `dc ivac`。
   如果其他移植也遇到「数据离线能解、固件里解不开」的现象，可以先查这一点。

### 后续

payload 卷（`EFI/UniXNU/unixnu.toml`）和内核还没打通，`kernel.macho` 也还没编，
这两块会继续推进。如果设备列表需要特定格式的信息，告诉我我按你们的格式补。

## 提交方式

| 方式 | 操作 |
| --- | --- |
| 手动（最快） | 打开 https://github.com/UniXNU/UniXNU/issues/new ，标题与正文从上文复制 |
| gh CLI | `gh issue create -R UniXNU/UniXNU -t "在 OPPO Find X7 Ultra（PHY120 / SM8650）上成功启动 UniXNU" -F docs/upstream-issue.md`（需先 `gh auth login`） |
| 让工具代发 | 需要一个带 `public_repo` 的 **classic** token（fine-grained token 无法访问非本人仓库） |
