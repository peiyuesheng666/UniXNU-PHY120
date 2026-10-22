# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T10:31:25Z |
| 提交 | `e81f73b6121a42504c5c710b8ca61b807a33f126` |
| 触发 | workflow_dispatch |
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
        enum kperf_request type = (enum kperf_request)arg1;
                                  ^~~~~~~~~~~~~~~~~~~~~~~~
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/osfmk/kperf/kperfbsd.c:809:36: warning: cast to smaller integer type 'enum kptimer_period_limit' from 'void *' [-Wvoid-pointer-to-enum-cast]
        enum kptimer_period_limit limit = (enum kptimer_period_limit)arg1;
                                          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2 warnings generated.
             CC profile_runtime.o
             CC profile_runtime_data.o
             CC bind_subr.o
             CC bind_vfsops.o
             CC bind_vnops.o
             CC bsd_tests.o
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/miscfs/bindfs/bind_vfsops.c:237:23: error: use of undeclared identifier 'BINDM_FORCE_ROOT'
                xmp->bindm_flags |= BINDM_FORCE_ROOT;
                                    ^
1 error generated.
make[7]: *** [bind_vfsops.o] Error 1
make[7]: *** Waiting for unfinished jobs....
/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/xnu-work/bsd/miscfs/bindfs/bind_vnops.c:191:22: warning: variable 'bind_mp' set but not used [-Wunused-but-set-variable]
        struct bind_mount * bind_mp;
                            ^
1 warning generated.
make[6]: *** [build_all] Error 2
make[5]: *** [do_all] Error 2
make[4]: *** [build_all] Error 2
make[3]: *** [build_all_recurse_into_conf] Error 2
make[2]: *** [build_all_recurse_into_bsd] Error 2
make[1]: *** [build_all_bootstrap_DEVELOPMENT^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 775: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=BCM2837 KERNEL_CONFIGS=DEVELOPMENT ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
unixnu: bash failed (2); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
