from read_data import read_data
from read_data import station, year
from read_data import realStation

def writeAll():
    stations = read_data()
    rs = []
    for station_id in stations:
        c = realStation(stations[station_id])
        rs.append(c)
        c.build()
        c.write_data()
        
def main():
    writeAll()

if __name__ == "__main__":
    main()