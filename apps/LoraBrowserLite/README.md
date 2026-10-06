# Lora Browser Lite

NasgorOS includes the upstream signed APK from release `v1.5.4` as a regular
product app. The APK is installed under `/product/app`, is not privileged, and
keeps its upstream signature. It requires Android 8.0 or newer.

Source: https://github.com/wahyu6070/lora-browser-lite/releases/tag/v1.5.4
Asset: `lora-1.5.4.apk`
SHA-256: `63cbfb1d35083d5e931f5f99a90f218d8ac17ae20615342ca06e8cb30769cc8a`

To update it, download the APK from a chosen release, verify its published
SHA-256, replace `LoraBrowserLite.apk`, and update this record. Do not re-sign
it; retaining the upstream signature allows normal in-place app updates.

Native libraries are extracted into the sibling `lib/` tree and installed for
the primary target ABI through `Android.mk`. The signed APK is copied unchanged
with dex preoptimization disabled. On updates, replace that tree with the new
APK's `lib/<abi>/*.so` entries and preserve executable mode (0755).

`LOCAL_OPTIONAL_USES_LIBRARIES` declares `androidx.window.extensions` followed by
`androidx.window.sidecar`, matching the APK manifest. Keep the order aligned when
updating the APK; manifest library verification remains enabled even though this
signed prebuilt does not use dex preoptimization.
