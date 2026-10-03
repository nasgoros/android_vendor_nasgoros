#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# -----------------------------------------------------------------
# nasgorOS OTA update package

NASGOROS_TARGET_PACKAGE := $(PRODUCT_OUT)/nasgorOS-$(NASGOROS_VERSION).zip

SHA256 := prebuilts/build-tools/path/$(HOST_PREBUILT_TAG)/sha256sum

$(NASGOROS_TARGET_PACKAGE): $(INTERNAL_OTA_PACKAGE_TARGET)
	$(hide) ln -f $(INTERNAL_OTA_PACKAGE_TARGET) $(NASGOROS_TARGET_PACKAGE)
	$(hide) $(SHA256) $(NASGOROS_TARGET_PACKAGE) | sed "s|$(PRODUCT_OUT)/||" > $(NASGOROS_TARGET_PACKAGE).sha256sum
	@echo "Package Complete: $(NASGOROS_TARGET_PACKAGE)" >&2

.PHONY: nasgoros
nasgoros: $(NASGOROS_TARGET_PACKAGE) $(DEFAULT_GOAL)
