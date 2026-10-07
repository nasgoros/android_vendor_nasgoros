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
| `config/features.mk`, `config/features/` | Feature switches and independent product modules |
| [`PORTING.md`](PORTING.md) | Android 18 / other-ROM porting notes and future feature workflow |
| [`ports/crdroid/`](ports/crdroid/README.md) | Pinned crDroid Settings customization sources and integration |
| `patches/apply.py` | Apply or verify nasgorOS adaptations after source synchronization |
| `FEATURES.md` | Feature list, rebranded strings and **removed apps** |
| [`branding/logo/`](branding/logo/README.md) | Nasgor OS PNG logo: dark profile avatar and transparent master for web/About |
| [`bootanimation/`](bootanimation/README.md) | 2D fried-rice logo, animated steam/loading, Android ZIP and previews |
| [`wallpapers/`](wallpapers/README.md) | Senja default home wallpaper: charcoal blue and soft amber |
| `overlay/branding/` | Generated overlays renaming LineageOS → NasgorOS |
| [`removed-packages/`](removed-packages/README.md) | Minimal apps and first boot without Lineage Setup Wizard |
| `apps/LoraBrowserLite/`, `apps/Zimux/` | Signed browser and file manager/terminal prebuilts, native libraries and update records |
| `apps/Provision/` | Reuses AOSP one-time provisioning; no welcome UI |
| `tools/gen-branding-overlay.py` | Regenerates `overlay/branding` from the source tree |
| `build/tasks/nasgoros.mk` | `mka nasgoros` target producing `NasgorOS-17.0-<date>-<type>-<device>.zip` and `NasgorOS-Recovery-17.0-<date>.img` |

## Building

The following commands are for a later build, once compilation is authorized.
The current crDroid integration has passed source checks only.

```bash
repo init -u https://github.com/nasgoros/android -b 17.0 --git-lfs
# add the device manifest, e.g. local_manifests/merlinx.xml from the manifest repo
repo sync -c -j8 --no-clone-bundle --no-tags
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD" --check
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD"
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD" --verify
source build/envsetup.sh
breakfast merlinx
mka nasgoros
```

Set `NASGOROS_BUILDTYPE=OFFICIAL` for official builds (default `UNOFFICIAL`).
