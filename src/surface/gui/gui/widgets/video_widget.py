from typing import Optional

import cv2
from cv2.typing import MatLike
from cv_bridge import CvBridge
from gui.event_nodes.subscriber import GUIEventSubscriber
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from sensor_msgs.msg import Image

from rov_msgs.msg import CameraControllerSwitch

WIDTH = 1280
HEIGHT = 720


class VideoWidget(QWidget):
    """A single video stream widget."""

    update_big_video_signal = pyqtSignal(QWidget)
    handle_frame_signal = pyqtSignal(Image)

    def __init__(self, topic: str, label_text: Optional[str] = None,
                 widget_width: int = WIDTH, widget_height: int = HEIGHT,
                 swap_rb_channels: bool = False) -> None:
        super().__init__()

        self.widget_width: int = widget_width
        self.widget_height: int = widget_height
        self.swap_rb_channels: bool = swap_rb_channels

        layout = QVBoxLayout()
        self.setLayout(layout)

        if label_text is not None:
            self.label = QLabel(label_text)
            self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.label.setStyleSheet('QLabel { font-size: 35px; }')
            layout.addWidget(self.label, Qt.AlignmentFlag.AlignHCenter)

        self.video_frame_label = QLabel()
        self.video_frame_label.setText(f'This topic had no frame: {topic}')
        layout.addWidget(self.video_frame_label)

        self.cv_bridge: CvBridge = CvBridge()

        self.handle_frame_signal.connect(self.handle_frame)
        self.camera_subscriber: GUIEventSubscriber = GUIEventSubscriber(
            Image, topic, self.handle_frame_signal)

    @pyqtSlot(Image)
    def handle_frame(self, frame: Image) -> None:
        cv_image: MatLike = self.cv_bridge.imgmsg_to_cv2(
            frame, desired_encoding='passthrough')

        qt_image: QImage = self.convert_cv_qt(cv_image, self.widget_width, self.widget_height)

        self.video_frame_label.setPixmap(QPixmap.fromImage(qt_image))

    def convert_cv_qt(self, cv_img: MatLike, width: int = 0, height: int = 0) -> QImage:
        """Convert from an opencv image to QPixmap."""
        # Color image
        if len(cv_img.shape) == 3:
            # Swap red & blue channels if necessary
            if self.swap_rb_channels:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

            h, w, ch = cv_img.shape
            bytes_per_line: int = ch * w

            img_format = QImage.Format.Format_RGB888

        # Grayscale image
        elif len(cv_img.shape) == 2:
            h, w = cv_img.shape
            bytes_per_line = w

            img_format = QImage.Format.Format_Grayscale8

        else:
            raise Exception("Somehow not color or grayscale image.")

        qt_image = QImage(cv_img.data, w, h, bytes_per_line, img_format)
        qt_image = qt_image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)

        return qt_image


class SwitchableVideoWidget(VideoWidget):
    """A single video stream widget that can be paused and played."""

    BUTTON_WIDTH = 120

    controller_signal = pyqtSignal(CameraControllerSwitch)

    def __init__(self, cam_topics: list[str], button_names: list[str],
                 controller_button_topic: Optional[str] = None,
                 default_cam_num: int = 0,
                 label_text: Optional[str] = None,
                 widget_width: int = WIDTH, widget_height: int = HEIGHT,
                 swap_rb_channels: bool = False):

        self.active_cam = default_cam_num
        self.cam_topics = cam_topics
        self.button_names = button_names

        super().__init__(cam_topics[self.active_cam], label_text, widget_width,
                         widget_height, swap_rb_channels)

        self.num_of_cams = len(cam_topics)

        if self.num_of_cams != len(button_names):
            self.camera_subscriber.get_logger().error("Number of cam topics != num of cam names")
            raise ValueError("Number of cam topics != num of cam names")

        self.button: QPushButton = QPushButton(button_names[self.active_cam])
        self.button.setMaximumWidth(self.BUTTON_WIDTH)
        self.button.clicked.connect(lambda: self.camera_switch(True))

        layout = self.layout()
        if isinstance(layout, QVBoxLayout):
            layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            self.camera_subscriber.get_logger().error("Missing Layout")

        if controller_button_topic is not None:
            self.controller_signal.connect(self.controller_camera_switch)
            self.controller_subscriber = GUIEventSubscriber(CameraControllerSwitch,
                                                            controller_button_topic,
                                                            self.controller_signal)

    @pyqtSlot(CameraControllerSwitch)
    def controller_camera_switch(self, switch: CameraControllerSwitch) -> None:
        self.camera_switch(switch.toggle_right)

    def camera_switch(self, toggle_right: bool) -> None:
        if toggle_right:
            self.active_cam = (self.active_cam + 1) % self.num_of_cams
        else:
            self.active_cam = (self.active_cam - 1) % self.num_of_cams

        self.camera_subscriber.destroy_node()
        self.camera_subscriber = GUIEventSubscriber(
            Image, self.cam_topics[self.active_cam], self.handle_frame_signal)
        self.button.setText(self.button_names[self.active_cam])


class PauseableVideoWidget(VideoWidget):
    """A single video stream widget that can be paused and played."""

    BUTTON_WIDTH = 120
    PAUSED_TEXT = 'Play'
    PLAYING_TEXT = 'Pause'

    def __init__(self, cam_topic: str, label_text: Optional[str] = None,
                 widget_width: int = WIDTH, widget_height: int = HEIGHT,
                 swap_rb_channels: bool = False) -> None:
        super().__init__(cam_topic, label_text, widget_width,
                         widget_height, swap_rb_channels)

        self.button: QPushButton = QPushButton(self.PLAYING_TEXT)
        self.button.setMaximumWidth(self.BUTTON_WIDTH)
        self.button.clicked.connect(self.toggle)

        layout = self.layout()
        if isinstance(layout, QVBoxLayout):
            layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            self.camera_subscriber.get_logger().error("Missing Layout")

        self.is_paused = False

    @pyqtSlot(Image)
    def handle_frame(self, frame: Image) -> None:
        if not self.is_paused:
            super().handle_frame(frame)

    def toggle(self) -> None:
        """Toggle whether this widget is paused or playing."""
        self.is_paused = not self.is_paused
        self.button.setText(self.PAUSED_TEXT if self.is_paused else self.PLAYING_TEXT)
