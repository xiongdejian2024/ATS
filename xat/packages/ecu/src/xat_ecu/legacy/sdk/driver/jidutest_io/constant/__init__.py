from enum import Enum, unique
from xat_ecu.legacy.sdk.driver.jidutest_io.constant.io_const import NiDeviceType

pkg_name = "jidutest_io"
pkg_ver = "0.1"
pkg_res_name = "__resource"
pkg_data_root_dir = f"{pkg_name}.{pkg_res_name}"
bin_name = "jidutest-io"

__all__ = [
    pkg_name,
    pkg_ver,
    pkg_res_name,
    pkg_data_root_dir,
    bin_name,
    NiDeviceType,
]