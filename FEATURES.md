# NasgorOS features

Every NasgorOS feature lives in `vendor/nasgoros` whenever possible, so it survives
LineageOS rebases and Android upgrades (17.0 → 18.0) with a clear record of
dependencies and upgrade work. See [PORTING.md](PORTING.md)
for the Android 18 / other-ROM workflow and `config/features.mk` for feature switches.

| Tier | Meaning | Upgrade risk |
|---|---|---|
| 1 | Resources, overlays, product variables only | low |
| 2 | Own apps/services using platform and SDK APIs | low–medium |
| 3 | Patches to LineageOS/AOSP code (`patches/`) | high |

## Feature list

| Feature | Tier | Files | Upgrade notes |
|---|---|---|---|
| Version & `ro.nasgoros.*` props | 1 | `config/version.mk` | none |
| Output names `NasgorOS-<ver>-<date>-<type>-<device>.zip`, `NasgorOS-Recovery-<ver>-<date>.img` | 1 | `build/tasks/nasgoros.mk` | relies on `INTERNAL_OTA_PACKAGE_TARGET`, `INSTALLED_RECOVERYIMAGE_TARGET` |
| 2D fried-rice boot animation, steam and loading loop | 1 | `bootanimation/`, `TARGET_BOOTANIMATION` in `config/features/bootanimation.mk` | uses LineageOS `TARGET_BOOTANIMATION` and AOSP `f` fade; regeneration and previews: [bootanimation/README.md](bootanimation/README.md) |
| Senja default launcher wallpaper | 1 | `wallpapers/nasgor-senja.png`, `config/features/wallpaper.mk` | uses AOSP `ro.config.wallpaper` and a product asset; see [wallpapers/README.md](wallpapers/README.md) |
| "LineageOS" → "NasgorOS" in all locales | 1 | `overlay/branding/` (generated), `tools/gen-branding-overlay.py` | **re-run the generator after every rebase** and commit |
| Minimal app selection and silent first boot | 1 | `removed-packages/`, `config/features/minimal-apps.mk`, `apps/Provision/`, `overlay/minimal/` | check module names, transitive overrides, backup defaults and AOSP Provision on upgrade |
| Gesture navigation enabled by default | 1 | `config/overlay/config.xml` → `/product/overlay/config/config.xml`, `config/features/navigation.mk` | replaces LineageSetupWizard's navigation step (AOSP OverlayConfig); re-check overlay package name after upgrades |
| About phone / NasgorOS overview cards | 3 | Settings `NasgorAboutHeaderPreference`, `res/*/nasgor_about*`; crDroid `NasgorAbout`; exported in `patches/` | keep both XML and Catalyst bindings, real device values, search/controller keys, light/dark colors |
| Settings hub and LineageParts entry routing | 2 | `packages/apps/NasgorSettings`, `config/features/settings.mk` | LineageParts part keys, component aliases and LineagePreferenceLib |
| FPS info overlay (single switch, draggable, top-right default, no notification) | 2 | `packages/apps/NasgorSettings` (`performance/`, `nasgor-settings-sysconfig.xml`) | platform `registerTaskFpsCallback` and `TYPE_APPLICATION_OVERLAY`; relies on `allow-in-power-save` to run without a foreground notification |
| Removed crDroid Axion Sandbox (app lock/hide/isolation/settings spoof) | 3 | `patches/frameworks_base/0002-remove-axion-sandbox.patch` (reverts crDroid commits 766dc51, 9d1d615, 2ddabbe, eec891c), `patches/vendor_addons/0002-remove-axion-sandbox.patch` (`sdk/ax_sandbox`), `patches/device_lineage_sepolicy/0001-remove-axion-sandbox.patch`; Sandbox/AppLocker dropped from manifest | **high**: touches AMS/PMS/WM/NMS/IME/A11y, `IActivityManager.aidl`, SystemUI. On a crDroid bump, regenerate by reverting the upstream Axion sandbox commits again. AOSP App Lock (`AppLockController`, `AppLockActivity`) is kept |
| Removed OmniJaws weather | 3 | `patches/frameworks_base/0003-remove-omnijaws-weather.patch` (OmniJawsClient, QS tile, lock screen weather, `LOCKSCREEN_WEATHER_*` keys), `patches/packages_apps_crDroidSettings/0002-remove-omnijaws-weather.patch`, `patches/packages_services_QuickLook/0001-remove-omnijaws-weather.patch`; OmniJaws and `packages/resources/apps` dropped from manifest | medium: `WeatherImageView`/`WeatherTextView` remain as always-hidden stubs because ~70 crDroid clock layouts reference them; AOSP smartspace weather is untouched |
| No OTA updates (Updater removed, System update entry hidden, no OTA maintainer fetch) | 1 | `config/features/no-ota.mk`, `no-ota/Android.mk`, `overlay/no-ota/`; Settings patch skips `fetchMaintainerFromOta` | check the Updater module name and `config_show_system_update_settings` on upgrade |
| Recovery installer banner (version, security patch, maintainer, builder, LiteGapps hint) | 2 | `build/tools/nasgoros_banner.py`, called from the device `releasetools.py` `FullOTA_InstallBegin` | each new device's releasetools must call it; props `ro.nasgoros.{display.version,codename,maintainer,builder}` |
| About phone hardware details (chipset, CPU clusters/clock, GPU, RAM, storage, display, battery) | 3 | Settings `NasgorHardwareCategory` in `patches/packages_apps_Settings/0001-*`; device prop `ro.nasgoros.chipset` | values read live; set `ro.nasgoros.chipset` per device for the marketing name |
| Complete crDroid Settings customization sources | 3 | `ports/crdroid/`, `patches/`, `config/crdroid.mk`, manifest `snippets/nasgor-crdroid.xml` | pinned matching Settings, SystemUI, framework and provider sources; apply patches after sync and test the full ROM |

## Recovery file manager

Tier 3, isolated in the `nasgoros/android_bootable_recovery` fork's `file_manager/`
module with small UI hooks. `NASGOROS_WITH_RECOVERY_FILE_MANAGER` defaults to true;
`ro.nasgoros.recovery_file_manager` controls menu visibility. The menu browses
storage roots managed by recovery (internal media when readable, SD and USB OTG).
Each entry has an overflow menu for delete, rename, move and details. Folder taps
open folders; Power/Enter opens the action menu, including Open folder.

Delete requires confirmation. Moves never overwrite existing names; cross-volume
moves flush a staged copy before removing the source. Symlinks are never followed,
storage roots cannot be mutated, and child mounts cannot be traversed. Encrypted
internal media remains unavailable until recovery supports the device's decryption.
No PIN/FBE decryption, raw partition editing or file-content editor is included.
Recovery boot/touch/hot-unplug tests on merlinx are required before release.

## Rebranded strings

Generated by `tools/gen-branding-overlay.py` for every locale:

| App | Strings |
|---|---|
| lineage-sdk (Settings › About phone) | `lineage_version`, `lineage_updates`, `lineage_api_level`, `lineageos_system_label` |
| SetupWizard (not shipped in minimal selection) | `os_name`, `setup_services`; retained overlays for optional restoration |
| LineageParts | `lineageparts_title`, `privacy_settings_category` |

Intentionally **not** renamed: "LineageOS legal" (license attribution), LineageOS statistics
(data goes to LineageOS). Updater is not shipped: nasgorOS has no OTA updates. The crDroid Settings-host patch reads `ro.nasgoros.display.version` for About phone.
The original `ro.lineage.version` property is retained and must not be overridden.

## Removed experiments

- **2-button navigation** (Android 9 style, `NavigationBarMode2ButtonOverlay`): removed
  2026-10-07 after testing on merlinx — it did not work on Android 17.

## Removed LineageOS/AOSP apps

Removed with `LOCAL_OVERRIDES_PACKAGES` in `removed-packages/Android.mk` (module
`NasgorRemovePackages`). No LineageOS repository is modified.

| Module | App | Origin | Replacement |
|---|---|---|---|
| `Jelly` | Browser | LineageOS | Lora Browser Lite (`NASGOROS_WITH_LORA_BROWSER`) |
| `ExactCalculator` | Calculator | AOSP | none (user installs one) |
| `Etar` | Calendar | LineageOS | none |
| `DeskClock` | Clock / alarms | AOSP | none — **no alarm/timer app** until one is installed |
| `Canvas` | Photo editor | LineageOS | none (added by LineageOS 2026-09-30; editor for Glimpse) |
| `Glimpse` | Gallery | LineageOS | Zix Gallery (planned) |
| `Gallery2` | Gallery (legacy) | AOSP | Zix Gallery (planned) |
| `messaging` | Messages (SMS/MMS) | AOSP | none — **no SMS app** until one is installed |
| `Twelve` | Music player | LineageOS | none |
| `Recorder` | Voice recorder | LineageOS | none |
| `AxSandbox` (+ `AppLocker`) | crDroid app sandbox / app lock | crDroid (Axion) | none; code removed, see below. AOSP App Lock remains |
| `OmniJaws` | crDroid weather provider | crDroid (OmniROM) | none; code removed, see below |

The minimal selection additionally excludes `Seedvault`, `LocalContactsBackup`,
`AudioFX`, `MusicFX`, `FMRadio`, `FmRecordingsProvider`, `BuiltInPrintService`,
`PrintRecommendationService`, `BasicDreams`, `PhotoTable`, `EasterEgg`, `Traceur`
and `LineageSetupWizard`. Camera, file manager, PDF printing, WebView and the
selected crDroid feature providers remain installed. See
[removed-packages/README.md](removed-packages/README.md) for effects, first-boot
provisioning, and restoration steps; restoring the wizard requires removing
`NasgorProvision` as well.

## Settings › NasgorOS

`packages/apps/NasgorSettings` adds a **NasgorOS** entry to the Settings home page.
With the port enabled, it opens the crDroid customization host. The existing
LineageParts hub is accessible from Miscellaneous > Additional system settings.
Without the port, the app opens this hub directly. LineageParts' own entries in stock Settings (System › Status
bar, Buttons, Profiles; Display › LiveDisplay; Gestures; Privacy › Trust) are disabled at
runtime so every feature appears only under NasgorOS. LineageParts itself is unchanged.

The full crDroid Settings source import adds the original customization tabs and
subpages, plus a NasgorOS Performance tab and About screen. See
[ports/crdroid/README.md](ports/crdroid/README.md) for source pins, licensing,
provider dependencies, patch application and validation scope. Launcher and
ordinary applications keep their existing sources.

## Efek visual default untuk perangkat ringan

Konfigurasi performa mematikan blur jendela,
menyetel skala animasi jendela/transisi ke 0,5×, dan mematikan screensaver
aktif otomatis. Pulse-on-track dan Pulse ambient nonaktif secara default; Pulse
visualizer tetap dapat dinyalakan lewat crDroid Settings (cuaca OmniJaws dihapus).
Wallpaper bergerak tidak dipilih sebagai wallpaper bawaan; picker/dukungan live
wallpaper tetap tersedia. Efek yang bergantung pada setelan pengguna tetap dapat
diaktifkan kembali. Nilai SettingsProvider hanya menjadi default saat profil
pengguna baru dibuat; pilihan yang sudah tersimpan tidak ditimpa saat upgrade.
Overlay default ini dimasukkan oleh `config/features/performance-defaults.mk`.

## Browser bawaan

Lora Browser Lite v1.5.4 dipasang sebagai aplikasi product biasa melalui
`config/features/lora-browser.mk`. APK, SHA-256 dan prosedur upgrade tercatat di
[apps/LoraBrowserLite/README.md](apps/LoraBrowserLite/README.md). Set
`NASGOROS_WITH_LORA_BROWSER=false` untuk mengecualikannya.

## Zimux bawaan

Zimux v1.4.3 (`com.zimux`) disertakan melalui `config/features/zimux.mk` sebagai
aplikasi product biasa. Flag `NASGOROS_WITH_ZIMUX=false` mengecualikannya.
APK bertanda tangan asli dan library native dibawa bersama; catatan update serta
porting ada di [apps/Zimux/README.md](apps/Zimux/README.md). Belum diuji di HP.
