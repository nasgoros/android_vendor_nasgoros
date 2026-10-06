# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
# Set overrides before inheriting the nasgorOS product. See PORTING.md.

NASGOROS_WITH_BOOTANIMATION ?= true
NASGOROS_WITH_WALLPAPER ?= true
NASGOROS_WITH_SETTINGS ?= true
NASGOROS_WITH_CRDROID_SETTINGS ?= true
NASGOROS_WITH_LORA_BROWSER ?= true
NASGOROS_WITH_ZIMUX ?= true

ifeq ($(NASGOROS_WITH_BOOTANIMATION),true)
$(call inherit-product, vendor/nasgoros/config/features/bootanimation.mk)
endif

ifeq ($(NASGOROS_WITH_WALLPAPER),true)
$(call inherit-product, vendor/nasgoros/config/features/wallpaper.mk)
endif

ifeq ($(NASGOROS_WITH_SETTINGS),true)
$(call inherit-product, vendor/nasgoros/config/features/settings.mk)
endif

ifeq ($(NASGOROS_WITH_CRDROID_SETTINGS),true)
ifneq ($(NASGOROS_WITH_SETTINGS),true)
$(error NASGOROS_WITH_CRDROID_SETTINGS requires NASGOROS_WITH_SETTINGS=true)
endif
$(call inherit-product, vendor/nasgoros/config/crdroid.mk)
endif

$(call inherit-product, vendor/nasgoros/config/features/performance-defaults.mk)

ifeq ($(NASGOROS_WITH_LORA_BROWSER),true)
$(call inherit-product, vendor/nasgoros/config/features/lora-browser.mk)
endif

ifeq ($(NASGOROS_WITH_ZIMUX),true)
$(call inherit-product, vendor/nasgoros/config/features/zimux.mk)
endif

# Recovery-only feature implemented by the nasgorOS recovery fork.
NASGOROS_WITH_RECOVERY_FILE_MANAGER ?= true
PRODUCT_VENDOR_PROPERTIES += ro.nasgoros.recovery_file_manager=$(NASGOROS_WITH_RECOVERY_FILE_MANAGER)
