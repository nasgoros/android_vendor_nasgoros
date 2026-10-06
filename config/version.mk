#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# NasgorOS follows the Android version (17.0 = Android 17)
NASGOROS_VERSION_MAJOR := 17
NASGOROS_VERSION_MINOR := 0
NASGOROS_CODENAME := Minimalist

NASGOROS_BUILD_DATE := $(shell date -u +%Y%m%d)

# Set NASGOROS_BUILDTYPE from the environment, e.g. `export NASGOROS_BUILDTYPE=OFFICIAL`
NASGOROS_BUILDTYPE ?= UNOFFICIAL
ifeq ($(filter OFFICIAL UNOFFICIAL,$(NASGOROS_BUILDTYPE)),)
    NASGOROS_BUILDTYPE := UNOFFICIAL
endif

# LINEAGE_BUILD is exported by `breakfast`/`lunch` and holds the device codename
NASGOROS_DEVICE := $(LINEAGE_BUILD)

# Internal version, e.g. 17.0-20261003-UNOFFICIAL-merlinx
NASGOROS_VERSION := $(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR)-$(NASGOROS_BUILD_DATE)-$(NASGOROS_BUILDTYPE)-$(NASGOROS_DEVICE)

# Maintainer and builder shown in Settings and the recovery installer, e.g.
# `export NASGOROS_MAINTAINER=wahyu6070`. Product properties cannot contain
# spaces, so spaces are stored as underscores and shown as spaces again.
NASGOROS_MAINTAINER ?= wahyu6070
NASGOROS_BUILDER ?= $(NASGOROS_MAINTAINER)
nasgoros_no_space = $(subst $(space),_,$(strip $(1)))

# Display version, e.g. "NasgorOS 17.0 Minimalist". The pieces are separate
# properties (no spaces allowed); Settings and the installer join them.
PRODUCT_PRODUCT_PROPERTIES += \
    ro.nasgoros.version=$(NASGOROS_VERSION) \
    ro.nasgoros.display.version=$(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR) \
    ro.nasgoros.codename=$(NASGOROS_CODENAME) \
    ro.nasgoros.maintainer=$(call nasgoros_no_space,$(NASGOROS_MAINTAINER)) \
    ro.nasgoros.builder=$(call nasgoros_no_space,$(NASGOROS_BUILDER)) \
    ro.nasgoros.build.version=$(NASGOROS_VERSION_MAJOR).$(NASGOROS_VERSION_MINOR) \
    ro.nasgoros.releasetype=$(NASGOROS_BUILDTYPE) \
    ro.nasgoros.device=$(NASGOROS_DEVICE)
