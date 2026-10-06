#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

"""NasgorOS banner printed by the recovery installer.

Device releasetools call print_banner(info) from FullOTA_InstallBegin. Values
come from the target build.prop files; missing values are shown as "unknown".
"""

_PARTITIONS = ("product.build.prop", "system_ext.build.prop", "build.prop",
               "vendor.build.prop")


def _prop(info, name):
  for key in _PARTITIONS:
    props = info.info_dict.get(key)
    if props is None:
      continue
    try:
      value = props.GetProp(name)
    except Exception:  # pylint: disable=broad-except
      value = None
    if value:
      return value
  return ""


def _person(value):
  # Spaces cannot be stored in product properties, so names use underscores.
  return value.replace("_", " ") if value else "unknown"


def print_banner(info):
  version = _prop(info, "ro.nasgoros.display.version") or "?"
  codename = _prop(info, "ro.nasgoros.codename")
  title = " ".join(x for x in ("NasgorOS", version, codename) if x)
  device = _prop(info, "ro.nasgoros.device") or _prop(info, "ro.product.device")
  model = next((m for m in (_prop(info, "ro.product.%smodel" % p) for p in
                ("", "product.", "vendor.", "odm.", "system.")) if m), "")
  rows = [
      ("Device", "%s (%s)" % (device, model) if model else device),
      ("Version", _prop(info, "ro.nasgoros.version")),
      ("Android", _prop(info, "ro.build.version.release")),
      ("Security patch", _prop(info, "ro.build.version.security_patch")),
      ("Build type", _prop(info, "ro.nasgoros.releasetype")),
      ("Build date", _prop(info, "ro.build.date")),
      ("Maintainer", _person(_prop(info, "ro.nasgoros.maintainer"))),
      ("Builder", _person(_prop(info, "ro.nasgoros.builder"))),
  ]
  line = "=" * 40
  script = info.script
  script.Print(line)
  script.Print("  " + title)
  script.Print("  based on LineageOS")
  script.Print(line)
  for label, value in rows:
    script.Print(" %-15s: %s" % (label, value or "unknown"))
  script.Print(line)
  script.Print(" GApps: flash LiteGapps after the ROM,")
  script.Print(" before the first boot, and again after")
  script.Print(" every ROM update (no addon.d).")
  script.Print(" No OTA updates: install new builds manually.")
  script.Print(line)
