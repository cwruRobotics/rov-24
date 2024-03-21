from gui.app import App
from gui.widgets.arm import Arm
from gui.widgets.flood_warning import FloodWarning
from gui.widgets.timer import TimerDisplay
from gui.widgets.video_widget import (CameraDescription, CameraType,
                                      SwitchableVideoWidget, VideoWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class DebugApp(App):
    def __init__(self) -> None:
        super().__init__('debug_gui_node')

        self.setWindowTitle('Debug GUI - CWRUbotix ROV 2024')

        main_layout = QVBoxLayout()
        video_layout = QHBoxLayout()
        self.setLayout(main_layout)

        front_cam_description = CameraDescription(CameraType.ETHERNET,
                                                  'front_cam/image_raw',
                                                  'Front Camera')

        main_video = VideoWidget(front_cam_description)

        bottom_cam_description = CameraDescription(CameraType.ETHERNET,
                                                   'bottom_cam/image_raw',
                                                   'Bottom Camera')
        depth_cam_description = CameraDescription(CameraType.DEPTH,
                                                  'depth_cam/image_raw',
                                                  'Depth Camera', 640, 360)

        video_area = SwitchableVideoWidget([bottom_cam_description, depth_cam_description],
                                           "camera_switch")

        video_layout.addWidget(main_video, alignment=Qt.AlignmentFlag.AlignHCenter)
        video_layout.addWidget(video_area, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addLayout(video_layout)

        bottom_screen_layout = QHBoxLayout()

        timer = TimerDisplay()
        bottom_screen_layout.addWidget(timer)

        flood_widget = FloodWarning()
        bottom_screen_layout.addWidget(flood_widget, alignment=Qt.AlignmentFlag.AlignHCenter |
                                       Qt.AlignmentFlag.AlignBottom)

        arm = Arm()
        bottom_screen_layout.addWidget(arm, alignment=Qt.AlignmentFlag.AlignRight |
                                       Qt.AlignmentFlag.AlignBottom)

        main_layout.addLayout(bottom_screen_layout)


def run_gui_debug() -> None:
    DebugApp().run_gui()
