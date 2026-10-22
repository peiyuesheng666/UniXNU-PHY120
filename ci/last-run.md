# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T10:40:44Z |
| 提交 | `e2b535f12f40b72bb39fb37a7480315e258d3a27` |
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
1 warning generated.
             CC fbt.o
             CC fbt_blacklist.o
             CC sdt.o
             CC sdt_subr.o
             CC systrace.o
             CC profile_prvd.o
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/dev/dtrace/systrace.c:1008:15: warning: cast to smaller integer type 'int' from 'void *' [-Wvoid-pointer-to-int-cast]
        int sysnum = SYSTRACE_SYSNUM(parg);
                     ^~~~~~~~~~~~~~~~~~~~~
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/dev/dtrace/systrace.c:349:42: note: expanded from macro 'SYSTRACE_SYSNUM'
#define SYSTRACE_SYSNUM(x)              ((int)(x) & ((1 << SYSTRACE_SHIFT) - 1))
                                         ^~~~~~~~
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/dev/dtrace/systrace.c:1010:12: warning: variable 'uargs' set but not used [-Wunused-but-set-variable]
        uint64_t *uargs = NULL;
                  ^
2 warnings generated.
             CC fasttrap.o
       GENERATE systrace_args.c from bsd.syscalls.master
             CC init_sysent.o
             CC syscalls.o
             AS cpu_in_cksum.o
             AS cpu_copy_in_cksum.o
             AS cpu_memcmp_mask.o
             CC systrace_args.o
5 warnings generated.
     LDFILELIST bsd
make[1]: *** [build_all_bootstrap_DEVELOPMENT^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 775: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=BCM2837 KERNEL_CONFIGS=DEVELOPMENT ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
unixnu: bash failed (2); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
