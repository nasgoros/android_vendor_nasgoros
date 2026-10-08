#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# -----------------------------------------------------------------
# NasgorOS OTA update package, e.g. NasgorOS-17.0-20261003-UNOFFICIAL-merlinx.zip

NASGOROS_TARGET_PACKAGE := $(PRODUCT_OUT)/NasgorOS-$(NASGOROS_VERSION).zip

NASGOROS_OVERLAY_CONFIG_CHECK := vendor/nasgoros/tools/check-overlay-config.sh
NASGOROS_AAPT2 := prebuilts/sdk/tools/linux/bin/aapt2

$(NASGOROS_TARGET_PACKAGE): $(INTERNAL_OTA_PACKAGE_TARGET) $(NASGOROS_OVERLAY_CONFIG_CHECK)
	$(hide) $(NASGOROS_OVERLAY_CONFIG_CHECK) $(TARGET_OUT_PRODUCT)/overlay $(NASGOROS_AAPT2)
	$(hide) ln -f $(INTERNAL_OTA_PACKAGE_TARGET) $(NASGOROS_TARGET_PACKAGE)
	@echo "Package Complete: $(NASGOROS_TARGET_PACKAGE)" >&2

.PHONY: nasgoros
nasgoros: $(NASGOROS_TARGET_PACKAGE) $(DEFAULT_GOAL)

# -----------------------------------------------------------------
# NasgorOS recovery image, e.g. NasgorOS-Recovery-17.0-20261003.img
# Only for devices with a dedicated recovery partition.

ifneq ($(INSTALLED_RECOVERYIMAGE_TARGET),)
NASGOROS_RECOVERY_IMAGE := $(PRODUCT_OUT)/NasgorOS-Recovery-$(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR)-$(NASGOROS_BUILD_DATE).img

$(NASGOROS_RECOVERY_IMAGE): $(INSTALLED_RECOVERYIMAGE_TARGET)
	$(hide) ln -f $(INSTALLED_RECOVERYIMAGE_TARGET) $(NASGOROS_RECOVERY_IMAGE)
	@echo "Recovery Complete: $(NASGOROS_RECOVERY_IMAGE)" >&2

nasgoros: $(NASGOROS_RECOVERY_IMAGE)
endif
