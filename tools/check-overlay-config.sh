#!/bin/bash
# SPDX-FileCopyrightText: The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Fails if a static overlay in the product overlay directory is not listed in the
# product overlay config.xml. With a config.xml present, Android leaves unlisted
# android:isStatic overlays disabled.
#
# Usage: check-overlay-config.sh <product/overlay dir> <aapt2>

dir=$1
aapt2=$2
config=$dir/config/config.xml

[ -f "$config" ] || exit 0

missing=0
while IFS= read -r -d '' apk; do
  manifest=$("$aapt2" dump xmltree --file AndroidManifest.xml "$apk" 2>/dev/null) || continue
  grep -q 'isStatic(0x0101055a)=true' <<< "$manifest" || continue
  package=$(sed -nE 's/.*A: package="([^"]+)".*/\1/p' <<< "$manifest" | head -1)
  if ! grep -q "package=\"$package\"" "$config"; then
    echo "error: static overlay $package (${apk#$dir/}) is missing from $config" >&2
    missing=1
  fi
done < <(find "$dir" -name '*.apk' -print0)

if [ $missing -ne 0 ]; then
  echo "error: add the overlays above to vendor/nasgoros/config/overlay/config.xml" >&2
fi
exit $missing
