"""vmsutilsv: Village Market Simulator Utility Functions.
Original Author: William O. Ruddick
Date: May-18-2018
"""

import numpy as np
import pygame
from scipy.interpolate import UnivariateSpline
import math
import networkx as nx

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
MYCOAGENT = 888
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
    elif iType == MYCOAGENT:
        tttype = "Swap Pool"
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


def mintToken(deposit,toToken):

    if toToken.connectorBalance != 0:


        tokensMinted = toToken.supply*((1+deposit /toToken.connectorBalance ) ** (toToken.cw )-1)

        if isinstance(tokensMinted, complex):
            print("Complex error (from) mintToken")
            return False


        newSupply = toToken.supply + tokensMinted
        newConnectorBalance = toToken.connectorBalance+deposit
        newPrice = newConnectorBalance/(newSupply*toToken.cw)

        toToken.supply = newSupply
        toToken.connectorBalance = newConnectorBalance
        toToken.price = newPrice

    else:
        print("Error xyz123")

    return tokensMinted

def pullReserve(withdraw,fromToken):

    if withdraw <0 :
        print("Error withdraw amount should be positive")
    if fromToken.connectorBalance != 0:


        reservePulledOut = fromToken.connectorBalance *( (1+-1*float(withdraw) / fromToken.supply) ** (1 / fromToken.cw)-1)

        if isinstance(reservePulledOut, complex):
            print("Complex error (from) pullReserve")
            return False


        newSupply = fromToken.supply - withdraw
        newConnectorBalance = fromToken.connectorBalance+reservePulledOut
        newPrice = newConnectorBalance/(newSupply*fromToken.cw)

        fromToken.supply = newSupply
        fromToken.connectorBalance = newConnectorBalance
        fromToken.price = newPrice

    else:
        print("Error xyz123")

    return -1*reservePulledOut



def convertPure(amount,fromToken,toToken):
    #print(">>pre convert utils: amount:",amount," from:",fromToken.price," to:",toToken.price, )
    #print("     >>supply:",fromToken.supply," connectorBalance:",fromToken.connectorBalance )
    purchaseReturn = 0
    if fromToken.connectorBalance != 0 and toToken.connectorBalance != 0:

        if amount >= fromToken.connectorBalance:
            amount = fromToken.connectorBalance - 0.00000001
            #print("adjust amount on convert")

        reservePulledOut = fromToken.connectorBalance * (1- (1-amount / fromToken.supply) ** (1/fromToken.cw ))

        if isinstance(reservePulledOut, complex):
            print("Complex error (from) convertPure a")
            return False


        newSupply = fromToken.supply - amount
        newConnectorBalance = fromToken.connectorBalance-reservePulledOut
        newPrice = newConnectorBalance/(newSupply*fromToken.cw)

        purchaseReturn = toToken.supply * ((1 + reservePulledOut / toToken.connectorBalance) ** (toToken.cw ) - 1)


        #print("purchaseReturn",purchaseReturn)

        if isinstance(purchaseReturn, complex):
            print("Complex error (from) convert Pure b")
            return False


        fromToken.supply = newSupply
        fromToken.connectorBalance = newConnectorBalance
        fromToken.price = newPrice

        tnewSupply = toToken.supply + purchaseReturn
        tnewConnectorBalance = toToken.connectorBalance+reservePulledOut
        tnewPrice = tnewConnectorBalance/(tnewSupply*toToken.cw)

        toToken.supply = tnewSupply
        toToken.connectorBalance = tnewConnectorBalance
        toToken.price = tnewPrice


    else:
        print("Converting to or from reserve")
    if False:

        newSupply = fromToken.supply + amount
        fromToken.supply = newSupply
        reservePulledOut = amount

        if toToken.connectorBalance != 0:

            if amount / toToken.connectorBalance <= -1:
                amount = -1*toToken.connectorBalance + 0.0000001
                print("adjust amount on convert B")
            purchaseReturn = toToken.supply * ((1 + reservePulledOut / fromToken.connectorBalance) ** (fromToken.cw) - 1)

            # print("purchaseReturn",purchaseReturn)

            if isinstance(purchaseReturn, complex):
                print("Complex error (from)")
                return False

            tnewSupply = toToken.supply + purchaseReturn
            tnewConnectorBalance = toToken.connectorBalance+reservePulledOut
            tnewPrice = tnewConnectorBalance/(tnewSupply*toToken.cw)

        else: #we are converting to a top level reserve with no connector
            #print("convert to top level: purchaseReturn:", currencyTypeToString(toToken.tokenID))
            #tpurchaseReturn = purchaseReturn
            tnewSupply = toToken.supply
            tnewConnectorBalance = 0
            tnewPrice = 1

        #print("tpurchaseReturn",tpurchaseReturn)


        #print("fromDiff:" ,fromValueDiffAfter - fromValueDiffBefore)



    return purchaseReturn


def convert(amount,fromToken,toToken):
    #print(">>pre convert utils: amount:",amount," from:",fromToken.price," to:",toToken.price, )
    #print("     >>supply:",fromToken.supply," connectorBalance:",fromToken.connectorBalance )

    if amount >= fromToken.connectorBalance:
        amount = fromToken.connectorBalance - 0.00000001
        #print("adjust amount on convert")
    purchaseReturn = fromToken.supply * ((1 + (-1)*amount / fromToken.connectorBalance) ** (fromToken.cw ) - 1)
    #print("purchaseReturn",purchaseReturn)
    if isinstance(purchaseReturn, complex):
        print("Complex error (from)")
        return False
    newSupply = fromToken.supply + purchaseReturn
    newConnectorBalance = fromToken.connectorBalance-amount
    newPrice = newConnectorBalance/(newSupply*fromToken.cw)

    tpurchaseReturn = 0

    if toToken.connectorBalance != 0:

        if amount / toToken.connectorBalance <= -1:
            amount = -1*toToken.connectorBalance + 0.0000001
            print("adjust amount on convert B")
        tpurchaseReturn = toToken.supply * ((1 + amount / toToken.connectorBalance) ** (toToken.cw) - 1)
        if isinstance(tpurchaseReturn, complex):
            print("Complex error (to)")
            return False #negative amount
        tnewSupply = toToken.supply + tpurchaseReturn
        tnewConnectorBalance = toToken.connectorBalance+amount
        tnewPrice = tnewConnectorBalance/(tnewSupply*toToken.cw)

    else: #we are converting to a top level reserve with no connector
        print("convert to top level: purchaseReturn:", currencyTypeToString(toToken.tokenID))
        tpurchaseReturn = amount
        tnewSupply = toToken.supply + tpurchaseReturn
        tnewConnectorBalance = 0
        tnewPrice = 1

    #print("tpurchaseReturn",tpurchaseReturn)

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


def find_closest_agents(click_pos, num_closest, traders):
    """
    Find the closest agents to the click position, only considering agents whose names start with 'b'.

    Parameters:
    click_pos (tuple): The x, y position of the click.
    num_closest (int): Number of closest agents to find.

    Returns:
    list: A list of the closest agents.
    """
    distances = []
    for agent in traders:
        if agent.ownToken == False: #they shold have their own voucher
            continue
        arect = agent.rect
        pos = arect.center
        
        #global zpos  # Access the global variable
        distance = (agent,math.hypot(pos[0] - click_pos[0], pos[1] - click_pos[1]))
        distances.append(distance)
    

        # Filter agents whose names start with 'b' and calculate distances
        #distances = [(name, math.hypot(pos[0] - click_pos[0], pos[1] - click_pos[1])) 
                 #for name, pos in zpos.items() if name.startswith('b')]
    if(len(distances) == 0):
        return distances
    if(len(distances) < num_closest):
        num_closest = len(distances)

    final_list = []
    if(len(distances) >= 1):
    
        distances.sort(key=lambda x: x[1])  # Sort by distance
        final_list = [name for name, _ in distances[:num_closest]]

    # Return closest agent names, limited to num_closest
    return final_list


def make_graph(swap_pools):
    # Create a graph of the swap pools
    G = nx.Graph()
    if swap_pools != None:        
        for pool in swap_pools:
            if pool.localSelling:
                for v_i in pool.cc:
                    G.add_node(v_i.token.tokenID)
                    for other_v_i in pool.cc:
                        if v_i != other_v_i:
                            G.add_edge(v_i.token.tokenID, other_v_i.token.tokenID, pool=pool.tIndex)

    return G

    
def find_feasible_paths(G, input_voucher, output_voucher, amount, max_path_length, swap_pools):

    #print(G)
    #print("Nodes in G:", G.nodes)
    #print("Edges in G:", G.edges)

    input_voucher_id = input_voucher.tokenID
    output_voucher_id = output_voucher.tokenID
    #print(f"Input voucher: {input_voucher_id}, Output voucher: {output_voucher_id}")

    def dfs(current_voucher, target_voucher, path, visited):
        if len(path) > max_path_length:
            return
        if current_voucher == target_voucher:
            feasible_paths.append(list(path))
            return
        if current_voucher not in G:
            print(f"Warning: {current_voucher} does not exist in the Graph")
            return

        for neighbor in G[current_voucher]:
            pool_name = G[current_voucher][neighbor]['pool']

            pool = next((p for p in swap_pools if p.tIndex == pool_name), None)
            neighbor_balance = 0
            if(pool != None):
                 nWalletToken = next((t for t in pool.cc if t.token.tokenID == neighbor), None)
                 if(nWalletToken != None):
                     neighbor_balance = nWalletToken.balance
                     if(neighbor_balance >= amount and neighbor not in visited):
                        if pool.localSelling:
                            #print("Neighbor: ", neighbor, "target: ",target_voucher)
                            path.append(neighbor)
                            visited.add(neighbor)
                            dfs(neighbor, target_voucher, path, visited)
                            path.pop()
                            visited.remove(neighbor)

    feasible_paths = []
    visited = set([input_voucher_id])
    dfs(input_voucher_id, output_voucher_id, [input_voucher_id], visited)
    return feasible_paths

# Function to print the path and SwapPools
def print_exchange_route(G, path):
    
    if not path:
        print("No exchange route found.")
        return

    #print("expanded exchange route: len:",range(len(path) - 1))
    for i in range(len(path) - 1):
        start_voucher, end_voucher = path[i], path[i + 1]
        # Retrieve the pool name from the edge data
        pool_name = G[start_voucher][end_voucher]['pool']
        #print(f"Exchange {start_voucher} for {end_voucher} in {pool_name}")

