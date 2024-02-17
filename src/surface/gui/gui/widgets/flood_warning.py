from gui.event_nodes.subscriber import GUIEventSubscriber
from gui.widgets.circle import CircleIndicator
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from rov_msgs.msg import Flooding


class FloodWarning(QWidget):
    signal = pyqtSignal(Flooding)

    def __init__(self) -> None:
        super().__init__()

        self.signal.connect(self.refresh)
        self.subscription = GUIEventSubscriber(
            Flooding,
            "flooding",
            self.signal,
        )
        # Create a latch variable
        self.warning_msg_latch = False
        # Create basic 2 vertical stacked boxes layout
        flood_layout = QVBoxLayout()
        # Create the label that tells us what this is

        header_layout = QHBoxLayout()
        label = QLabel("Flooding Status")
        font = QFont("Arial", 14)
        label.setFont(font)
        header_layout.addWidget(label)
        self.indicator_circle = CircleIndicator(radius=10)
        header_layout.addWidget(self.indicator_circle)

        flood_layout.addLayout(header_layout)

        self.indicator = QLabel("No Water present")
        self.indicator.setFont(font)
        flood_layout.addWidget(self.indicator)
        self.setLayout(flood_layout)

    @pyqtSlot(Flooding)
    def refresh(self, msg: Flooding) -> None:
        if msg.flooding:
            self.indicator.setText("FLOODING")
            self.subscription.get_logger().error("Robot is actively flooding, do something!")
            self.warning_msg_latch = True
            self.indicator_circle.set_off()
        else:
            self.indicator.setText("No Water present")
            self.indicator_circle.set_on()
            if self.warning_msg_latch:
                self.subscription.get_logger().warning("Robot flooding has reset itself.")
                self.warning_msg_latch = False
