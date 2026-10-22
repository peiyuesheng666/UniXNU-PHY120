# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T10:34:31Z |
| 提交 | `10f91fadced11d1947c007e6f6eda0bebec95c1c` |
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
  File "<stdin>", line 6
    f.write_text('/* PHY120 CI */
                 ^
SyntaxError: unterminated string literal (detected at line 6)
build-xnu-4k-baseline.sh: line 70: python3 -  <<'INNER'
import pathlib
f = pathlib.Path('.cache/xnu-work/bsd/miscfs/bindfs/bind_vfsops.c')
if f.exists():
    t = f.read_text()
    if '#define BINDM_FORCE_ROOT' not in t:
        f.write_text('/* PHY120 CI */
#ifndef BINDM_FORCE_ROOT
'
                     '#define BINDM_FORCE_ROOT 0x80000000u
#endif

' + t)
        print('PHY120 CI: defined BINDM_FORCE_ROOT')
INNER
 failed
unixnu: bash failed (1); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
