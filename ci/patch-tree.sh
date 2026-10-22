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
