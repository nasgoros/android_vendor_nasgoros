#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

LOCAL_PATH := $(call my-dir)

# Placeholder module whose only job is to override (= keep out of the build)
# LineageOS/AOSP apps that NasgorOS does not ship. See FEATURES.md.
include $(CLEAR_VARS)
LOCAL_MODULE := NasgorRemovePackages
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_TAGS := optional
LOCAL_OVERRIDES_PACKAGES := \
    AudioFX \
    BasicDreams \
    BuiltInPrintService \
    Canvas \
    DeskClock \
    EasterEgg \
    Etar \
    ExactCalculator \
    FMRadio \
    FmRecordingsProvider \
    Gallery2 \
    Glimpse \
    Jelly \
    LineageSetupWizard \
    LocalContactsBackup \
    messaging \
    MusicFX \
    PhotoTable \
    PrintRecommendationService \
    Recorder \
    Seedvault \
    Traceur \
    Twelve
LOCAL_UNINSTALLABLE_MODULE := true
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_SRC_FILES := /dev/null
include $(BUILD_PREBUILT)
