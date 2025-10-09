import time
import numpy as np
import Trace_GUI_2 as tg2


# WHEEL_DIAMETER = 2
GEAR_DIAMETER = 6 / np.pi
ARM = 5
wheel_angle = 0
steering_angle = [0, (-90, 90), 0.1]
displacement = 0

def analysis():
    global wheel_angle, GEAR_DIAMETER, displacement
    
    GEAR_DIAMETER = float(GEAR_DIAMETER)
    displacement = (steering_angle[0] * np.pi / 180) * GEAR_DIAMETER
    if GEAR_DIAMETER > 10 / np.pi: GEAR_DIAMETER = 10 / np.pi
    wheel_angle = np.arcsin(displacement / ARM) * 180 / np.pi

if __name__ == "__main__":
    trace_dict = {
        "displacement": displacement,
        "wheel_angle": wheel_angle,
    }

    control_dict = {
        "GEAR_DIAMETER": GEAR_DIAMETER
    }

    slider_dict = {
        "steering_angle": steering_angle
    }

    tg2.create_gui(caller_globals=globals(), tracked_dict=trace_dict, controled_dict=control_dict, slider=slider_dict)

    while tg2.flag:
        # print("Running...")
        analysis()
        # print(displacement, steering_angle[0])
        # time.sleep(1)