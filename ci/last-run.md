# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T12:07:40Z |
| 提交 | `994d46fb5ac8792f263d5ced6e49391e9dda1991` |
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
     -exported_symbol[s_list] command line option
  "_pmap_iommu_unmap", referenced from:
     -exported_symbol[s_list] command line option
  "_sart_get_desc", referenced from:
     -exported_symbol[s_list] command line option
  "_t6000dart_get_desc", referenced from:
     -exported_symbol[s_list] command line option
  "_t6000dart_vo_tte", referenced from:
     -exported_symbol[s_list] command line option
  "_t8020dart_get_desc", referenced from:
     -exported_symbol[s_list] command line option
  "_t8020dart_vo_tte", referenced from:
     -exported_symbol[s_list] command line option
  "_t8110dart_get_desc", referenced from:
     -exported_symbol[s_list] command line option
  "_t8110dart_max_translation_levels", referenced from:
     -exported_symbol[s_list] command line option
  "_t8110dart_vo_tt_index", referenced from:
     -exported_symbol[s_list] command line option
  "_t8110dart_vo_tte", referenced from:
     -exported_symbol[s_list] command line option
  "_uat_get_desc", referenced from:
     -exported_symbol[s_list] command line option
ld: symbol(s) not found for architecture arm64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make[3]: *** [/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/build/xnu/ios-obj/RELEASE_ARM64_BCM2837//mach.release.bcm2837.unstripped.noctf] Error 1
make[2]: *** [build_all] Error 2
make[1]: *** [build_all_bootstrap_RELEASE^ARM64^BCM2837] Error 2
make: *** [build] Error 2
build-xnu-4k-baseline.sh: line 776: make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" SDKROOT="${XNU_SDKROOT:-iphoneos}" ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=BCM2837 KERNEL_CONFIGS=${XNU_KERNEL_CONFIG:-DEVELOPMENT} ARCH_STRING_FOR_CURRENT_MACHINE_CONFIG=arm64 LARGE_MEMORY_DEFINE=-UARM_LARGE_MEMORY ARM64_LINK_ADDR=0xfffffff007004000 ARM64_PLKSEG_ADDR=0xfffffff004004000 DEPLOYMENT_TARGET_FLAGS="-miphoneos-version-min=17.0 -DXNU_TARGET_OS_IOS" DEPLOYMENT_LINKER_FLAGS="-Wl,-ios_version_min,17.0" RC_DARWIN_KERNEL_VERSION="$XNU_DARWIN" RC_ProjectSourceVersion="$XNU_VERSION" BUILD_LTO=0 BOUND_CHECKS=0 BUILD_WERROR="${XNU_BUILD_WERROR:-0}" MAKEJOBS=-j"${JOBS:-4}" CFLAGS_EXTRA="$EXTRA_CFLAGS" "${EXTRA_MAKE_ARGS[@]}" OBJROOT="$ROOT/build/xnu/ios-obj" SYMROOT="$ROOT/build/xnu/ios-sym" DSTROOT="$ROOT/build/xnu/ios-dst" failed
unixnu: bash failed (2); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
