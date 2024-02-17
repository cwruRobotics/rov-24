"""When run sets up environment for the robot to run on boot."""

import os
import pathlib
import subprocess  # nosec
import sys

from ament_index_python.packages import get_package_share_directory
from robot_upstart.job import Job


def main() -> None:
    """
    Set up Pi file environment.

    Copies udev rules from this package into udev folder.
    Also uses robot_upstart to allow robot to automatically start on power on.

    """
    pi_main_share = get_package_share_directory("pi_main")

    launch_dir = os.path.join(pi_main_share, "launch")
    launch_src = os.path.join(launch_dir, "pi_launch.py")
    launch_dst = os.path.join(launch_dir, "pi.launch.py")

    try:
        os.unlink(launch_dst)
    except FileNotFoundError:
        pass

    os.symlink(launch_src, launch_dst)

    file_location = pathlib.Path(__file__).parent.resolve()
    udev_script = os.path.join(file_location, "udev_copy.py")

    cmd = [
        "/usr/bin/sudo",
        "/usr/bin/python3",
        udev_script,
        pi_main_share,
    ]

    try:
        process = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
        )  # nosec
    # Logs Error
    except subprocess.CalledProcessError as error:
        print(error.stderr)
        sys.exit(1)

    # Success Message
    print(process.stdout.decode())

    install_path = os.path.join(pi_main_share, "..", "..", "..")
    workspace_path = os.path.join(install_path, "setup.bash")
    clean_path = os.path.normpath(workspace_path)

    cwrubotix_job = Job(
        name="cwrubotix_pi",
        workspace_setup=clean_path,
    )
    cwrubotix_job.symlink = True
    cwrubotix_job.uninstall()
    cwrubotix_job.add(
        package="pi_main",
        filename="launch/pi.launch.py",
    )
    cwrubotix_job.install()
