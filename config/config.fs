# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
#
# File modes for the product image (TARGET_FS_CONFIG_GEN, via BoardConfigExtra.mk).
#
# Zimux runs some of its bundled libraries as programs (proot, busybox, tar...).
# Libraries installed beside a system app get mode 0644 by default, so running
# them failed with "Permission denied" (error 13), even as root.
[product/app/Zimux/lib/arm64/*]
mode: 0755
user: AID_ROOT
group: AID_ROOT
caps: 0
