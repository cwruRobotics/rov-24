from collections.abc import MutableSequence

import rclpy
from flight_control.pixhawk_instruction import PixhawkInstruction
from mavros_msgs.msg import OverrideRCIn
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import qos_profile_sensor_data, qos_profile_system_default
from rclpy.subscription import Subscription
from sensor_msgs.msg import Joy

from rov_msgs.msg import CameraControllerSwitch, Manip

# Button meanings for PS5 Control might be different for others
X_BUTTON: int = 0  # Manipulator 0
O_BUTTON: int = 1  # Manipulator 1
TRI_BUTTON: int = 2  # Manipulator 2
SQUARE_BUTTON: int = 3  # Manipulator 3
L1: int = 4
R1: int = 5
L2: int = 6
R2: int = 7
PAIRING_BUTTON: int = 8
MENU: int = 9
PS_BUTTON: int = 10
LJOYPRESS: int = 11
RJOYPRESS: int = 12
# Joystick Directions 1 is up/left -1 is down/right
# X is forward/backward Y is left/right
# L2 and R2 1 is not pressed and -1 is pressed
LJOYY: int = 0
LJOYX: int = 1
L2PRESS_PERCENT: int = 2
RJOYY: int = 3
RJOYX: int = 4
R2PRESS_PERCENT: int = 5
DPADHOR: int = 6
DPADVERT: int = 7


class ManualControlNode(Node):
    def __init__(self) -> None:
        super().__init__("manual_control_node", parameter_overrides=[])

        self.rc_pub: Publisher = self.create_publisher(
            OverrideRCIn, "mavros/rc/override", qos_profile_system_default
        )

        self.subscription: Subscription = self.create_subscription(
            Joy, "joy", self.controller_callback, qos_profile_sensor_data
        )

        # Manipulators
        self.manip_publisher: Publisher = self.create_publisher(
            Manip, "manipulator_control", qos_profile_system_default
        )

        # Cameras
        self.camera_toggle_publisher = self.create_publisher(
            CameraControllerSwitch, "camera_switch", qos_profile_system_default
        )

        self.manip_buttons: dict[int, ManipButton] = {
            X_BUTTON: ManipButton("claw0"),
            O_BUTTON: ManipButton("claw1"),
            TRI_BUTTON: ManipButton("light"),
        }

        self.seen_left_cam = False
        self.seen_right_cam = False

    def controller_callback(self, msg: Joy) -> None:
        self.joystick_to_pixhawk(msg)
        self.manip_callback(msg)
        self.camera_toggle(msg)

    def joystick_to_pixhawk(self, msg: Joy) -> None:
        axes: MutableSequence[float] = msg.axes
        buttons: MutableSequence[int] = msg.buttons

        instruction = PixhawkInstruction(
            pitch=axes[DPADVERT],  # DPad
            roll=buttons[R1] - buttons[L1],  # L1/R1 buttons
            vertical=axes[RJOYX],  # Right Joystick Z
            forward=axes[LJOYX],  # Left Joystick X
            lateral=-axes[LJOYY],  # Left Joystick Y
            yaw=(axes[R2PRESS_PERCENT] - axes[L2PRESS_PERCENT]) / 2,  # L2/R2 buttons
        )

        # Smooth out adjustments
        instruction.apply(lambda value: value * abs(value))

        self.rc_pub.publish(instruction.to_override_rc_in())

    def manip_callback(self, msg: Joy) -> None:
        buttons: MutableSequence[int] = msg.buttons

        for button_id, manip_button in self.manip_buttons.items():
            just_pressed: bool = False

            if buttons[button_id] == 1:
                just_pressed = True

            if manip_button.last_button_state is False and just_pressed:
                new_manip_state: bool = not manip_button.is_active
                manip_button.is_active = new_manip_state

                log_msg: str = f"manip_id= {manip_button.claw}, manip_active= {new_manip_state}"
                self.get_logger().info(log_msg)

                manip_msg: Manip = Manip(
                    manip_id=manip_button.claw, activated=manip_button.is_active
                )
                self.manip_publisher.publish(manip_msg)

            manip_button.last_button_state = just_pressed

    def camera_toggle(self, msg: Joy) -> None:
        """Cycles through connected cameras on pilot GUI using menu and pairing buttons."""
        buttons: MutableSequence[int] = msg.buttons

        if buttons[MENU] == 1:
            self.seen_right_cam = True
        elif buttons[PAIRING_BUTTON] == 1:
            self.seen_left_cam = True
        elif buttons[MENU] == 0 and self.seen_right_cam:
            self.seen_right_cam = False
            self.camera_toggle_publisher.publish(CameraControllerSwitch(toggle_right=True))
        elif buttons[PAIRING_BUTTON] == 0 and self.seen_left_cam:
            self.seen_left_cam = False
            self.camera_toggle_publisher.publish(CameraControllerSwitch(toggle_right=False))


class ManipButton:
    def __init__(self, claw: str) -> None:
        self.claw: str = claw
        self.last_button_state: bool = False
        self.is_active: bool = False


def main() -> None:
    rclpy.init()
    manual_control = ManualControlNode()
    executor = MultiThreadedExecutor()
    rclpy.spin(manual_control, executor=executor)
