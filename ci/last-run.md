# 最近一次内核构建

| 项 | 值 |
| --- | --- |
| 时间 | 2026-10-22T12:17:48Z |
| 提交 | `8cf948d92b343aca096043b71c1079dfbaab308b` |
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
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/include/AvailabilityPrivate.modulemap
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/os/availability.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/Availability.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityInternal.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityInternalLegacy.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityMacros.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/AvailabilityVersions.h
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/include/os_availability.modulemap
-- Installing: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/.cache/fakeroot/usr/local/libexec/availability.pl
Traceback (most recent call last):
  File "/Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/tree/scripts/prepare-xnu-source.py", line 49, in <module>
    CACHE.write_bytes(urllib.request.urlopen(URL, timeout=30).read())
                      ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 187, in urlopen
    return opener.open(url, data, timeout)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 493, in open
    response = meth(req, response)
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 602, in http_response
    response = self.parent.error(
        'http', request, response, code, msg, hdrs)
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 531, in error
    return self._call_chain(*args)
           ~~~~~~~~~~~~~~~~^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 464, in _call_chain
    result = func(*args)
  File "/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 611, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 403: rate limit exceeded
build-xnu-4k-baseline.sh: line 51: python3 scripts/prepare-xnu-source.py failed
unixnu: bash failed (1); full log: /Users/runner/work/UniXNU-PHY120/UniXNU-PHY120/UniXNU/out/PHY120/logs/kernel-bootstrap.log
```
