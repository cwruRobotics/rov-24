import rclpy
from rclpy.node import Node
from rov_msgs.msg import Flooding
import lgpio


class floodDetector(Node):

    def __init__(self) -> None:
        super().__init__('gpio_reader', parameter_overrides=[])
        self.publisher_ = self.create_publisher(Flooding, '/tether/flooding', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self) -> None:
        # Pins used for GPIO
        detect1: int = 17
        # GPIO Boilerplate
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_input(h, detect1)

        data1: bool = lgpio.gpio_read(h, detect1)

        print("Pin 17: %s" % data1)

        # If any of the sensors detect water, send true to /tether/flooding

        msg = Flooding()

        if data1:
            msg.flooding = True
        else:
            msg.flooding = False
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.flooding)


def main(args: None = None) -> None:
    rclpy.init()
    flood_detector: floodDetector = floodDetector()
    rclpy.spin(flood_detector)
    flood_detector.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
