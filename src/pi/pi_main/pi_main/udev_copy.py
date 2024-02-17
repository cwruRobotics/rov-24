"""Copies udev rules from separate process to ensure ideal protections of sudo."""

import os
import shutil
import sys

if __name__ == "__main__":
    SHARE_DIR = sys.argv[1]

    udev_src_dir = os.path.join(SHARE_DIR, "udev_rules")
    udev_dst_dir = os.path.join("/etc", "udev", "rules.d")

    shutil.copytree(
        udev_src_dir,
        udev_dst_dir,
        dirs_exist_ok=True,
    )
    print("Copying udev rules.")
