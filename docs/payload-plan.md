# payload 卷为什么读不到，以及怎么修

## 现象

`EFI/UniXNU/unixnu.toml` 放进 `boot.img` 的 ramdisk，或放进 `vendor_boot.img` 的
vendor_ramdisk，UniXNU 菜单里都没有我们自己的启动项。

## 根因（源码级确认）

UniXNU 是通过 `EFI_SIMPLE_FILE_SYSTEM_PROTOCOL` 读 payload 卷的，而卷要先变成**块设备**。
在这套固件里，这条路是：

```
某个厂商驱动 InstallProtocol(gEfiRamPartitionProtocolGuid)
        ↓
RamManagerLib（Silicon/Qualcomm/QcomPkg/Library/RamManagerLib/RamManager.c）
        ↓
RamManagerDxe → 用 RAM 分区表建块设备 → FatDxe 挂 FAT → UniXNU 读 unixnu.toml
```

而 `RamManagerLib` **只是消费者**：

```c
Status = gBS->LocateProtocol (&gEfiRamPartitionProtocolGuid, NULL, (VOID *)&mRamPartitionProtocol);
if (EFI_ERROR (Status)) {
  DEBUG ((EFI_D_ERROR, "Failed to Locate RAM Partition Protocol!\n"));
```

在整个 tree（`Silicon/`、`Common/Mu`、`Platforms/`、`Binaries/`）里搜
`gEfiRamPartitionProtocolGuid`，**只找到消费者，没有发布者**。发布者在我们没有的那部分
厂商二进制里，而它的数据来源是 SMEM 分区表（`RamPartitionTableLib.c` 里的
`Unable to read memory partition table from SMEM`）。

我们这条启动路径下 SMEM 没被初始化，所以整条链断在最上游。

## 为什么不能把 payload 塞进固件卷

固件卷只有 3 MiB（`[uefi_fd] size = 0x300000`，XBL 给的窗口就这么大），
而 payload 里最终要放 `kernel.macho`（预链接后 30 MiB 量级）——放不下。

## 建议的修法：让 BootShim 把 ramdisk 指针交出来

ABL 加载我们的 `boot.img` 时，按 arm64 启动协议会把 DT / ramdisk 的地址放在 x0..x3
里交给下一个阶段。现在的 `BootShim.S` 只用了自己算出来的地址，**把这几个寄存器丢了**。

所以：

1. **改 `BootShim.S`**：进入固件前，把 x0..x3 存到一个固定地址（自己选一个在
   `MemoryMapLib` 里预留的小页，比如 `0xA73F F000`），或者直接把 payload 的
   基址/长度写进去。
2. **新增一个很小的 DXE 驱动**（`PHY120RamDiskDxe`）：
   - 从那个固定地址读到 ramdisk 基址和长度
   - 调 EDK2 现成的 `gEfiRamDiskProtocol->Register (Base, Size, ...)`
     （需要把 `MdeModulePkg/Universal/Disk/RamDiskDxe/RamDiskDxe.inf` 加进 DSC/FDF）
   - `RamDiskDxe` 会发布 `BlockIo` + `DiskIo` + `SimpleFileSystem`，`FatDxe` 自动挂载
3. 这样 UniXNU 就能在卷里看到 `\EFI\UniXNU\unixnu.toml`，**完全不依赖 SMEM 和
   RAM 分区表**。

工作量估计：BootShim 改动十几行汇编，驱动 150 行 C + INF + FDF 条目。
这是目前最短、最可控的一条路。

## 备选（更省事但有代价）

- 把 payload 放到 UFS 的某个可写分区（比如单独划一个 FAT 分区），
  但需要原生 UFS 驱动先工作，而且刷分区有风险。
- 等原厂 SMEM / RAM 分区表那套跑通（要和厂商驱动栈一起调，目前卡在
  `SmemDxe: SMEM is not initialized by Boot`）。
