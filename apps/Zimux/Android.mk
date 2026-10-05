# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := Zimux
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_SRC_FILES := Zimux.apk
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_PRODUCT_MODULE := true
LOCAL_MULTILIB := first
LOCAL_DEX_PREOPT := false
# Copy the signed release APK byte-for-byte; repacking invalidates its signature.
LOCAL_REPLACE_PREBUILT_APK_INSTALLED := $(LOCAL_PATH)/$(LOCAL_SRC_FILES)
# System packages do not extract native libraries at first boot. Install the
# release's libraries beside the APK, selected for the app's primary architecture.
LOCAL_PREBUILT_JNI_LIBS_arm64 := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/lib/arm64-v8a/*.so))
LOCAL_PREBUILT_JNI_LIBS_arm := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/lib/armeabi-v7a/*.so))
LOCAL_PREBUILT_JNI_LIBS_x86 := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/lib/x86/*.so))
LOCAL_PREBUILT_JNI_LIBS_x86_64 := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/lib/x86_64/*.so))
include $(BUILD_PREBUILT)
