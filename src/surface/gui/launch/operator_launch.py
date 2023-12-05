from launch.launch_description import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction


def generate_launch_description() -> LaunchDescription:
    """Asynchronously launches operator's gui node."""
    gui_node: Node = Node(
        package='gui',
        executable='run_operator',
        parameters=[{'theme': LaunchConfiguration('theme', default='dark')}],
        remappings=[("/surface/gui/bottom_cam/image_raw", "/tether/bottom_cam/image_raw"),
                    ("/surface/gui/task_request", "/surface/task_request"),
                    ("/surface/gui/task_feedback", "/surface/task_feedback"),
                    ("/surface/gui/auto_docker_control", "/surface/auto_docker_control")],
        emulate_tty=True,
        output='screen'
    )

    namespace_launch = GroupAction(
        actions=[
            PushRosNamespace('gui'),
            gui_node
        ]
    )

    return LaunchDescription([namespace_launch])
