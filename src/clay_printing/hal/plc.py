"""Hardware abstraction layer for PLC communication."""
import pyads
from pydantic import BaseModel, Field
from typing import List, Any
from threading import Lock

class PLC(BaseModel):
    """Hardware abstraction class for reading and writing variables from and to PLC."""

    netid: str = Field(..., description="Net ID of the PLC")
    ip: str = Field(..., description="IP address of the PLC")

    connection: Any = Field(default=None, description="PLC connection object")
    lock_dict: Lock = Field(default_factory=Lock, description="Lock for dictionary operations")
    lock_ads: Lock = Field(default_factory=Lock, description="Lock for ADS communication")

    def __init__(self, **data):
        super().__init__(**data)
        self.connection = pyads.Connection(self.netid, pyads.PORT_TC3PLC1)

    def close(self):
        """Close the connection to the PLC."""
        if self.connection and self.connection.is_open:
            self.connection.close()
        print("PLC connection closed")

    def connect(self) -> bool:
        """Connect to the PLC."""
        with self.lock_ads:
            if not self.connection.is_open:
                self.connection.open()
            try:
                self.connection.read_device_info()
            except pyads.ADSError as e:
                print(f"Error: {e}")
                return False
            else:
                print(f"Connection: {self.connection.is_open}")
                return True
    def read_variables(self):
        """Reads all structs from PLC and stores inside class."""
        if not self.connect():
            raise AdsConnectionError(
                "Could not read variable from PLC, PLC connection failed."
            )
        with self.lock_ads:
            raise NotImplementedError

    def write_variables(self):
        """Writes all variables that have been set."""
        if not self.connect():
            raise AdsConnectionError(
                "Could not read variable from PLC, PLC connection failed."
            )
        with self.lock_ads:
            raise NotImplementedError

    class Config:
        arbitrary_types_allowed = True  # Allow non-Pydantic types (e.g., pyads.Connection, Lock)


class AdsConnectionError(Exception):
    pass