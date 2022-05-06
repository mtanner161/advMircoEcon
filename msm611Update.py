# MSM Web Application Model Using Game Theory

# import needed packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#import sheets
mineralMarketSize = pd.read_excel(
    r"./minesmineralmodel/outputs/two_degree/cleanMarketSize Pandas.xlsx")
mineralPriceTable = pd.read_excel(
    r"./minesmineralmodel/inputs/two_degree/mineralPrice.xlsx")

# Marginal Costs
aluminumPrice = mineralPriceTable.iloc[0]
copperPrice = mineralPriceTable.iloc[12]
nickelPrice = mineralPriceTable.iloc[36]
marginalCostAluminum = 700
marginalCostCopper = 3548
marginalCostNickel = 9000

mineralMarketSizeNp = mineralMarketSize.to_numpy()  # turn in array for analysis

# get number of years and mineral
numberOfYears = len(mineralMarketSizeNp) - 1
numberOfMinerals = len(mineralMarketSize.columns)

# create array of zeros with correct dimensions of numberOfYears and numberofMinerals
deltaMarketSize = np.zeros([numberOfYears, numberOfMinerals], dtype=float)

# Calculate Marginal
for i in range(0, numberOfMinerals):
    for j in range(0, numberOfYears):
        deltaMarketSize[j][i] = mineralMarketSizeNp[j+1][i] - \
            mineralMarketSizeNp[j][i]

cleanDeltaMarketSize = pd.DataFrame(
    deltaMarketSize, columns=mineralMarketSize.columns)


cleanDeltaMarketSize.to_excel(r"./advMircoEcon/deltaMarketSize.xlsx")


plt.rcParams["figure.figsize"] = (11, 5)  # set default figure size
plt.rcParams["figure.figsize"] = (11, 5)  # set default figure size


def utility(comsumption, gamma):
    return comsumption**(1-gamma) / (1-gamma)


def v_star(x, beta, gamma):
    return (1 - beta**(1 / gamma))**(-gamma) * utility(x, gamma)


beta, gamma = 0.95, 1.8
x_grid = np.linspace(0.1, 5, 100)

fig, ax = plt.subplots()

ax.plot(x_grid, v_star(x_grid, beta, gamma), label='value function')

ax.set_xlabel('$x$', fontsize=12)
ax.legend(fontsize=12)

plt.show()


def c_star(x, beta, gamma):
    return (1 - beta ** (1/gamma)) * x


fig, ax = plt.subplots()
ax.plot(x_grid, c_star(x_grid, beta, gamma), label='default parameters')
ax.plot(x_grid, c_star(x_grid, beta + 0.02, gamma), label=r'higher $\beta$')
ax.plot(x_grid, c_star(x_grid, beta, gamma + 0.2), label=r'higher $\gamma$')
ax.set_ylabel(r'$\sigma(x)$')
ax.set_xlabel('$x$')
ax.legend()

plt.show()


# Constants Needed for non cartel
alphaZero = -0.434
alphaOne = -0.33
alphaTwo = 0.391
gammaR = 0.011
gammaT = 3.194
gammaE = 4.474
gammaB = 4.882
quanityFringe = 0.8654
xT = 30
unitCost = 5.55

variableA = (
    (-alphaZero / alphaOne) + ((-alphaTwo / alphaOne) * xT) +
    ((1 / alphaOne) * quanityFringe)
)
variableB = -1 / alphaOne

# Question 1

# Define all marginal costs
mariginalCostR = gammaR + unitCost
marginalCostT = gammaT + unitCost
marginalCostE = gammaE + unitCost
marginalCostB = gammaB + unitCost

# since python doesnt havea vpasolve like MATLAB - we have to use matrix's to solve this.  Set up the linear equations by hand, then hardcoded the matrix
matrixA = np.array(
    [
        [1, 1, 1, 1, -1],
        [-2 * variableB, -1 * variableB, -1 * variableB, -1 * variableB, 0],
        [-1 * variableB, -2 * variableB, -1 * variableB, -1 * variableB, 0],
        [-1 * variableB, -1 * variableB, -2 * variableB, -1 * variableB, 0],
        [-1 * variableB, -1 * variableB, -1 * variableB, -2 * variableB, 0],
    ]
)

# second matrix - the answers
matrixB = np.array(
    [
        0,
        mariginalCostR - variableA,
        marginalCostT - variableA,
        marginalCostE - variableA,
        marginalCostB - variableA,
    ]
)

fourFirmNashEqualibrum = np.linalg.inv(matrixA).dot(matrixB)

print(fourFirmNashEqualibrum)  # check answer

# Question 2 - Assume Only Two Firms

# Nash Equalibrum
mariginalCostFirmOne = unitCost + gammaR
mariginalCostFirmTwo = unitCost + gammaR  # both are equal

matrixC = np.array(
    [
        [1, 1, -1],
        [-2 * variableB, -1 * variableB, 0],
        [-1 * variableB, -2 * variableB, 0],
    ]
)
matrixD = np.array(
    [0, mariginalCostFirmOne - variableA, mariginalCostFirmTwo - variableA]
)

twoFirmNashEqualibrum = np.linalg.inv(matrixC).dot(matrixD)

print(twoFirmNashEqualibrum)  # check answer

priceNash = 11.21
quanityOptimal = twoFirmNashEqualibrum[2]
profitNash = (
    priceNash * quanityOptimal - mariginalCostFirmOne
)  # equals MR and MC = which checks out for Nash game so makes sense

# Cartel Profits

# Set new Variables
alphaZeroCartel = 0.066
alphaOneCartel = -0.248
alphaTwoCartel = 0.323
gammaRCartel = -0.188
gammaTCartel = 3.138
gammaECartel = 4.426
gammaBCartel = 4.880

mariginalCostFirmOne = unitCost + gammaRCartel
mariginalCostFirmTwo = unitCost + gammaRCartel  # both are equal

matrixE = np.array(
    [
        [1, 1, -1],
        [-2 * variableB, -1 * variableB, 0],
        [-1 * variableB, -2 * variableB, 0],
    ]
)
matrixF = np.array(
    [0, mariginalCostFirmOne - variableA, mariginalCostFirmTwo - variableA]
)

twoFirmCatrel = np.linalg.inv(matrixE).dot(matrixF)

print(
    twoFirmCatrel
)  # notice q increase - that is good which means that our profit should increase - which matches theory!

priceCartel = 13.6
quanityOptimalCartel = twoFirmCatrel[2]
profitCartel = priceCartel * quanityOptimalCartel - mariginalCostFirmOne

# Deviation Profits
deviationProfit = profitCartel - priceNash
print(deviationProfit)

# Question 3 - discount factor

discountFactor = 1 - (priceCartel / profitNash)
print(discountFactor)  # 0.76
