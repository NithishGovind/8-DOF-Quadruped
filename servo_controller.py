import serial
import time
import serial.tools.list_ports

# Global serial object
ser = None


def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None


def initialize_serial_connection():
    global ser
    arduino_port = find_arduino_port()

    if arduino_port is None:
        raise Exception("Arduino not found. Please check the connection.")

    print(f"Found Arduino on port: {arduino_port}")
    ser = serial.Serial(arduino_port, 9600, timeout=1)
    time.sleep(2)  # Allow Arduino reset


def move_servo(servo_num, angle):
    global ser
    if ser is None:
        raise Exception("Serial connection not initialized.")

    command = f"{servo_num},{angle}\n"
    ser.write(command.encode())
    print(f"Sent: {command.strip()}")
    time.sleep(0.05)  # Small delay


def set_pose(angles, delay_time=0.5):
    """
    Takes a list of 8 angles and sends them to the servos.
    Handles reversing where necessary.
    """
    if len(angles) != 8:
        raise ValueError("Exactly 8 angles must be provided.")

    for i in range(8):
        if i == 4 or i == 6:
            physical_angle = 180 - angles[i]
        elif i == 5 or i == 7:
            physical_angle = 100 - angles[i]
        else:
            physical_angle = angles[i]

        move_servo(i, physical_angle)

    time.sleep(delay_time)


def close_serial_connection():
    global ser
    if ser is not None:
        ser.close()
        print("Serial connection closed.")
