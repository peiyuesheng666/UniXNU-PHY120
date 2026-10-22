# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T13:18:21Z |
| 提交 | `4917b579937c260468dfb284f05af46073909436` |
| 触发 | push |
| 作业状态 | failure |

## 产物

```
(没有 kernel 输出)
```

## kernel.log 末尾 150 行

```
== submodules /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU
== tree /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree
== kernel: XNU
== kernel: bootstrap pass for the compile records
+ bash /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/scripts/build-xnu-4k-baseline.sh
      vtable for IOServiceCompatibility in IOService.cpo
      vtable for IOPMPowerSource in IOPMPowerSource.cpo
      ...
  "IOService::MetaClass::Dispatch(IORPC)", referenced from:
      vtable for IOService::MetaClass in IOService.cpo
  "vtable for IODispatchSource", referenced from:
      IODataQueueDispatchSource::init() in IOUserServer.cpo
      IODataQueueDispatchSource::free() in IOUserServer.cpo
      IOInterruptDispatchSource::init() in IOUserServer.cpo
      IOInterruptDispatchSource::free() in IOUserServer.cpo
      IOServiceNotificationDispatchSource::init() in IOUserServer.cpo
      IOServiceNotificationDispatchSource::free() in IOUserServer.cpo
      IOServiceStateNotificationDispatchSource::init() in IOUserServer.cpo
      ...
  NOTE: a missing vtable usually means the first non-inline virtual member function has no definition.
  "_native_legacy_display_late_probe", referenced from:
      _bsd_init in bsd_init.o
      _bsd_autoconf in bsd_init.o
  "_native_legacy_display_probe", referenced from:
      _bsd_init in bsd_init.o
      _native_mobile_graphics_client_probe in IOUserClient.cpo
  "_native_mobile_display_provider_probe", referenced from:
      _native_mobile_graphics_client_probe in IOUserClient.cpo
ld: symbol(s) not found for architecture arm64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make[3]: *** [/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/build/xnu/ios-obj/DEVELOPMENT_ARM64_BCM2837//mach.development.bcm2837.unstripped.noctf] Error 1
make[2]: *** [build_all] Error 2
make[1]: *** [build_all_bootstrap_DEVELOPMENT^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 776: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=${XNU_MACHINE_CONFIG:-BCM2837} KERNEL_CONFIGS=${XNU_KERNEL_CONFIG:-DEVELOPMENT} ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
== kernel: prepare storage headers
+ python3 /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/scripts/prepare-storage-headers.py
+ bash /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/scripts/build-xnu-4k-baseline.sh
PHY120: seeded 3 cached listings into .cache/sources
PHY120: iokit/conf/files      138 ->      138 lines (DriverKit iig dropped)
PHY120: dropped -mach_msg2 from MIGKSFLAGS
Restored 0 omitted public headers from Apple; blob hashes verified
Boot progress requires the audited UFS/owner-root, Virtio and source-corecrypto build
unixnu: bash failed (1); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel.log
```
