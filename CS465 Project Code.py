# CS465 Project
# David Tran

import requests
import pandas
import matplotlib.pyplot as matplot

def getCities(dataf):
    cities = []
    for i in range (0, len(dataf)):
        cities.append(dataf["city"][i])

    return set(cities)

def getCountries(dataf):
    countries = []
    for i in range (0, len(dataf)):
        countries.append(dataf["country"][i])

    return set(countries)
                      
def main():
    openaq = "https://api.openaq.org/v1/measurements"
    response = requests.get(openaq)

    #print(response.json())
    df = pandas.DataFrame.from_dict(pandas.io.json.json_normalize(response.json()["results"]), orient='columns')
    print(df)

    #countries = getCountries(df)
    #cities = getCities(df)

    cities_DFs = dict()
    for city, df_city in df.groupby("city"):
        cities_DFs[city] = df_city
    print(cities_DFs.keys())

    # group multiple cities on same graph (match country) ############ ?? 
    for city in cities_DFs.keys():
        cities_DFs[city].plot(kind="scatter", x="value", y="value", title=city)

    matplot.show()
    
    #df.plot()
    #matplot.show()

main()
