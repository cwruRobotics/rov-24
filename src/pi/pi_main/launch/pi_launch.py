"""pi_launch launch file."""
import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace


def generate_launch_description() -> LaunchDescription:
    """
    Generate LaunchDescription for pi_main.

    Returns
    -------
    LaunchDescription
        Launches camera_streamer package and pixhawk_communication package.

    """
    NAMESPACE = 'pi'
    # Manipulator Controller
    # manip_path: str = get_package_share_directory('manipulators')
    #
    # manip_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         os.path.join(
    #             manip_path, 'launch', 'manip_launch.py'
    #         )
    #     ])
    # )

    # Camera Streamer
    cam_path: str = get_package_share_directory('camera_streamer')

    cam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                cam_path, 'launch', 'camera_launch.py'
            )
        ])
    )

    # Pixhawk Communication
    pixhawk_path: str = get_package_share_directory('pixhawk_communication')

    pixhawk_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                pixhawk_path, 'launch', 'mavros_launch.py'
            ),
        ])
    )

    # Heartbeat
    heartbeat_path: str = get_package_share_directory('heartbeat')

    heartbeat_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                heartbeat_path, 'launch', 'heartbeat_launch.py'
            )
        ])
    )

    # realsense_path: str = get_package_share_directory('realsense')

    # # Launches Realsense
    # realsense_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         os.path.join(
    #             realsense_path, 'launch', 'realsense_launch.py'
    #         )
    #     ]),
    #     launch_arguments={'align_depth.enable': 'true'}.items()
    # )

    namespace_launch = GroupAction(
        actions=[
            PushRosNamespace(NAMESPACE),
            # manip_launch,
            pixhawk_launch,
            cam_launch,
            heartbeat_launch,
            # realsense_launch
        ]
    )

    return LaunchDescription([
        namespace_launch,
    ])
