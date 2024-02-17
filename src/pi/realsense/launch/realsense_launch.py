"""realsense_launch launch file."""

import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import SetRemap


def generate_launch_description() -> LaunchDescription:
    """
    Generate LaunchDescription for the realsense package.

    Returns
    -------
    LaunchDescription
        Launches realsense launch file.

    """
    realsense_path: str = get_package_share_directory("realsense2_camera")

    # Launches Realsense
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(realsense_path, "launch", "rs_launch.py")]),
        # Values are width x height x fps.
        launch_arguments={
            "depth_module.profile": "640x360x30",
            "initial_reset": "true",
            "rgb_camera.profile": "640x360x30",
            "align_depth.enable": "true",
        }.items(),
    )

    realsense_action = GroupAction(
        actions=[
            SetRemap(
                src="/pi/camera/color/image_raw",
                dst="/depth_cam/image_raw",
            ),
            SetRemap(
                src="/pi/camera/color/camera_info",
                dst="/depth_cam/camera_info",
            ),
            SetRemap(
                src="/pi/camera/aligned_depth_to_color/image_raw",
                dst="/depth_cam/depth_to_color",
            ),
            realsense_launch,
        ]
    )

    return LaunchDescription([realsense_action])
