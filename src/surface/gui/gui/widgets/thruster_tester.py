import os
import time
from enum import IntEnum
from threading import Event, Thread
from typing import Optional

from ament_index_python.packages import get_package_share_directory
from gui.gui_nodes.event_nodes.client import GUIEventClient
from gui.gui_nodes.event_nodes.subscriber import GUIEventSubscriber
from mavros_msgs.srv import CommandLong, ParamPull
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import (QCheckBox, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QWidget)
from rcl_interfaces.msg import ParameterValue
from rcl_interfaces.srv import GetParameters, SetParameters
from rclpy.parameter import Parameter

from rov_msgs.msg import VehicleState

MOTOR_COUNT = 8
SERVO_FUNCTION_OFFSET = 32


class TestMotorClient(GUIEventClient):

    def test_motor_for_time(self, motor_index: int, thread_event: Optional[Event] = None,
                            throttle: float = 0.50, duration: float = 2.0) -> None:
        """
        Run a motor for an (approximate) length of time (blocking).

        Based on https://github.com/mavlink/qgroundcontrol/blob/f79b466/src/Vehicle/Vehicle.cc

        Parameters
        ----------
        motor_index : int
            A motor index, from 1 to 8
        thread_event: Optional[Event]
            A thread Event for stopping threads early by default None.
        throttle : float
            A float from -1 to 1, where -1 is full reverse and 1 is full forward
        duration : float
            Time in seconds to run the motor

        """
        throttle = max(min(throttle, 1.0), -1.0)  # Clamp the throttle between -1 and 1
        throttle_percent = 50 * throttle + 50  # Rescale to be from 0 to 100, with 50 at the center

        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_request_async(
                CommandLong.Request(
                    command=209,  # MAV_CMD_DO_MOTOR_TEST
                    param1=float(motor_index),  # Motor number
                    param2=0.0,  # MOTOR_TEST_THROTTLE_PERCENT
                    param3=float(throttle_percent),
                    param4=0.0,  # Time between tests
                    param5=0.0,  # Number of motors to test
                    param6=2.0  # MOTOR_TEST_ORDER_BOARD
                )
            )

            time.sleep(0.05)

            if thread_event and thread_event.is_set():
                self.get_logger().info("pog")
                break


class MotorDirection(IntEnum):
    NORMAL = 1
    NO_SPIN = 0
    REVERSED = -1


class ThrusterBox(QWidget):

    def __init__(self, pin_number: int, test_motor_client: TestMotorClient) -> None:
        """
        Initialize ThrusterBox.

        Parameters
        ----------
        pin_number : int
            The pin number of the thruster.
        test_motor_client : GUIEventClient
            Passed in client from parent widget.

        """
        super().__init__()

        self.test_motor_client = test_motor_client

        vert_layout = QVBoxLayout()

        layout = QHBoxLayout()
        label = QLabel(str(pin_number))
        label.setMaximumWidth(20)

        pin_input = QLineEdit()

        pin_number_validator = QIntValidator()
        pin_number_validator.setRange(1, MOTOR_COUNT)
        pin_input.setValidator(pin_number_validator)

        pin_input.insert(str(pin_number))
        pin_input.setMaximumWidth(20)

        check_box = QCheckBox()

        layout.addWidget(label)
        layout.addWidget(pin_input)
        layout.addWidget(check_box)

        vert_layout.addLayout(layout)

        button = QPushButton(f"Test Motor {pin_number}")
        button.clicked.connect(self.async_send_motor_test)

        vert_layout.addWidget(button)
        self.setLayout(vert_layout)

        self.pin_input = pin_input
        self.checkbox = check_box
        self.thread_event = Event()

    def all_thrusters(self, thrusters: list['ThrusterBox']) -> None:
        self.thrusters = thrusters

    def async_send_motor_test(self) -> None:
        """Send motor test based on input asynchronously."""
        for thruster in self.thrusters:
            thruster.thread_event.set()
        time.sleep(0.2)
        self.thread_event.clear()

        Thread(target=self.send_motor_test, daemon=True, name="thruster_box_test",
               args=((self.thread_event,))).start()

    def send_motor_test(self, thread_event: Event) -> None:
        """
        Send motor test based on input.

        Parameters
        ----------
        thread_event : Event
            A thread Event for stopping threads early.

        """
        direction = self.get_direction()

        if direction is MotorDirection.NORMAL:
            throttle = 0.5
        elif direction is MotorDirection.REVERSED:
            throttle = -0.5

        current_pin = int(self.pin_input.text()) - 1
        self.test_motor_client.test_motor_for_time(current_pin, thread_event, throttle)
        self.test_motor_client.test_motor_for_time(current_pin, thread_event, 0.0, 300)

    def set_pin_from_param(self, pin_val: int) -> None:
        """
        Set the pin value of the input from a parameter value.

        Parameters
        ----------
        pin_val : int
            The value to set the input to.

        """
        self.pin_input.setText(
                str(pin_val - SERVO_FUNCTION_OFFSET)
            )

    def get_pin_for_param(self) -> int:
        """
        Return the function value.

        Returns
        -------
        int
            The SERVO_FUNCTION value of the box.

        """
        return int(self.pin_input.text()) + SERVO_FUNCTION_OFFSET

    def get_direction(self) -> MotorDirection:
        """
        Return the MotorDirection of the ThrusterBox.

        Returns
        -------
        MotorDirection
            The MotorDirection of the ThrusterBox.

        """
        return MotorDirection.REVERSED if self.checkbox.isChecked() else MotorDirection.NORMAL

    def set_direction(self, direction: MotorDirection) -> None:
        """
        Update the checkbox to the MotorDirection.

        Parameters
        ----------
        direction : MotorDirection
            The Direction to update the checkbox.

        """
        if direction == MotorDirection.NORMAL:
            set_check = False
        elif direction == MotorDirection.REVERSED:
            set_check = True
        elif direction == MotorDirection.NO_SPIN:
            return
        else:
            self.test_motor_client.get_logger().warning("Got unexpected input for check boxes.")

        self.checkbox.setChecked(set_check)


class ThrusterImage(QWidget):
    def __init__(self) -> None:
        """Initialize ThrusterImage."""
        super().__init__()
        image_layout = QVBoxLayout()

        gui_path = get_package_share_directory('gui')
        picture_path = os.path.join(gui_path, 'images',
                                    'vectored6dof-frame.png')
        image = QLabel()
        pixmap = QPixmap(picture_path)
        image.setPixmap(pixmap.scaledToHeight(200))

        # https://www.ardusub.com/quick-start/vehicle-frame.html
        image_text = QLabel(("Green thrusters indicate counter-clockwise propellers and blue"
                             "thrusters indicate clockwise propellers (or vice-versa)."))

        image_text.setWordWrap(True)

        image_layout.addWidget(image)
        image_layout.addWidget(image_text)
        self.setLayout(image_layout)


class ThrusterAssigner(QWidget):

    vehicle_state_callback_signal = pyqtSignal(VehicleState)
    pull_motors_callback_signal = pyqtSignal(ParamPull.Response)
    param_send_callback_signal = pyqtSignal(SetParameters.Response)
    param_get_callback_signal = pyqtSignal(GetParameters.Response)

    def __init__(self, test_motor_client: TestMotorClient) -> None:
        """
        Initialize Widget and ROS.

        Parameters
        ----------
        test_motor_client : TestMotorClient
            Passed in client from parent widget.

        """
        self.init_widget(test_motor_client)
        self.init_ros()

    def init_widget(self, test_motor_client: TestMotorClient) -> None:
        """
        Initialize widget.

        Parameters
        ----------
        test_motor_client : TestMotorClient
            Passed in client from parent widget.

        """
        super().__init__()
        heading = QLabel("Thruster Pin Configuration")

        pin_numbers_grid = QGridLayout()
        self.thruster_boxes: list[ThrusterBox] = []

        COL_COUNT = 2
        ROW_COUNT = int(MOTOR_COUNT / COL_COUNT)

        for i in range(1, MOTOR_COUNT + 1):
            index = i - 1
            box = ThrusterBox(i, test_motor_client)
            self.thruster_boxes.append(box)

            on_first_column = index < ROW_COUNT
            column = 0 if on_first_column else 1
            row = index % ROW_COUNT
            pin_numbers_grid.addWidget(box, row, column)

        for thruster_box in self.thruster_boxes:
            thruster_box.all_thrusters(self.thruster_boxes)

        pin_numbers_grid.setColumnStretch(0, 1)
        pin_numbers_grid.setColumnStretch(3, 1)
        pin_numbers_grid.setColumnStretch(6, 1)

        pin_assignment_button = QPushButton()
        pin_assignment_button.setText("Send Pin Assignments")
        pin_assignment_button.clicked.connect(self.send_pin_assignments)

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addLayout(pin_numbers_grid)
        layout.addWidget(pin_assignment_button)
        self.setLayout(layout)

    def init_ros(self) -> None:
        """Initialize ROS part of ThrusterAssigner."""
        self.pixhawk_activated = False

        self.vehicle_state_subscriber = GUIEventSubscriber(
            VehicleState,
            "vehicle_state_event",
            self.vehicle_state_callback_signal
        )
        self.vehicle_state_callback_signal.connect(self.vehicle_state_callback)

        self.param_pull_client = GUIEventClient(
            ParamPull,
            "mavros/param/pull",
            self.pull_motors_callback_signal,
            10.0
        )
        self.pull_motors_callback_signal.connect(self.pull_param_handler)

        self.param_send_client = GUIEventClient(
            SetParameters,
            "mavros/param/set_parameters",
            self.param_send_callback_signal
        )
        self.param_send_callback_signal.connect(self.param_send_signal_handler)

        self.param_get_client = GUIEventClient(
            GetParameters,
            "mavros/param/get_parameters",
            self.param_get_callback_signal
        )
        self.param_get_callback_signal.connect(self.param_get_signal_handler)

    def vehicle_state_callback(self, msg: VehicleState) -> None:
        """
        Pull params after the pixhawk is connected.

        Parameters
        ----------
        msg : VehicleState
            VehicleState message.

        """
        if msg.pixhawk_connected and not self.pixhawk_activated:
            self.param_pull_client.send_request_async(ParamPull.Request())
            self.pixhawk_activated = True
        elif msg.pixhawk_connected:
            self.pixhawk_activated = False

    @pyqtSlot(ParamPull.Response)
    def pull_param_handler(self, _: ParamPull.Response) -> None:
        """
        Log response to ParamPull service.

        Parameters
        ----------
        res : ParamPull.Response
            ParamPull.Response message.

        """
        self.param_pull_client.get_logger().info("Succesfully pulled param from pixhawk")

        param_names = [f"SERVO{i + 1}_FUNCTION" for i in range(MOTOR_COUNT)]

        param_names.extend([f"MOT_{i + 1}_DIRECTION" for i in range(MOTOR_COUNT)])

        self.param_get_client.send_request_async(GetParameters.Request(
            names=param_names
        ))

    def send_pin_assignments(self) -> None:
        """Send pin assignments to the pixhawk."""
        # https://wiki.ros.org/mavros/Plugins#param
        # https://ardupilot.org/copter/docs/parameters.html#servo10-parameters

        param_list: list[Parameter] = []
        for i, thruster_box in enumerate(self.thruster_boxes):
            # https://ardupilot.org/copter/docs/parameters.html#servo1-function-servo-output-function
            pin_function = thruster_box.get_pin_for_param()
            param = Parameter(f"SERVO{i + 1}_FUNCTION",
                              Parameter.Type.INTEGER,
                              pin_function).to_parameter_msg()
            param_list.append(param)

        for i, thruster_box in enumerate(self.thruster_boxes):
            direction = thruster_box.get_direction()
            param = Parameter(f"MOT_{i + 1}_DIRECTION",
                              Parameter.Type.INTEGER,
                              direction).to_parameter_msg()
            param_list.append(param)

        req = SetParameters.Request(parameters=param_list)
        self.param_send_client.send_request_async(req)

    @pyqtSlot(SetParameters.Response)
    def param_send_signal_handler(self, _: SetParameters.Response) -> None:
        """
        Log response to SetParameters service.

        Parameters
        ----------
        res : SetParameters.Response
            SetParameters.Response message.

        """
        self.param_send_client.get_logger().info("Succesfully sent params to /mavros/param.")

    @pyqtSlot(GetParameters.Response)
    def param_get_signal_handler(self, res: GetParameters.Response) -> None:
        """
        Log response to GetParameters service.

        Parameters
        ----------
        res : GetParameters.Response
            GetParameters.Response message.

        """
        self.param_get_client.get_logger().info("Succesfully got params from /mavros/param.")
        params: list[ParameterValue] = res.values
        for i, thruster_box in enumerate(self.thruster_boxes):
            thruster_box.set_pin_from_param(params[i].integer_value)

        for i, thruster_box in enumerate(self.thruster_boxes):
            val = params[i + MOTOR_COUNT].integer_value
            thruster_box.set_direction(val)


class ThrusterTester(QWidget):
    """Widget to command the pixhawk to test the thrusters, and reassign thruster ports."""

    test_command_callback_signal = pyqtSignal(CommandLong.Response)

    def __init__(self) -> None:
        super().__init__()

        # TODO Our ROS Node count is getting kind of crazy lol
        self.test_cmd_client = TestMotorClient(
            CommandLong,
            "mavros/cmd/command",
            self.test_command_callback_signal
        )
        self.test_command_callback_signal.connect(self.command_response_handler)

        layout = QVBoxLayout()

        test_button = QPushButton()
        test_button.setText("Test Thrusters")
        test_button.clicked.connect(self.async_send_test_message)

        self.thruster_assigner = ThrusterAssigner(self.test_cmd_client)

        layout.addWidget(self.thruster_assigner)
        layout.addWidget(test_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(ThrusterImage())
        main_layout.addLayout(layout)

        self.setLayout(main_layout)

    def async_send_test_message(self) -> None:
        """Asynchronously send a test message."""
        Thread(target=self.send_test_message, daemon=True, name="thruster_test_thread").start()

    def send_test_message(self) -> None:
        """Send a test message for each motor."""
        for motor_index in range(MOTOR_COUNT):
            self.thruster_assigner.thruster_boxes[motor_index].thread_event.set()
            self.test_cmd_client.get_logger().info(f"Testing thruster {motor_index + 1}")
            self.test_cmd_client.test_motor_for_time(motor_index)
            self.test_cmd_client.test_motor_for_time(motor_index, None, 0.0, 0.5)

    @pyqtSlot(CommandLong.Response)
    def command_response_handler(self, res: CommandLong.Response) -> None:
        """
        Log response to CommandLong service.

        Parameters
        ----------
        res : CommandLong.Response
            CommandLong.Response message.

        """
        self.test_cmd_client.get_logger().info(f"Test response: {res.success}, {res.result}")
