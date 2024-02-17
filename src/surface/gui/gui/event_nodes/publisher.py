import re

from rclpy.node import Node
from rclpy.publisher import MsgType
from rclpy.qos import QoSProfile, qos_profile_system_default


class GUIEventPublisher(Node):
    """Publisher for sending messages from the GUI."""

    def __init__(
        self,
        msg_type: MsgType,
        topic: str,
        qos_profile: QoSProfile = qos_profile_system_default,
    ) -> None:
        # Name this node with a sanitized version of the topic
        name = f'publisher_{re.sub(r"[^a-zA-Z0-9_]", "_", topic)}'
        super().__init__(name, parameter_overrides=[])

        self.publisher = self.create_publisher(
            msg_type,
            topic,
            qos_profile,
        )

    def publish(self, msg: MsgType) -> None:
        """Send a message with the provided parameters."""
        self.publisher.publish(msg)
