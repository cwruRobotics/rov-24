import signal
import sys

import qdarktheme
import rclpy
from PyQt6.QtWidgets import QApplication, QWidget
from rclpy.node import Node


class App(QWidget):
    """Main app window."""

    def __init__(self, node_name: str):
        self.app: QApplication = QApplication(sys.argv)
        rclpy.init()
        super().__init__()
        self.node = Node(node_name, parameter_overrides=[])

        self.node.declare_parameter('theme', '')
        self.resize(1850, 720)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        rclpy.shutdown()

    def run_gui(self):
        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        if self.node.get_parameter('theme').get_parameter_value().string_value == "dark":
            qdarktheme.setup_theme()
        elif self.node.get_parameter('theme').get_parameter_value().string_value == "watermelon":
            # UGLY But WORKS
            self.app.setStyleSheet("QWidget { background-color: green; color: pink; }")
        else:
            qdarktheme.setup_theme("light")
        # Clean up resources
        self.node.destroy_node()
        self.show()
        sys.exit(self.app.exec())
