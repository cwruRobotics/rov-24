from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """Asynchronously launches operator's gui node."""
    gui_node: Node = Node(
        package='gui',
        executable='run_operator',
        parameters=[
                {'theme': LaunchConfiguration('theme', default='dark')}],
        remappings=[("/surface/gui/publisher_fmu_in_vehicle_command", "/fmu/in/vehicle_command")]
    )

    return LaunchDescription([gui_node])
