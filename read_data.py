from dataclasses import dataclass
from typing import List


@dataclass
class year:# Klasse zum Speichern von Daten eines Jahres.
    year:int
    months:List[float]


@dataclass
class station:# Klasse zum Speichern und verwalten von Daten bezülich einer Station. 
    station_id:int
    years:List[year]


def read_data(path):# Einlesen der Daten
    stations = dict()#Dict
    with open(path) as f: # öffnen der Datei.
        for line in f: # für jede Zeile.
            data = line.replace("\n", "").split(",") #csv string zu einer liste umwandeln (nach Kommata trennen und newline entfernen)
            if not data[0]=="Station": #Nach dem Header
                y=year(data[1], list(map(lambda a:float(a),data[2:]))) #Das Jahrobjekt initialisieren.
                if data[0] in stations.keys(): # Wenn die Station schon erfasst wurde.
                    stations[data[0]].years.append(y) #Bei der relevanten Station das Jahrobjekt der Liste hinzufügen. 
                else: #Sonst
                    stations[data[0]] = station(data[0], [y]) #Neues Stationsobjekt intiallisieren und im Dict speichern.  
    return stations #Dict zurückgeben


class realStation:
    def __init__(self, s:station):
        #Initialisieren der  Variablen
        self.mon_avg=[[] for i in range(12)]  
        self.season_avg = [0 for i in range(4)]
        self.ann_avg=0  
        self.dmon=None
        self.dann=None
        self.id = int(s.station_id)
        self.data = s.years
        self.is_acceptable = len(self.data) >= 20
        self.mon_avg:List[float]
        self.data.sort(key=lambda a:int(a.year))
        self.data[0].months = [-9999] + self.data[0].months
        for i in range(1, len(self.data)):
            self.data[i].months = self.data[i-1].months[-1:] + self.data[i].months #Den Dez des (i-1) Jahres zu dem (i)ten Jahr tun.

    def step1(self):
        #Der erste Schritt
        mon_count = [0 for i in range(12)]
        if self.is_acceptable: 
            for current_year in self.data:
                for i in range(len(self.mon_avg)):
                    if current_year.months[i+1] != -9999:
                        self.mon_avg[i].append(current_year.months[i+1])
                        mon_count[i] += 1
            for i in range(len(self.mon_avg)):
                   self.mon_avg[i] = sum(self.mon_avg[i]) / mon_count[i]
            print(f"{self.id}: step1 finished")
        else:
            print(f"{self.id}: step1 failed")

    def step2(self):
        #Der zweite Schritt
        seas1 = self.mon_avg[0:2] + self.mon_avg[-1:]
        seas2 = self.mon_avg[2:5]
        seas3 = self.mon_avg[5:8]
        seas4 = self.mon_avg[8:11]
        self.season_avg = [sum(seas1)/len(seas1), sum(seas2)/len(seas2), sum(seas3)/len(seas3), sum(seas4)/len(seas4)] 
        print(f"{self.id}: step2 finished")

    def step3(self):
        #Der dritte Schritt
        self.ann_avg =sum(self.season_avg)/4
        print(f"{self.id}: step3 finished")

    def step4(self):
        #Der vierte Schritt
        self.dmon=self.data.copy()
        for year in self.dmon:
            for i in range(len(year.months)):
                if not year.months[i] == -9999:
                    year.months[i]=year.months[i]-self.mon_avg[(11+i)%12]
        print(f"{self.id}: step4 finished")
    
    def step5(self):
        #Der fünfte Schritt
        self.dseas=[[[] for i in range(4)] for year in self.dmon]
        for i in range(len(self.dmon)):
            cyear = self.dmon[i]
            for j in range(len(cyear.months)-1):
                if not cyear.months[j] == -9999:
                    self.dseas[i][j//3].append(cyear.months[j])
            for g in range(4):
                if len(self.dseas[i][g])>1:
                    self.dseas[i][g] = sum(self.dseas[i][g])/len(self.dseas[i][g])
                else:
                    self.dseas[i][g] = -9999
        print(f"{self.id}: step5 finished")

    def step6(self):
        #Der sechste Schritt
        self.dann = [-9999 for i in range(len(self.dseas))]
        for i in range(len(self.dseas)):
            cy = self.dseas[i]
            cy = list(filter(lambda x: not x == -9999, cy))
            if len(cy) > 2:
                self.dann[i] = sum(cy)/len(cy) 
            else:
                self.dann[i] = -9999
        print(f"{self.id}: step6 finished")

    def step7(self):
        #Der siebte Schritt
        self.seas = [[0 for i in range(4)] for i in range(len(self.dseas))]
        self.ann = [-9999 for i in range(len(self.dann))]
        for year in range(len(self.dseas)):
            for season in range(4):
                if self.dseas[year][season] == -9999:
                    self.seas[year][season] = -9999
                else:
                    self.seas[year][season] = self.season_avg[season] + self.dseas[year][season]
            if self.dann[year] == -9999:
                self.ann[year] = -9999
            else:
                self.ann[year] = self.ann_avg + self.dann[year]
        print(f"{self.id}: step7 finished")
    
    def build(self):
        #Alle Schritte
        if self.is_acceptable:
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
            self.step7()
        else:
            print(f"Bad Station ignored:{self.id}")
        print("---------------------------------------------------------------------")


    def write_data(self):
        with open("Data/" + str(self.id) + ".csv", "w+") as f:
            f.write("year,DJF,MAM,JJA,SON,ANN\n")
            for index, year in enumerate(self.data):
                seas = [round(self.seas[index][0]/100,2), round(self.seas[index][1]/100,2), round(self.seas[index][3]/100,2), round(self.seas[index][3]/100,2), round(self.ann[index]/100, 2)]
                for i in range(5):
                    if seas[i] == -99.99:
                        seas[i] = "NaN"

                f.write(f"{year.year},{seas[0]},{seas[1]},{seas[2]},{seas[3]},{seas[4]}\n")
      