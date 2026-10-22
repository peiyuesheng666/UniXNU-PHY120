# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T11:05:03Z |
| 提交 | `dbb8923b9a23001b682ae85b22b7876877a740d7` |
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
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/sys/cdefs.h:1193:45: note: expanded from macro '__probable'
#define __probable(x)   __builtin_expect(!!(x), 1)
                                            ^
             CC multi_layer_pkt_log.o
             CC entropy_sysctl.o
             CC audit_session.o
             CC audit_syscalls.o
             CC pthread_shims.o
             CC pthread_priority.o
             CC pthread_workqueue.o
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/pthread/pthread_shims.c:345:16: warning: variable 'kr' set but not used [-Wunused-but-set-variable]
        kern_return_t kr;
                      ^
1 warning generated.
             CC bsd_init.o
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/pthread/pthread_workqueue.c:1904:7: warning: variable 'start_timer' set but not used [-Wunused-but-set-variable]
        bool start_timer = false;
             ^
       GENERATE init_sysent.c from bsd.syscalls.master
1 warning generated.
             CC syscalls.o
             AS cpu_in_cksum.o
             AS cpu_copy_in_cksum.o
2 warnings generated.
             AS cpu_memcmp_mask.o
             CC init_sysent.o
     LDFILELIST bsd
make[1]: *** [build_all_bootstrap_RELEASE^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 776: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=BCM2837 KERNEL_CONFIGS=${XNU_KERNEL_CONFIG:-DEVELOPMENT} ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
unixnu: bash failed (2); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
