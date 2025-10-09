import Trace_GUI as tg
import time

if __name__ == '__main__':
    # global flag, label1, label2, label3
    label1 = time.time()
    label2 = 123
    label3 = "My name is Ahmed"
    my_dict = {
        "label1": label1,
        "label2": label2,
        "label3": label3,
        "flag": tg.flag,
        "test_1": time.time(),
        "test_2": "time.time()"
    }
    control = {
        "Value_1": 1,
        "Value_2": 2,
        "Value_3": 3,
        "Value_4": 4,
        "Value_5": 5,
        "Value_6": 6,
        "Value_7": 7,
        "Value_8": 8
    }
    tg.create_gui(caller_globals=globals(), tracked_dict=my_dict, controled_dict=control)
    # print(tg.flag)
    while tg.flag:
        label2 += 1  # Modify the global variable directly
        print(label2)  # Prints the updated label2
        time.sleep(1)