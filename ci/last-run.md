# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T10:51:36Z |
| 提交 | `1b267e1c46a62b7cb86ede906af8b2cd12a39377` |
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
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/kern/kern_exec.c:7582:7: warning: declaration shadows a local variable [-Wshadow]
                int length = (int)chunk - resid;
                    ^
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/kern/kern_exec.c:7574:9: note: previous declaration is here
        size_t length = strlen(path);
               ^
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/kern/kern_exec.c:7598:28: warning: implicit conversion loses integer precision: 'int' to 'mode_t' (aka 'unsigned short') [-Wimplicit-int-conversion]
                        VATTR_SET(&va, va_mode, mode);
                        ~~~~~~~~~~~~~~~~~~~~~~~~^~~~~
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/sys/vnode.h:513:57: note: expanded from macro 'VATTR_SET'
#define VATTR_SET(v, a, x)              do { (v)-> a = (x); VATTR_SET_ACTIVE(v, a);} while(0)
                                                     ~  ^
             CC mac_iokit.o
8 warnings and 6 errors generated.
make[7]: *** [kern_exec.o] Error 1
make[7]: *** Waiting for unfinished jobs....
             CC mac_file.o
make[6]: *** [build_all] Error 2
make[5]: *** [do_all] Error 2
make[4]: *** [build_all] Error 2
make[3]: *** [build_all_recurse_into_conf] Error 2
make[2]: *** [build_all_recurse_into_bsd] Error 2
             CC mac_priv.o
             CC mac_pty.o
             CC mac_kext.o
             CC mac_mach.o
     LDFILELIST security
make[1]: *** [build_all_bootstrap_RELEASE^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 775: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=BCM2837 KERNEL_CONFIGS=${XNU_KERNEL_CONFIG:-DEVELOPMENT} ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
unixnu: bash failed (2); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
