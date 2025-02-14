from datetime import datetime

from loguru import logger

from .hal.plc import PLC

# =================================================================================
"""Global value"""

CLIENT_ID = "5.151.68.134.1.1"  # PLC AMSNETID
CLIENT_IP = "169.254.200.9"  # PLC IP
NOW_DATE = datetime.now().date().strftime("%Y%m%d")  # Date

# =================================================================================

# process_running = input("Do you want to start the process? (y/n): ")
# process_stop = input("Do you want to stop the process? (y/n): ")


def main():
  """Main function to run the process."""

  plc = PLC(netid=CLIENT_ID, ip=CLIENT_IP)
  plc.connect()
  logger.info("The process is running.")
  logger.info(f"Data:{NOW_DATE}")

  plc.read_variables("GVL_LAP.f_CP1_status_torque")
  # plc.write_variables("GVL_LAP.n_Concrete_Pump_Set_Speed", 30)

  plc.close()
  logger.info("the process closed.")

# TODO: Implement the process to run the process.
# while process_running:
#   if not process_running or process_stop:
#     Logger.info("The process is not running.")
#     plc.close()
#     break


if __name__ == "__main__":
  main()
