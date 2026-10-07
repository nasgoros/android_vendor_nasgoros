# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Offer the Android 9 style 2-button navigation (pill + back) in
# Settings > System > Gestures > System navigation. AOSP keeps the mode
# (SystemUI, Launcher3 quickstep, Settings) but no longer ships the overlay.

PRODUCT_PACKAGES += NavigationBarMode2ButtonOverlay

# Gesture navigation on by default. LineageSetupWizard normally enables it during
# setup; NasgorOS ships silent provisioning instead (NasgorProvision), so the
# gestural overlay is default-enabled through AOSP's overlay config. It stays
# mutable, so users can still pick 3-button or 2-button navigation in Settings.
PRODUCT_COPY_FILES += \
    vendor/nasgoros/config/overlay/config.xml:$(TARGET_COPY_OUT_PRODUCT)/overlay/config/config.xml
