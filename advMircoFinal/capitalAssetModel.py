import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import math
import numpy as np

# function to calculate covariance of two variables


def covariance(x, y):
    meanX = sum(x)/float(len(x))
    meanY = sum(y)/float(len(y))
    sub_x = [i - meanX for i in x]
    sub_y = [i - meanY for i in y]
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    denominator = len(x)-1
    cov = numerator/denominator
    return cov

# calculates variance


def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n
    return variance


# reads in relevent data
dataSpy = pd.read_csv(r"./advMircoEcon/advMircoFinal/dataSpy.csv")
qDemandRaw = pd.read_excel(
    r"./minesmineralmodel/outputs/two_degree/cleanDemandPandas.xlsx")
historicalMineralPrices = pd.read_csv(r"./advMircoEcon/pricesHistorical.csv")

# Known values
quanityNickel2019 = qDemandRaw.iloc[18, 12]
quanityCopper2019 = qDemandRaw.iloc[18, 36]
priceNickel2019 = 14000
priceCopper2019 = 6062.65
captialInvestment = 1500000000
copperMarketShare = 0.008
nickelMarketShare = 0.008
operatingExpenses = 25000000


# priceElasticies
copperElas = 1.048
nickelElas = 2.922

# Calculate constantA using 2019 data
constantACopper = quanityCopper2019 / math.pow(priceCopper2019, copperElas)
constantANickel = quanityNickel2019 / math.pow(priceNickel2019, nickelElas)

# create a table
expectedValueAll = pd.DataFrame(columns=["Copper", "Nickel", "Risk Free"])


# create lists to hold expectedValues
totalExpValueCopperList = []
totalExpValueNickelList = []
totalExpValueRiskFreeList = []
totalExpValueRiskFree = 0

for i in range(18, len(qDemandRaw)):
    # extact each line for analysis
    row = qDemandRaw.iloc[i]
    copperQDemand = row["Copper"]
    nickelQDemand = row["Nickel"]

    # calculate future price of copper and nickel
    priceCopper = math.exp(
        (np.log(copperQDemand / constantACopper) / copperElas))
    priceNickel = math.exp(
        (np.log(nickelQDemand / constantANickel) / nickelElas))
    # calculate total revuene
    totalRevCopper = priceCopper * copperQDemand * copperMarketShare
    totalRevNickel = priceNickel * nickelQDemand * nickelMarketShare

    # getting expected return (value) per year
    if i == 18:  # making to sure include captial investment in first year
        totalExpValueCopper = totalRevCopper - captialInvestment - operatingExpenses
        totalExpValueNickel = totalRevNickel - captialInvestment - operatingExpenses
        totalExpValueRiskFree = totalExpValueRiskFree + captialInvestment

    else:
        totalExpValueCopper = totalRevCopper - operatingExpenses
        totalExpValueNickel = totalRevNickel - operatingExpenses
        totalExpValueRiskFree = totalExpValueRiskFree * 1.04

    totalExpValueCopperList.append(totalExpValueCopper)
    totalExpValueNickelList.append(totalExpValueNickel)
    totalExpValueRiskFreeList.append(totalExpValueRiskFree)


# Calculate Beta - aka covariance since our SD of risk free asset = 1

historicalCopperPriceList = historicalMineralPrices["value copper"].tolist()
historicalNickelPriceList = historicalMineralPrices["value nickel"].tolist()
historicalRiskFreePriceList = dataSpy["spy"].tolist()
del historicalRiskFreePriceList[3102:]


print(len(historicalCopperPriceList))
print(len(historicalNickelPriceList))
print(len(historicalRiskFreePriceList))
# normalize the data based on first price

covCopper = covariance(historicalCopperPriceList, historicalRiskFreePriceList)
covNickel = covariance(historicalRiskFreePriceList, historicalNickelPriceList)
varRiskFree = variance(historicalRiskFreePriceList)


def normailize(dataFrame):
    x = dataFrame.copy()
    for i in x.columns[1:]:
        x[i] = x[i]/x[i][0]
    return x


normalizedSpy = normailize(dataSpy)


def interactive_plot(df, title):
    fig = px.line(title=title)
    for i in df.columns[1:]:
        fig.add_scatter(x=df['timestamp'], y=df[i], name=i)
    fig.show()


interactive_plot(normalizedSpy, "Boobs")

ySpy = normalizedSpy["open"]
xSpy = normalizedSpy["timestamp"]
yXme = normalizedSpy["open"]
xXme = normalizedSpy["timestamp"]

fig, ax = plt.subplot()

ax.plot(xSpy, ySpy)

plt.show()

print("yay")