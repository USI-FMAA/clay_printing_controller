"""Hardware abstraction layer for PLC communication."""

from threading import Lock
from typing import Any

import pyads
from loguru import logger
from pydantic import BaseModel, Field


class PLC(BaseModel):
  """Hardware abstraction class for reading and writing variables from and to PLC."""

  netid: str = Field(..., description="Net ID of the PLC")
  ip: str = Field(..., description="IP address of the PLC")

  connection: Any = Field(default=None, description="PLC connection object")
  lock_dict: Lock = Field(default_factory=Lock, description="Lock for dictionary operations")
  lock_ads: Lock = Field(default_factory=Lock, description="Lock for ADS communication")

  def __init__(self, **data):
    super().__init__(**data)
    self.connection = pyads.Connection(self.netid, pyads.PORT_TC3PLC1, self.ip)

  def connect(self) -> bool:
    """Connect to the PLC."""
    if not self.connection.is_open:
      self.connection.open()
    try:
      self.connection.read_device_info()
    except pyads.ADSError as e:
      logger.error(f"Error: {e}")
      return False
    else:
      logger.info(f"Connection: {self.connection.is_open}")
      return True

  def close(self):
    """Close the connection to the PLC."""
    if self.connection and self.connection.is_open:
      self.connection.close()
    logger.info("PLC connection closed")

  def read_variables(self, variable: str) -> None:
    """Reads variable from PLC by given variable name.

    Args:
        variables: str

    Returns:
        Any: boolean or string

    Raises:
        AdsConnectionError: [TODO:throw]
    """
    if not self.connect():
      raise AdsConnectionError("Could not read variable from PLC, PLC connection failed.")

    try:
      value = self.connection.read_by_name(variable)
      logger.info(f"Reading {variable}: {value}")
      return None

    except KeyError as e:
      logger.error(f"Error: {e}")
      return None

  def write_variables(self, variable: str, value: Any) -> None:
    """Writes variable to PLC by given variable name.

    Args:
        variable: str
        value: bollean or string

    Returns:
        None

    Raises:
        AdsConnectionError:
    """
    if not self.connect():
      raise AdsConnectionError("Could not read variable from PLC, PLC connection failed.")
    try:
      self.connection.write_by_name(variable, value)
      logger.info(f"writing {variable}: {value} to PLC")
      return None
    except KeyError as e:
      logger.error(f"Error: {e}")
      return None

  class Config:
    arbitrary_types_allowed = True  # Allow non-Pydantic types (e.g., pyads.Connection, Lock)


class AdsConnectionError(Exception):
  pass
