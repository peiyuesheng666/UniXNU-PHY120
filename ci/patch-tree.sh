#!/bin/bash
# Applied to the prepared XNU work tree, right after UniXNU's source prepare and
# before the compile starts.
#
# iokit/DriverKit/*.iig.cpp are generated from Apple's internal Interface
# Definition files. The open source tree cannot build them: they reference
# Apple-only symbols (IORPCMessageFromMach) and the generation step asks clang for
# -mach_msg2, which the toolchain does not know. They are marked
# "optional iokitcpp" in iokit/conf/files, so dropping those entries removes them
# from the build entirely. DriverKit is user-space driver support and is not used
# by anything this port boots.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CONF="$ROOT/.cache/xnu-work/iokit/conf/files"
[ -f "$CONF" ] || { echo "PHY120: no iokit/conf/files, nothing to do"; exit 0; }

before=$(wc -l < "$CONF")
grep -v -E 'DriverKit/[A-Za-z0-9_]+\.iig\.cpp' "$CONF" > "$CONF.new" || true
mv "$CONF.new" "$CONF"
after=$(wc -l < "$CONF")
echo "PHY120: iokit/conf/files $before -> $after lines (DriverKit iig dropped)"

# The kernel-server MIG flags ask for -mach_msg2, which the mig shipped with this
# Xcode does not implement: it forwards the flag to clang, which rejects it, and
# mig then fails with "no SubSystem declaration". Drop it from the flag list.
MAKEDEF="$ROOT/.cache/xnu-work/makedefs/MakeInc.def"
if [ -f "$MAKEDEF" ] && grep -q -- '-mach_msg2' "$MAKEDEF"; then
  sed -i '' 's/^\([[:space:]]*\)-mach_msg2[[:space:]]*$/\1# PHY120: -mach_msg2 dropped, not supported by this mig/' "$MAKEDEF"
  echo "PHY120: dropped -mach_msg2 from MIGKSFLAGS"
fi

# Authenticate the Apple directory listings. Without this the shared runner IP hits
# the anonymous API rate limit (HTTP 403) and the source prepare aborts.
PREP="$ROOT/.cache/xnu-work/../scripts/prepare-xnu-source.py"
for CAND in "$ROOT/scripts/prepare-xnu-source.py" "$ROOT/../scripts/prepare-xnu-source.py"; do
  [ -f "$CAND" ] || continue
  python3 - "$CAND" <<'INNER'
import os, pathlib, sys
p = pathlib.Path(sys.argv[1]); s = p.read_text()
if "GH_TOKEN_FOR_FETCH" in s:
    print("PHY120: fetch already authenticated"); raise SystemExit(0)
tok = os.environ.get("GH_TOKEN_FOR_FETCH", "")
if not tok:
    print("PHY120: no token in env, leaving fetch unauthenticated"); raise SystemExit(0)
inject = ("_tok = os.environ.get('GH_TOKEN_FOR_FETCH')\n"
          "if _tok:\n"
          "    _orig = urllib.request.urlopen\n"
          "    def _open(url, *a, **kw):\n"
          "        req = urllib.request.Request(url if isinstance(url, str) else url)\n"
          "        req.add_header('Authorization', 'Bearer ' + _tok)\n"
          "        return _orig(req, *a, **kw)\n"
          "    urllib.request.urlopen = _open\n")
s = s.replace("import urllib.request", "import urllib.request\n" + inject, 1)
p.write_text(s)
print("PHY120: authenticated", p)
INNER
done
