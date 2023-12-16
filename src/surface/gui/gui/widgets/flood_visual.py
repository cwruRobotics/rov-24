# /flooding (boolean) (True is flooding)
from rov_msgs.msg import Flooding
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from gui.event_nodes.subscriber import GUIEventSubscriber
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class FloodVisual(QWidget):

    signal: pyqtSignal = pyqtSignal(Flooding)

    def __init__(self):
        super().__init__()
        # Boilerplate PyQt Setup to link to ROS through a signal/subscriber
        self.signal.connect(self.refresh)
        self.subscription: GUIEventSubscriber = GUIEventSubscriber(Flooding,
                                                                   '/flooding',
                                                                   self.signal,
                                                                   10)
        # Create basic 2 vertical stacked boxes layout
        self.layout = QVBoxLayout()
        # Create the label that tells us what this is
        self.label = QLabel('Flooding Indicator')
        # Set font and size
        font = QFont("Arial", 14)
        self.label.setFont(font)

        self.layout.addWidget(self.label)
        # Create the Indicator with a default state of green circle (green = good)
        self.indicator = QLabel("🟢")
        # Set font and size
        font = QFont("Arial", 36)
        self.indicator.setFont(font)

        self.layout.addWidget(self.indicator)

        self.setLayout(self.layout)

    @pyqtSlot(Flooding)
    def refresh(self, msg: Flooding):
        if Flooding.flooding:
            self.indicator.setText("🔴")
