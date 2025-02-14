from .hal.plc import PLC
from datetime import datetime

# =================================================================================
"""Global value"""

#TODO: change it
CLIENT_ID = "5.151.68.134.1.1"  # PLC AMSNETID
CLIENT_IP = "169.254.200.9" # PLC IP
NOW_DATE = datetime.now().date().strftime("%Y%m%d")  # Date

# =================================================================================

process_running = input("Do you want to start the process? (y/n): ")
process_stop = input("Do you want to stop the process? (y/n): ")

def main():
  """Main function to run the process."""

  plc = PLC(netid=CLIENT_ID, ip=CLIENT_IP)
  plc.connect()

  while process_running:

    if not process_running or process_stop:
      print("The process is not running.")
      plc.close()
      break


if __name__ == '__main__':
    main()
    pass