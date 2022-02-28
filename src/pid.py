import time


class PID:
    def __init__(self, p, i, d):
        self.Kp = p
        self.Ki = i
        self.Kd = d
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.clear()

    def clear(self):
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.output = 0.0

    def update(self, feedback_value):
        error = self.SetPoint - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * error  # 比例 P
            self.ITerm += error * delta_time  # 积分 I
            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time  # 微分 D
            self.last_time = self.current_time
            self.last_error = error
            self.output = (
                self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
            )

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time
