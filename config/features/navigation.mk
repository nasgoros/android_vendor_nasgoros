# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Gesture navigation on by default. LineageSetupWizard normally enables it during
# setup; NasgorOS ships AOSP Provision (silent provisioning) instead, so the
# gestural overlay is default-enabled through AOSP's overlay config. It stays
# mutable, so users can still pick 3-button navigation in Settings.
#
# The Android 9 style 2-button mode was tried and removed (2026-10-07): it did not
# work on Android 17 (Launcher3 quickstep support is largely gone).
PRODUCT_COPY_FILES += \
    vendor/nasgoros/config/overlay/config.xml:$(TARGET_COPY_OUT_PRODUCT)/overlay/config/config.xml
