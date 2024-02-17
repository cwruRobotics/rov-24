import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace


def generate_launch_description() -> LaunchDescription:
    gui_path: str = get_package_share_directory("gui")
    controller_path: str = get_package_share_directory("ps5_controller")
    flir_path: str = get_package_share_directory("rov_flir")

    # Launches Gui
    gui_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    gui_path,
                    "launch",
                    "pilot_launch.py",
                )
            ]
        ),
    )

    # Launches Controller
    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    controller_path,
                    "launch",
                    "controller_launch.py",
                )
            ]
        ),
    )

    # Launches flir
    flir_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(flir_path, "launch", "flir_launch.py")]),
    )

    namespace_launch = GroupAction(
        actions=[PushRosNamespace("surface"), gui_launch, controller_launch, flir_launch]
    )

    return LaunchDescription([namespace_launch])
