# CS465 Project
# OpenAQ API
# David Tran

import requests
import pandas
import matplotlib.pyplot as matplot
import datetime

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

def best_fit(X, Y):
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    m = numer / denum
    b = ybar - m * xbar

    print('Line of Best Fit:\ny = {:.2f}x + {:.2f}'.format(m, b))
    return b, m

def main():
    aq_param = "pm25" # particle matter 2.5µm
    city_input = "Bakersfield"
    openaq = "https://api.openaq.org/v1/measurements?city="+city_input+"&country=US&date_from=2019-11-01&date_to=2019-11-30&order_by=date&limit=10000&parameter="+aq_param
    response = requests.get(openaq)

    #print(response.json())
    df = pandas.DataFrame.from_dict(pandas.io.json.json_normalize(response.json()["results"]), orient='columns')
    print(df)

    #countries = getCountries(df)
    #cities = getCities(df)

    cities_DFs = dict()
    for city, df_city in df.groupby("city"):
        cities_DFs[city] = df_city
    if 'N/A' in cities_DFs: # error
        cities_DFs.pop('N/A', None)
    print(cities_DFs.keys())

    for city in cities_DFs.keys():
        timeArr = []
        valueArr = []
        country = ""
        parameter = ""
        for i in range (0, len(cities_DFs[city])):
            #print (cities_DFs[city].iloc[i])
            #print (cities_DFs[city].iloc[i]["date.utc"])
            country = cities_DFs[city].iloc[i]["country"]
            parameter = cities_DFs[city].iloc[i]["parameter"]
            cTime = cities_DFs[city].iloc[i]["date.utc"].replace("-","").replace(":","").replace("T","").replace("Z","")
            #print(cTime)
            cTimeSimp = cTime[6:8]
            #print(cTimeSimp)
            cVal = cities_DFs[city].iloc[i]["value"]
            timeArr.append(int(cTimeSimp))
            valueArr.append(int(cVal))     
        matplot.figure(figsize=(15, 5))
        a, b = best_fit(timeArr, valueArr)
        matplot.scatter(timeArr, valueArr)
        yfit = [a + b * xi for xi in timeArr]
        matplot.plot(timeArr, yfit, color="red")
        matplot.title(city + ", " + country)
        matplot.xlabel("day (Nov 2019)")
        #matplot.xlim(0, 1000)
        matplot.ylabel("value (µg/m³), " + parameter)
        #matplot.ylim(0, 1000)

    matplot.show()

main()
