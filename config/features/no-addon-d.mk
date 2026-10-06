# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Product decision: no addon.d. /system/addon.d is not shipped and the
# installer does not back up or restore addon.d scripts (see
# build/tasks/nasgoros.mk). After a ROM update, flash LiteGapps again.

PRODUCT_PACKAGES += NasgorNoAddonD
