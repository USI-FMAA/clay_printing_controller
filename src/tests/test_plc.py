from unittest.mock import patch

import pyads
import pytest

from clay_printing.hal.plc import PLC


@pytest.fixture
def plc():
  netid = "1.2.3.4.5.6"
  ip = "192.168.1.1"
  return PLC(netid=netid, ip=ip)


@patch("clay_printing.hal.plc.pyads.Connection")
def test_connect_success(MockConnection, plc):
  """Test successful connection to the PLC."""
  print("Setting up mock connection...")
  mock_conn = MockConnection.return_value
  mock_conn.is_open = False
  mock_conn.read_device_info.return_value = None
  mock_conn.open.side_effect = lambda: setattr(mock_conn, "is_open", True)

  print("Before calling plc.connect()")
  result = plc.connect()
  print("After calling plc.connect()")

  mock_conn.open.assert_called_once()
  mock_conn.read_device_info.assert_called_once()
  assert result is True


@patch("clay_printing.hal.plc.pyads.Connection")
def test_connect_failure(MockConnection, plc):
  mock_conn = MockConnection.return_value
  mock_conn.is_open = False
  mock_conn.read_device_info.side_effect = pyads.ADSError

  result = plc.connect()

  mock_conn.open.assert_called_once()
  mock_conn.read_device_info.assert_called_once()
  assert result is False


#
#
# @patch("your_module.pyads.Connection")  # Mock pyads.Connection
# def test_read_variables_success(MockConnection, plc):
#   mock_conn = MockConnection.return_value
#   mock_conn.is_open = True
#   mock_conn.read_by_name.return_value = "value"
#
#   value = plc.read_variables("variable_name")
#
#   mock_conn.read_by_name.assert_called_once_with("variable_name")
#   assert value is None  # The method returns None but logs the value
#
#
# @patch("your_module.pyads.Connection")  # Mock pyads.Connection
# def test_write_variables_success(MockConnection, plc):
#   mock_conn = MockConnection.return_value
#   mock_conn.is_open = True
#
#   plc.write_variables("variable_name", "value")
#
#   mock_conn.write_by_name.assert_called_once_with("variable_name", "value")
#
#
# @patch("your_module.pyads.Connection")  # Mock pyads.Connection
# def test_read_variables_connection_error(MockConnection, plc):
#   mock_conn = MockConnection.return_value
#   mock_conn.is_open = False
#
#   with pytest.raises(AdsConnectionError):
#     plc.read_variables("variable_name")
#
#
# @patch("your_module.pyads.Connection")  # Mock pyads.Connection
# def test_write_variables_connection_error(MockConnection, plc):
#   mock_conn = MockConnection.return_value
#   mock_conn.is_open = False
#
#   with pytest.raises(AdsConnectionError):
#     plc.write_variables("variable_name", "value")
