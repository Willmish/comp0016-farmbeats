from traceback import format_tb
from pid import PID
import time

def humidity_pid_control(P, I, D, temprature, clock):
    #P = 1.2
    #I = 1
    #D = 0.001
    pid = PID(P, I, D)
    pid.SetPoint = temprature
    feedback = 0
    feedback_list = []
    time_list = []

    for i in range(1, 100):
        pid.update(feedback)
        output = pid.output
        print("output: ")
        print(output)
        feedback += output
        time.sleep(clock)
        print(feedback)
        print("  ")
        #print(time)
        feedback_list.append(feedback)
        time_list.append(i)

humidity_pid_control(1.2, 1, 0.001, 22, 1)
