from gui.gui_nodes.event_nodes.client import GUIEventClient
from gui.gui_nodes.event_nodes.subscriber import GUIEventSubscriber
from gui.styles.custom_styles import ButtonIndicator
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel

from rov_msgs.msg import VehicleState
from mavros_msgs.srv import SetMode


ENABLE_REQUEST = SetMode.Request(base_mode=0, custom_mode="ALT_HOLD")
DISABLE_REQUEST = SetMode.Request(base_mode=0, custom_mode="MANUAL")
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 60
BUTTON_STYLESHEET = 'QPushButton { font-size: 20px; }'


class DepthHold(QWidget):
    """Widget for setting the pixhawk's stabilization mode."""

    command_response_signal = pyqtSignal(SetMode.Response)
    vehicle_state_signal = pyqtSignal(VehicleState)

    def __init__(self) -> None:

        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Depth Hold"))

        self.setLayout(layout)

        h_layout = QHBoxLayout()

        self.enable_button = ButtonIndicator()
        self.disable_button = ButtonIndicator()

        self.enable_button.setText("Enable")
        self.disable_button.setText("Disable")

        self.enable_button.setMinimumWidth(BUTTON_WIDTH)
        self.disable_button.setMinimumWidth(BUTTON_WIDTH)

        self.enable_button.setMinimumHeight(BUTTON_HEIGHT)
        self.disable_button.setMinimumHeight(BUTTON_HEIGHT)

        self.enable_button.setStyleSheet(BUTTON_STYLESHEET)
        self.disable_button.setStyleSheet(BUTTON_STYLESHEET)
        self.enable_button.set_inactive()
        self.disable_button.set_inactive()

        self.enable_button.clicked.connect(self.enable_clicked)
        self.disable_button.clicked.connect(self.disable_clicked)

        h_layout.addWidget(self.disable_button)
        h_layout.addWidget(self.enable_button)

        layout.addLayout(h_layout)

        self.command_response_signal.connect(self.response_callback)

        self.set_mode_callback = GUIEventClient(SetMode, "mavros/set_mode",
                                                self.command_response_signal,
                                                expected_namespace='/tether')

        self.mavros_subscription = GUIEventSubscriber(
            VehicleState,
            'vehicle_state_event',
            self.vehicle_state_signal,
        )

        self.vehicle_state_signal.connect(self.vehicle_state_callback)

    def enable_clicked(self) -> None:
        """Send a mavros service request to enable depth hold
        """
        self.set_mode_callback.send_request_async(ENABLE_REQUEST)

    def disable_clicked(self) -> None:
        """Send a mavros service request to disable depth hold
        """
        self.set_mode_callback.send_request_async(DISABLE_REQUEST)

    @pyqtSlot(SetMode.Response)
    def response_callback(self, res: SetMode.Response) -> None:
        """If the service call failed, send a ros warning

        Parameters
        ----------
        res : SetMode.Response
            The mavros service response
        """
        if not res.mode_sent:
            self.set_mode_callback.get_logger().warn("Failed to set pixhawk mode.")

    @pyqtSlot(VehicleState)
    def vehicle_state_callback(self, msg: VehicleState) -> None:
        """Update the button styles to show the status of the pixhawk

        Parameters
        ----------
        msg : VehicleState
            The mavros vehicle state message
        """
        if msg.pixhawk_connected:
            if msg.depth_hold_enabled:
                self.enable_button.set_on()
                self.disable_button.remove_state()
            else:
                self.enable_button.remove_state()
                self.disable_button.set_off()
        else:
            self.enable_button.set_inactive()
            self.disable_button.set_inactive()
