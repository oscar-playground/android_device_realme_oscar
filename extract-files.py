#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/oplus',
    'vendor/realme/sm6375-common',
    'vendor/qcom/opensource/display',
]

blob_fixups: blob_fixups_user_type = {
    'odm/lib64/libAlgoProcess.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V1-ndk_platform.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('odm/lib64/libCOppLceTonemapAPI.so', 'odm/lib64/libaps_frame_registration.so', 'odm/lib64/libYTCommon.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/hw/com.qti.chi.override.so': blob_fixup()
        .add_needed('libcamera_metadata_shim.so')
        .sig_replace(
            'FD 7B BC A9 F8 5F 01 A9 FD 03 00 91 F6 57 02 A9 F4 4F 03 A9 09 A0 40 A9 F3 03 00 AA 3F 01 08 EB E2 00 00 54 68 01 80 52',
            'C0 03 5F D6 F8 5F 01 A9 FD 03 00 91 F6 57 02 A9 F4 4F 03 A9 09 A0 40 A9 F3 03 00 AA 3F 01 08 EB E2 00 00 54 68 01 80 52',
        ),
    'vendor/lib64/libmidasserviceintf_aidl.so': blob_fixup()
        .remove_needed('android.frameworks.stats@1.0.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'oscar',
    'realme',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm6375-common', module.vendor
    )
    utils.run()
