import pytest

from bench.transport import SerialDevice, SimDevice


def pytest_addoption(parser):
    parser.addoption(
        "--port",
        default=None,
        help="Port série de la carte (ex. COM3 ou /dev/ttyACM0). Sans option : simulateur.",
    )


def pytest_report_header(config):
    port = config.getoption("--port")
    return f"Cible des tests : {'MATÉRIEL sur ' + port if port else 'SIMULATEUR (aucune carte)'}"


@pytest.fixture(scope="session")
def dut(request):
    port = request.config.getoption("--port")
    device = SerialDevice(port) if port else SimDevice()
    yield device
    device.close()


@pytest.fixture(autouse=True)
def idle(dut):
    dut.to_idle()
