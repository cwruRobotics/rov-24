from gui.app import App
from gui.widgets.arm import Arm
from gui.widgets.flood_warning import FloodWarning
from gui.widgets.video_widget import SwitchableVideoWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout


class PilotApp(App):
    def __init__(self) -> None:
        super().__init__('pilot_gui_node')

        self.setWindowTitle('Pilot GUI - CWRUbotix ROV 2024')

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Look into QStackedLayout for possibly switching between
        # 1 big camera feed and 2 smaller ones
        video_area = SwitchableVideoWidget(["front_cam/image_raw",
                                            "bottom_cam/image_raw",
                                            "camera/color/image_raw"],
                                           ["Front Camera",
                                            "Bottom Camera",
                                            "Depth Camera"],
                                           "camera_switch")
        layout.addWidget(video_area, alignment=Qt.AlignmentFlag.AlignCenter)

        floodWidget = FloodWarning()
        layout.addWidget(floodWidget, alignment=Qt.AlignmentFlag.AlignRight |
                         Qt.AlignmentFlag.AlignTop)

        arm = Arm()
        layout.addWidget(arm, alignment=Qt.AlignmentFlag.AlignRight |
                         Qt.AlignmentFlag.AlignBottom)


def run_gui_pilot() -> None:
    PilotApp().run_gui()
