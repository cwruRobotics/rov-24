from gui.app import App
from gui.widgets.arm import Arm
from gui.widgets.video_widget import SwitchableVideoWidget
from gui.widgets.flood_visual import FloodVisual
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout


class PilotApp(App):
    def __init__(self) -> None:
        super().__init__('pilot_gui_node')

        self.setWindowTitle('Pilot GUI - CWRUbotix ROV 2024')

        layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(layout)

        self.video_area = SwitchableVideoWidget(["front_cam/image_raw",
                                                 "bottom_cam/image_raw",
                                                 "camera/color/image_raw"],
                                                ["Front Camera",
                                                 "Bottom Camera",
                                                 "Depth Camera"],
                                                "camera_switch")
        layout.addWidget(self.video_area, alignment=Qt.AlignmentFlag.AlignCenter)

        self.floodWidget: FloodVisual = FloodVisual()
        layout.addWidget(self.floodWidget, alignment=Qt.AlignmentFlag.AlignRight
                         | Qt.AlignmentFlag.AlignTop)

        self.arm: Arm = Arm()
        layout.addWidget(self.arm,
                         alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)


def run_gui_pilot() -> None:
    PilotApp().run_gui()
