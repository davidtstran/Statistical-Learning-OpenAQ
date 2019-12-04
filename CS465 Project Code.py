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
    
    b = (sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar) / (sum([xi**2 for xi in X]) - n * xbar**2)
    a = ybar - b * xbar

    print(b, a)
    print('best fit line:\ny = {:.2f}x + {:.2f}'.format(b, a))

    return a, b

def c_graph(c):
    city_input = c
    aq_param = "pm25" # particle matter 2.5µm
    params = "&date_from=2019-11-01&date_to=2019-11-30&order_by=date&sort=asc&limit=10000&format=json"
    openaq = "https://api.openaq.org/v1/measurements?city="+city_input+"&parameter="+aq_param+params
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
            cTimeSimp = cTime[6:10]
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
        matplot.xlabel("day (Nov 2019) [DDHH]")
        #matplot.xlim(0, 1000)
        matplot.ylabel("value (µg/m³), " + parameter)
        matplot.ylim(0, 100)

def main():
    c_graph("Kansas City")
    c_graph("Fairbanks")
    c_graph("Bakersfield")
    c_graph("Wilmington")
    c_graph("Honolulu")

    matplot.show()
main()
