# 内核构建流水线（GitHub Actions，无需 Mac）

工作流：`.github/workflows/unixnu-kernel.yml`
产物：`kernel.macho`（`./unixnu build kernel` 会顺带用 IPSW 的 kernelcache 做预链接）

## 已经打通的环节

| 步骤 | 状态 | 说明 |
| --- | --- | --- |
| macOS runner | ✅ | `macos-14`，自带 Xcode 15 + iPhoneOS SDK |
| 工具链 | ✅ | `brew install cmake ninja unifdef llvm mtools dtc` |
| `unixnu defconfig PHY120_defconfig` | ✅ | 我们的 defconfig 被正确解析 |
| `unixnu fetch` | ✅ | xnu-10063 等源码 + 子模块 |
| `unixnu ipsw fetch` | ✅ | KernelCache / DeviceTree / StaticTrustCache 下载成功 |
| 补丁 + 源码准备 | ✅ | `patches/xnu/*` 应用，DriverKit 头文件回填 |
| 编译 | ⏳ | 已编过 `bsd` 全量与 `iokit` 大部分 |

## 路上踩到的坑（都已解决）

1. **`brew install xcodes` 在 arm64 上没 bottle**（Tier 3）——
   `blacktop` harness 的 `install_deps` 只要缺一个依赖就整段 brew。
   解决：预装 `jq gum bash cmake ninja` + 放一个 `xcodes` 桩（只针对 harness 路线，
   官方路线不需要）。
2. **`gum choose` 要 TTY** —— harness 在没有 `MACOS_VERSION` 时会交互式让选版本，
   CI 里直接报 `could not open TTY`。解决：固定 `MACOS_VERSION`。
3. **`http 403: rate limit exceeded`** —— UniXNU 的 `scripts/prepare-xnu-source.py`
   用裸 `urllib` 调 3 次 GitHub API 列目录，撞共享 runner IP 的匿名限流。
   解决：给这几处调用注入 runner 自己的 `GITHUB_TOKEN`。
4. **`use of undeclared identifier 'BINDM_FORCE_ROOT'`**（`bsd/miscfs/bindfs/bind_vfsops.c`）——
   Apple 内部的 bindfs 挂载标志位，开源树里没有。
   解决：`build-xnu-4k-baseline.sh` 支持 `XNU_EXTRA_CFLAGS`，
   传 `-DBINDM_FORCE_ROOT=0x80000000U`（该标志在开源代码里永不被置位，语义等价）。
   注意：**不要**去改 `.cache/xnu-work` 里的源码——那棵树是构建过程中才生成的，
   构建前的步骤改了也没用（这个坑我们踩过一次）。

## 当前的拦路点

```
DriverKit/OSObject.iig.cpp:233:26: error: use of undeclared identifier 'IORPCMessageFromMach'
```

DriverKit 生成的 `OSObject.iig.cpp` 调用了 `IORPCMessageFromMach`，同样只存在于
Apple 内部头文件里（IORPC 那一套）。

可行的处理方向，按代价从低到高：

1. **降到 `RELEASE` 配置**：`DEVELOPMENT` 会把 DriverKit 的 iig 生成物全部编进来，
   `RELEASE` 未必需要；先试一次，成本最低。
2. **补声明**：用 `XNU_EXTRA_CFLAGS` 加一个宏桩（例如把调用替换成返回 0），
   只在编译期生效，不影响我们要跑的路径（DriverKit 在手机上用不到）。
3. **摘除 DriverKit**：从构建里去掉 `iokit/DriverKit` 的 iig 目标（改 Makefile 或
   用 `patches/xnu` 加一个补丁）。

## 怎么读结果

- 工作流每次结束会把结论 + 日志尾部写进 `ci/last-run.md` 并推回仓库，
  所以 `git fetch` 就能看到，不需要 API 权限。
- 完整构建日志在产物 `phy120-kernel` 里（`out/PHY120/logs/kernel-bootstrap.log`），
  job 日志会被截断，排错要看这个文件。

## 刷机几何（不变）

| 分区 | LUN | 起始扇区 | 扇区数 × 扇区 |
| --- | --- | --- | --- |
| `boot_a` | 4 | 121734 | 49152 × 4096 |
| `vendor_boot_a` | 4 | 315974 | 49152 × 4096 |
