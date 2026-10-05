# crDroid Settings for nasgorOS (Android 17)

Scope: all customization screens from crDroid Settings `17.0`, with the
framework/SystemUI implementations and providers those screens need. The main
launcher, Dialer, Updater, kernel and nasgorOS vendor product stay on their
existing sources. The separate minimal-app selection removes Lineage Setup
Wizard and optional apps; see [removed-packages/README.md](../../removed-packages/README.md). No GApps product is inherited; nasgorOS remains
vanilla, with LiteGapps installed separately by the user.

The import is pinned to exact revisions in `sources.lock.json` and the manifest
`snippets/nasgor-crdroid.xml`. Reusing the matching backend avoids preferences
that merely store a setting without a component implementing it.

## Customization screens

The original Status bar, Quick settings, Lock screen, Buttons, User interface,
Notifications, Sound and Miscellaneous screens and their subpages are retained.
Their device capability checks remain in place: for example, UDFPS choices do
not become available on a device without an under-display fingerprint reader.
`preferences.json` inventories 337 upstream preference entries across 34 XML
screens, including navigation and upstream About entries; it is an inventory,
not a count of features validated on a phone.

NasgorOS adds a **Performance** tab opening the FPS/CPU/GPU monitor, and replaces
the About tab with NasgorOS version, source/download links and upstream credit.
Miscellaneous also opens the original LineageParts hub for LiveDisplay, profiles,
charging and Trust. About phone, firmware and About NasgorOS share a lightweight
overview card with device-derived values and light/dark palettes.
Internal crDroid namespaces and original source license headers are retained.
Some upstream files are GPL-3.0, others Apache-2.0; do not relabel the entire
import as Apache-2.0.

## Sources and integration

- `sources.lock.json`: 27 pinned repositories (25 crDroid dependencies plus the
  Lineage overlay and wallpaper sources), source paths and reasons.
- `config/crdroid.mk`: required feature providers and font/clock/navigation
  resources. It deliberately selects resources without inheriting the whole
  `vendor/addons/config.mk` product.
- `patches/series.json`: the small nasgorOS adaptations, separately from upstream.
- `overlay/crdroid`: localized NasgorOS screen title and About-phone logo.
- `ro.nasgoros.crdroid_settings`: routes the NasgorOS homepage entry to the
  full customization host; it does not disable every backend feature.

Feature providers such as GameSpace, OmniJaws, OmniStyle, QuickLook, ThemeStore
and the sidebar implement options in Settings. They are dependencies, rather
than a switch to crDroid Home or replacement of ordinary applications.

The native backend includes the matching crDroid `frameworks/av` and
`system/core`. The former supplies per-app audio volume APIs and the TIFF tags
used by the DNG creator; the latter supplies the extended camera face layout
and camera commands. Mixing crDroid `frameworks/base` with the Lineage versions
of these repositories fails to compile `libandroid_runtime`.

The Lineage wallpaper app is retained with a small compatibility patch adding
`SystemSettingsRepository.stringSetting`. It observes `Settings.System` with
the same lifecycle, default-value and background-dispatcher behavior as the
app's existing secure-settings implementation, satisfying the shared crDroid API.
The 2026-10-06 build exposed this interface mismatch at 61%; after applying the
patch, the original `WallpaperPicker2Lib` Kotlin compiler command passed in the
build container with the build's JDK 21, and the complete-ROM build was resumed.

The upstream addons bootanimation module is excluded by a patch because it
would duplicate Lineage's module. NasgorOS' existing `TARGET_BOOTANIMATION`
continues to select the rice animation. A separate Lineage-overlay patch removes
four duplicate font modules so the complete addons font catalog can be used.
The Senja wallpaper remains configured.
About phone reads `ro.nasgoros.display.version`; upstream donation reminders and
crDroid maintainer lookups are disabled for NasgorOS.

## Build workflow

After the manifest and vendor changes are available in the chosen repositories:

```bash
# From the Android source tree:
repo sync -c -j4
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD" --check
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD"
python3 vendor/nasgoros/patches/apply.py --source-root "$PWD" --verify
source build/envsetup.sh
breakfast merlinx
m -j4 NasgorSettings Settings SystemUI
# Then build the full ROM and test it on the device.
```

Patch application checks all pinned revisions and conflicts before writing. It
skips already-applied patches and keeps unrelated local edits. It will not
silently apply the port to the old Lineage-only source tree.

For the workspace's full clones, verify without modifying `src/`:

```bash
python3 repos/android_vendor_nasgoros/patches/apply.py --clones repos --verify
```

Do not flash just a new Settings APK onto the old ROM expecting these features
to work: the matching framework and SystemUI belong in the same ROM build.

## Porting and validation status

See [PORTING.md](../../PORTING.md) for feature switches, isolated integrations,
Android 18 / other-ROM upgrade steps, API boundaries and the patch maintenance
checklist. Boot animation, wallpaper and NasgorSettings have separate product
modules under `config/features/`.

Source checks on 2026-10-06 passed: 27 exact source pins, the merged manifest,
resource/manifest XML files, 10 explicit activity intents, definitions for
160 selected product packages, and reconstruction of all six adaptation patches.
These checks do not validate the complete Soong dependency graph or SELinux policy.

An earlier NasgorSettings app build completed against the previous Lineage tree.
It does not validate the final monitor/routing changes or this crDroid port.
The first complete-ROM attempt reached native compilation and exposed the missing
`frameworks/av` and `system/core` dependencies. After adding the matching pinned
repositories, the original compiler commands for `android_media_AudioSystem.cpp`,
`android_hardware_Camera.cpp` and `android_hardware_camera2_DngCreator.cpp` passed
in the build container. The new `AppVolumeData` header was generated from the
upstream AIDL with the real AIDL compiler; validation outputs were isolated from
the ROM build outputs. Complete-ROM and device validation remain required.

Re-run source checks without compiling:

```bash
python3 repos/android_vendor_nasgoros/tools/check-crdroid-port.py \
  --clones repos --manifest repos/android
```

## Validation required before release

Verify the complete component/ROM build, first boot, Settings navigation, the
FPS overlay while switching apps, locking/unlocking, notification stop action,
CPU/GPU fallback values, all supported customization categories, and LiteGapps
compatibility. Device-dependent measurements must show unavailable when the
kernel or driver does not expose them; refresh rate must never substitute for FPS.

Upstream: https://github.com/crdroidandroid/android_packages_apps_crDroidSettings/tree/17.0
