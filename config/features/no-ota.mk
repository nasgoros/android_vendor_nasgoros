# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Product decision: no OTA updates in Settings or recovery. New builds are
# flashed manually (recovery "Apply update"); see no-ota/Android.mk.

PRODUCT_PACKAGES += NasgorNoOta

PRODUCT_PACKAGE_OVERLAYS += vendor/nasgoros/overlay/no-ota
PRODUCT_ENFORCE_RRO_EXCLUDED_OVERLAYS += vendor/nasgoros/overlay/no-ota
