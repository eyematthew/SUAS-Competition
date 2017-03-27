from dronekit import connect, VehicleMode
import socket
import multiprocessing
from logger import *
from time import sleep
from interop_client import InteropClientConverter
from static_math import *
from sda_converter import SDAConverter
from converter_functions import *
from SDA import *

TK1_ADDRESS = ('IP', 9001)

UAV_CONNECTION_STRING = "127.0.0.1:14550"

INTEROP_URL = "http://10.10.130.2:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "2429875295"

MSL = 430
MIN_REL_FLYING_ALT = 100
MAX_REL_FLYING_ALT = 750

def log_vehicle_state(vehicle, logger_name):
    """
    Log a vehicle's state
    """
    log(logger_name, " Get all vehicle attribute values:")
    log(logger_name, " Autopilot Firmware version: %s" % vehicle.version)
    log(logger_name, "   Major version number: %s" % vehicle.version.major)
    log(logger_name, "   Minor version number: %s" % vehicle.version.minor)
    log(logger_name, "   Patch version number: %s" % vehicle.version.patch)
    log(logger_name, "   Release type: %s" % vehicle.version.release_type())
    log(logger_name, "   Release version: %s" % vehicle.version.release_version())
    log(logger_name, "   Stable release?: %s" % vehicle.version.is_stable())
    log(logger_name, " Autopilot capabilities")
    log(logger_name, "   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
    log(logger_name, "   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
    log(logger_name, "   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
    log(logger_name, "   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
    log(logger_name, "   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
    log(logger_name, "   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
    log(logger_name, "   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
    log(logger_name, "   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
    log(logger_name, "   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
    log(logger_name, "   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
    log(logger_name, "   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
    log(logger_name, "   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
    log(logger_name, "   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
    log(logger_name, "   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
    log(logger_name, " Global Location: %s" % vehicle.location.global_frame)
    log(logger_name, " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    log(logger_name, " Local Location: %s" % vehicle.location.local_frame)
    log(logger_name, " Attitude: %s" % vehicle.attitude)
    log(logger_name, " Velocity: %s" % vehicle.velocity)
    log(logger_name, " GPS: %s" % vehicle.gps_0)
    log(logger_name, " Gimbal status: %s" % vehicle.gimbal)
    log(logger_name, " Battery: %s" % vehicle.battery)
    log(logger_name, " EKF OK?: %s" % vehicle.ekf_ok)
    log(logger_name, " Last Heartbeat: %s" % vehicle.last_heartbeat)
    log(logger_name, " Rangefinder: %s" % vehicle.rangefinder)
    log(logger_name, " Rangefinder distance: %s" % vehicle.rangefinder.distance)
    log(logger_name, " Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    log(logger_name, " Heading: %s" % vehicle.heading)
    log(logger_name, " Is Armable?: %s" % vehicle.is_armable)
    log(logger_name, " System status: %s" % vehicle.system_status.state)
    log(logger_name, " Groundspeed: %s" % vehicle.groundspeed)    # settable
    log(logger_name, " Airspeed: %s" % vehicle.airspeed)    # settable
    log(logger_name, " Mode: %s" % vehicle.mode.name)    # settable
    log(logger_name, " Armed: %s" % vehicle.armed)    # settable

def target_listener(logger_queue, configurer, received_targets_array):
	"""
	Listen for targets sent from the TK1
	"""
    configurer(logger_queue)
	name = multiprocessing.current_process().name

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.bind(TK1_ADDRESS)
	#sock.listen(1)
	log(name, "Waiting for a connection to the TK1...")
	#connection, client_address = sock.accept()
	log(name, "Connected to TK1")

	while True:
		sleep(0.5)

if __name__ == '__main__':
	#interop_server_client = InteropClientConverter(MSL, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

	logger_queue = multiprocessing.Queue(-1)
	logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
	logger_listener_process.start()

    manager = multiprocessing.Manager()
    received_targets = manager.list()
    # target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_listener_configurer, received_targets))
    # target_listener_process.start()

    logger_listener_configurer(configurer)
    name = multiprocessing.current_process().name

    log(name, "Connecting to UAV on: %s" % UAV_CONNECTION_STRING)
    vehicle = connect(UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(name, "Connected to UAV on: %s" % UAV_CONNECTION_STRING)
    log_vehicle_state(vehicle, name)

	log(name, "Downloading waypoints from UAV on: %s" % UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    log(name, "Waiting for UAV to be armable")
	while not vehicle.is_armable:
        sleep(0.05)
    log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle))
    sda_converter.set_waypoints(waypoints)

    try:
    	while True:
            current_location = get_location(vehicle)

    		#interop_server_client.post_telemetry(current_location)
    		#stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    		#obstacle_map.reset_obstacles()
            # TODO: Convert obstacles to Location objects
    		#for stationary_obstacle in stationary_obstacles:
    		#	obstacle_map.add_obstacle(stationary_obstacle)

            if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_reached_current_waypoint():
                vehicle.mode = VehicleMode("AUTO")

            sda_converter.set_uav_position(current_location)
            obj_avoid_coordinates = sda_converter.avoid_obstacles()

    		if obj_avoid_coordinates:
    			log("root", "Avoiding obstacles...")
                vehicle.simple_goto(obj_avoid_coordinates)
    except:
        vehicle.close()
