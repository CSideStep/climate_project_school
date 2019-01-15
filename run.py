from read_data import read_data
from read_data import station, year
from read_data import realStation
import sys
import os

def writeAll(path):
    if not os.path.isdir("./Data"):#Wenn der Ordner Data in dem aktuellen Verzeichniss nicht existiert:
        os.mkdir("./Data")#Eine Ordner Data im aktuellen Verzeichniss erstellen
    if not os.path.isfile(path):#Wenn hinter dem übergebenen Dateipfad keine Datei ist:
        path = "real_data.csv"#standard Datei benutzen
    stations = read_data(path)#Einlesen der Daten und erzeugen von Objekten, welche die einzelnen Stationen darstellen 
    rs = []#realStation Objekte werden in dieser Liste gesammelt   
    for station_id in stations:#für jede Station in der Liste von Stationen
        c = realStation(stations[station_id]) #realStation-Objekt erstellen
        rs.append(c) #das Objekt der Liste hinzufügen
        c.build()#die erforderlichen Schritte ausführen
        c.write_data()#Das Ergenis aufschreiben

if __name__ == "__main__":
    writeAll(sys.argv[1]) #Benutzung: python run.py <filename.csv>