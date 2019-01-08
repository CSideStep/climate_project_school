from  read_data import station
class realStation:
    mon_avg=[0 for i in range(12)]
    def __init__(self, s:station):
        self.id = int(s.station_id)
        self.data = s.years
        self.is_acceptable = len(self.data) >= 20

    def build_mon_avg(self):
        if self.is_acceptable: 
            for current_year in self.data:
                for i in range(len(self.mon_avg)):
                    self.mon_avg[i] += current_year[i]
            self.mon_avg = list(map(lambda a: a/len(self.data), self.mon_avg))
        else:
            print("Failed")
