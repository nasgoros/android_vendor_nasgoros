# Zimux

NasgorOS ships the original signed Zimux v1.4.2 release as a regular app under
`/product/app/Zimux`. Package: `com.zimux`; versionCode: 7; minSdk: 26;
targetSdk: 36. No platform signing, privileged permissions or automatic root grant
are added. Users grant storage and other requested access through Android.

- Release: https://github.com/wahyu6070/zimux/releases/tag/v1.4.2
- Asset: `zimux-1.4.2.apk` (22,675,799 bytes)
- SHA-256: `e4d01b960a3a9e0f4cc9ebe724e191ec9aea8860aab49ed66a637a66d679167c`
- Disable inclusion: set `NASGOROS_WITH_ZIMUX=false` before inheriting the product.

## Packaging and updates

The release uses `extractNativeLibs=true` and compressed native libraries. Android
does not extract these for a bundled system app. `Android.mk` installs the exact
libraries from `lib/<abi>/` beside the APK, choosing the primary target architecture.
All four release ABIs are kept in the source for portability. Executable modes are
preserved for the terminal helpers. The original APK is copied unchanged so its
upstream signature remains valid; updates must use the same signing identity.
Dex preoptimization is disabled for this prebuilt.

For updates, verify the new upstream APK's checksum, replace `Zimux.apk`, and
regenerate the sibling `lib/` directory from the APK's `lib/<abi>/*.so` entries.
Remove old extracted libraries first, preserve names and executable mode (0755),
and update the version, SDK levels and hash above. Do not re-sign or repack the APK.
On an Android upgrade, recheck the prebuilt Make rules and native-library install
paths before building. After an authorized build, check app launch, file access,
terminal startup, archive handling and an in-place upstream APK update on device.

APK hash, manifest and extracted library contents were checked locally. The ROM
has not been compiled or tested on a device with this app.
