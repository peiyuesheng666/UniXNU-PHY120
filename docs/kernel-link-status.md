# 内核编译：现在只差链接

编译阶段全过（`bsd` / `osfmk` / `iokit`），日志 477 KB，零编译错误。
链接阶段剩下未定义符号，全部来自 **NativeMobileDisplay kit**：

```
_native_legacy_display_probe
_native_legacy_display_late_probe
_native_mobile_display_provider_probe
```

## 为什么

这几个 probe 由 `drivers/NativeMobileDisplay` 定义，而构建要把该 kit 编成静态库、
通过 `CONFIG_XNU_*_ARCHIVE` 传进链接。现有 defconfig 只配了两个归档：

```
CONFIG_XNU_NATIVE_VIRTIO_BLOCK_ARCHIVE="{tree}/build/native-virtio-block-verified-bundle/libNativeVirtioBlock.a"
CONFIG_XNU_VERIFIED_ROOT_ARCHIVE="{tree}/build/verified-root-os-xnu-bundle/libVerifiedRootProbe.a"
CONFIG_XNU_EXTRA_LD_ARCHIVES=""
```

缺 display kit 的那一条（以及生成该库的脚本步骤）。

## 实验记录（都是真跑出来的）

| legacy display | mobile display | 未定义符号 |
| --- | --- | --- |
| n | n | 1 个：`native_legacy_display_probe`（59 处引用） |
| y | n | 同上 |
| y | y | 3 个（多了 `late_probe`、`provider_probe`） |

说明守卫宏不是 `XNU_NATIVE_LEGACY_DISPLAY`，打开配置只会**增加**引用。

## 下一步（按代价排序）

1. 找到 UniXNU 里生成 display kit 归档的脚本（对应 `scripts/build-native-virtio-bindings.py`
   那一类），把产物接到 `CONFIG_XNU_EXTRA_LD_ARCHIVES`。
2. 或在 `ci/patch-tree.sh` 里给这三个 probe 加 `weak` 空实现（先让内核链接出来，
   上机时不进显示路径即可）。
3. 参考 sheng 仓库的 defconfig，看它是怎么配 display 归档的。

## 已修掉的坑（累计 18 个）

xcodes bottle / gum TTY / GitHub 限流 ×3 / `BINDM_FORCE_ROOT` / DriverKit iig /
`-mach_msg2` / owner `#error` ×3 / MOCKFS / KPI 导出表 / `PMCR0_EL1` /
hook 装错位置 ×2 / `ROOT` 未绑定 / 缓存名不匹配。
