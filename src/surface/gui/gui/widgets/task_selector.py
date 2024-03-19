from gui.gui_nodes.event_nodes.client import GUIEventClient
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget

from rov_msgs.srv import AutonomousFlight, AutonomousFlight_Request, AutonomousFlight_Response

WIDTH = 200


class TaskSelector(QWidget):
    """QWidget that handles task selection with a dropdown."""

    # Declare signals with "object" params b/c we don't have access to
    # the ROS service object TaskRequest_Response
    scheduler_response_signal: pyqtSignal = pyqtSignal(AutonomousFlight_Response)

    def __init__(self) -> None:
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        # Create Start button
        self.start_btn = QPushButton("Start Auto Docking")
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.start_btn.setFixedHeight(75)
        self.start_btn.setFixedWidth(WIDTH)

        # Create Stop button
        self.stop_btn = QPushButton("Stop Auto Docking")
        self.stop_btn.clicked.connect(self.stop_btn_clicked)
        self.stop_btn.setFixedHeight(75)
        self.stop_btn.setFixedWidth(WIDTH)

        # Add 'Task: ' label
        self.task_status: QLabel = QLabel()
        self.task_status.setFixedWidth(WIDTH)
        self.task_status.setText('Auto Docking: Disabled')

        # Setup Grid
        layout.addWidget(self.task_status, 1, 1, 2, 2)
        layout.addWidget(self.start_btn, 2, 1)
        layout.addWidget(self.stop_btn, 3, 1)

        self.scheduler_response_signal.connect(self.handle_scheduler_response)
        self.task_controller = GUIEventClient(AutonomousFlight, 'auto_docker_control',
                                              self.scheduler_response_signal)

    def start_btn_clicked(self) -> None:
        """Tell the back about the user selecting the start button."""
        self.task_controller.get_logger().info(
            'GUI changed task to: Auto Docking')

        self.task_status.setText('Auto Docking: Enabled')

        self.task_controller.send_request_async(
            AutonomousFlight_Request(start=True))

    def stop_btn_clicked(self) -> None:
        """Tell the back about the user selecting the manual control button."""
        self.task_controller.get_logger().info(
            'GUI changed task to: Manual Control')

        self.task_status.setText('Auto Docking: Disabled')

        self.task_controller.send_request_async(
            AutonomousFlight_Request(start=False))

    @pyqtSlot(AutonomousFlight_Response)
    def handle_scheduler_response(self, response: AutonomousFlight_Response) -> None:
        """Handle scheduler response to request sent from gui_changed_task."""
        msg = 'Auto docking is '
        if response.is_running:
            msg += 'now running'
        else:
            msg += 'no longer running'
        self.task_controller.get_logger().info(msg)
