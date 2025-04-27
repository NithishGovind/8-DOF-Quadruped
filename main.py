# main.py

import servo_controller as sc
import time

def get_angles_from_user():
    print("\nEnter 8 angles (0 to 180 degrees), separated by spaces:")
    user_input = input("Angles: ")
    try:
        angles = list(map(int, user_input.strip().split()))
        if len(angles) != 8:
            raise ValueError
        # Clamp values between 0 and 180
        angles = [max(0, min(180, angle)) for angle in angles]
        return angles
    except:
        print("Invalid input. Please enter exactly 8 integer values between 0 and 180.")
        return None

if __name__ == "__main__":
    try:
        sc.initialize_serial_connection()

        while True:
            angles = None
            while angles is None:
                angles = get_angles_from_user()

            sc.set_pose(angles, delay_time=1)

            cont = input("\nSend another set? (y/n): ").strip().lower()
            if cont != 'y':
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        sc.close_serial_connection()
