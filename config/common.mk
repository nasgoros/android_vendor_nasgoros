#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# nasgorOS is layered on top of LineageOS. This file is pulled in by
# vendor/lineage/config/common.mk through vendor/extra/product.mk, so any
# device that builds LineageOS builds nasgorOS without changes.

include vendor/nasgoros/config/version.mk

PRODUCT_PRODUCT_PROPERTIES += \
    ro.nasgoros.base=LineageOS

# Boot animation (regenerate with bootanimation/generate.py)
TARGET_BOOTANIMATION := vendor/nasgoros/bootanimation/bootanimation.zip

# Rebrand user-visible "LineageOS" strings in every locale (tools/gen-branding-overlay.py)
PRODUCT_PACKAGE_OVERLAYS += vendor/nasgoros/overlay/branding
PRODUCT_ENFORCE_RRO_EXCLUDED_OVERLAYS += vendor/nasgoros/overlay/branding

# Settings > NasgorOS (packages/apps/NasgorSettings)
PRODUCT_PACKAGES += \
    NasgorSettings

# Apps removed from NasgorOS (see FEATURES.md)
PRODUCT_PACKAGES += \
    NasgorRemovePackages
