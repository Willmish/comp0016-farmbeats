from pid import PID  #导入上面的PID算法
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline


def test_pid(P, I , D, L):

    pid = PID.PID(P, I, D)

    pid.SetPoint=1.1
    pid.setSampleTime(0.01)

    END = L
    feedback = 0
    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        feedback +=output #PID控制系统的函数
        time.sleep(0.01)
        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = spline(time_list, feedback_list, time_smooth)
    plt.figure(0)
    plt.grid(True)
    plt.plot(time_smooth, feedback_smooth,'b-')
    plt.plot(time_list, setpoint_list,'r')
    plt.xlim((0, L))
    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('PythonTEST PID--xiaomokuaipao',fontsize=15)

    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(1.2, 1, 0.001, L=100)