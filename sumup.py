from read_data import realStation
def ann_time_series(stations):
    years = dict()
    for s in stations:
        for index, year in enumerate(s.data):
            if year.year in years.keys():
                years[year.year].append(s.ann[index]/100)
            else:
                years[year.year] = []
                years[year.year].append(s.ann[index]/100)
    for key in years.keys():
        usefullData = list(filter(lambda x: not x == -99.99, years[key]))
        years[key] = [sum(usefullData)/len(usefullData), len(usefullData)]
    return years