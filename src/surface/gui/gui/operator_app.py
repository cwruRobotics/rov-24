from gui.app import App
from gui.widgets.logger import Logger
from gui.widgets.debug_tab import DebugWidget
from gui.widgets.task_selector import TaskSelector
from gui.widgets.timer import Timer
from PyQt6.QtWidgets import QGridLayout, QTabWidget, QWidget, QVBoxLayout


class OperatorApp(App):
    def __init__(self) -> None:
        super().__init__('operator_gui_node')

        self.setWindowTitle('Operator GUI - CWRUbotix ROV 2024')

        # Main tab
        main_tab = QWidget()
        main_layout = QGridLayout()
        main_tab.setLayout(main_layout)

        timer = Timer()
        main_layout.addWidget(timer, 0, 1)

        task_selector = TaskSelector()
        main_layout.addWidget(task_selector, 1, 1)

        logger = Logger()
        main_layout.addWidget(logger, 1, 0)

        # Add tabs to root
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)

        tabs = QTabWidget()
        tabs.addTab(main_tab, "Main")
        tabs.addTab(DebugWidget(), "Debug")

        root_layout.addWidget(tabs)


def run_gui_operator() -> None:
    OperatorApp().run_gui()
