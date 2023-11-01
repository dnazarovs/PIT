class EventDto:

    def __init__(self, lecture, t_start, t_end):
        self.lecture = lecture
        self.t_start = t_start
        self.t_end = t_end

    def to_dict(self):
        return {
            'lecture': self.lecture,
            't_start': self.t_start,
            't_end': self.t_end
        }
