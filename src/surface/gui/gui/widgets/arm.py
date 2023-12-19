from gui.event_nodes.client import GUIEventClient
from gui.event_nodes.subscriber import GUIEventSubscriber
from gui.theme import PROPERTY_NAME, Style
from mavros_msgs.srv import CommandBool
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from rov_msgs.msg import VehicleState


class Arm(QWidget):
    """Arm widget for sending Arm Commands."""

    ARM_REQUEST = CommandBool.Request(value=True)
    DISARM_REQUEST = CommandBool.Request(value=False)
    BUTTON_WIDTH = 120
    BUTTON_HEIGHT = 60
    BUTTON_STYLESHEET = 'QPushButton { font-size: 20px; }'

    command_response_signal: pyqtSignal = pyqtSignal(CommandBool.Response)
    vehicle_state_signal = pyqtSignal(VehicleState)

    def __init__(self) -> None:

        super().__init__()

        layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(layout)

        self.arm_button: QPushButton = QPushButton()
        self.disarm_button: QPushButton = QPushButton()

        self.arm_button.setText("Arm")
        self.disarm_button.setText("Disarm")

        self.arm_button.setMinimumWidth(self.BUTTON_WIDTH)
        self.disarm_button.setMinimumWidth(self.BUTTON_WIDTH)

        self.arm_button.setMinimumHeight(self.BUTTON_HEIGHT)
        self.disarm_button.setMinimumHeight(self.BUTTON_HEIGHT)

        self.arm_button.setStyleSheet(self.BUTTON_STYLESHEET)
        self.disarm_button.setStyleSheet(self.BUTTON_STYLESHEET)
        self.arm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)
        self.disarm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)

        self.arm_button.clicked.connect(self.arm_clicked)
        self.disarm_button.clicked.connect(self.disarm_clicked)

        layout.addWidget(self.arm_button)
        layout.addWidget(self.disarm_button)

        self.command_response_signal.connect(self.arm_status)

        self.arm_client: GUIEventClient = GUIEventClient(
            CommandBool,
            "mavros/cmd/arming",
            self.command_response_signal,
            expected_namespace='/tether'
        )

        self.mavros_subscription = GUIEventSubscriber(
            VehicleState,
            'vehicle_state_event',
            self.vehicle_state_signal,
        )

        self.vehicle_state_signal.connect(self.vehicle_state_callback)

    def arm_clicked(self) -> None:
        self.arm_client.send_request_async(self.ARM_REQUEST)

    def disarm_clicked(self) -> None:
        self.arm_client.send_request_async(self.DISARM_REQUEST)

    @pyqtSlot(CommandBool.Response)
    def arm_status(self, res: CommandBool.Response) -> None:
        if not res:
            self.arm_client.get_logger().warn("Failed to arm or disarm.")

    @pyqtSlot(VehicleState)
    def vehicle_state_callback(self, msg: VehicleState) -> None:
        if msg.pixhawk_connected:
            if msg.armed:
                self.arm_button.setProperty(PROPERTY_NAME, Style.ON)
                self.disarm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)
            else:
                self.arm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)
                self.disarm_button.setProperty(PROPERTY_NAME, Style.OFF)
        else:
            self.arm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)
            self.disarm_button.setProperty(PROPERTY_NAME, Style.INACTIVE)

        for button in (self.arm_button, self.disarm_button):
            style = button.style()
            if style is not None:
                style.polish(button)
            else:
                self.arm_client.get_logger().error("Gui button missing a style")
