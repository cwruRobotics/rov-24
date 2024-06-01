from queue import Queue
from typing import Generator, TypeVar
from collections import deque
import pytest
from transceiver.serial_reader import SerialReaderPacketHandler

from rov_msgs.msg import FloatData

T = TypeVar('T')

PACKET = "ROS:11,1,1:313901,988.53;314843,988.57;315785,988.99;316727,991.56;317669,996.21;318611,1002.36;319553,1010.36;320495,1021.11;321437,1034.42;322379,1050.23;323321,1051.86;324263,1053.20;325206,1053.32;326146,1053.46;327088,1053.52;328030,1053.58;328972,1053.61;329914,1053.64;330856,1053.61;331798,1053.60;332740,1053.65;333682,1053.58;334624,1053.53;335566,1053.52;336508,1053.39;337453,1053.41;338395,1053.46;339337,1053.37;340279,1053.42;341221,1053.49;342163,1053.54"  # noqa: E501

NOT_THREE_SECTIONS = "ROS:11,1,1313901,988.53;314843,988.57;315785,988.99;316727,991.56;317669,996.21;318611,1002.36;319553,1010.36;320495,1021.11;321437,1034.42;322379,1050.23;323321,1051.86;324263,1053.20;325206,1053.32;326146,1053.46;327088,1053.52;328030,1053.58;328972,1053.61;329914,1053.64;330856,1053.61;331798,1053.60;332740,1053.65;333682,1053.58;334624,1053.53;335566,1053.52;336508,1053.39;337453,1053.41;338395,1053.46;339337,1053.37;340279,1053.42;341221,1053.49;342163,1053.54"  # noqa: E501

HEADER_TWO_ELEMENTS = "ROS:11,1:313901,988.53;314843,988.57;315785,988.99;316727,991.56;317669,996.21;318611,1002.36;319553,1010.36;320495,1021.11;321437,1034.42;322379,1050.23;323321,1051.86;324263,1053.20;325206,1053.32;326146,1053.46;327088,1053.52;328030,1053.58;328972,1053.61;329914,1053.64;330856,1053.61;331798,1053.60;332740,1053.65;333682,1053.58;334624,1053.53;335566,1053.52;336508,1053.39;337453,1053.41;338395,1053.46;339337,1053.37;340279,1053.42;341221,1053.49;342163,1053.54"  # noqa: E501


ROS_SINGLE_ONE = "ROS:SINGLE:25:5552,992.4500"
ROS_SINGLE_TWO = "ROS:SINGLE:25:11071,994.4299"
ROS_SINGLE_THREE = "ROS:SINGLE:25:16592,992.9600"
ROS_SINGLE_FOUR = "ROS:SINGLE:25:22112,993.3699"
ROS_SINGLE_FIVE = "ROS:SINGLE:25:27631,993.2600"


@pytest.fixture
def packet_handler() -> Generator[SerialReaderPacketHandler, None, None]:
    yield SerialReaderPacketHandler()


def test_message_parser(packet_handler: SerialReaderPacketHandler) -> None:
    msg = packet_handler.message_parser(PACKET)

    assert msg == FloatData(
        team_number=11,
        profile_number=1,
        profile_half=1,
        time_data=[5.231683254241943, 5.247383117675781, 5.263083457946777, 5.278783321380615, 5.294483184814453, 5.310183525085449, 5.325883388519287, 5.341583251953125, 5.357283115386963, 5.372983455657959, 5.388683319091797, 5.404383182525635, 5.420100212097168, 5.435766696929932, 5.4514665603637695, 5.467166900634766, 5.4828667640686035, 5.498566627502441, 5.514266490936279, 5.529966831207275, 5.545666694641113, 5.561366558074951, 5.577066898345947, 5.592766761779785, 5.608466625213623, 5.624216556549072, 5.639916896820068, 5.655616760253906, 5.671316623687744, 5.687016487121582, 5.702716827392578],  # noqa 501
        depth_data=[-0.2521384060382843, -0.25173041224479675, -0.24744650721549988, -0.2212330847978592, -0.1738041341304779, -0.11107552796602249, -0.029477344825863838, 0.08017022162675858, 0.21592919528484344, 0.3771876096725464, 0.39381325244903564, 0.40748095512390137, 0.4087049067020416, 0.41013288497924805, 0.41074487566947937, 0.4113568663597107, 0.41166284680366516, 0.411968857049942, 0.41166284680366516, 0.41156086325645447, 0.4120708405971527, 0.4113568663597107, 0.41084685921669006, 0.41074487566947937, 0.40941891074180603, 0.4096229076385498, 0.41013288497924805, 0.40921491384506226, 0.4097248911857605, 0.4104388654232025, 0.41094887256622314]]  # noqa 501
    )

    with pytest.raises(ValueError, match="Packet expected 3 sections, found 2 sections"):
        packet_handler.message_parser(NOT_THREE_SECTIONS)

    with pytest.raises(ValueError, match="Packet header length of 3 expected found 2 instead"):
        packet_handler.message_parser(HEADER_TWO_ELEMENTS)


def test_handle_ros_single(packet_handler: SerialReaderPacketHandler) -> None:
    packet_handler.handle_ros_single(ROS_SINGLE_ONE)
    test_queue: Queue[float] = Queue(5)
    test_queue.put(992.4500)

    assert equal(packet_handler.surface_pressures, test_queue)
    assert packet_handler.surface_pressure == 992.4500

    packet_handler.handle_ros_single(ROS_SINGLE_TWO)
    test_queue.put(994.4299)

    assert equal(packet_handler.surface_pressures, test_queue)
    assert packet_handler.surface_pressure == 992.43995

    packet_handler.handle_ros_single(ROS_SINGLE_THREE)
    test_queue.put(992.9600)

    assert equal(packet_handler.surface_pressures, test_queue)
    assert packet_handler.surface_pressure == 992.6133

    packet_handler.handle_ros_single(ROS_SINGLE_FOUR)
    test_queue.put(993.3699)

    assert equal(packet_handler.surface_pressures, test_queue)
    assert packet_handler.surface_pressure == 992.80245

    packet_handler.handle_ros_single(ROS_SINGLE_FIVE)
    test_queue.put(993.26)

    assert equal(packet_handler.surface_pressures, test_queue)
    assert packet_handler.surface_pressure == 992.89396

    # Test no more get added
    packet_handler.handle_ros_single(ROS_SINGLE_FIVE)
    assert equal(packet_handler.surface_pressures, test_queue)


def equal(q1: Queue[T], q2: Queue[T]) -> bool:
    if isinstance(q1.queue, deque) and isinstance(q2.queue, deque):
        return q1.queue == q2.queue
    return False