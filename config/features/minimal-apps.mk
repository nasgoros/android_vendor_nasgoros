# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0

# AOSP Provision itself comes from handheld_system_ext.mk.
PRODUCT_PACKAGES += \
    NasgorRemovePackages

PRODUCT_PACKAGE_OVERLAYS += vendor/nasgoros/overlay/minimal
PRODUCT_ENFORCE_RRO_EXCLUDED_OVERLAYS += vendor/nasgoros/overlay/minimal
