#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

NASGOROS_VERSION_MAJOR := 1
NASGOROS_VERSION_MINOR := 0
NASGOROS_CODENAME := Minimalist

NASGOROS_BUILD_DATE := $(shell date -u +%Y%m%d)

# Set NASGOROS_BUILDTYPE from the environment, e.g. `export NASGOROS_BUILDTYPE=OFFICIAL`
NASGOROS_BUILDTYPE ?= UNOFFICIAL
ifeq ($(filter OFFICIAL UNOFFICIAL BETA,$(NASGOROS_BUILDTYPE)),)
    NASGOROS_BUILDTYPE := UNOFFICIAL
endif

# LINEAGE_BUILD is exported by `breakfast`/`lunch` and holds the device codename
NASGOROS_DEVICE := $(LINEAGE_BUILD)

# Internal version, e.g. 1.0-20261003-UNOFFICIAL-merlinx
NASGOROS_VERSION := $(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR)-$(NASGOROS_BUILD_DATE)-$(NASGOROS_BUILDTYPE)-$(NASGOROS_DEVICE)

# Display version, e.g. nasgorOS 1.0 Minimalist
NASGOROS_DISPLAY_VERSION := nasgorOS $(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR) $(NASGOROS_CODENAME)

PRODUCT_PRODUCT_PROPERTIES += \
    ro.nasgoros.version=$(NASGOROS_VERSION) \
    ro.nasgoros.display.version=$(NASGOROS_DISPLAY_VERSION) \
    ro.nasgoros.build.version=$(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR) \
    ro.nasgoros.releasetype=$(NASGOROS_BUILDTYPE) \
    ro.nasgoros.device=$(NASGOROS_DEVICE)
