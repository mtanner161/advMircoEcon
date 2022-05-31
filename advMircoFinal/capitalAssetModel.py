# Capital Asset Flow Predictions

# Model Developed and Coded by Wilson Martin and Michael Tanner


# Import Packages as needed
import matplotlib.pyplot as plt
import pandas as pd
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

# normalization functioned needed


def normailize(dataFrame):
    x = dataFrame.copy()
    for i in x.columns[1:]:
        x[i] = x[i]/x[i][0]
    return x


# reads in relevent data
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
tBill = 2.8

# priceElasticies - Long Term
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

# Master Loop to begin calculating year-by-year expected values - stores results in lists above
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

    else:
        totalExpValueCopper = totalRevCopper - operatingExpenses
        totalExpValueNickel = totalRevNickel - operatingExpenses

    # appends the list to add the lastest year
    totalExpValueCopperList.append(totalExpValueCopper)
    totalExpValueNickelList.append(totalExpValueNickel)

# Calculate Beta - aka covariance since our SD of risk free asset = 1
historicalCopperPriceList = historicalMineralPrices["value copper"].tolist()
historicalNickelPriceList = historicalMineralPrices["value nickel"].tolist()

# Calculatiing Percents for CAPM
copperDiffListPercent = []
nickelDiffListPercent = []
marketDiffListPercent = []

for x, y in zip(totalExpValueCopperList[0::], totalExpValueCopperList[1::]):
    copperDiffListPercent.append((y-x)/x*100)

for x, y in zip(totalExpValueNickelList[0::], totalExpValueNickelList[1::]):
    nickelDiffListPercent.append((y-x)/x*100)

for i in range(0, len(copperDiffListPercent)):
    marketDiffPercent = (
        copperDiffListPercent[i] + nickelDiffListPercent[i]) / 2
    marketDiffListPercent.append(marketDiffPercent)

# calculate covariance
covCopper = covariance(copperDiffListPercent, marketDiffListPercent)
covNickel = covariance(nickelDiffListPercent, marketDiffListPercent)
varMarket = variance(marketDiffListPercent)  # variance calculation


# calculate the beta
betaCopper = covCopper / varMarket
betaNickel = covNickel / varMarket

# get empty lists
capmCopperList = []
capmNickelList = []

for i in range(0, len(copperDiffListPercent) - 1):
    capmCopper = tBill + (betaCopper * (marketDiffListPercent[i] - tBill))
    capmNickel = tBill + (betaNickel * (marketDiffListPercent[i] - tBill))
    capmCopperList.append(capmCopper)
    capmNickelList.append(capmNickel)


# calculate average
returnCopperSumMean = sum(capmCopperList) / len(capmCopperList)
returnNickelSumMean = sum(capmNickelList) / len(capmNickelList)

# get a list year - not needed in the model
yearList = [2020]
for i in range(1, 30):
    yearList.append(yearList[i-1] + 1)

dict = {"year": yearList, "copper return": capmCopperList,
        "nickel return": capmNickelList}

df = pd.DataFrame(dict)

df.to_csv(r"./advMircoEcon/advMircoFinal/dataCAPM.csv")
