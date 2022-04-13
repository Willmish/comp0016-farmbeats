import random
from time import sleep
from tools.pid import PID


setvalue = 55
sampletime = 1
tolerant = 5


def test_pid():
    END = 30
    p_parameter = 1.2
    i_parameter = 0.5
    d_parameter = 0.001
    pid = PID(p_parameter, i_parameter, d_parameter)
    # pid.setSampleTime(sampletime)
    pid.SetPoint = setvalue
    feedback = 0
    feedback_list = []
    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        feedback += output
        sleep(sampletime)
        feedback_list.append(feedback)
        if (i > tolerant):
            assert setvalue + 1 > feedback > setvalue - 1
    print(feedback_list)


def test_pid_sudden_change():
    END = 30
    EMERG = 15
    p_parameter = 1.2
    i_parameter = 0.5
    d_parameter = 0.001
    pid = PID(p_parameter, i_parameter, d_parameter)
    # pid.setSampleTime(sampletime)
    pid.SetPoint = setvalue
    feedback = 0
    feedback_list = []
    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        feedback += output
        sleep(sampletime)
        feedback_list.append(feedback)
        if i == EMERG:
            feedback = random.randint(0, 100)
        if (i > tolerant + EMERG):
            assert setvalue + 1 > feedback > setvalue - 1
    print(feedback_list)


def test_pid_multirange():
    for j in range(1, 50):
        END = 30
        p_parameter = 1.2
        i_parameter = 0.5
        d_parameter = 0.001
        pid = PID(p_parameter, i_parameter, d_parameter)
        # pid.setSampleTime(sampletime)
        number = random.randint(0,100)
        pid.SetPoint = number
        feedback = 0
        feedback_list = []
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            feedback += output
            sleep(0.1)
            feedback_list.append(feedback)
            if (i > tolerant):
                assert number + 1 > feedback > number - 1
        print(feedback_list)
