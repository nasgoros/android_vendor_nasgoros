# nasgorOS vendor

Branding and configuration for **nasgorOS**, an Android distribution based on
[LineageOS](https://lineageos.org).

Branch `17.0` tracks LineageOS `lineage-24.0` (Android 17).

## How it works

LineageOS' `vendor/lineage/config/common.mk` inherits `vendor/extra/product.mk`
if it exists. The nasgorOS manifest links this repo's `product.mk` there, so
every LineageOS device tree builds nasgorOS without modification.

| File | Purpose |
|---|---|
| `config/version.mk` | nasgorOS version and `ro.nasgoros.*` properties |
| `config/common.mk` | Common nasgorOS product configuration |
| `FEATURES.md` | Feature list, rebranded strings and **removed apps** |
| `bootanimation/` | Boot animation (`generate.py` + `bootanimation.zip`) |
| `overlay/branding/` | Generated overlays renaming LineageOS → NasgorOS |
| `removed-packages/` | Apps not shipped in NasgorOS |
| `tools/gen-branding-overlay.py` | Regenerates `overlay/branding` from the source tree |
| `build/tasks/nasgoros.mk` | `mka nasgoros` target producing `NasgorOS-17.0-<date>-<type>-<device>.zip` and `NasgorOS-Recovery-17.0-<date>.img` |

## Building

```bash
repo init -u https://github.com/nasgoros/android -b 17.0 --git-lfs
# add the device manifest, e.g. local_manifests/merlinx.xml from the manifest repo
repo sync -c -j8 --no-clone-bundle --no-tags
source build/envsetup.sh
breakfast merlinx
mka nasgoros
```

Set `NASGOROS_BUILDTYPE=OFFICIAL` for official builds (default `UNOFFICIAL`).
