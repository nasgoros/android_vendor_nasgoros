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
