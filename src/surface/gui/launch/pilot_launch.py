from enum import Enum

from launch.actions import GroupAction
from launch.launch_description import DeclareLaunchArgument, LaunchDescription
from launch.substitutions.launch_configuration import LaunchConfiguration
from launch.substitutions.equals_substitution import EqualsSubstitution
from launch.conditions.if_condition import IfCondition
from launch_ros.actions import Node, PushRosNamespace


class GUIVersion(str, Enum):
    PILOT = 'pilot'
    DEBUG = 'debug'


def pilot_node_generator(executable: str, gui_version: GUIVersion,
                         gui_version_substitution: LaunchConfiguration) -> Node:
    """
    Generate pilot nodes.

    Parameters
    ----------
    executable : str
        Name of the executable to run.
    gui_version : GUIVersion
        Enum for which gui being run
    gui_version_substitution : LaunchConfiguration
        LaunchConfiguration for the gui argument.

    Returns
    -------
    Node
        Return launch_ros Node.

    """
    return Node(
        package='gui',
        executable=executable,
        parameters=[{'theme': LaunchConfiguration('theme', default='dark')}],
        remappings=[("/surface/gui/mavros/cmd/arming", "/tether/mavros/cmd/arming"),
                    ("/surface/gui/camera_switch", "/surface/camera_switch"),
                    ("/surface/gui/bottom_cam/image_raw", "/surface/bottom_cam/image_raw"),
                    ("/surface/gui/front_cam/image_raw", "/surface/front_cam/image_raw"),
                    ("/surface/gui/depth_cam/image_raw", "/tether/depth_cam/image_raw"),
                    ("/surface/gui/vehicle_state_event", "/surface/vehicle_state_event"),
                    ("/surface/gui/flooding", "/tether/flooding")],
        emulate_tty=True,
        output='screen',
        condition=IfCondition(EqualsSubstitution(gui_version.value, gui_version_substitution)))


def generate_launch_description() -> LaunchDescription:
    """Asynchronously launches pilot's gui node."""
    gui_version_arg = DeclareLaunchArgument('gui', default_value=GUIVersion.PILOT,
                                            choices=[GUIVersion.PILOT, GUIVersion.DEBUG])

    gui_version_substitution = LaunchConfiguration('gui', default=GUIVersion.PILOT)
    pilot_node = pilot_node_generator('run_pilot', GUIVersion.PILOT, gui_version_substitution)
    debug_node = pilot_node_generator('run_debug', GUIVersion.DEBUG, gui_version_substitution)

    namespace_launch = GroupAction(
        actions=[
            PushRosNamespace('gui'),
            pilot_node,
            debug_node
        ]
    )

    return LaunchDescription([namespace_launch,
                              gui_version_arg])
