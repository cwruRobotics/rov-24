import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from rov_msgs.srv import AutonomousFlight


class AutoDocker(Node):
    def __init__(self) -> None:
        super().__init__(
            "auto_docker",
            parameter_overrides=[],
        )

        self.control_server = self.create_service(
            AutonomousFlight,
            "auto_docker_control",
            self.task_control_callback,
        )

        self.running = False

        # TODO: Add cam frame subscriber here to act as control loop for auto docking

    def task_control_callback(
        self,
        request: AutonomousFlight.Request,
        response: AutonomousFlight.Response,
    ) -> AutonomousFlight.Response:
        self.running = request.start
        response.is_running = self.running

        return response


def main() -> None:
    rclpy.init()
    auto_docker = AutoDocker()
    executor = MultiThreadedExecutor()
    rclpy.spin(auto_docker, executor=executor)
