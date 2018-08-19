"""vmsutilsv043: Village Market Simulator Utility Funcations.
Original Author: William O. Ruddick
Date: May-18-2018
"""

import numpy as np
import pygame
from scipy.interpolate import UnivariateSpline

NC = 181
CC = 212 #default number - but increases in value for new CCs

reserveTokenID=251

CIRCLE = 4
BANKCIRCLE = 5
RETAILSQUARE = 1
FRETAILSQUARE = 7
MARKETSQUARE = 6
TRIANGLE = 2
DIAMOND = 3


BANK = 66
EXTERNALMARKET = 55
GENERIC = 44
RETAIL = 33
FOREIGNRETAIL = 333
LOCALSERVICE = 22
LOCALPRODUCER = 77
EXPORTSERVICE = 11
LOCALSERVICECOOP = 222
LOCALPRODUCERCOOP = 777
EXCHANGE = 9898

#Trade Types tradeType
#sell/purchase, 
LOCALTRADESERVICES = 130
LOCALTRADESTOCK = 230
#makeDeposit/acceptDeposit, 
DEPOSIT = 330
FEES = 331
SAVINGS = 332
DIVIDEND = 430
LOAN = 530 #giveLoan/acceptLoan
CLEARING = 630 #giveLoan/acceptLoan
EXTSERVICES = 730 #purchaseImport/theMarket.sellExport
EXTSTOCK = 830#theMarket.purchaseExport/sellExport


yeardays=365/12.0 #dayspermonth

def isCC(ccNum):
    global CC
    if ccNum >= CC:
        return True
    return False

def tradeTypeToString(iType):
    tttype = "error"
    if iType == LOCALTRADESERVICES:
        tttype = "LocalServices"
    elif iType == LOCALTRADESTOCK:
        tttype = "LocalStock"
    elif iType == DEPOSIT:
        tttype = "DEPOSIT"
    elif iType == SAVINGS:
        tttype = "SAVINGS"
    elif iType == FEES:
        tttype = "FEES"
    elif iType == DIVIDEND:
        tttype = "DIVIDEND"
    elif iType == LOAN:
        tttype = "LOAN"
    elif iType == CLEARING:
        tttype = "CLEARING"
    elif iType == EXTSERVICES:
        tttype = "ExportServices"
    elif iType == EXTSTOCK:
        tttype = "ExportStock"
    return tttype


def currencyTypeToString(iType):
    tttype = "error"
    if iType == NC:
        tttype = "NC"

    elif iType == CC:
        tttype = "(cc)"

    elif iType >CC:
        tttype = "(cc"+str(iType)+")"
    return tttype


def traderTypeToString(iType):
    tttype = "error type not found: ", iType
    if iType == BANK:
        tttype = "Coop"
    elif iType == EXTERNALMARKET:
        tttype = "ExternalMarket"
    elif iType == GENERIC:
        tttype = "GENERIC"
    elif iType == RETAIL:
        tttype = "RetailShop"
    elif iType == FOREIGNRETAIL:
        tttype = "ForeignRetail"
    elif iType == LOCALSERVICE:
        tttype = "LocalService"
    elif iType == LOCALPRODUCER:
        tttype = "LocalProducer"
    elif iType == EXPORTSERVICE:
        tttype = "ServiceExporter"
    return tttype

#nonRandom Double-Shuffle
def shuffleMix(ztraders):
    #ztraders = ['1','2','3','4','5','6','7','8','9','10','11']
    
    A = list(ztraders)
    numT = len(ztraders)

    B = A[:int(len(A)/2)]
    C = A[int(len(A)/2):]
    D = []

    lenB=len(B)
    lenC=len(C)
    inc = 0
    if lenC>=lenB:
        for c in C:
            D.append(c)
            if inc < lenB:
                D.append(B[inc])
                inc+=1
    else:
        for b in B:
            D.append(b)
            if inc < lenC:
                D.append(C[inc])
                inc+=1
    
    D = list(reversed(D))
    
    return D

def writeVideo():
    #create image array
    image_array = []

    path = '/home/wor/Projects/Programming/Bangla-Pesa-Python/plotsv4/*.png'   
    files=glob.glob(path)   
    for file in files:     
        print (file)
        f=open(file, 'r')  
        f.readlines()   
        image_array.append(f)
        f.close() 
    duration = len(image_array)
    command = [ FFMPEG_BIN,
                '-y', # (optional) overwrite output file if it exists
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-s', '420x360', # size of one frame
                '-pix_fmt', 'rgb24',
                '-r', '24', # frames per second
                '-i', '-', # The imput comes from a pipe
                '-an', # Tells FFMPEG not to expect any audio
                '-vcodec', 'mpeg',
                'my_output_videofile.mp4' ]

    #pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)
    #pipe.proc.stdin.write( image_array.tostring() )
    fps = 50#24
    sp.call(["avconv","-y","-r",str(fps),"-i", "./plotsv4/myfile_%05d.png","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video.avi"])

def convert(amount,fromToken,toToken):
    #print(">>pre convert utils: amount:",amount," from:",fromToken.price," to:",toToken.price)
    purchaseReturn = fromToken.supply * ((1 + (-1)*amount / fromToken.connectorBalance) ** (fromToken.cw ) - 1)
    #print("purchaseReturn",purchaseReturn)
    if isinstance(purchaseReturn, complex):
        return False
    newSupply = fromToken.supply + purchaseReturn
    newConnectorBalance = fromToken.connectorBalance-amount
    newPrice = newConnectorBalance/(newSupply*fromToken.cw)



    tpurchaseReturn = toToken.supply * ((1 + amount / toToken.connectorBalance) ** (toToken.cw) - 1)
    #print("tpurchaseReturn",tpurchaseReturn)
    if isinstance(tpurchaseReturn, complex):
        return False
    tnewSupply = toToken.supply + tpurchaseReturn
    tnewConnectorBalance = toToken.connectorBalance+amount
    tnewPrice = tnewConnectorBalance/(tnewSupply*toToken.cw)

    fromValueDiffBefore = fromToken.price * amount

    fromToken.supply = newSupply
    fromToken.connectorBalance = newConnectorBalance

    fromToken.price = newPrice


    fromValueDiffAfter = fromToken.price * amount

    #print("fromDiff:" ,fromValueDiffAfter - fromValueDiffBefore)

    toValueDiffBefore = toToken.price * amount
    toToken.supply = tnewSupply
    toToken.connectorBalance = tnewConnectorBalance
    toToken.price = tnewPrice
    #print("<<post convert utils: from:",fromToken.price," to:",toToken.price)

    toValueDiffAfter = toToken.price * amount
    #print("toDiff:" ,toValueDiffAfter - toValueDiffBefore)
    #print("totalDiff:", fromValueDiffAfter - fromValueDiffBefore + toValueDiffAfter - toValueDiffBefore)

    return True

def calculatePurchaseReturn(supply, balance, weight, amount):
    return supply * ((1 + amount / balance) ** (weight / 1000000) - 1)

def calculateSaleReturn(supply, balance, weight, amount):
    return balance * (1 - (1 - amount / supply) ** (1000000 / weight))


def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


def GRLC(values):
    '''
    Calculate Gini index, Gini coefficient, Robin Hood index, and points of 
    Lorenz curve
    Lorenz curve values as given as lists of x & y points [[x1, x2], [y1, y2]]
    @param values: List of values
    @return: [Gini index, Gini coefficient, Robin Hood index, [Lorenz curve]] 
    '''
    n = len(values)
    assert(n > 0), 'Empty list of values'
    sortedValues = sorted(values) #Sort smallest to largest

    #Find cumulative totals
    cumm = [0]
    for i in range(n):
        cumm.append(sum(sortedValues[0:(i + 1)]))

    #Calculate Lorenz points
    LorenzPoints = [[], []]
    sumYs = 0           #Some of all y values
    robinHoodIdx = -1   #Robin Hood index max(x_i, y_i)
    for i in range(1, n + 2):
        x = 100.0 * (i - 1)/n
        y = 100.0 * (cumm[i - 1]/float(cumm[n]))
        LorenzPoints[0].append(x)
        LorenzPoints[1].append(y)
        sumYs += y
        maxX_Y = x - y
        if maxX_Y > robinHoodIdx: robinHoodIdx = maxX_Y   
    
    giniIdx = 100 + (100 - 2 * sumYs)/n #Gini index 

    return [giniIdx, giniIdx/100, robinHoodIdx, LorenzPoints]


#create a continuios distribution from discreet data
def smoother(seasonalImportSmooth,seasonalImportOrig,sRounds,rounds,seasonalMarketArray,seasonalImportFlat):
    #global seasonalImportSmooth
    #global seasonalImportOrig
    #global sRounds
    seasonalImportSmooth=[]
    sRounds=[]
    r=0
    while r < rounds:
        sRounds.append(r)
        seasonalImportSmooth.append(0.0)
        r = r+1        
    seasonalImportSmooth[0]=seasonalMarketArray[0]

    m1=1
    maxrDist = 0
    while m1 < rounds:
        fMonth = float(m1)/yeardays
        xMonth = fMonth % 12.0
        theMonth = int(xMonth)
        theMonthMult = seasonalMarketArray[theMonth]
        nextMonth = int((theMonth +1) %12)
        theNextMonthMult = seasonalMarketArray[nextMonth]

        z1 = m1 +1
        while z1 < rounds*2:
            zMonth = float(z1)/yeardays
            zMonth = zMonth % 12.0
            zheMonth = int(zMonth)
            if zheMonth != theMonth:
                break
            else:
                z1=z1+1
        rDist = z1-m1
        if rDist > maxrDist:
            maxrDist = rDist

        if rDist == maxrDist :
            seasonalImportSmooth[m1]=theMonthMult
        else:
            seasonalImportSmooth[m1]=np.NaN

        m1= m1+1
        if rDist <= 1:
            maxrDist = 0
        
    yn, tn = tnorm(seasonalImportSmooth, step=-1*rounds, k=3, smooth=0, show=False)
    g=0
    while g < len(yn):
#        sRounds[g]=tn[g]
        seasonalImportSmooth[g]=yn[g]
        seasonalImportOrig.append(yn[g])
        seasonalImportFlat.append(0.5)
        g = g+1

    return seasonalImportSmooth, seasonalImportOrig, seasonalImportFlat, sRounds


#normalize smoothed data
def tnorm(y, axis=0, step=1, k=3, smooth=0, mask=None, show=False, ax=None):

    #y = np.asarray(y)
    y = np.asarray(y)
    if axis:
        y = y.T
    if y.ndim == 1:
        y = np.reshape(y, (-1, 1))
    # turn mask into NaN
    if mask is not None:
        y[y == mask] = np.NaN
    # delete rows with missing values at the extremities
    while y.size and np.isnan(np.sum(y[0])):
        y = np.delete(y, 0, axis=0)
    while y.size and np.isnan(np.sum(y[-1])):
        y = np.delete(y, -1, axis=0)
    # check if there are still data
    if not y.size:
        return None, None
    if y.size == 1:
        return y.flatten(), None

    t = np.linspace(0, 100, y.shape[0])
    if step == 0:
        tn = t
    elif step > 0:
        tn = np.linspace(0, 100, np.round(100 / step + 1))
    else:
        tn = np.linspace(0, 100, -step)
    yn = np.empty([tn.size, y.shape[1]]) * np.NaN
    for col in np.arange(y.shape[1]):
        # ignore NaNs inside data for the interpolation
        ind = np.isfinite(y[:, col])
        if np.sum(ind) > 1:  # at least two points for the interpolation
            spl = UnivariateSpline(t[ind], y[ind, col], k=k, s=smooth)
            yn[:, col] = spl(tn)

    if show:
        _plot(t, y, ax, tn, yn)

    if axis:
        y = y.T
    if yn.shape[1] == 1:
        yn = yn.flatten()

#    print len(yn)
 #   print len(tn)
  #  print tn

    return yn, tn


