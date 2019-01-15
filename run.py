from read_data import read_data
from read_data import station, year
from read_data import realStation
import sys
import os

def writeAll(path):
    if not os.path.isdir("./Data"):
        os.mkdir("./Data")
    if not os.path.isfile(path):
        path = "real_data.csv"
    stations = read_data(path)
    rs = []
    for station_id in stations:
        c = realStation(stations[station_id])
        rs.append(c)
        c.build()
        c.write_data()

if __name__ == "__main__":
    writeAll(sys.argv[1])