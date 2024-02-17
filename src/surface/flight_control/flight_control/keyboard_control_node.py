from typing import Optional

import rclpy.utilities
from flight_control.pixhawk_instruction import PixhawkInstruction
from mavros_msgs.msg import OverrideRCIn
from pynput.keyboard import Key, KeyCode, Listener
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import qos_profile_system_default

# key bindings
FORWARD = "w"
BACKWARD = "s"
LEFT = "a"
RIGHT = "d"
UP = "2"
DOWN = "x"

ROLL_LEFT = "j"
ROLL_RIGHT = "l"
PITCH_UP = "i"
PITCH_DOWN = "k"
YAW_LEFT = "h"
YAW_RIGHT = ";"

HELP = "p"

HELP_MSG = """
Use keyboard to control ROV

Key Bindings:
[2]
[w]            [i]
[a][s][d]   [h][j][k][l][;]
[x]

[w] = Forward
[s] = Backward
[a] = Left
[d] = Right
[2] = Up
[x] = Down

[j] = Roll Left
[l] = Roll Right
[i] = Pitch Up
[k] = Pitch Down
[h] = Yaw Left
[;] = Yaw Right

[p] = Show this help"""


class KeyboardListenerNode(Node):
    def __init__(self) -> None:
        super().__init__(
            "keyboard_listener_node",
            parameter_overrides=[],
        )

        self.rc_pub: Publisher = self.create_publisher(
            OverrideRCIn,
            "mavros/rc/override",
            qos_profile_system_default,
        )

        self.get_logger().info(HELP_MSG)
        self.status = {
            FORWARD: False,
            BACKWARD: False,
            LEFT: False,
            RIGHT: False,
            UP: False,
            DOWN: False,
            ROLL_LEFT: False,
            ROLL_RIGHT: False,
            PITCH_UP: False,
            PITCH_DOWN: False,
            YAW_LEFT: False,
            YAW_RIGHT: False,
        }

    def on_press(
        self,
        key: Optional[Key | KeyCode],
    ) -> None:
        try:
            key_name: str = ""
            if isinstance(key, KeyCode):
                key_name = key.char
                if key_name is None:
                    return
            elif isinstance(key, Key):
                key_name = key.name
            else:
                return

            if key_name == HELP:
                self.get_logger().info(HELP_MSG)
            else:
                self.status[key_name] = True

            self.pub_rov_control()

        except Exception as exception:
            self.get_logger().error(str(exception))
            raise exception

    def on_release(
        self,
        key: Optional[Key | KeyCode],
    ) -> None:
        try:
            key_name: str = ""
            if isinstance(key, KeyCode):
                key_name = key.char
                if key_name is None:
                    return
            elif isinstance(key, Key):
                key_name = key.name
            else:
                return

            if key_name == HELP:
                pass
            else:
                self.status[key_name] = False

            self.pub_rov_control()

        except Exception as exception:
            self.get_logger().error(str(exception))
            raise exception

    def pub_rov_control(self) -> None:
        instruction = PixhawkInstruction(
            pitch=self.status[PITCH_UP] - self.status[PITCH_DOWN],
            roll=self.status[ROLL_LEFT] - self.status[ROLL_RIGHT],
            vertical=self.status[UP] - self.status[DOWN],
            forward=self.status[FORWARD] - self.status[BACKWARD],
            lateral=self.status[LEFT] - self.status[RIGHT],
            yaw=self.status[YAW_LEFT] - self.status[YAW_RIGHT],
        )

        self.rc_pub.publish(instruction.to_override_rc_in())

    def spin(self) -> None:
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            while rclpy.utilities.ok() and listener.running:
                rclpy.spin_once(
                    self,
                    timeout_sec=0.1,
                )


def main() -> None:
    rclpy.init()
    KeyboardListenerNode().spin()


if __name__ == "__main__":
    main()
