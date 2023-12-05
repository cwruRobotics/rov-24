from mavros_msgs.msg import OverrideRCIn
from dataclasses import dataclass
from typing import Callable

# Brown out protection
SPEED_THROTTLE: float = 0.85

# Range of values Pixhawk takes
# In microseconds
ZERO_SPEED: int = 1500
MAX_RANGE_SPEED: int = 400
RANGE_SPEED: float = MAX_RANGE_SPEED * SPEED_THROTTLE

# Channels for RC command
MAX_CHANNEL: int = 8
MIN_CHANNEL: int = 1

FORWARD_CHANNEL: int = 4  # X
THROTTLE_CHANNEL: int = 2  # Z (vertical)
LATERAL_CHANNEL: int = 3  # Y (left & right)
PITCH_CHANNEL: int = 0  # Pitch
YAW_CHANNEL: int = 5  # Yaw
ROLL_CHANNEL: int = 1  # Roll


@dataclass
class PixhawkInstruction:
    """
    Store movement instructions for the Pixhawk.

    Each instruction should be a float in the range [-1.0, 1.0].
    """

    forward: float = 0
    vertical: float = 0
    lateral: float = 0
    pitch: float = 0
    yaw: float = 0
    roll: float = 0

    def apply(self, function_to_apply: Callable[[float], float]) -> None:
        """Apply a function to each dimension of this PixhawkInstruction."""
        self.forward = function_to_apply(self.forward)
        self.vertical = function_to_apply(self.vertical)
        self.lateral = function_to_apply(self.lateral)
        self.pitch = function_to_apply(self.pitch)
        self.yaw = function_to_apply(self.yaw)
        self.roll = function_to_apply(self.roll)

    def to_override_rc_in(self) -> OverrideRCIn:
        """Convert this PixhawkInstruction to an rc_msg with the appropriate channels array."""
        rc_msg = OverrideRCIn()

        self.apply(lambda value: int(RANGE_SPEED * value) + ZERO_SPEED)

        rc_msg.channels[FORWARD_CHANNEL] = self.forward
        rc_msg.channels[THROTTLE_CHANNEL] = self.vertical
        rc_msg.channels[LATERAL_CHANNEL] = self.lateral
        rc_msg.channels[PITCH_CHANNEL] = self.pitch
        rc_msg.channels[YAW_CHANNEL] = self.yaw
        rc_msg.channels[ROLL_CHANNEL] = self.roll

        return rc_msg
