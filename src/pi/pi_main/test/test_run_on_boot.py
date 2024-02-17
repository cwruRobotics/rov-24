import os

from pi_main.run_on_boot import main

ROS_DISTRO = os.getenv("ROS_DISTRO")

EXPECTED_SYSTEM_FILES = [
    f"/etc/ros/{ROS_DISTRO}/cwrubotix_pi.d/.installed_files",
    f"/etc/ros/{ROS_DISTRO}/cwrubotix_pi.d/pi.launch.py",
    "/usr/sbin/cwrubotix_pi-start",
    "/usr/sbin/cwrubotix_pi-stop",
]


def test_install_on_boot() -> None:
    """Test that file copying and systemd are made."""
    main()

    # Test for rules files being copied correctly
    # Could be split into a separate test but main() does both
    actual_rules_files = set(
        os.listdir(
            os.path.join(
                "/etc",
                "udev",
                "rules.d",
            )
        )
    )
    expected_rules_files = set(
        [
            "i2c.rules",
            "camera.rules",
            "pixhawk.rules",
        ]
    )
    assert expected_rules_files.issubset(actual_rules_files)

    # Checks for files created by robot_upstart
    for file in EXPECTED_SYSTEM_FILES:
        assert os.path.isfile(file)
