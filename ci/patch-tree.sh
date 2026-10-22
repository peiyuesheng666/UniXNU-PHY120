#!/bin/bash
# Applied to the prepared XNU work tree by build-xnu-4k-baseline.sh, right before
# UniXNU's source prepare step.
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SELF=$(cd "$(dirname "$0")" && pwd)

# 1. Seed the Apple directory listings so prepare-xnu-source.py never needs the
#    network. On a shared runner IP its unauthenticated API calls hit the anonymous
#    rate limit and abort the build before it starts.
SEED_DIR="$SELF/phy120-xnu-cache"
if [ -d "$SEED_DIR" ]; then
  mkdir -p "$ROOT/.cache/sources"
  cp "$SEED_DIR"/*.json "$ROOT/.cache/sources/"
  echo "PHY120: seeded $(ls -1 "$SEED_DIR" | wc -l | tr -d ' ') cached listings into .cache/sources"
fi

# 2. Drop the DriverKit iig translation units. They are generated from Apple's
#    internal interface definitions, use IORPCMessageFromMach and ask clang for
#    -mach_msg2. iokit/conf/files marks them "optional iokitcpp", so removing the
#    entries takes them out of the build. DriverKit is user-space driver support and
#    is not used by anything this port boots.
CONF="$ROOT/.cache/xnu-work/iokit/conf/files"
if [ -f "$CONF" ]; then
  before=$(wc -l < "$CONF")
  grep -v -E 'DriverKit/[A-Za-z0-9_]+\.iig\.cpp' "$CONF" > "$CONF.new" || true
  mv "$CONF.new" "$CONF"
  echo "PHY120: iokit/conf/files $before -> $(wc -l < "$CONF") lines (DriverKit iig dropped)"
fi

# 3. MIGKSFLAGS asks for -mach_msg2, which this Xcode's mig forwards to clang,
#    which rejects it; mig then aborts with "no SubSystem declaration".
MAKEDEF="$ROOT/.cache/xnu-work/makedefs/MakeInc.def"
if [ -f "$MAKEDEF" ] && grep -q -- '-mach_msg2' "$MAKEDEF"; then
  sed -i '' 's/^\([[:space:]]*\)-mach_msg2[[:space:]]*$/\1# PHY120: -mach_msg2 dropped, unsupported by this mig/' "$MAKEDEF"
  echo "PHY120: dropped -mach_msg2 from MIGKSFLAGS"
fi
