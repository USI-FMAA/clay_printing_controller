import sys

sys.path.append("..") # assign the parent folder as path
from loguru import logger

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

from clay_printing.hal.plc import PLC


# the connection detail for plc
CLIENT_ID = "5.151.68.134.1.1"  # PLC AMSNETID
CLIENT_IP = "169.254.200.9"  # PLC IP

# the connection detail for robot
ROBOT_HOST = "192.168.10.10"
ROBOT_HOST = "169.254.200.20"
# ROBOT_HOST = "localhost"
ROBOT_PORT = 30004
robot_running = True

# inputs and outputs we want to read from RTDE
config_filename = "control_loop_configuration.xml"
conf = rtde_config.ConfigFile(config_filename)

state_names, state_types = conf.get_recipe("state")
setp_names, setp_types = conf.get_recipe("setp")
watchdog_names, watchdog_types = conf.get_recipe("watchdog")

# connect to robot
try:
    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()
    
    logger.info('')
    logger.info("Robot Connected!")
except:
    logger.error("Robot is not connected")
    robot_running = False

try:
    # connect to PLC
    plc = PLC(netid=CLIENT_ID, ip=CLIENT_IP)
    plc.connect()
    # logger.info("PLC is connected and running!")
    plc_running = True
except:
    logger.error("PLC is not connected")
    plc_running = False


if robot_running:

    logger.info('')
    logger.info("Receiving these values from UR:")
    logger.info(state_names)
    logger.info('')
    logger.info("Allow Write for these variable to UR:")
    logger.info(setp_names)
    logger.info('')
    logger.info("Watchdog Names:")
    logger.info(watchdog_names)

    # setup recipes
    con.send_output_setup(state_names, state_types)
    setp = con.send_input_setup(setp_names, setp_types)
    watchdog = con.send_input_setup(watchdog_names, watchdog_types)

    # start data synchronization
    if not con.send_start():
        logger.warning("Could not connect to synchronization")
        sys.exit()


    initial_state = con.receive()
    initial_actual_digital_output_bits = initial_state.actual_digital_output_bits
    initial_output_int_register_1 = initial_state.output_int_register_1
    initial_output_int_register_2 = initial_state.output_int_register_2
    initial_target_q = initial_state.target_q

    # The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
    watchdog.input_int_register_0 = 1

    # control loop
    move_completed = True
    while robot_running:
        # receive the current state
        current_state = con.receive()

        if current_state is None:
            break

        # if plc is connected, report the state to robot
        # if plc.connect(False):
        #     forward = plc.read_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
        #     backward = plc.read_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)
        # else:
        #     forward = False
        #     backward = False
            
        # if robot_running:
        #     if forward: setp.input_int_register_3 = 1
        #     elif backward: setp.input_int_register_3 = 2
        #     else: setp.input_int_register_3 = 0 # off
        
        if current_state.safety_status_bits != 1:
            logger.error("Safety Triggered. Turning Pump OFF!")
            if plc.connect(report=False):
                        plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
                        plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)
                    


        # check if there is any change in register 1 > pump forward On/Off
        if initial_output_int_register_1 != current_state.output_int_register_1:

            # check so we dont jump from forward to backward and vice versa: in that case turn pump off and warn user
            if initial_output_int_register_1 == 1 and current_state.output_int_register_1 == 2 or \
                initial_output_int_register_1 == 2 and current_state.output_int_register_1 == 1:
                    logger.warning("Turning Pump OFF - Wrong change of direction:")
                    logger.warning("Going from Forward to Backward or vice versa")
                    if plc.connect(report=False):
                        plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
                        plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)
                    
                    break

            initial_output_int_register_1 = current_state.output_int_register_1

            if initial_output_int_register_1 == 0:
                logger.info("Pump OFF")
                if plc.connect(report=False):
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)

            if initial_output_int_register_1 == 1:
                logger.info("Pump Forward")
                if plc.connect(report=False):
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", True)
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)

            if initial_output_int_register_1 == 2:
                logger.info("Pump Backward")
                if plc.connect(report=False):
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
                    plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", True)
            

        # check if there is any change in register 2 > pump speed
        if initial_output_int_register_2 != current_state.output_int_register_2:
            initial_output_int_register_2 = current_state.output_int_register_2
            if initial_output_int_register_2 < 5:
                logger.warning(f"The speed is too Low: {initial_output_int_register_2} < Min Speed, 5 rpm")
            elif initial_output_int_register_2 > 50:
                logger.warning(f"The speed is too High: {initial_output_int_register_2} > Max Speed, 75 rpm")
            else:
                logger.info(f"Setting the speed to {initial_output_int_register_2}")
                if plc.connect(False):
                    plc.write_variables("GVL_LAP.n_Concrete_Pump_Set_Speed", initial_output_int_register_2)
        

        # kick watchdog
        con.send(watchdog)


if plc.connect():
    logger.warning("Disconnecting -> Setting Pump OFF")
    plc.write_variables("GVL_LAP.b_Concrete_Pump_Forward_On", False)
    plc.write_variables("GVL_LAP.b_Concrete_Pump_Backward_On", False)

con.send_pause()
con.disconnect()