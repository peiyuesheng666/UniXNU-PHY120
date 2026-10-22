# 同 SoC 的参考项目（同步记录）

PHY120 是 SM8650，和下面几个项目同一颗芯片。它们的进度领先我们很多，
这里记录能直接借鉴的东西，避免重复踩坑。

## 一加 Ace 5（giulia，SM8650）

上游文档页：https://unixnu.com/zh/devices/giulia

| 项目 | 状态 |
| --- | --- |
| [tycykp/UniXNU-OnePlus-Ace5](https://github.com/tycykp/UniXNU-OnePlus-Ace5) | **已到 Hello / 设置界面**（2026-10-22 实机记录），触控开发中 |
| `jasper2863/UniXNU-giulia` | 上游文档记录为「已到 GUI 进度条，安装服务受阻」（写这份文档时仓库已 404，可能改名或转私有） |

两个项目都走 **iOS 16 / Darwin 22** 路线。这一点对我们很关键：
我们最早的困局是「UniXNU 主干固定在 xnu-10063（Darwin 23 = iOS 17），
而 iPhone X 只到 iOS 16」，既然 SM8650 上已有两个项目在 Darwin 22 上跑通，
那么 PHY120 也应该按 iOS 16 路线规划，而不是硬啃 iOS 17。

### 他们已经打通的、我们还没通的

| 子系统 | 他们的证据 | 我们的状态 |
| --- | --- | --- |
| UEFI 交接 | 已验证 | ✅ 已验证（菜单能出） |
| XNU 启动、CPU0、SGI | 部分验证 | ❌ `kernel.macho` 未编 |
| 原生 UFS 读取 | 已验证 | ❌ 未开始 |
| USB CDC 调试串口 | 已验证 | ❌ 未开始 |
| HFSX 根卷读写挂载 | 已验证 | ❌ 未开始 |
| `launchd` / 系统服务 | 已验证 | ❌ 未开始 |
| 图形界面 | 到 Hello / 设置 | ❌ 未开始 |
| 触控 | 控制器身份与报文已验证 | ❌ 未开始 |
| Wi-Fi | WCN7850 停在 `Detect.Quiet` | 未开始 |

### 可以直接借鉴的工程做法

1. **Linux 构建依赖清单**（他们的 README 明确列出，我们当时踩过 NuGet/extdep 的坑）：
   `build-essential`、Clang/LLVM + LLD、`uuid-dev`、NASM、`gcc-aarch64-linux-gnu`、
   ACPICA 工具、`dtc`，以及 **Mono + mono 证书包**（上游 NuGet 工具需要）。
   我们本地是靠从旧构建树里拷 `Mu-Basetools_extdep` / `mu_nasm_extdep` /
   `onecrypto-bin_extdep` 绕过去的，换成 Mono + NuGet 才是干净做法。
2. **仓库结构**：`sources.json` 锁上游版本、`hardware/` 放机器可读硬件事实与测试证据、
   `tests/` 放离线测试、`.github/workflows/` 跑 CI。
   我们现在只有 `board.toml` + `docs/`，后续应该补 `sources.json` 和 `hardware/`。
3. **验证分四级**，不能混为一谈：编译成功 / 产物校验 / 实机启动 / 功能可用。
   尤其别把「编译过了」当成「功能可用」。
4. **userdata 的 LBA 从实机只读 GPT 读**，并记录 CRC。
   他们的 256 GB 机器是 `first_lba = 3920350`、`last_lba = 61321210`；
   我们 PHY120 从刷机 XML 得到的 `first_lba = 4555500 (0x4582EC)`，
   `last_lba` 仍是 0，需要在实机上补读。

### 尚未对上的一个点

他们的 `board.toml` 里 `[ipsw]` 仍然指向
`iPad_Pro_HFR_17.7.11_21H461_Restore.ipsw`（`iPad7,1` / `j120ap` / `chip_id 0x8011`），
但我们这里记的是「iOS 16 / Darwin 22」开发路线。
两者如何对应（内核源码版本与 userland IPSW 的组合方式）暂时不清楚，
等我们真正开始编内核时再去他们的仓库里确认 `sources.json` 和 `ios16/` 目录的用法。

## 对 PHY120 的结论

- 目标系统改为 **iOS 16 / Darwin 22** 路线，而不是死守 iOS 17
- 下一步优先级：先解决 payload 卷（`unixnu.toml`）能不能被固件认出来，
  再谈内核；厂商 DXE 驱动栈可以向他们请教顺序
