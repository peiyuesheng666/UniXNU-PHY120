# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T12:24:09Z |
| 提交 | `a4a60c5b971e9bd5e7ecc8fb985e472628f1fa93` |
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
[13/15] Generating os_availability.modulemap
[14/15] Generating AvailabilityPrivate.modulemap
[14/15] Install the project...
-- Install configuration: ""
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/AppleInternal
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/PrivateHeaders/AvailabilityInternalPrivate.h -> ../../../../../../../usr/local/include/AvailabilityInternalPrivate.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/PrivateHeaders/AvailabilityProhibitedInternal.h -> ../../../../../../../usr/local/include/AvailabilityProhibitedInternal.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/os/availability.h -> ../../../../../../../../usr/include/os/availability.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/Availability.h -> ../../../../../../../usr/include/Availability.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/AvailabilityInternal.h -> ../../../../../../../usr/include/AvailabilityInternal.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/AvailabilityInternalLegacy.h -> ../../../../../../../usr/include/AvailabilityInternalLegacy.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/AvailabilityMacros.h -> ../../../../../../../usr/include/AvailabilityMacros.h
-- Created symlink: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/AvailabilityVersions.h -> ../../../../../../../usr/include/AvailabilityVersions.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/dyld/VersionMap.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/dyld/for_dyld_priv.inc
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/AvailabilityInternalPrivate.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/AvailabilityProhibitedInternal.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/os_availability_private.modulemap
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/AvailabilityPrivate.modulemap
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/os/availability.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/Availability.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityInternal.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityInternalLegacy.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityMacros.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityVersions.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/os_availability.modulemap
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/libexec/availability.pl
Restored 26 omitted public headers from Apple; blob hashes verified
scripts/phy120-patch-tree.sh: line 18: ROOT: unbound variable
build-xnu-4k-baseline.sh: line 52: bash scripts/phy120-patch-tree.sh failed
unixnu: bash failed (1); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
