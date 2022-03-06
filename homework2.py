## Python Homework 2 Replication

import numpy as np

# Constants Needed for non cartel
alphaZero = -0.434
alphaOne = -0.33
alphaTwo = 0.391
gammaR = 0.011
gammaT = 3.194
gammaE = 4.474
gammaB = 4.882
qF = 0.8654
xT = 30
cObs = 5.55

variableA = (
    (-alphaZero / alphaOne) + ((-alphaTwo / alphaOne) * xT) + ((1 / alphaOne) * qF)
)
variableB = -1 / alphaOne

## Question 1

# Define all marginal costs
mariginalCostR = gammaR + cObs
marginalCostT = gammaT + cObs
marginalCostE = gammaE + cObs
marginalCostB = gammaB + cObs

matrixA = np.array(
    [
        [1, 1, 1, 1, -1],
        [-2 * variableB, -1 * variableB, -1 * variableB, -1 * variableB, 0],
        [-1 * variableB, -2 * variableB, -1 * variableB, -1 * variableB, 0],
        [-1 * variableB, -1 * variableB, -2 * variableB, -1 * variableB, 0],
        [-1 * variableB, -1 * variableB, -1 * variableB, -2 * variableB, 0],
    ]
)

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

print(fourFirmNashEqualibrum)  ## check answer

##Question 2 - Assume Only Two Firms

## Nash Equalibrum
mariginalCostFirmOne = cObs + gammaR
mariginalCostFirmTwo = cObs + gammaR  ## both are equal

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

print(twoFirmNashEqualibrum)  ## check answer

priceNash = 11.21
quanityOptimal = twoFirmNashEqualibrum[2]
profitNash = (
    priceNash * quanityOptimal - mariginalCostFirmOne
)  ## equals MR and MC = which checks out for Nash game so makes sense

## Cartel Profits

# Set new Variables
alphaZeroCartel = 0.066
alphaOneCartel = -0.248
alphaTwoCartel = 0.323
gammaRCartel = -0.188
gammaTCartel = 3.138
gammaECartel = 4.426
gammaBCartel = 4.880

mariginalCostFirmOne = cObs + gammaRCartel
mariginalCostFirmTwo = cObs + gammaRCartel  ## both are equal

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

print(twoFirmCatrel)  ##notice q increase - that is good

priceCartel = 13.6
quanityOptimalCartel = twoFirmCatrel[2]
profitCartel = priceCartel * quanityOptimalCartel - mariginalCostFirmOne

## Deviation Profits
deviationProfit = profitCartel - priceNash
print(deviationProfit)

## Question 3 - discount factor

discountFactor = 1 - (priceCartel / profitNash)
print(discountFactor)  ## 0.76
