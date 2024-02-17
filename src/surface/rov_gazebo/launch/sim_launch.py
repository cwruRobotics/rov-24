import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

NAMESPACE = "simulation"


def generate_launch_description() -> LaunchDescription:
    rov_gazebo_path: str = get_package_share_directory("rov_gazebo")
    ros_gz_sim_path: str = get_package_share_directory("ros_gz_sim")
    surface_main_path: str = get_package_share_directory("surface_main")

    world_path: str = os.path.join(
        rov_gazebo_path,
        "worlds",
        "world.sdf",
    )

    # Process the URDF file
    xacro_file = os.path.join(
        rov_gazebo_path,
        "description",
        "rov.xacro",
    )
    robot_description = Command(["xacro ", xacro_file])
    params = {"robot_description": robot_description}

    pool_file = os.path.join(
        rov_gazebo_path,
        "description",
        "pool.xacro",
    )
    pool_description = Command(["xacro ", pool_file])
    pool_params = {"robot_description": pool_description}

    # Create a robot_state_publisher node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],
        namespace=NAMESPACE,
        emulate_tty=True,
    )

    pool_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[pool_params],
        namespace=NAMESPACE,
        remappings=[
            (
                f"/{NAMESPACE}/robot_description",
                f"/{NAMESPACE}/pool_description",
            )
        ],
        emulate_tty=True,
    )

    # Launches Gazebo
    gazeboLaunch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    ros_gz_sim_path,
                    "launch",
                    "gz_sim.launch.py",
                )
            ]
        ),
        launch_arguments={"gz_args": world_path}.items(),
    )

    # Spawn entity
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "ROV",
            "-allow_renaming",
            "true",
        ],
        namespace=NAMESPACE,
        emulate_tty=True,
    )

    gz_spawn_pool = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic",
            "pool_description",
            "-name",
            "pool",
            "-allow_renaming",
            "true",
        ],
        namespace=NAMESPACE,
        emulate_tty=True,
    )

    # Not using keyboard launch file
    # TODO?
    # I think we should probably switch over all our single
    # Node launch files to something like this
    keyboard_driver = Node(
        package="keyboard_driver",
        executable="keyboard_driver_node",
        output="screen",
        name="keyboard_driver_node",
        namespace=NAMESPACE,
        remappings=[
            (
                f"/{NAMESPACE}/manual_control",
                "/manual_control",
            )
        ],
        emulate_tty=True,
    )

    # cam_bridge = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     namespace=NAMESPACE,
    #     name="cam_bridge",
    #     arguments=[
    #         "/bottom_cam/image_raw@sensor_msgs/msg/Image@gz.msgs.Image",
    #         "/bottom_cam/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
    #         "/front_cam/image_raw@sensor_msgs/msg/Image@gz.msgs.Image",
    #         "/front_cam/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
    #         "/manip_cam/image_raw@sensor_msgs/msg/Image@gz.msgs.Image",
    #         "/depth_cam@sensor_msgs/msg/Image@gz.msgs.Image",
    #         "/depth_cam/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked",
    #     ],
    #     remappings=[
    #         (f"/{NAMESPACE}/bottom_cam/image_raw", "/bottom_cam/image_raw"),
    #         (f"/{NAMESPACE}/bottom_cam/camera_info", "/bottom_cam/camera_info"),
    #         (f"/{NAMESPACE}/front_cam/image_raw", "/front_cam/image_raw"),
    #         (f"/{NAMESPACE}/front_cam/camera_info", "/front_cam/camera_info"),
    #         (f"/{NAMESPACE}/manip_cam/image_raw", "/manip_cam/image_raw"),
    #         (f"/{NAMESPACE}/depth_cam", "/depth_cam/image_raw"),
    #         (f"/{NAMESPACE}/depth_cam/points", "/depth_cam/points"),
    #     ],
    #     output="screen",
    #     emulate_tty=True
    # )

    # Launches Controller
    surface_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    surface_main_path,
                    "launch",
                    "surface_all_nodes_launch.py",
                )
            ]
        ),
    )

    return LaunchDescription(
        [
            robot_state_publisher,
            pool_state_publisher,
            gazeboLaunch,
            gz_spawn_entity,
            gz_spawn_pool,
            keyboard_driver,
            # cam_bridge,
            surface_launch,
        ]
    )
