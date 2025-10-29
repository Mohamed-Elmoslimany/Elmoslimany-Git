import time
import numpy as np
import Trace_GUI2 as tg2


# WHEEL_DIAMETER = 2
GEAR_DIAMETER = 10 / np.pi
ARM_1 = 10
ARM_2 = 1.5
SLIDER_OFSET = 1
wheel_angle = 0
steering_angle = [0, (-180, 180), 0.1]
displacement = 0
angle = 0
R = 0
k = 0

def analysis():
    global wheel_angle, GEAR_DIAMETER, displacement, angle, R, k, ARM_1, ARM_2, SLIDER_OFSET
    
    GEAR_DIAMETER = float(GEAR_DIAMETER)
    ARM_1 = float(ARM_1)
    ARM_2 = float(ARM_2)
    SLIDER_OFSET = float(SLIDER_OFSET)

    displacement = (steering_angle[0] * np.pi / 180) * GEAR_DIAMETER
    if GEAR_DIAMETER > 10 / np.pi: GEAR_DIAMETER = 10 / np.pi
    try:
        angle = np.arctan2(SLIDER_OFSET, displacement)
        R = np.sqrt(SLIDER_OFSET ** 2 + displacement ** 2)
        k = (ARM_1 ** 2 + SLIDER_OFSET ** 2 + ARM_2 ** 2 + displacement ** 2) / (2 * ARM_1)
        wheel_angle = np.rad2deg(np.arcsin(R/k) - angle)
    except:
        pass

if __name__ == "__main__":
    trace_dict = {
        "displacement": displacement,
        "wheel_angle": wheel_angle,
        "angle": angle,
        "R": R,
        "k": k,

    }

    control_dict = {
        "GEAR_DIAMETER": GEAR_DIAMETER,
        "ARM_1": ARM_1,
        "ARM_2": ARM_2,
        "SLIDER_OFSET": SLIDER_OFSET
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