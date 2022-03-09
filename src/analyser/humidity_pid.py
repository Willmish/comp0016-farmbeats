from pid import PID
import time
import matplotlib.pyplot as plt


def humidity_pid_control(p, i, d, temprature, clock):
    # P = 1.2
    # I = 1
    # D = 0.001
    pid = PID(p, i, d)
    pid.SetPoint = temprature
    feedback = 0
    feedback_list = []
    time_list = []
    # target_list = []
    plt.figure(0)

    for i in range(1, 100):
        pid.update(feedback)
        output = pid.output
        print("output: ")

        plt.plot(output)
        feedback += output
        time.sleep(clock)
        plt.plot(i, feedback, marker=".")
        print(feedback)
        print("  ")
        # print(time)
        # target_list.append(temprature)
        feedback_list.append(feedback)
        time_list.append(i)

    plt.grid(True)
    plt.xlim((0, 100))
    plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
    plt.xlabel("time (s)")
    plt.ylabel("PID (PV)")
    plt.title("Humidity test", fontsize=15)
    plt.grid(True)
    plt.show()


humidity_pid_control(1.2, 0.5, 0.001, 22, 1)
