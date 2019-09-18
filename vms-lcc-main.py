"""vms-cc-main-v047: Village Market Simulator.
Original Author: William O. Ruddick
Contact: will@grassrootseconomics.org
Website: grassrootseconomics.org
Date: May-18-2018
Code: Draft - pre-release v047

This simulator takes an agent based approach to simulating basic economic intereactions with two currencies.
Field surveys from (7) locations across Kenya and South Africa suggest that the fragility of local markets due to exogenous market conditions gives rise to volatile local markets that result in chronic seasonal illiquidity and local market stagnation. Further data suggests that endogenous sources of liquidity through circulating vouchers refered to as Community Currency (CC) can counteract these seasonal trends and increase overall trade volume.

A model of Community Currency (CC), implemented for sustainable development purposes in Kenya and South Africa, is presented here and used as a basis for an Agent Based Model (ABM). The ABM presents a simplified approach to understanding the mechanisms, impacts and limitations of Community Currencies on regional markets. Findings from the model must be validated by survey data. Preliminary findings suggest that CCs can stabilize and increase trade in local markets during erratic or seasonal exogenous market conditions. Furthermore, the effects of CCs on local markets are found to be highly dependent on the size of existing local production and service sectors.
"""



import pygame, random, sys, glob, os
from pygame.locals import *
import pylab as plt
import numpy as np

import matplotlib.cm as cm
import matplotlib.cm as mpl
import vmsutilsv049 as utils
import colormaps as cmaps
import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

STARTDATE = datetime.datetime(2018, 8, 7, 00, 00) #1st trading on blockchain of a tomato in Kenya
print ("Start Date: ",STARTDATE.isoformat(' '))
startMonth = STARTDATE.month
currentMonthNum = startMonth

random.seed(18)
print (sys.version)
visual = True
cclMode = 0 #into to represent ccMode

displayPlots = visual#False#True
displayTrade = visual#False#True
savingsMode = False#visual#True
loanMode = savingsMode#False#visual#True

importMode = True
exportMode = True#False
seasonalMode = True#False
heatMode = False
heatOn = False #allows for the heatmap to turn on dynamically
ccMode = True
clientsModeB=False
seedingMode = False
autoMode = False#True #runs through several iterations of the simulation
clearingMode = True#False
bondingMode = False

NCHEAT = True
CCHEAT = True


saveImageMode = False
moveTrader= False
MINPUSAGECC = 0.99

if displayPlots == False:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

#MARKET DEMOGRAPHICS#

############SMALLMARKETLocal100
#pRETAIL = 40
#pFOREIGNRETAIL = 10
#pLOCALSERVICE = 20
#pLOCALPRODUCER = 20
#pEXPORTSERVICE = 10

############SMALLMARKETNONLOCAL
#pRETAIL = 5
#pFOREIGNRETAIL = 5
#pLOCALSERVICE = 5
#pLOCALPRODUCER = 5
#pEXPORTSERVICE = 5
#
############MARKET100
pRETAIL = 20
pFOREIGNRETAIL = 20
pLOCALSERVICE = 10
pLOCALPRODUCER = 10
pEXPORTSERVICE = 40

############MARKET200
#pRETAIL = 38
#pFOREIGNRETAIL = 10
#pLOCALSERVICE = 69
#pLOCALPRODUCER = 84
#pEXPORTSERVICE = 400

#numStartSCoops = 0
numStartSCoops = 2
numStartPCoops = 2

pNonAccepting = 0.1 #%
pNonAcceptingStep = 0.1
pNonAcceptingMax = 0.9

############MARKET200
#pRETAIL = 40
#pFOREIGNRETAIL = 22
#pLOCALSERVICE = 60
#pLOCALPRODUCER = 60
#pEXPORTSERVICE = 18


############MARKET1000
#pRETAIL = 200
#pFOREIGNRETAIL = 110
#pLOCALSERVICE = 300
#pLOCALPRODUCER = 300
#pEXPORTSERVICE = 90

#####FEW
#pRETAIL = 10
#pFOREIGNRETAIL = 5
#pLOCALSERVICE = 15
#pLOCALPRODUCER = 15
#pEXPORTSERVICE = 5


tRETAIL = 0
tFOREIGNRETAIL = 0
tLOCALPRODUCER = 0
tLOCALSERVICE = 0
if pRETAIL >= 1:
    tRETAIL = 0
if pFOREIGNRETAIL >= 1:
    tFOREIGNRETAIL = 1
if pLOCALPRODUCER >= 1:
    tLOCALPRODUCER = 1
if pLOCALSERVICE >= 1:
    tLOCALSERVICE = 1

#diversityLevelMax requirment on the minimum number of trade partners
diversityLevelMax = tRETAIL +tFOREIGNRETAIL + tLOCALPRODUCER + tLOCALSERVICE

#MAXTRADERS = 100
MAXTRADERS = pRETAIL + pFOREIGNRETAIL + pLOCALSERVICE + pLOCALPRODUCER + pEXPORTSERVICE


if pRETAIL == 1:
    diversityLevelMax = diversityLevelMax -1
if pFOREIGNRETAIL == 1:
    diversityLevelMax = diversityLevelMax -1
if pLOCALPRODUCER == 1:
    diversityLevelMax = diversityLevelMax -1
if pLOCALSERVICE == 1:
    diversityLevelMax = diversityLevelMax -1

#plt.rc('legend',fontsize=8) # using a size in points
#plt.rc('axes',titlesize=10) # using a size in points

os.environ['SDL_VIDEO_CENTERED'] = '1'

TRADEMOVERATE = 8#10#how fast are trades completed
DAILYCYCLES = 50#200#number of game cycles equalling one day

clickedTrader=1#-1#used for interface
clickedToken=-1#-1#used for interface
FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS

WINDOWWIDTH = 1244
WINDOWHEIGHT = 700
#SUBWINDOWWIDTH = WINDOWWIDTH -120
#SUBWINDOWHEIGHT = 420

SUBWINDOWWIDTH = WINDOWWIDTH - 80
SUBWINDOWHEIGHT = WINDOWHEIGHT - 80

BORDERWIDTH = 10
BORDERHEIGHT = 10

OFFSETWIDTH = 40
OFFSETHEIGHT = 40



CLOCKBORDERWIDTH = 30
CLOCKBORDERHEIGHT = 20

INFOWIDTH = 350
INFOHEIGHT = WINDOWHEIGHT-BORDERHEIGHT*2

TOFFSETWIDTH = OFFSETWIDTH - 10
legendOffsetX = BORDERWIDTH+30
legendOffsetY = INFOHEIGHT-150


TEXTCOLOR = (0, 0, 0)

BLUE  = (  0,   0, 255)
LIGHTBLUE  = (  20,   20, 155)
PURPLE  = (  150,   0, 120)
PINK  = (  250,   0, 220)
ORANGE  = (  200,   70, 10)
DARKORANGE  = (  235,   70, 30)
DARKERORANGE  = (  255,   120, 50)
RED  = (  255,   0, 0)
YELLOW  = (  255,   200, 0)
DARKRED  = (  155,   0, 0)
GREEN  = (  0,   255, 0)
WHITE  = (  255,   255, 255)
GREY  = (  111,   111, 222)
BLACK  = (  0,   0, 0)
BACKGROUNDCOLOR = BLACK
DARKGREEN = (  0, 155,   0)
DARKERGREEN = (  0, 80,   0)
LIGHTGREEN  = (  100,   255, 100)

heatSprites = pygame.sprite.Group()
legendSprites = pygame.sprite.Group()
tokenSprites = pygame.sprite.Group()






infoRect = pygame.Surface((INFOWIDTH,INFOHEIGHT))  # the size of your rect
infoRect.set_alpha(150)                # alpha level infoRect.set_alpha(128)
#infoRect.fill((255,255,255))# this fills the entire surface
infoRect.fill((210,255,215))# this fills the entire surface


heatBtnSize = (65,20)  # the size of your rect
heatBntRectal = pygame.Rect(legendOffsetX+250, legendOffsetY-35,heatBtnSize[0],heatBtnSize[1])
heatBtnRect = pygame.Surface(heatBtnSize)  # the size of your rect
heatBtnRect.set_alpha(150)                # alpha level infoRect.set_alpha(128)
#infoRect.fill((255,255,255))# this fills the entire surface
heatBtnRect.fill((110,255,215))# this fills the entire surface


clearBtnSize = (40,20)  # the size of your rect
clearBntRectal = pygame.Rect(legendOffsetX+250, legendOffsetY+19,clearBtnSize[0],clearBtnSize[1])
clearBtnRect = pygame.Surface(clearBtnSize )  # the size of your rect
clearBtnRect.set_alpha(150)                # alpha level infoRect.set_alpha(128)
#infoRect.fill((255,255,255))# this fills the entire surface
clearBtnRect.fill((110,255,215))# this fills the entire surface

tokenBtnSize = (55,20)  # the size of your rect
tokenBntRectal = pygame.Rect(legendOffsetX+250, legendOffsetY-10,tokenBtnSize[0],tokenBtnSize[1])
tokenBtnRect = pygame.Surface(tokenBtnSize )  # the size of your rect
tokenBtnRect.set_alpha(150)                # alpha level infoRect.set_alpha(128)
#infoRect.fill((255,255,255))# this fills the entire surface
tokenBtnRect.fill((110,255,215))# this fills the entire surface


tenxBtnSize = (40,20)  # the size of your rect
tenxBntRectal = pygame.Rect(legendOffsetX+250, legendOffsetY+45,tenxBtnSize[0],tenxBtnSize[1])
tenxBtnRect = pygame.Surface(tenxBtnSize )  # the size of your rect
tenxBtnRect.set_alpha(150)                # alpha level infoRect.set_alpha(128)
#infoRect.fill((255,255,255))# this fills the entire surface
tenxBtnRect.fill((110,255,215))# this fills the entire surface

BOARDMARGIN = 40
BOARDSIZEX=WINDOWWIDTH-INFOWIDTH-BORDERWIDTH*3-BOARDMARGIN
BOARDSIZEY=WINDOWHEIGHT-BORDERHEIGHT*2-BOARDMARGIN
boardRect = pygame.Surface((BOARDSIZEX,BOARDSIZEY))  # the size of your rect
boardRect.set_alpha(60)                # alpha level infoRect.set_alpha(128)
boardRect.fill((255,255,255))# this fills the entire surface

BOARDOFFSETX = BORDERWIDTH*2+INFOWIDTH+BOARDMARGIN/2
BOARDOFFSETY = BORDERHEIGHT+BOARDMARGIN/2


'''
CELLSIZE = 2

wormCCSegmentRect = pygame.Surface((CELLSIZE+2, CELLSIZE+2))
wormCCInnerSegmentRect = pygame.Surface((CELLSIZE-1+2, CELLSIZE-1+2))
wormCCSegmentRect.fill(DARKGREEN)# this fills the entire surface
wormCCInnerSegmentRect.fill(LIGHTGREEN)# this fills the entire surface

wormNCSegmentRect = pygame.Surface((CELLSIZE, CELLSIZE))
wormNCInnerSegmentRect = pygame.Surface((CELLSIZE-1, CELLSIZE-1))
wormNCSegmentRect.fill(DARKERORANGE)# this fills the entire surface
wormNCInnerSegmentRect.fill(DARKORANGE)# this fills the entire surface
'''
try:
    ccImage = pygame.image.load('nc.png')
    ncImage = pygame.image.load('cc.png')
    retailShopImage = pygame.image.load('shop-green.png')
    foreignRetailShopImage = pygame.image.load('shop-red.png')
    serviceShopImage = pygame.image.load('services.png')
    coopShopImage = pygame.image.load('coop.png')
    coopServicesShopImage = pygame.image.load('coopservices.png')
    coopProductionShopImage = pygame.image.load('coopproduction.png')
    productionShopImage = pygame.image.load('production.png')
    marketImage = pygame.image.load('city.png')
    workerImage = pygame.image.load('worker_sm.png')
    curveImage = pygame.image.load('curve.png')
except:
    print("png loaded")

#infoRect = pygame.Rect(BORDERWIDTH, BORDERHEIGHT, INFOWIDTH, INFOHEIGHT )


TOTALSTARTINGNC = 0
STOCKGROWTHRATE = 0 #stock increase per cycle?
STOCKCONSUMPTIONRATE = 1
SERVICESGROWTHCYCLE = 4 #services increase per cycle?
SERVICESGROWTHAMOUNT = 0 #services increase per cycle?
stockStartAmt = 5000
stockStartStd = stockStartAmt*.1
servicesStartAmt = 5000
servicesStartStd = servicesStartAmt*.1

STARTSIZE = 5 #dimension of traders
MINSIZE = 4 #smallest size of traders
MAXSIZE = 60 #max size of traders

TILESIZE = 4 #used for heatmap

coolingAmtOrig = 13#amount of cooling for heatmap
heatingAmtOrig = 19#amount of heating for heatmap
coolingFREQOrig = 2#for heatmap number of cycles to wait to cool

coolingAmt = coolingAmtOrig #for heatmap
heatingAmt = heatingAmtOrig #for heatmap
coolingFREQ = coolingFREQOrig #for heatmap number of cycles to wait to cool




TRADESIZE = 5 #size of trade graphic
MINTRADESIZE = 4 #maxsize of trade graphic
MAXTRADESIZE = 10 #minsize of trade graphic

#ccVault = 100000#amount of CC avalible to purchase
#ccXng = 1.5#amount of CC avalible to purchase

AVGTRADE = 200#average amount of $ traded
STDTRADE = 225#gaussian standard deviation from average Trade size
MINTRADEAMT = 50#int(AVGTRADE/3.0) #smallest $ trade possible
MAXTRADEAMT = 1000#int(AVGTRADE*3.0) #largest $ trade possible

IMPORTMULT = 4.00 #scaling the effect of market seasonaly
#TRADESCALEFACTOR = 0.8 #was used for scaling trade
IMPORTMULTSTEP=0.5
IMPORTMULTMAX=3.5#20.0

ccPercent = 0.1# Percentage of CC is accepted by retail shops
ccPercentStep = 0.05 # Optional stepping

ccLocalPercent = 1.0 #Percentage of CC accespted by local shops
ccLocalPercentStep = 0.01  # Optional stepping

#ncStartRange = 5000  # Amount of National Currency allocated at start
ncStartAmt = 500#10000  # Amount of National Currency allocated at start
ncStartStd = ncStartAmt*.2  # Amount of National Currency allocated at start
ncEndAmt = 300000  # Optional stepping
ncStepAmt = 500  # Optional stepping

ccStartAmt = 0 #Amount of CC allocated at start
ccStepAmt = 100
ccEndAmt = 5000

maxSavings = 5000 #maxSavings amount of savings
minSavings = 500 #minimum amount of savings
STARTSAVINGS = 0#400*MAXTRADERS #inital bank collateral
fractionalReserve = 0.10

#text_file = open("stats-v043-hpc.csv", "w")

#text_file.write('cclMode, ccPer,ccAmt,ncAmt,NCPur,CCPur,TotPur,exported,AllTrade,NCNumSales,CCNumSales,retailTradeNC,retailTradeCC,retailNC+CC,nonRetailNC, nonRetailCC, nonRetailNC+CC, cycles, bSaved, bLoaned, bDebt, bSavings, bNC\n')



NEIGHBORSEARCHSIZE = 200 #square area of nearest trade partners
MAXNEIGHBORSEARCHSIZE = NEIGHBORSEARCHSIZE*4 #square area of nearest trade partners
NUMTRADEPARTNERS = 5 # total number of trading partners
if MAXTRADERS <=5:
    #numBuddies = MAXTRADERS-1 #those nearest
    NUMTRADEPARTNERS = MAXTRADERS-1 # total number of trading partners
#elif MAXTRADERS >30:
    #numBuddies = MAXTRADERS-1 #those nearest
#    NUMTRADEPARTNERS = 15 # total number of trading partners


#MAXTRADES = 1 # of active trades between Trader and TradePartners
theta = np.linspace(0.0, 2 * np.pi, MAXTRADERS, endpoint=False)
thetawidth = (2*np.pi) / MAXTRADERS
pltColor = 'gold'


TRADEBINTICKS = DAILYCYCLES*3 #count the volume of trade in this many ticks = 1 week
PLTFREQ = TRADEBINTICKS #how often to update the plots automatically

pause = False

if autoMode == True:
    #importMode = False
    #exportMode = False
    #seasonalMode = True#False
    #heatOn = False
    #heatMode = True
    #ccMode = True#False
    #savingsMode = False
    #loanMode = False
    clearingMode = False

ONEYEAR = DAILYCYCLES*365
HALFYEAR = int(ONEYEAR/2.0)
QUARTERYEAR = int(HALFYEAR/2.0)
MONTH = ONEYEAR/12

#Cycles used in autoMode
heatModeCycle = 30*ONEYEAR
importModeCycle = 30*ONEYEAR
exportModeCycle = 30*ONEYEAR#STARTDATE+timedelta(years=30)#30*ONEYEAR#2*MONTH
seasonalModeCycle = 30*ONEYEAR#STARTDATE+timedelta(years=30)#30*ONEYEAR#4*MONTH
ccModeCycle = 30*ONEYEAR#STARTDATE+timedelta(years=30)#30*ONEYEAR#1*ONEYEAR+8*MONTH
savingsModeCycle = 30*ONEYEAR#STARTDATE+timedelta(years=30)#999*0.5*MONTH#1*ONEYEAR+8*MONTH
loanModeCycle = 30*ONEYEAR#STARTDATE+timedelta(years=30)#9999*0.5*MONTH#1*ONEYEAR+8*MONTH
clearingModeCycle = DAILYCYCLES*15#30*ONEYEAR#STARTDATE+timedelta(days=15)#1*int(MONTH/2)
endCycle = 66*ONEYEAR#STARTDATE+timedelta(months=18)#1*ONEYEAR+8*MONTH

repeatCycle = 0#2*ONEYEAR#500*DAILYCYCLES#MONTH#0.25*MONTH#1*ONEYEAR # how long to run in repeatMode
numRepeatsTot = 1


lastRepeatCycle = 0
lastRepeatCycleTicks = 0
numRepeats = 0
overAllCycle = 0

tickLocs            = [1,    30,   60,   90,   120,   150,   180,   210, 240,  270,  300,  330, 350]
#monthTicks          = ('Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun')
 #relative amount of exportationbuying external goods
#seasonalMarketArray = [  .5,  .6,  .4,    .5,    .4, .95,  .5,    .05,  .2,   .6,  .4,  .55,     .5]

monthTicks          = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan')
#seasonalMarketArray = [.05,    .2,   .6,  .4,  .55,   .5,  .5,  .6, .4, .5,  .4,   .95,  .5, .05]
seasonalMarketArray = [.05,    .2,   .4,  .5,  .6,   .4,  .5,  .3, .4, .3,  .9,   1.2,  1.1, .05]



seasonalImportSmooth = []
seasonalImportOrig = []
seasonalImportFlat = []
sRounds = []
importExportRatio = 1.08
DAYSINYEAR=365
rounds = DAYSINYEAR #number of days in a year for seasonality
cycles = 0

def toggleHeatMode(onswitch):
    global heatMode
    global heatingAmt
    global coolingAmt
    heatMode = onswitch
    if heatMode == False: #coolit
        heatingAmt = 0

    else:
        heatingAmt = heatingAmtOrig
        coolingAmt = coolingAmtOrig
        coolingFREQ = coolingFREQOrig
        heatOn=True
    print ("Adjust HeatMap Mode", heatMode)

def toggleCCMode(onswitch,players):
    return
    global ccMode
    ccMode = onswitch
    #ccAmt = 100
    for p in players:
        if ccMode == False: #coolit
            p.cc = []#0
        else:
            p.cc = []#p.STARTCC

    print ("Adjust CC Mode", ccMode)

def toggleSavingsMode(onswitch):
    global savingsMode
    savingsMode = onswitch

    print ("Adjust Savings Mode", savingsMode)

def toggleLoanMode(onswitch):
    global loanMode
    loanMode = onswitch

    print ("Adjust Loan Mode", loanMode)


def toggleImportMode(onswitch):
    global importMode
    importMode = onswitch

    print ("Adjust Import Mode", importMode)


def toggleClearingMode(onswitch):
    global clearingMode
    clearingMode = onswitch

    #print ("Adjust Clearing Mode", clearingMode)

def toggleExportMode(onswitch):
    global exportMode
    exportMode = onswitch
    print ("Adjust export Mode", exportMode)


def toggleBondingMode(onswitch):
    global bondingMode
    global curveImage
    bondingMode = onswitch
    if bondingMode == False:
        for le in legendSprites:
            if le.legendType == utils.EXCHANGE:
                newImage = pygame.image.load('curve.png').convert_alpha()
                curveImage = newImage
                le.image = newImage

        for tt in traders:
            if tt.ownToken == False:
                tt.preferedToken = None
    elif bondingMode == True:
        for le in legendSprites:
            if le.legendType == utils.EXCHANGE:
                newImage = pygame.image.load('curve2.png').convert_alpha()
                #newImage = pygame.transform.rotozoom(newImage, 0, 1.6)
                #utils.fill(newImage,pygame.Color(3, 67, 100, 50))
                curveImage = newImage
                le.image = newImage

        for tt in traders:
            topBal = 0
            topToken = None
            tt.preferedToken = None
            for cci in tt.cc:

                if cci.balance > topBal and cci.token.trading:
                    topBal = cci.balance
                    topToken = cci.token
            if topToken is not None:
                tt.preferedToken = topToken
                print ("prefered token", utils.currencyTypeToString(topToken.tokenID))



    print ("Adjust bondingMode", bondingMode)

def toggleSeasonalMode(onswitch):
    global seasonalMode
    global seasonalImportSmooth
    global seasonalImportOrig
    global seasonalImportFlat
    seasonalMode = onswitch
    if seasonalMode == False:
        seasonalImportSmooth = seasonalImportFlat
    else:
        seasonalImportSmooth = seasonalImportOrig
    print ("Adjust Seasonal Mode ", seasonalMode)

    #return the current day based ont he start day
def cyclesToDate():
    global cycles
    global DAILYCYCLES
    simdays = int(cycles/DAILYCYCLES)

    STARTDATE = datetime.datetime(2018, 8, 7, 00, 00) #1st trading on blockchain of a tomato in Kenya
    #STARTDATE = datetime.datetime(2017, 12, 1, 00, 00)
    currentDate =  STARTDATE+timedelta(days=simdays)
    #print ("Current Date: ",currentDate.isoformat(' '))

    return currentDate #currentDate.day


def cyclesToMonth():
    days = cyclesToDays()
    months = int(days/MONTHS)
    return months

def buddiesMode(event,t):
    #print ("Show everyone who clicked Trader trades with!")
    global clientsModeB
    for z in t.tradeBuddies:
        z.drawCon =True
        z.drawConColor = PURPLE
        z.drawSelf(background)
    clientsModeB = False
    if displayTrade:
        pygame.display.update()

def clientsMode(event,t):
    # If the mouse moves on top of a player - set his fill and his tradebuddies
    #print ("Show everyone who trades with clicked Trader!")
    global clientsModeB
    for z in traders:
        for zt in z.tradeBuddies:
            if zt.rect.center == t.rect.center:
                z.drawCon =True
                z.drawConColor = RED
                z.drawSelf(background)
    clientsModeB = True
    if displayTrade:
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    global pause
    global displayPlots
    global importMode
    global exportMode
    global savingsMode
    global loanMode
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print("<><><>Terminate on Key Press")
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    print("<><><>Terminate on Key Press")
                    terminate()
                elif event.key == pygame.K_SPACE:
                    pause = True
                    print ("PAUSE")
                    paused()
                elif event.key == pygame.K_p:
                    displayPlots = True
                    print ("PLOTS1")
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def paused():

    global pause
    print ("Paused called", pause)
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE: # pressing escape quits
                    print("<><><>Terminate on Key Press")
                    terminate()
                elif event.key == pygame.K_SPACE:
                    pause = False
                elif event.key == pygame.K_p:
                    displayPlots = True
                    print ("PLOTS2")
                return

        pygame.display.update()
        #mainClock.tick(FPS)
        mainClock.tick()

def getGini(allPlayers):
    moneyList = []
    for p in allPlayers:
        moneyList.append(p.nc)
        #print (moneyList)

    result = GRLC(moneyList)

    return float(result[0])

def toggleSeedingMode(traders,mode):

    if False: #mode==True:
        for b in traders:
            if b.subType!=utils.FOREIGNRETAIL:
                b.cc = []#ccStartAmt
                b.STARTCC = ccStartAmt
                b.debt = ccStartAmt

                b.aScale = (STARTSIZE-MINSIZE)/float(1+b.STARTNC+b.STARTSTOCK+b.STARTCC+b.STARTSERVICES)
                b.maxMoney = (MAXSIZE - b.bScale)/b.aScale
                b.minMoney = (MINSIZE - b.bScale)/b.aScale


                theBank.debt = theBank.debt + ccStartAmt
                theBank.savings = theBank.savings + ccStartAmt

                theBank.loaned = theBank.loaned + ccStartAmt
                theBank.saved = theBank.saved + ccStartAmt
    else:
        for b in traders:
            if b.subType!=utils.FOREIGNRETAIL:
                b.cc = []
                b.STARTCC = 0
                b.aScale = (STARTSIZE-MINSIZE)/float(1+b.STARTNC+b.STARTSTOCK+b.STARTCC+b.STARTSERVICES)
                b.maxMoney = (MAXSIZE - b.bScale)/b.aScale
                b.minMoney = (MINSIZE - b.bScale)/b.aScale

                #b.debt = ccStartAmt
        theBank.debt = 0
        theBank.savings = 0

        theBank.loaned = 0
        theBank.saved = 0


def generateTraders(traders):
    global theBank
    global theMarkets
    global TOTALSTARTINGNC
    global numStartCoops
    global clickedTrader
    sCoops = 0
    pCoops = 0
    zIndex = 0
    for i in range(0, pEXPORTSERVICE, 1):
        t = Trader(utils.GENERIC,100,100,zIndex)
        t.setupExportServiceTrader()
        traders.append(t)
        zIndex = zIndex+1
        TOTALSTARTINGNC=TOTALSTARTINGNC+t.nc
    for i in range(0, pRETAIL, 1):
        t = Trader(utils.GENERIC,100,100,zIndex)
        t.setupRetailShop()
        traders.append(t)
        zIndex = zIndex+1
        TOTALSTARTINGNC=TOTALSTARTINGNC+t.nc
    for i in range(0, pFOREIGNRETAIL, 1):
        t = Trader(utils.GENERIC,100,100,zIndex)
        t.setupForeignRetailShop()
        traders.append(t)
        zIndex = zIndex+1
        TOTALSTARTINGNC=TOTALSTARTINGNC+t.nc
    for i in range(0, pLOCALSERVICE, 1):
        t = Trader(utils.GENERIC,100,100,zIndex)

        zIndex = zIndex+1
        TOTALSTARTINGNC=TOTALSTARTINGNC+t.nc
        if sCoops < numStartSCoops:
            t.coop = True
            print("serviceCoop")
            sCoops +=1
        t.setupLocalServices()
        traders.append(t)

    for i in range(0, pLOCALPRODUCER, 1):

        t = Trader(utils.GENERIC,100,100,zIndex)

        zIndex = zIndex+1
        TOTALSTARTINGNC=TOTALSTARTINGNC+t.nc

        if pCoops < numStartPCoops:
            t.coop = True
            print("ProdCoop")
            pCoops +=1
            #t = Trader(utils.GENERIC,OFFSETWIDTH+SUBWINDOWWIDTH/2+BORDERWIDTH/2,OFFSETHEIGHT+SUBWINDOWHEIGHT-BORDERHEIGHT*3-5,zIndex)
        t.setupLocalProduction()
        traders.append(t)

def isntViewable(newPos):

    if newPos[0]>=(BOARDOFFSETX+BOARDSIZEX) or newPos[0]<=BOARDOFFSETX or newPos[1]>=(BOARDOFFSETY+BOARDSIZEY-30) or newPos[1]<=BOARDOFFSETY+30:
        return True
    else:
        return False


def generateTraderLocationsSpiral(traders):

    xinc = 2
    yinc = 2

    radius = 100.0
    rotation = np.pi
    startAngle = 0.0

    numSpokes = 10

    resolution = radius / numSpokes#len(traders)
    #print ("resolution",resolution)
    radiusIncrement = 20#radius / resolution
    rotationIncrement = rotation / resolution
    spokeRotationIncrement = (np.pi * 2.0) / 5#float(numSpokes)
    spokeRotation = startAngle
    direction = 1

    extraOff = 32
    startx = INFOWIDTH+OFFSETWIDTH*2
    endx = WINDOWWIDTH
    starty = extraOff
    endy = WINDOWHEIGHT
    pos = (int(INFOWIDTH+(endx-startx)/2),int((endy-starty)/2))

    #print ("startPos ",pos)
    #keep moving the radius out (will have to stager Trader Types)
    curRadius = radiusIncrement#0.0
    curAngle = spokeRotation

    tradersShuffle = utils.shuffleMix(traders)

    for t in tradersShuffle:

        #if t.coop==True:
        #    continue

        #while curRadius <= radius:
        newx = int(curRadius * np.sin(curAngle))
        newy = int(curRadius * np.cos(curAngle))
        newPos = (pos[0] + newx, pos[1] + (direction * newy))

        if isntViewable(newPos):
            #print(newPos[0])
            #print("x range: ",startx, endx-extraOff,utils.traderTypeToString(t.subType))

            #print(newPos[1])
            #print("y range: ",extraOff,endy-extraOff, utils.traderTypeToString(t.subType))
            direction = direction*-1
            curRadius = radiusIncrement*2.5
            curAngle = spokeRotation#spokeRotationIncrement
            newx = int(curRadius * np.sin(curAngle))
            newy = int(curRadius * np.cos(curAngle))
            newPos = (pos[0] + newx, pos[1] + (direction * newy))
            spokeRotation += spokeRotationIncrement

        t.setLocation(newPos[0],newPos[1])
        collisionRect = True
        collisions=0
        rounda = 0
        tempPos = newPos
        finda = 0
        #print("index",t.tIndex)
        while collisionRect:

            tLocXopy = list(traders)
            tLocXopy.remove(t)
            for odat in tLocXopy:
                odatRect = odat.rect.inflate(5,5)
                if t.rect.colliderect(odatRect) == True or isntViewable(t.rect.center):
                    collisionRect = True
                    collisions=collisions+1
                    #print ("collided", t.rect, odatRect)
                    break

            if collisionRect == True:
                tempPos = (tempPos[0]+xinc,tempPos[1]+yinc)
                t.setLocation(tempPos[0],tempPos[1])
                finda+=1
                if isntViewable(tempPos):
                    #print ("****---",finda)
                    if finda > 300:
                        xinc = xinc*-1
                        yinc = yinc*-1
                        tempPos = (newPos[0]+xinc,newPos[1]+yinc)
                        t.setLocation(tempPos[0],tempPos[1])
                        finda = 0

                    elif finda > 200:
                        xinc = xinc*1
                        yinc = yinc*-1
                        tempPos = (newPos[0]+xinc,newPos[1]+yinc)
                        t.setLocation(tempPos[0],tempPos[1])

                    elif finda > 100:
                        xinc = xinc*-1
                        yinc = yinc*1
                        tempPos = (newPos[0]+xinc,newPos[1]+yinc)
                        t.setLocation(tempPos[0],tempPos[1])



            if collisions==0:
                collisionRect = False
            collisions = 0
            rounda +=1
            #print (rounda)
            if rounda > 600:
                collisionRect = False
                print ("Overlapping Error",round, finda)
                Rx = random.randint(startx, endx)
                Ry = random.randint(starty, endy)
                t.setLocation(Rx,Ry)



        curRadius += radiusIncrement
        curAngle += rotationIncrement

        #pygame.draw.aalines(display, (255, 255, 255), False, spoke)

        #t.setLocation(newPos[0],newPos[1])




def generateTraderLocations(traders):

    extraOff = 10
    #Set location
    traderNumt = 0
    for t in traders:

        #if t.coop==True:
        #    continue
        traderNumt = traderNumt + 1
    #while len(traders) < MAXTRADERS:
        traderLocx = random.randint(INFOWIDTH+OFFSETWIDTH+BORDERWIDTH+STARTSIZE+extraOff, OFFSETWIDTH+SUBWINDOWWIDTH-STARTSIZE-BORDERWIDTH)
        traderLocy = random.randint(OFFSETHEIGHT+BORDERHEIGHT+extraOff, OFFSETHEIGHT+SUBWINDOWHEIGHT-STARTSIZE-BORDERHEIGHT-extraOff)
        t.setLocation(traderLocx,traderLocy)


        #t = Trader(GENERICTRADER,traderLocx,traderLocy,STARTSIZE,theMarkets)
        #largerBankRect = theBank.rect.inflate(50,50)
        #don't overlap on other traders
        collisionRect = False
        maxCollisionChecks = 200
        currentCollisionCheck = 1
        while collisionRect == False and currentCollisionCheck<maxCollisionChecks:
            currentCollisionCheck = currentCollisionCheck +1
            #if currentCollisionCheck == maxCollisionChecks:
            #    print (traderNumt ,"Collision in Locations")

            tLocXopy = list(traders)
            tLocXopy.remove(t)
            for odat in tLocXopy:
                #odatRect = odat.rect.inflate(1,1)
                odatRect = odat.rect.inflate(5,5)
                if t.rect.colliderect(odatRect) == True:
                    collisionRect = True
                    #print ("collided", t.rect, odatRect)
                    break

            if collisionRect == True:
                traderLocx = random.randint(INFOWIDTH+OFFSETWIDTH+BORDERWIDTH+STARTSIZE+extraOff, OFFSETWIDTH+SUBWINDOWWIDTH-STARTSIZE-BORDERWIDTH)
                traderLocy = random.randint(OFFSETHEIGHT+BORDERHEIGHT+extraOff, OFFSETHEIGHT+SUBWINDOWHEIGHT-STARTSIZE-BORDERHEIGHT-extraOff)
                #t = Trader(GENERICTRADER,traderLocx,traderLocy,STARTSIZE,theMarkets)
                t.setLocation(traderLocx,traderLocy)
                collisionRect = False
            else:
                collisionRect = True
                break


def generateTraderLocation(trader):
    global traders
    extraOff = 10
    #Set location
    traderNumt = 0
    if True:

        #if t.coop==True:
        #    continue
        traderNumt = traderNumt + 1
    #while len(traders) < MAXTRADERS:
        traderLocx = random.randint(INFOWIDTH+OFFSETWIDTH+BORDERWIDTH+STARTSIZE+extraOff, OFFSETWIDTH+SUBWINDOWWIDTH-STARTSIZE-BORDERWIDTH)
        traderLocy = random.randint(OFFSETHEIGHT+BORDERHEIGHT+extraOff, OFFSETHEIGHT+SUBWINDOWHEIGHT-STARTSIZE-BORDERHEIGHT-extraOff)
        trader.setLocation(traderLocx,traderLocy)


        #t = Trader(GENERICTRADER,traderLocx,traderLocy,STARTSIZE,theMarkets)
        #largerBankRect = theBank.rect.inflate(50,50)
        #don't overlap on other traders
        collisionRect = False
        maxCollisionChecks = 200
        currentCollisionCheck = 1
        while collisionRect == False and currentCollisionCheck<maxCollisionChecks:
            currentCollisionCheck = currentCollisionCheck +1
            #if currentCollisionCheck == maxCollisionChecks:
            #    print (traderNumt ,"Collision in Locations")

            tLocXopy = list(traders)
            #tLocXopy.remove(trader)
            for odat in tLocXopy:
                #odatRect = odat.rect.inflate(1,1)
                odatRect = odat.rect.inflate(5,5)
                if trader.rect.colliderect(odatRect) == True:
                    collisionRect = True
                    #print ("collided", trader.rect, odatRect)
                    break

            if collisionRect == True:
                traderLocx = random.randint(INFOWIDTH+OFFSETWIDTH+BORDERWIDTH+STARTSIZE+extraOff, OFFSETWIDTH+SUBWINDOWWIDTH-STARTSIZE-BORDERWIDTH)
                traderLocy = random.randint(OFFSETHEIGHT+BORDERHEIGHT+extraOff, OFFSETHEIGHT+SUBWINDOWHEIGHT-STARTSIZE-BORDERHEIGHT-extraOff)
                #t = Trader(GENERICTRADER,traderLocx,traderLocy,STARTSIZE,theMarkets)
                trader.setLocation(traderLocx,traderLocy)
                collisionRect = False
            else:
                collisionRect = True
                break


def generateTradeBuddies(playerList):
    for dude in playerList:
        if dude.subType==utils.FOREIGNRETAIL:
            continue
        currentList = list(playerList)
        currentList.remove(dude)
        #neighborsList = generateNeighbors(dude,currentList,NEIGHBORSEARCHSIZE,numBuddies)

        #while len(dude.tradeBuddies) < numBuddies and len(neighborsList) >0:

        bRETAIL = 0
        bFOREIGNRETAIL = 0
        bLOCALSERVICE = 0
        bLOCALPRODUCER = 0
        bEXPORTSERVICE = 0

        #ensure that one of each type of partner exists

        currentSearchSize = NEIGHBORSEARCHSIZE
        #neighborsList = generateTradeNeighbors(dude,currentList,currentSearchSize,dude.numTradePartners) ######THE1
        neighborsList = generateNeighbors(dude,currentList,currentSearchSize,dude.numTradePartners)
        #print ("Neighbors: ",len(neighborsList))
        #for ne in neighborsList:
        #    print ("<>", traderTypeToString(ne.subType))
        neighborLen = len(neighborsList)

        #while len(dude.tradeBuddies) < dude.numTradePartners and len(neighborsList) >0 and currentSearchSize <= MAXNEIGHBORSEARCHSIZE:
        while len(dude.tradeBuddies) < dude.numTradePartners and currentSearchSize < MAXNEIGHBORSEARCHSIZE:

            neighborLen = len(neighborsList)-1
            #print ("neighbors: ", neighborLen)

            if neighborLen <1:
                #print (currentSearchSize, " search size2")

                #neighborsList = generateTradeNeighbors(dude,currentList,currentSearchSize,dude.numTradePartners)
                currentSearchSize = currentSearchSize+NEIGHBORSEARCHSIZE
                neighborsList = generateNeighbors(dude,currentList,currentSearchSize,dude.numTradePartners)

            if len(neighborsList) > 0:
                newTradeBuddy = random.choice(neighborsList)#neighborsList[neighborIndex]#
                if newTradeBuddy.localSelling==True:
                    dude.tradeBuddies.append(newTradeBuddy)
                    neighborsList.remove(newTradeBuddy)
                    currentList.remove(newTradeBuddy)




def generateNeighbors(dude,players,searchSize,numToFind):
    neighborWidth = searchSize
    neighborHeight = searchSize
    neighbors = []

    oldSearchRect = dude.rect

#    print ("dude.rect: ",dude.rect)
    searchPass = 1
    searchRect = oldSearchRect.inflate(searchSize,searchSize)
    #while len(neighbors)<numToFind:

#        print ("search pass: ", searchPass, searchRect)
    for p in players:
        if p.rect.colliderect(searchRect)==1 and p.rect.colliderect(oldSearchRect)!=1:
            neighbors.append(p)
#                    print ("neighbor ", p.rect)
    #if searchRect.width >= WINDOWWIDTH*2:
    #    print ("a: no more found: search pass: ", searchPass, searchRect, len(neighbors))
    #    return neighbors

    oldSearchRect = searchRect
    searchPass = searchPass +1

    return neighbors



def generateTradeNeighbors(dude,players,searchSize,numToFind):
    neighborWidth = searchSize
    neighborHeight = searchSize
    neighbors = []

    oldSearchRect = dude.rect

    bRETAIL = 0
    bFOREIGNRETAIL = 0
    bLOCALSERVICE = 0
    bLOCALPRODUCER = 0
    #bEXPORTSERVICE = 0


#    print ("dude.rect: ",dude.rect)
    searchPass = 1
    passDiversity = False
    passNumber = False
    passNeighbors = False


    diversityLevel = 0
    while passNeighbors == False:
        searchRect = oldSearchRect.inflate(searchSize,searchSize)
        #print ("search pass: ", searchPass, searchRect)
        for p in players:
            diversityLevel = 0
            #print("Searching Nei")
            if p.rect.colliderect(searchRect)==1 and p.rect.colliderect(oldSearchRect)!=1:
                neighbors.append(p)
                #passNeighbors = True

                if p.subType == utils.RETAIL:
                    bRETAIL = bRETAIL+1
                elif p.subType == utils.FOREIGNRETAIL:
                    bFOREIGNRETAIL = bFOREIGNRETAIL+1
                elif p.subType == utils.LOCALSERVICE:
                    bLOCALSERVICE = bLOCALSERVICE+1
                elif p.subType == utils.LOCALPRODUCER:
                    bLOCALPRODUCER = bLOCALPRODUCER+1

                if bRETAIL >= 1 and tRETAIL == 1:
                    diversityLevel = diversityLevel + 1
                if bFOREIGNRETAIL >= 1 and tFOREIGNRETAIL  == 1:
                    diversityLevel = diversityLevel + 1
                if bLOCALPRODUCER >= 1 and tLOCALPRODUCER == 1:
                    diversityLevel = diversityLevel + 1
                if bLOCALSERVICE >= 1 and tLOCALSERVICE == 1:
                    diversityLevel = diversityLevel + 1

                if diversityLevel >= diversityLevelMax:
                    passDiversity = True
                    #print ("Passed Diversity")
                if len(neighbors)>=numToFind:
                    passNumber = True
                    #print ("Passed Number")
                if passNumber and passDiversity:
                    passNeighbors = True

                #print "neighbor ", p.rect


        if searchRect.width >= WINDOWWIDTH*4:
            return neighbors

        oldSearchRect = searchRect
        searchPass = searchPass +1

    return neighbors


class heatSurf(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        #self.surface = pygame.Surface((TILESIZE, TILESIZE), HWSURFACE|DOUBLEBUF)
        #self.image = pygame.Surface((TILESIZE, TILESIZE))#, HWSURFACE|DOUBLEBUF)
        self.image = pygame.Surface((TILESIZE, TILESIZE), HWSURFACE|DOUBLEBUF)
        self.heat = 0 #goes from cold = 0 ... to maxheat
        self.rect = self.image.get_rect(topleft=pos)
        self.image.set_colorkey(BLACK)
        self.image.fill(BLACK)
    #def drawSelf(self,theSurface):


class legendDude(pygame.sprite.Sprite):
    def __init__(self,nimage,pos,traderType):
        pygame.sprite.Sprite.__init__(self)
        self.legendType = traderType
        #self.surface = pygame.Surface((TILESIZE, TILESIZE), HWSURFACE|DOUBLEBUF)
        #self.image = pygame.Surface((TILESIZE, TILESIZE))#, HWSURFACE|DOUBLEBUF)
        self.image = nimage #pygame.Surface((TILESIZE, TILESIZE), HWSURFACE|DOUBLEBUF)
        self.rect = self.image.get_rect(topleft=pos)
        #self.image.set_colorkey(BLACK)
        #self.image.fill(BLACK)

                    #background.blit(self.image, self.rect.center)

class Trade:
    def __init__(self,currency,amount,tradeType,source,dest,token):
        self.tradeType = tradeType
        self.token=token

        self.currency = currency
        self.money = int(amount)

        self.source = source
        self.dest = dest
        self.size = TRADESIZE*(amount/AVGTRADE)
        if self.size < MINTRADESIZE:
            self.size = MINTRADESIZE
        if self.size > MAXTRADESIZE:
            self.size = MAXTRADESIZE

        #self.locx = source.rect.topleft[0]
        #self.locy = source.rect.topleft[-1]

        self.locx = source.rect.centerx
        self.locy = source.rect.centery


        #self.destLocx = dest.rect.bottomright[0]
        #self.destLocy = dest.rect.bottomright[-1]

        self.destLocx = dest.rect.centerx
        self.destLocy = dest.rect.centery


        self.heating = True#False
        self.heating = NCHEAT



        if utils.isCC(currency):#if currency == utils.CC:
            self.heating = CCHEAT
            #self.nc = 0

            #self.locx = source.rect.bottomleft[0]
            #self.locy = source.rect.bottomleft[-1]

            self.locx = source.rect.centerx
            self.locy = source.rect.top

            #self.destLocx = dest.rect.topright[0]
            #self.destLocy = dest.rect.topright[-1]

            self.destLocx = dest.rect.centerx
            self.destLocy = dest.rect.top

        if self.dest.traderType ==  utils.EXTERNALMARKET or self.dest.traderType == utils.BANK:
            self.destLocx = dest.rect.centerx
            self.destLocy = dest.rect.centery

            if utils.isCC(currency):#if currency == utils.CC:
                self.darkColor = DARKERGREEN
                self.lightColor = DARKGREEN
            else:
                self.darkColor = DARKERORANGE
                self.lightColor = DARKORANGE



        if self.source.traderType ==  utils.EXTERNALMARKET or self.source.traderType == utils.BANK:
            self.locx = source.rect.centerx
            self.locy = source.rect.centery
            #self.CELLSIZE = 3
            if utils.isCC(currency):#if currency == utils.CC:
                self.darkColor = DARKERGREEN
                self.lightColor = DARKGREEN
            else:
                self.darkColor = DARKERORANGE
                self.lightColor = DARKORANGE



        #self.wormLength = 4
        self.maxWormLength = 10
        self.wormLength = 6

        self.wormLength = int(self.wormLength*(self.money/AVGTRADE))
        if self.wormLength <1:
            self.wormLength =1
        elif self.wormLength > self.maxWormLength:
            self.wormLength =self.maxWormLength



        self.wormCoords = [{'x': self.locx,     'y': self.locy}]
        self.rect = pygame.Rect(self.locx,self.locy, self.size, self.size)
#        self.surface = subSurface
        #self.surface = pygame.transform.scale(traderImage, (int(self.size), int(self.size)))
        #print (self.size)
        self.surface = pygame.Surface((int(self.size), int(self.size)), HWSURFACE|DOUBLEBUF)

        if self.tradeType ==  utils.EXTSERVICES or self.tradeType==utils.EXTSTOCK or  self.tradeType==utils.DEPOSIT or self.tradeType==utils.LOAN or self.tradeType==utils.CLEARING or self.tradeType==utils.DIVIDEND or self.tradeType==utils.SAVINGS or self.tradeType==utils.FEES:
            self.heating=False

    #drawing a trade
    def drawSelf(self,theSurface):
        global clickedToken
        #keep track of where the trade has gone and draw all segments up to a max length
        aaa = 1
        for coord in self.wormCoords:
#            print aaa, coord
            aaa = aaa +1
            if aaa > self.wormLength+1:
                print ("WORM ERROR", len(self.wormCoords))
                break
            x = coord['x']
            y = coord['y']
            #wormSegmentRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
            #pygame.draw.rect(theSurface, self.darkColor, wormSegmentRect)
            #wormInnerSegmentRect = pygame.Rect(x + 2, y + 2, self.CELLSIZE-1, self.CELLSIZE-1)
            #pygame.draw.rect(theSurface, self.lightColor, wormInnerSegmentRect)

            if utils.isCC(self.currency):#==utils.CC:
                toImage = None
                if self.currency == clickedToken:

                    #newImage = pygame.transform.rotozoom(newImage, 0, 1.6)
                    toImage = pygame.transform.rotozoom(self.token.spriteImg, 0, 2)
                    utils.fill(toImage,pygame.Color(223, 230, 200, 50))
                    #print("a",toImage)
                else:
                    toImage = self.token.spriteImg
                    #print("b",toImage)
                background.blit(toImage, (x, y))
                #background.blit(wormCCInnerSegmentRect,(x + 2, y + 2))
                #background.blit(wormCCSegmentRect,(x, y))

            elif self.currency==utils.NC:
                background.blit(ncImage, (x, y))
                #background.blit(wormNCInnerSegmentRect,(x + 2, y + 2))
                #background.blit(wormNCSegmentRect,(x, y))

    def move(self):
        mright = self.destLocx - self.rect.centerx
        mtop = self.destLocy - self.rect.centery
        if  mright > 0 and mright >= TRADEMOVERATE :
            self.rect.move_ip(1 * TRADEMOVERATE,0)
            #                    print ("move right")
        elif mright > 0 and mright <= TRADEMOVERATE:
            self.rect.move_ip(1 * mright,0)
            #                    print ("move right2")
        elif mright < 0 and -1*mright >= TRADEMOVERATE:
            self.rect.move_ip(-1 * TRADEMOVERATE,0)
            #                    print ("move left")
        elif mright < 0 and -1*mright <= TRADEMOVERATE:
            self.rect.move_ip(mright,0)
            #                    print ("move left2")

        elif mtop >0 and mtop >= TRADEMOVERATE:
            self.rect.move_ip(0, 1 * TRADEMOVERATE)
            #                    print ("move down")
        elif mtop >0 and mtop <= TRADEMOVERATE:
            self.rect.move_ip(0, 1 * mtop)
            #                    print ("move down2")
        elif mtop < 0 and -1*mtop >= TRADEMOVERATE:
            self.rect.move_ip(0, -1 * TRADEMOVERATE)
            #                    print ("move up")
        elif mtop < 0 and -1*mtop <= TRADEMOVERATE:
            self.rect.move_ip(0, mtop)
            #                    print ("move up2")

    def hasArrived(self):

        #don't let it arrrive till the last of the tail
        #if the head has arrived - delete it
        #

        if len(self.wormCoords) == 1:
            #mright = self.destLocx - self.wormCoords[0]['x']
            #mtop = self.destLocy - self.wormCoords[0]['y']

            mright = self.destLocx - self.rect.centerx
            mtop = self.destLocy - self.rect.centery
            if abs(mright) < TRADEMOVERATE and abs(mtop) < TRADEMOVERATE:

                return True
            else:

                return False
        else:
            mright = self.destLocx - self.wormCoords[0]['x']
            mtop = self.destLocy - self.wormCoords[0]['y']
            if abs(mright) < TRADEMOVERATE and abs(mtop) < TRADEMOVERATE:
                self.wormLength = self.wormLength - 1
                self.heating=False

            return False


    def validate(self):
        sourceMoney = self.source.nc
        destMoney = self.dest.nc
        if utils.isCC(self.currency): #if self.currency == utils.CC:
            sourceMoney = self.source.getCCValueToken(self.currency)
            destMoney = self.dest.getCCValueToken(self.currency)

        if self.tradeType == utils.LOCALTRADESTOCK:
            if sourceMoney >= self.money and self.dest.stock >= (self.money):
                #print "valid"
                return True
            #elif sourceMoney >= self.dest.stock and self.dest.stock < (self.money):
            #    self.money = self.dest.stock #reduce to the amount of stock of destination
            #    return True
            #elif sourceMoney < self.money and self.money >0 and self.dest.stock >= (sourceMoney):
            #    self.money = sourceMoney #reduce the amount purchased to the sources money
            #    return True
            else:
                #print "inside validate: Stock Trade fail: trade money: ", self.money, " source.money ", sourceMoney ," dest stock: ", self.dest.stock
                return False
        if self.tradeType == utils.LOCALTRADESERVICES:
            if sourceMoney >= self.money and self.dest.services >= (self.money):
                return True
            #elif sourceMoney >= self.dest.services and self.dest.services < (self.money):
            #    self.money = self.dest.services #reduce to the amount of services of destination
            #    return True
            #elif sourceMoney < self.money and self.money >0 and self.dest.services >= (sourceMoney):
            #    self.money = sourceMoney #reduce the amount purchased to the sources money
            #    return True
            else:
                #print ("inside validate: Services Trade fail: trade money: ", self.money, " source.money ", sourceMoney ," dest services: ", self.dest.stock)
                return False


        elif self.tradeType == utils.FEES:

            if self.source.nc >= self.money:
                return True
            else:
                #print "Error FEES", utils.traderTypeToString(self.source.subType)
                return False


        elif self.tradeType == utils.EXTSTOCK:
            # money going from market to trader
            #dest = Trader
            #source = market
            self.source.bankTrading == False
            if self.dest.stock >= self.money and sourceMoney >= self.money:
                #if self.source.traderType == EXTERNALMARKET:
                #    print "verified EXTSTOCK money source = market"

                #if self.dest.traderType == EXTERNALMARKET:
                    #print "verified EXTSTOCK market = dest. source money", sourceMoney, currencyTypeToString(self.currency)

                #print "Verified EXTSTOCK : dest.stock", self.dest.stock, " trade amt: ",self.money

                return True
            else:

                if self.dest.stock < self.money and self.dest.stock > 0:
                    #print "pre fixed: trade amt: ", self.money, " dest.stock", self.dest.stock
                    #print "dest type:", self.dest.traderType
                    #print "source type:",self.source.traderType
                    self.money = self.dest.stock
                    if self.money > sourceMoney and sourceMoney > 0:
                        self.money = sourceMoney
                    #print "fixed: trade amt: ", self.money

                    return True

                if sourceMoney < self.money:
                    self.money = sourceMoney
                    return True

                if self.dest.traderType == utils.EXTERNALMARKET:
                    #print "failed verified EXTSTOCK market = dest"
                    print ("Failed to verify EXTSTOCK : dest.stock", self.dest.stock, " trade amt: ",self.money, " source.money: ", sourceMoney)



                return False
        elif self.tradeType == utils.EXTSERVICES:
            # money going from market to trader
            #dest = Trader
            #source = market
            if self.dest.services >= self.money and sourceMoney >= self.money:
                #if self.source.traderType == EXTERNALMARKET:
                    #print "verified EXTSERVICES money source = market"
                return True
            else:
                #print "Failed to verify EXTSERVICES : dest.services", self.dest.services, " trade amt: ",self.money

                if self.dest.services < self.money and self.dest.services > 0:
                    self.money = self.dest.services
                    if self.money > sourceMoney and sourceMoney > 0:
                        self.money = sourceMoney

                    return True

                return False
        else:
            print ("ERROR unknown trade type: ", self.tradeType)
            return False


    #depending on type of trade do a
    #sell/purchase,
    #makeDeposit/acceptDeposit,
    #giveLoan/acceptLoan
    #purchaseImport           /theMarket.sellExport
    #theMarket.purchaseExport/sellExport

    def completeTrade(self):

        selfMoney = self.money
        sourceMoney = self.source.nc
        destMoney = self.dest.nc
        if utils.isCC(self.currency):#if self.currency == utils.CC:
            sourceMoney = self.source.cc
            destMoney = self.dest.cc

        if self.tradeType == utils.LOCALTRADESTOCK:

            if self.dest.sellStock(selfMoney,self.currency) and self.source.purchaseStock(selfMoney,self.currency):
                #self.dest.adjustSize()
                #self.source.adjustSize()
                #print ("Stock Purchase ", self.money)
                return True
            else:
                #print ("Fail Stock Purchase ")
                return False

        if self.tradeType == utils.LOCALTRADESERVICES:
            if self.dest.sellServices(selfMoney,self.currency) and self.source.purchaseServices(selfMoney,self.currency):
                #self.dest.adjustSize()
                #self.source.adjustSize()
                return True
            else:
                return False
        elif self.tradeType ==  utils.CLEARING:
            if self.source.makeClearing(selfMoney,self.currency) and self.dest.acceptClearing(selfMoney,self.currency):
                #if self.dest.traderType != utils.BANK:
                #    self.dest.adjustSize()
                return True
            else:
                #print ("Error Clearing")
                return False

        elif self.tradeType ==  utils.DIVIDEND:
            if self.source.giveDividend(selfMoney,self.currency) and self.dest.acceptDividend(selfMoney,self.currency): #source = bank, dest = other
                #if self.dest.traderType != utils.BANK:
                #    self.dest.adjustSize()
                return True
            else:
                print ("Error Clearing")
                return False


        elif self.tradeType == utils.EXTSTOCK:
            if self.source.purchaseExportedStock(selfMoney) and self.dest.sellStockToMarket(selfMoney):
                #if self.dest.traderType == EXTERNALMARKET:
                #    print ("c EXTSTOCK dest = market & source = ", traderTypeToString(self.source.subType))

                #elif self.source.traderType == EXTERNALMARKET:
                #    print ("c EXTSTOCK source = market & dest = ", traderTypeToString(self.dest.subType))


                #if self.dest.traderType==utils.GENERIC:
                #    self.dest.adjustSize()

                #elif self.source.traderType==utils.GENERIC:
                #    self.source.adjustSize()

                return True
            else:

                #if self.dest.traderType == EXTERNALMARKET:
                print ("failed EXTSTOCK source = market - selling stock")

                return False
        elif self.tradeType == utils.EXTSERVICES:
            #source = source of money ... = market, dest = dude
            if self.source.purchaseExportedServices(selfMoney) and self.dest.sellServicesToMarket(selfMoney):
                #if self.source.traderType == EXTERNALMARKET:
                #    print ("c EXTSERVICES source = market & dest = ", traderTypeToString(self.dest.subType))

                #elif self.dest.traderType == EXTERNALMARKET:
                #    print ("c EXTSERVICES dest = market & source = ", traderTypeToString(self.source.subType))

                #if self.source.subType==FOREIGNRETAIL:
                #    print ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")

                #if self.dest.traderType==utils.GENERIC:
                #    self.dest.adjustSize()

                #elif self.source.traderType==utils.GENERIC:
                #    self.source.adjustSize()

                return True
            else:
                #if self.source.traderType == EXTERNALMARKET:
                print ("failed EXTSERVICES source = market")
                print ("dest services: ",self.dest.services)

                return False
        else:
            print ("UNKNOWN trade type :", self.tradeType)


class WalletToken:
    def __init__(self,token, balance):
        self.token = token
        self.balance = balance
        #starting value is 1:1 with national currency

    def getValue(self):
        return self.balance*self.token.price


class Token:
    def __init__(self,tokenID, supply, connector, cw,trading,spriteImg):
        self.tokenType = utils.CC
        self.tokenID = tokenID
        self.supply = supply
        self.cw = cw
        self.spriteImg = spriteImg
        self.connector = connector #if connector = null it is not convertable
        self.trading = trading
        if connector is None:
            self.connectorBalance = 0
            self.cw = 0
            self.price = 1
        else:
            self.connectorBalance = self.supply*self.cw
            self.cw = cw #connector weight
            self.price = self.connectorBalance/(self.supply*self.cw)

        #starting value is 1:1 with national currency
    def adjustPrice(self):
        if self.connector is None:
            self.price = 1
        else:
            self.price = self.connectorBalance/(self.supply*self.cw)


#Basic Economic Trader
class Trader:
    def __init__(self,traderType,locx,locy,zIndex):
        self.traderType = traderType
        self.tIndex = zIndex
        self.preferedToken = None

        self.numTradePartners = NUMTRADEPARTNERS
        self.image = pygame.Surface((STARTSIZE, STARTSIZE))
        self.rect = pygame.Rect(locx,locy, STARTSIZE, STARTSIZE)
        #self.surface = pygame.transform.scale(traderImage, (STARTSIZE, STARTSIZE))
        #self.surface = pygame.Surface((STARTSIZE, STARTSIZE))

        #self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC)
        self.aScale = 0.1
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale
        self.lastLoanAmt = 0

        self.subType = traderType
        self.coop = False
        self.ownToken = False
        self.size = STARTSIZE
        self.locx = locx
        self.locy = locy
        self.color = GREY
        self.originalColor = GREY
        self.fillColor = GREY
        self.ringColor = GREY
        self.ringWidth = 1
        self.originalRingColor = GREY
        self.originalFillColor = GREY
        self.startColor = GREY
        self.fill = 1
        self.shape = None
        self.STARTCC=0#ccStartAmt
        self.STARTNC=0#ncStartAmt
        self.STARTSTOCK=0#ncStartAmt
        self.STARTSERVICES=0#ncStartAmt
        self.minTradeAccepted=MINTRADEAMT

        self.nc = self.STARTNC
        self.cc = [] #self.STARTCC

        self.stock = self.STARTSTOCK# [10,2,4,43] [2,2,1] [99]
        #buy stocks of type ABCDEFG.....
        #sell stock of type  A.....
        #base stock is autogenerated [12]
        #which can be sold .... or turned into [0,6]
        #which can be sold .... or turned into [0,0,2]
        #2A=1B. 2B=1C, 2C=1D

        #competition for stock



        self.services = self.STARTSERVICES



        self.tradeBuddies = [] #this are people that the player always trades with
        self.tradeBuddiesIndex = 0 #this are people that the player always trades with
        self.closestMarket = None
        if self.traderType != utils.EXTERNALMARKET:
            self.closestMarket = theMarkets[0]

        self.trades = [] #list of trades
        self.tradeInfo = [] #list of trades for display



        self.waitToTradeCycles = int(DAILYCYCLES/1.0) #daily make X purchases per day
        self.waitToTradeCyclesOrig = int(DAILYCYCLES/1.0) #daily make 5 purchases per day
        if self.waitToTradeCycles <= 0:
            self.waitToTradeCycles = 1 #daily make 2 purchases per day
        self.waitToConsumeStockCycles = DAILYCYCLES #daily
        self.waitToGrowStockCycles = DAILYCYCLES*2 #daily
        self.waitToGrowServicesCycles = DAILYCYCLES*1  #daily
        self.waitToConsumeServices = DAILYCYCLES*2 #daily
        self.waitToDepositCycles = DAILYCYCLES*2 #weekly
        self.waitToLoanCycles =  DAILYCYCLES*7#monthly
        self.waitToClearCycles =  DAILYCYCLES*7#monthly
        self.waitToDividendCycles =  DAILYCYCLES*30#monthly
        self.waitToFeesCycles = int(7*DAILYCYCLES/1.0)
        self.waitToDefaultCycles = int(30*DAILYCYCLES/1.0)

        self.waitToImportCycles = DAILYCYCLES #exporting labor
        self.waitToExportCyclesOrig = DAILYCYCLES*8 #exporting labor
        self.waitToExportCycles = self.waitToExportCyclesOrig #exporting labor

        self.waitToSwitchExportingModeCycles = int(DAILYCYCLES*15) #daily make 5 purchases per day
        '''
        self.lastDefaultCycle  = int(random.random()*self.waitToDefaultCycles)
        self.lastFeeCycle  = int(random.random()*self.waitToFeesCycles)
        self.lastNCTradeCycle = int(random.random()*self.waitToTradeCycles)
        self.lastCCTradeCycle = int(random.random()*self.waitToTradeCycles)
        self.lastSwitchofExportingModeCycle = int(random.random()*self.waitToExportCyclesOrig)
        self.lastLoanCycle = int(random.random()*self.waitToLoanCycles)
        self.lastDepositCycle = int(random.random()*self.waitToDepositCycles)
        self.lastImportCycle = int(random.random()*self.waitToImportCycles)
        self.lastExportCycle = int(random.random()*self.waitToExportCycles)
        self.lastStockConsumptionCycle = int(random.random()*self.waitToConsumeStockCycles)
        self.lastServicesConsumptionCycle = int(random.random()*self.waitToConsumeServices)
        self.lastServicesGrowthCycle = int(random.random()*self.waitToGrowServicesCycles)
        self.lastStockGrowthCycle = int(random.random()*self.waitToGrowStockCycles)
        self.lastClearingCycle = int(random.random()*self.waitToClearCycles)
        '''

        self.lastDefaultCycle  = self.waitToDefaultCycles/(self.tIndex+3)
        self.lastFeeCycle  = self.waitToFeesCycles/(self.tIndex+3)
        self.lastNCTradeCycle = self.waitToTradeCycles/(self.tIndex+3)
        self.lastCCTradeCycle = self.waitToTradeCycles/(self.tIndex+3)
        self.lastSwitchofExportingModeCycle = self.waitToExportCyclesOrig/(self.tIndex+3)
        self.lastLoanCycle = self.waitToLoanCycles/(self.tIndex+3)
        self.lastDepositCycle = self.waitToDepositCycles/(self.tIndex+3)
        self.lastImportCycle = self.waitToImportCycles/(self.tIndex+3)
        self.lastExportCycle = self.waitToExportCycles/(self.tIndex+3)
        self.lastStockConsumptionCycle = self.waitToConsumeStockCycles/(self.tIndex+3)
        self.lastServicesConsumptionCycle = self.waitToConsumeServices/(self.tIndex+3)
        self.lastServicesGrowthCycle = self.waitToGrowServicesCycles/(self.tIndex+3)
        self.lastStockGrowthCycle = self.waitToGrowStockCycles/(self.tIndex+3)
        self.lastClearingCycle = self.waitToClearCycles/(self.tIndex+3)


        self.lastDividendCycle = 0


        self.stockConsumptionRate = STOCKCONSUMPTIONRATE
        self.stockGrowthRate = STOCKGROWTHRATE
        self.servicesGrowthAmount = 0
        self.costToGrowStock = STOCKGROWTHRATE


        self.savings = 0
        self.debt = 0

        self.saved = 0
        self.loaned = 0

        self.imported = 0
        self.exported = 0
        self.localSelling = True
        self.exporting = True
        self.importing = True
        self.bankTrading = False # waiting to trade
        self.defaulting = False
        self.drawCon = False
        self.drawConColor = LIGHTBLUE

        self.profit = 0.2 #20% for each sale of stock Trader makes a profit of self.profit

        self.minPUsageCC = MINPUSAGECC#0.20 #fraction of sales vs usage of CC
        #self.minP


        self.purchasesNC = 0
        self.purchasesCC = 0
        self.deposits = 0
        self.clearingAmt = 0
        self.salesNC = 0
        self.salesCC = 0
        self.numSalesNC = 0
        self.numSalesCC = 0
        self.tradeNum = 0


    def reset(self):

        self.size = STARTSIZE
        self.color = GREY
        self.originalColor = GREY
        self.fillColor = GREY
        self.ringColor = GREY
        self.ringWidth = 1
        self.originalRingColor = GREY
        self.originalFillColor = GREY
        self.startColor = GREY
        self.fill = 1
        self.shape = None
        self.STARTCC=0#ccStartAmt
        self.STARTNC=0#ncStartAmt
        self.STARTSTOCK=0#ncStartAmt
        self.STARTSERVICES=0#ncStartAmt

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES
        self.lastLoanAmt = 0

        del self.trades[:]
        self.trades = [] #list of trades
        del self.tradeInfo[:]
        self.tradeInfo = [] #list of errors


        self.waitToTradeCycles = int(DAILYCYCLES/1.0) #daily make 5 purchases per day
        self.waitToTradeCyclesOrig = int(DAILYCYCLES/1.0) #daily make 5 purchases per day
        if self.waitToTradeCycles <= 0:
            self.waitToTradeCycles = 1 #daily make 2 purchases per day
        self.waitToConsumeStockCycles = DAILYCYCLES #daily
        self.waitToGrowStockCycles = DAILYCYCLES*2 #daily
        self.waitToGrowServicesCycles = DAILYCYCLES*1  #daily
        self.waitToConsumeServices = DAILYCYCLES*2 #daily
        self.waitToDepositCycles = DAILYCYCLES*4 #weekly
        self.waitToLoanCycles =  DAILYCYCLES*7#monthly
        self.waitToImportCycles = DAILYCYCLES #exporting labor
        self.waitToClearCycles =  DAILYCYCLES*7#monthly
        self.waitToExportCyclesOrig = DAILYCYCLES*8 #exporting labor
        self.waitToExportCycles = self.waitToExportCyclesOrig #exporting labor
        self.waitToSwitchExportingModeCycles = int(DAILYCYCLES*15) #daily make 5 purchases per day
        self.waitToDividendCycles =  DAILYCYCLES*30#monthly
        self.waitToFeesCycles = int(7*DAILYCYCLES/1.0)
        self.waitToDefaultCycles = int(30*DAILYCYCLES/1.0)


        self.lastDefaultCycle  = self.waitToDefaultCycles/(self.tIndex+3)
        self.lastFeeCycle  = self.waitToFeesCycles/(self.tIndex+3)
        self.lastNCTradeCycle = self.waitToTradeCycles/(self.tIndex+3)
        self.lastCCTradeCycle = self.waitToTradeCycles/(self.tIndex+3)
        self.lastSwitchofExportingModeCycle = self.waitToExportCyclesOrig/(self.tIndex+3)
        self.lastLoanCycle = self.waitToLoanCycles/(self.tIndex+3)
        self.lastDepositCycle = self.waitToDepositCycles/(self.tIndex+3)
        self.lastImportCycle = self.waitToImportCycles/(self.tIndex+3)
        self.lastExportCycle = self.waitToExportCycles/(self.tIndex+3)
        self.lastStockConsumptionCycle = self.waitToConsumeStockCycles/(self.tIndex+3)
        self.lastServicesConsumptionCycle = self.waitToConsumeServices/(self.tIndex+3)
        self.lastServicesGrowthCycle = self.waitToGrowServicesCycles/(self.tIndex+3)
        self.lastStockGrowthCycle = self.waitToGrowStockCycles/(self.tIndex+3)
        self.lastClearingCycle = self.waitToClearCycles/(self.tIndex+3)
        self.lastDividendCycle = 0

        self.stockConsumptionRate = STOCKCONSUMPTIONRATE
        self.stockGrowthRate = STOCKGROWTHRATE
        self.servicesGrowthAmount = 0
        self.costToGrowStock = STOCKGROWTHRATE


        self.savings = 0
        self.debt = 0
        self.saved = 0
        self.loaned = 0
        self.imported = 0
        self.exported = 0
        self.localSelling = True
        self.exporting = True
        self.importing = True
        self.bankTrading = False # waiting to trade
        self.defaulting = False
        self.drawCon = False
        self.drawConColor = LIGHTBLUE

        self.profit = 0.2 #20% for each sale of stock Trader makes a profit of self.profit
        self.minPUsageCC = MINPUSAGECC#0.20 #fraction of sales vs usage of CC


        self.debt = 0
        self.purchasesNC = 0
        self.purchasesCC = 0
        self.deposits = 0
        self.clearingAmt = 0
        self.salesNC = 0
        self.salesCC = 0
        self.numSalesNC = 0
        self.numSalesCC = 0
        self.tradeNum = 0
        self.tradeBuddiesIndex=0

    def getNextBuddy(self):
        if self.tradeBuddiesIndex >= len(self.tradeBuddies):
            self.tradeBuddiesIndex = 0
        bud = self.tradeBuddies[self.tradeBuddiesIndex]
        self.tradeBuddiesIndex +=1
        return bud

    def addTradeList(self,tt):
        if displayPlots:
            self.tradeNum = self.tradeNum +1
            tradeInfo = ""
            if tt.dest.tIndex==self.tIndex:
                tradeInfo = '%s: sold %s%s of %s, to %s' % (self.tradeNum,int(tt.money),utils.currencyTypeToString(tt.currency), utils.tradeTypeToString(tt.tradeType), utils.traderTypeToString(tt.source.subType))
            else:
                tradeInfo = '%s: bought %s%s of %s, from %s' % (self.tradeNum,int(tt.money),utils.currencyTypeToString(tt.currency), utils.tradeTypeToString(tt.tradeType), utils.traderTypeToString(tt.dest.subType))
            #print(tradeInfo)
            self.tradeInfo.insert(0,tradeInfo)
            if len(self.tradeInfo) > 18:
                del self.tradeInfo[18:]

    def convertAllCC(self,destToken,tokenList,deleteDest):
        #traderRem = self
                    #remove traders tokens from circulation or sell back to SC
        for wtkn in self.cc:
            #print ("pre remove token:", utils.currencyTypeToString(wtkn.token.tokenID), "bal:", wtkn.balance,wtkn.token.price)
            if wtkn.token.tokenID != destToken.tokenID:
                if utils.convert(wtkn.balance,wtkn.token,destToken):
                    wtkn.balance = 0
                    #print ("post remove token:", utils.currencyTypeToString(wtkn.token.tokenID), "bal:", wtkn.balance, wtkn.token.price)
                else:
                    print("convert Fail 1")

        if deleteDest == True:
            for wtkn in self.cc:
                if wtkn.token.tokenID == destToken.tokenID:
                    wtkn.balance = 0
                    print("remove destToken itself():", utils.currencyTypeToString(wtkn.token.tokenID))

    def addTrade(self,tt):
        if self.subType != utils.BANK:
            self.trades.append(tt)

        #addTradeList(self,tt):

    def setupExportServiceTrader(self):
            #print ("retail shop")

        self.subType=utils.EXPORTSERVICE

        self.STARTCC=0
        self.STARTNC=0
        self.STARTNC=ncStartAmt#random.gauss(ncStartAmt,ncStartStd)
        if self.STARTNC<=0:
            self.STARTNC = 0
        self.STARTSTOCK=0
        self.STARTSERVICES=servicesStartAmt#random.gauss(servicesStartAmt,servicesStartStd)
        if self.STARTSERVICES<=0:
            self.STARTSERVICES = 0

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES

        self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC+self.STARTSERVICES)
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale

        self.stockGrowthRate = 0 #does not produce own stock - must buy from market
        self.stockConsumptionRate = 3000
        self.waitToConsumeStockCycles = DAILYCYCLES*2 #daily

        self.servicesGrowthAmount = self.STARTSERVICES#int(100*MAXTRADERS/5) #each day they have this much to offer
        self.waitToGrowServicesCycles = DAILYCYCLES

        self.color = DARKORANGE
        self.originalColor = DARKORANGE

        self.ringColor = DARKGREEN
        self.originalRingColor = DARKGREEN


        self.fillColor = BLUE
        self.originalFillColor = BLUE

        self.fill = 1
        self.shape = utils.TRIANGLE
        self.image = workerImage
        self.exporting = True
        self.importing = False
        self.localSelling = True#False
        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))


    def setupRetailShop(self):
            #print ("retail shop")
        self.subType=utils.RETAIL

        self.STARTCC=0
        self.STARTNC=ncStartAmt#random.gauss(ncStartAmt,ncStartStd)
        if self.STARTNC<=0:
            self.STARTNC = 0

        #self.STARTNC=random.randint(0,ncStartAmt)
        #self.STARTSTOCK=500
        self.STARTSTOCK=stockStartAmt#random.gauss(stockStartAmt,stockStartStd)
        if self.STARTSTOCK<=0:
            self.STARTSTOCK = 0

        self.STARTSERVICES=0

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES

        self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC+self.STARTSERVICES)
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale

        self.stockGrowthRate = 0 #does not produce own stock - must buy from market
        self.stockConsumptionRate = 0
        self.servicesGrowthAmount = 0 #a chance to grow once broke

        self.color = DARKORANGE
        self.originalColor = DARKORANGE
        self.fillColor = GREEN
        self.originalFillColor = GREEN
        self.ringColor = DARKGREEN
        self.originalRingColor = DARKGREEN

        self.fill = 1
        self.shape = utils.RETAILSQUARE
        self.image = retailShopImage
        self.exporting = False
        self.importing = True
        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))

    #print ("retail shop whom spends all money in the external market")
    def setupForeignRetailShop(self):

        self.subType=utils.FOREIGNRETAIL

        self.STARTCC=0
        self.STARTNC=0
        #self.STARTSTOCK=500
        self.STARTSTOCK=stockStartAmt#random.gauss(stockStartAmt,stockStartStd)
        if self.STARTSTOCK<=0:
            self.STARTSTOCK = 0

        self.STARTSERVICES=0

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES

        self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC+self.STARTSERVICES)
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale

        self.stockGrowthRate = 0 #does not produce own stock - must buy from market
        self.stockConsumptionRate = 0
        self.servicesGrowthAmount = 0 #a chance to grow once broke

        self.color = DARKRED
        self.originalColor = self.color

        self.ringColor = DARKRED
        self.originalRingColor = DARKRED

        self.fillColor = RED
        self.originalFillColor = RED

        self.fill = 1
        self.shape = utils.FRETAILSQUARE
        self.image = foreignRetailShopImage
        self.exporting = False
        self.importing = True
        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))

    def setupLocalServices(self):
        #print ("local services")

        self.subType=utils.LOCALSERVICE

        self.STARTCC=0#ccStartAmt
        self.STARTNC=ncStartAmt#random.gauss(ncStartAmt,ncStartStd)
        if self.STARTNC<=0:
            self.STARTNC = 0

        #self.STARTNC=random.randint(0,ncStartAmt)
        self.STARTSTOCK=0
        self.STARTSERVICES=servicesStartAmt#random.gauss(servicesStartAmt,servicesStartStd)
        if self.STARTSERVICES<=0:
            self.STARTSERVICES = 0

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES

        self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC+self.STARTSERVICES)
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale
        self.shape = utils.CIRCLE

        self.stockGrowthRate = 0 #does not produce own stock - must buy from market
        self.waitToConsumeStockCycles = DAILYCYCLES*2 #daily
        self.stockConsumptionRate = 300

        self.servicesGrowthAmount = 500#int(100*MAXTRADERS/5) #each day they have this much to offer
        self.waitToGrowServicesCycles = DAILYCYCLES

        self.color = DARKGREEN
        self.originalColor = self.color
        self.ringColor = DARKGREEN
        self.originalRingColor = DARKGREEN

        self.fillColor = GREEN
        self.originalFillColor = GREEN


        self.fill = 1
        self.exporting = False
        self.importing = False

        self.image = serviceShopImage

        if self.coop==True:
            self.color=GREEN
            self.originalColor=GREEN
            #self.setSize(int(STARTSIZE*2))
            #self.shape=utils.BANKCIRCLE
            self.fillColor=DARKRED
            self.originalFillColor=DARKRED
            self.ringColor = GREEN
            self.originalRingColor = GREEN
            self.numtradepartners=MAXTRADERS-1
            self.image = coopServicesShopImage

            initialCC = 10000
            if masterWallet.balance <initialCC:
                initalCC = masterWallet.balance
            self.cc.append(WalletToken(reserveToken,initialCC))
            masterWallet.balance = masterWallet.balance - initialCC

        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))




    def setupLocalProduction(self):
        #print ("local production")

        self.subType=utils.LOCALPRODUCER

        self.STARTCC=0#ccStartAmt
        self.STARTNC=ncStartAmt#random.gauss(ncStartAmt,ncStartStd)
        if self.STARTNC<=0:
            self.STARTNC = 0

        #self.STARTNC=random.randint(0,ncStartAmt)
        self.STARTSTOCK=stockStartAmt#random.gauss(stockStartAmt,stockStartStd)
        if self.STARTSTOCK<=0:
            self.STARTSTOCK = 0



        self.STARTSERVICES=0

        self.nc = self.STARTNC
        self.cc = []#self.STARTCC
        self.stock = self.STARTSTOCK
        self.services = self.STARTSERVICES

        self.aScale = (STARTSIZE-MINSIZE)/float(1+self.STARTNC+self.STARTSTOCK+self.STARTCC+self.STARTSERVICES)
        self.bScale = MINSIZE
        self.maxMoney = (MAXSIZE - self.bScale)/self.aScale
        self.minMoney = (MINSIZE - self.bScale)/self.aScale


        self.stockGrowthRate = self.STARTSTOCK
        self.waitToGrowStockCycles = DAILYCYCLES
        self.stockConsumptionRate =2
        self.waitToConsumeStockCycles = DAILYCYCLES*3
        self.servicesGrowthAmount = 0

        self.color = DARKGREEN
        self.originalColor = self.color

        self.ringColor = DARKGREEN
        self.originalRingColor = DARKGREEN


        self.fillColor = GREEN
        self.originalFillColor = GREEN

        self.shape = utils.DIAMOND
        self.image = productionShopImage
        self.fill = 1
        self.exporting = False
        self.importing = False

        if self.coop==True:
            self.color=GREEN
            self.originalColor=GREEN
            #self.setSize(int(STARTSIZE*2))
            #self.shape=utils.BANKCIRCLE
            self.fillColor=DARKRED
            self.originalFillColor=DARKRED
            self.ringColor = GREEN
            self.originalRingColor = GREEN
            self.numtradepartners=MAXTRADERS-1
            self.image = coopProductionShopImage
            initialCC = 10000
            if masterWallet.balance <initialCC:
                initalCC = masterWallet.balance
            self.cc.append(WalletToken(reserveToken,initialCC))
            masterWallet.balance = masterWallet.balance - initialCC

        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))

    def setupMarket(self):
        if importMode:
            self.color=YELLOW
        else:
            self.color=YELLOW

        self.color=DARKRED
        self.originalColor=DARKRED
        self.fillColor=DARKORANGE
        self.originalFillColor=DARKORANGE
        self.ringColor = DARKORANGE
        self.originalRingColor = DARKORANGE

        self.shape=utils.MARKETSQUARE
        self.image = marketImage
        #self.setSize(int(STARTSIZE*3))
        self.fill = 1
        self.stock = np.inf #sys.maxsize
        self.services = np.inf #sys.maxsize
        self.nc = np.inf #sys.maxsize
        self.cc = []#0
        self.profit = 0.05 # 20% markup on goods sold
        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))

    def setupExchange(self):
        if importMode:
            self.color=YELLOW
        else:
            self.color=YELLOW

        self.color=DARKRED
        self.originalColor=DARKRED
        self.fillColor=DARKORANGE
        self.originalFillColor=DARKORANGE
        self.ringColor = DARKORANGE
        self.originalRingColor = DARKORANGE

        self.shape=utils.MARKETSQUARE
        self.image = curveImage
        #self.setSize(int(STARTSIZE*3))
        self.fill = 1
        self.stock = 0 #sys.maxsize
        self.services = 0 #sys.maxsize
        self.nc = 0 #sys.maxsize
        self.cc = []#0
        self.profit = 0.05 # 20% markup on goods sold
        self.exporting = False
        self.importing = False

        self.rect=self.image.get_rect(topleft=(self.locx,self.locy))

    def setupBank(self):
        self.color=GREEN
        self.originalColor=GREEN
        #self.setSize(int(STARTSIZE*2))
        self.shape=utils.BANKCIRCLE
        self.fillColor=DARKRED
        self.originalFillColor=DARKRED
        self.ringColor = GREEN
        self.originalRingColor = GREEN

        self.fill = 1
        self.nc = 0
        self.cc = []#0
        self.stock = 0
        self.savings = STARTSAVINGS
        self.debt = 0
        self.saved = 0
        self.loaned = 0
        self.profit = 0.00 # 10% interest on loans

    def setLocation(self,locx,locy):
        self.locx = locx
        self.locy = locy
        self.rect = self.image.get_rect(topleft=(locx,locy))

    def getCCValue(self):
        value = 0

        for cci in self.cc:
            if True:#cci.token.trading:
                value = value+cci.getValue()
        return value

    def getCCTradableValue(self):
        value = 0

        for cci in self.cc:
            if cci.token.trading:
                value = value+cci.getValue()
        return value

    def getCCValueToken(self,currencyID):
        value = 0

        for cci in self.cc:
            if cci.token.tokenID == currencyID:
                value = value+cci.getValue()
        return value


    def cleanCCList(self): #on purchase (not exchange)
        ccn = self.cc.copy()
        self.cc.clear()
        self.cc = []
        for cci in ccn:
            if cci.balance >0:
                self.cc.append(cci)

    def adjustCCValue(self,change,currencyID): #on purchase (not exchange)

        #print("pre Change:",change,"Total CC:",self.getCCValue())
        if change <0:


            if -1*change>self.getCCValue(): #not enough to purchase here
                print("Not enough CC!")

                #return LookupError
            else:
                for cci in self.cc:
                    if cci.token.tokenID == currencyID:
                        ccVal = cci.getValue()#total individual CC value
                        remainder = ccVal - -1*change
                        if remainder >=0:
                            #adjust the number of tokens
                            newVal = ccVal+change
                            cci.balance=newVal/cci.token.price
                            break
                        else: #not enough in that CC alone
                         change = remainder
                         #print("looping to find enough cc")
                         #continue

        elif change >0: #adding CC. Check if CC already exists and add balance, otherwise add it to the list
            foundCC = False
            for cc in self.cc:
                if cc.token.tokenID == currencyID:
                    cc.balance = cc.balance +change/cc.token.price
                    foundCC=True
                    #print("Found it CC abc")
                    break
            if foundCC==False:
                #for token in tokens:
                   # print("IDs: ",currencyID,token.tokenID)
                    #if token.tokenID == currencyID:
                tToken = None# Token(currencyID, 1, reserveToken, defaultCW, True)
                for tk in tokens:
                    #print(tk.tokenID, currencyID)
                    if tk.tokenID == currencyID:
                        tToken =tk
                        #print("Found token")
                        break
                if tToken is None:
                    print("NONE FOUND!")
                wToken = WalletToken(tToken,change/tToken.price)
                self.cc.append(wToken)
                foundCC=True
                if self.preferedToken is None: # the first time you get a new token you prefer that one
                    self.preferedToken = tToken
                #        break
            if foundCC==False:
                print("Token not found ERROR",len(self.cc))
        #self.cleanCCList()
        #print("post Change:",change,"Total CC:",self.getCCValue())



    def adjustSize(self):
        return
        self.size = self.rect.width
        newMoney = self.nc+self.stock+self.getCCValue()+self.services-self.debt
        newSize = self.aScale*(newMoney)+self.bScale
        #print ("size: ", self.size, " newSize: ",newSize)
        #print ("money: ", self.money, " amt: ",amt)
        #sizeChange = int(round(newSize - self.size))
        #print ("sizeChange: ", sizeChange)

        if newMoney <= self.minMoney:
            newSize = MINSIZE
            #sizeChange = int(round(MINSIZE - self.size))
            #self.color=RED
            #print ("MIN ",sizeChange)
        elif newMoney >= self.maxMoney:
            newSize = MAXSIZE
            #self.color=GREEN
            #print ("MAX ",sizeChange)
        #elif newMoney > minMoney and newMoney <maxMoney:
            #self.color=GREY

        sizeChange = newSize - self.size

        if sizeChange != 0:
            center = self.rect.center
            #print ("self.rect.width: ",self.rect.width)
            self.rect.inflate_ip(sizeChange,sizeChange)
            #print ("self.rect.width: ",self.rect.width)
            newCenter = self.rect.center
            if newCenter[0] != center[0] and newCenter[1] != center[1]:
                xChange = center[0] - newCenter[0]
                yChange = center[1] - newCenter[1]
                self.rect.move_ip(xChange,yChange)
            self.size = self.rect.width

        if self.size <=0:
            print ("ERROR negative size")
        #print ("final size: ",self.size)

    def setSize(self,size):
        return
        self.size = size
        self.rect = pygame.Rect(self.rect.left,self.rect.top, size, size)
        #self.surface = pygame.transform.scale(traderImage, (size, size))
        self.surface = pygame.Surface((STARTSIZE, STARTSIZE))

    def purchaseStock(self,amt,currency): #buy something - remove money
        global pause
        selfMoney = self.nc
        if utils.isCC(currency):
            selfMoney = self.getCCValue()
        if selfMoney < amt:
            print ("ERROR!!!!!!!!!!!!!!!!!!!! purchase stock amount: ", amt, " money: ", selfMoney, utils.currencyTypeToString(currency))
            return False

        if utils.isCC(currency):
            self.adjustCCValue(-amt,currency) #self.cc = self.cc - amt
            self.purchasesCC = self.purchasesCC + amt
        else:
            self.nc = self.nc - amt
            self.purchasesNC = self.purchasesNC + amt

        #consume all stock - no resale
        #self.stock = self.stock + amt #- int(self.profit*amt)
        return True
#        print ("purchase: New Stock: ", self.stock)
#        print ("purchase final size: ", self.size, "final Money: ", self.money)


    def purchaseServices(self,amt,currency): #buy something - remove money
        global pause
        selfMoney = self.nc
        if utils.isCC(currency):
            selfMoney = self.getCCValue()
        if selfMoney < amt:
            print ("ERROR!!!!!!!!!!!!!!!!!!!! service purchase amount: ", amt, " money: ", selfMoney, utils.currencyTypeToString(currency))
            return False



        #self.services = self.services + amt service is consumed (can't be resold
        if utils.isCC(currency): #remove CC in a sequence
            self.adjustCCValue(-amt,currency) #self.cc = self.cc - amt
            self.purchasesCC = self.purchasesCC + amt
        else:
            self.nc = self.nc - amt
            self.purchasesNC = self.purchasesNC + amt


        return True
#        print ("purchase: New Stock: ", self.stock)
#        print ("purchase final size: ", self.size, "final Money: ", self.money)

    def sellStock(self,amt,currency): #sell something = adding money
        global pause
        if (self.stock) < (amt): #refund the money?
            print ("ERROR not enough stock!", utils.currencyTypeToString(currency), utils.traderTypeToString(self.subType))
            #pause = True
            #self.tradebuddy = False
            return False
        #print ("<<Sale>>")

        self.stock = self.stock - amt+int(self.profit*amt)
        #self.money = self.money + amt

        if utils.isCC(currency): #remove CC in a sequence
            self.adjustCCValue(amt,currency) #self.cc = self.cc - amt
            self.salesCC = self.salesCC + amt
            self.numSalesCC = self.numSalesCC +1
        else:
            self.nc = self.nc + amt
            self.salesNC = self.salesNC + amt
            self.numSalesNC = self.numSalesNC +1

        return True


    def sellServices(self,amt,currency): #sell something = adding money
        global pause

        if (self.services) < int(amt): #refund the money
            print ("ERROR not enough services (sellSerive)!")
            #pause = True
            #self.tradebuddy = False
            return False
        #print ("<<Sale>>")

        self.services = self.services-amt+int(self.profit*amt)
        #self.money = self.money + amt
        if utils.isCC(currency): #remove CC in a sequence
            self.adjustCCValue(amt,currency) #self.cc = self.cc - amt
            self.salesCC = self.salesCC + amt
            self.numSalesCC = self.numSalesCC +1
        else:
            self.nc = self.nc + amt
            self.salesNC = self.salesNC + amt
            self.numSalesNC = self.numSalesNC +1

        return True

    def purchaseExportedStock(self,amt):  #purchases some stock from Market
        if self.nc < amt:
            print ("ERROR not enough money to purchase Expored Stock")
            return False

        #if self.traderType != utils.EXTERNALMARKET:
        #    print ("Crazy Market 1 ")
        #    print ("old Stock:", self.stock, " nc:", self.nc, " amt:", amt, " new stock:", self.stock + amt +amt*self.profit, traderTypeToString(self.subType))


        self.nc = self.nc-amt #buy stock for less from the market
        self.stock = self.stock + amt +amt*self.profit
        #print ("new Stock: ", self.stock)
        self.imported = self.imported+amt   #this counts as a export if viewed from theMarket
        self.bankTrading = False
        #if self.traderType == EXTERNALMARKET:
        #    print ("self = External Market: purchaseExportedStock amt:",amt)
        #    print ("market exported:",self.exported , " imported: ", self.imported)


        return True


    def purchaseExportedServices(self,amt):  #the market purchases some services
        if self.traderType != utils.EXTERNALMARKET:
            self.nc = self.nc-amt
        self.imported = self.imported+amt   #this counts as a export if viewed from theMarket


       # if self.traderType == EXTERNALMARKET:
       #     print ("self = External Market: purchaseExportedServices amt:",amt)
       #     print ("market exported:",self.exported , " imported: ", self.imported)

        return True

    def sellStockToMarket(self,amt):  #the trader sells stock to the externalMarket
        if self.stock < amt:#+amt*self.profit):
            print ("ERROR not enough stock to Export!: money:", amt, " stock: ", self.stock)
            return False



        #if self.traderType == EXTERNALMARKET:
        #    print ("self = External Market: sellExportedStock amt:",amt)
        #    print ("market exported:",self.exported , " imported: ", self.imported)

        self.nc = self.nc+amt
        #the stock was purchased for this amt and should resold at a higher rate.
        self.stock = self.stock-amt#-int(amt-amt*self.profit)
        self.exported = self.exported+amt#-amt*self.profit



        return True

    def sellServicesToMarket(self,amt):  #the trader sells services like labour to the  externalMarket
        if self.services < int(amt):
            print ("ERROR not enough services to Export!: money:", amt, " services: ", self.services)
            return False

        if self.traderType == utils.EXTERNALMARKET:
            #print ("self = External Market: sellExportedServices amt:",amt)
            self.nc = self.nc+amt
            self.exported = self.exported+amt#-amt*self.profit
            #print ("market exported:",self.exported , " imported: ", self.imported)
            return True
        else:
            self.nc = self.nc+amt
            self.services = int(self.services-amt+amt*self.profit)
            self.exported = self.exported+amt-amt*self.profit
            return True


    def acceptDividend(self,amt,currency):

        if self.traderType == utils.BANK: #this is theBank
            print ("Error acceptDivi, ", utils.traderTypeToString(self.traderType) )
            return False

        if amt <= self.debt:
            self.debt = self.debt - amt
        elif amt > self.debt:
            payOff = amt - b.debt
            self.debt=0
            self.nc = self.nc+payOff

        self.bankTrading = False

        return True

    def giveDividend(self,amt,currency): #this is the bank

        if self.traderType != utils.BANK: #this is theBank
            print ("Error giveDivi")
            return False

        self.savings = self.savings - amt

        self.bankTrading = False
        return True




    def acceptClearing(self,amt,currency):

        if self.traderType == utils.BANK: #this is theBank

            if currency == utils.NC:
                print ("ERROR! in acceptClearing NC")
                return False

            self.debt = self.debt-amt

            return True
        else: #this is not the Bank
            if utils.isCC(currency):#if currency == utils.CC:
                print ("ERROR! in acceptClearing CC")
                return False

            self.nc = self.nc+amt
            self.clearingAmt = self.clearingAmt +amt

            return True

        print ("Error in AcceptClearing")
        return False


    #a market or bank
    def drawSelf(self,theSurface):
        global traders
        if clickedTrader == self.tIndex and moveTrader:
            self.rect.center = pygame.mouse.get_pos()
            self.locx = self.rect.left
            self.locy = self.rect.top
            for trds in traders:
                for ztrades in trds.trades:
                    if ztrades.dest.tIndex == self.tIndex:
                        ztrades.destLocx = self.rect.centerx
                        ztrades.destLocy = self.rect.centery


        background.blit(self.image, (self.rect.x, self.rect.y))

        outerLineRect = self.image.get_rect(topleft=(self.locx,self.locy)).inflate(5,5)

        if self.defaulting:
            pygame.draw.rect(theSurface, self.ringColor, outerLineRect, 1)

        if self.drawCon:
            pygame.draw.rect(theSurface, self.drawConColor, outerLineRect, 2)

        if clickedTrader == self.tIndex:
            pygame.draw.rect(theSurface, BLUE, outerLineRect, 3)




    #EXPORT GOODS - the market to buy goods or services from community
    #the market is in charge of this .... and it is seasonal
    def marketLogistics(self,theTraders):
        global cycles
        currentTraders = list(theTraders)

        if exportMode and cycles - self.lastExportCycle >= self.waitToExportCycles:
            zCurrentRounds = cycles
            seasonLen = len(seasonalImportSmooth)

            date = cyclesToDate()
            day_of_year = date.timetuple().tm_yday

            today = day_of_year#date.day

            if today > seasonLen:
                print("wrong date error!:",today, seasonLen)
                today = today % seasonLen


            #print (day_of_year, today, date.month, seasonLen)

            currentSeasonalExportMult = seasonalImportSmooth[today-1]#*(exportMult)
            #print ("<><>month: ",date.month,day_of_year,currentSeasonalExportMult)
            self.waitToExportCycles = self.waitToExportCyclesOrig*(1-currentSeasonalExportMult)


            for b in currentTraders: #convert stock and services into cash
                #theTradeBuddy = random.choice(currentTraders)
                theTradeBuddy = b
                if b.exporting == False:
                    continue

                if b.exporting == False:
                    print ("Fuu Error")

                isExportingAlready = False
                for tt in b.trades:
                    if tt.tradeType == utils.EXTSTOCK or tt.tradeType == utils.EXTSERVICES:
                        isExportingAlready = True
                        break

                if isExportingAlready == True:
                    continue
                if isExportingAlready == True:
                    print ("CONTINUE?!?! not working")

                dest = theTradeBuddy.rect

                #tradeRand=0
                #if currentSeasonalExportMult >=0:#.4:
                #exportAmt = int(AVGTRADE*IMPORTMULT*currentSeasonalExportMult)
                exportAmt = int(random.gauss(AVGTRADE,STDTRADE)*IMPORTMULT*currentSeasonalExportMult)

                if exportAmt <=MINTRADEAMT:
                    exportAmt = MINTRADEAMT
                tradebuddy = True

                #foo = random.randint(1,10)
                tradeType = utils.EXTSERVICES

                #tradeType = EXTSTOCK
                if b.subType == utils.EXPORTSERVICE or b.subType == utils.LOCALSERVICE:
                    tradeType = utils.EXTSERVICES
                    if b.services < exportAmt and b.services > 0:
                        exportAmt = b.services
                    elif b.services == 0:
                        exportAmt = 0

                else: #LOCALPRODUCER
                    tradeType = utils.EXTSTOCK #
                    if b.stock < exportAmt and b.stock > 0:
                        exportAmt = b.stock
                    elif b.stock == 0:
                        exportAmt = 0


                #if b.subType == FOREIGNRETAIL:
                #    if b.stock < exportAmt and b.stock > 0:
                #        exportAmt = b.stock

                #elif b.stock < exportAmt and b.stock > 0:
                #    exportAmt = b.stock
                #print ("export labour amt: ", exportAmt)


                if exportAmt>0:
                    tradebuddy=True
                    newExportTrade = Trade(utils.NC,exportAmt,tradeType,b.closestMarket,theTradeBuddy,None)
                    #b.trades.append(newExportTrade)
                    b.addTrade(newExportTrade)
                    self.lastExportCycle = cycles

                else:
                    tradebuddy = False




    #General trade and converstion to CC
    def logistics(self):
        global cycles
        global lastTokenID
        global lastColorTokenIndex
        alreadyImporting = False
        alreadyBanking = False
        if len(self.trades) > 0:
            for st in self.trades:
                if st.tradeType == utils.EXTSERVICES or st.tradeType == utils.EXTSTOCK:
                    alreadyImporting = True
                elif st.tradeType==utils.DEPOSIT or st.tradeType==utils.LOAN or st.tradeType==utils.CLEARING or st.tradeType==utils.DIVIDEND:
                    alreadyBanking = True
                else:
                    return

        selfLocalTrading = True
        if (self.subType == utils.RETAIL or self.subType == utils.FOREIGNRETAIL) and importMode == False:
            selfLocalTrading = False

        #if (self.subType == utils.EXPORTSERVICE) and exportMode == False:
        #    selfLocalTrading = False



        denomTSF = float(self.nc+self.getCCValue()+self.stock+self.services+1.0+self.savings)
        numeratorTSF = float(self.STARTNC+self.STARTCC+self.STARTSTOCK+self.STARTSERVICES+1.0)
        tradeSpeedFactor = 1
        if denomTSF <=0:
            tradeSpeedFactor = 10000000
        else:
            tradeSpeedFactor = numeratorTSF/denomTSF

        self.waitToTradeCycles =  int(self.waitToTradeCyclesOrig*(tradeSpeedFactor)) #more money more trading = shorter wait time

        if self.waitToTradeCycles < DAILYCYCLES/6:
            self.waitToTradeCycles = DAILYCYCLES/6

        if self.waitToTradeCycles > DAILYCYCLES*6:
            self.waitToTradeCycles = DAILYCYCLES*6


        numcBuddies = len(self.tradeBuddies)

        #TRADE with other TRADERS
        if self.nc+self.getCCValue() >= AVGTRADE and self.traderType == utils.GENERIC and cycles - self.lastNCTradeCycle >= self.waitToTradeCycles and numcBuddies >0 and selfLocalTrading and self.subType != utils.FOREIGNRETAIL:

            #if cycles - self.lastNCTradeCycle >= 400*self.waitToTradeCycles:
            #    print("waiting to trade!!!", utils.traderTypeToString(self.subType), self.tIndex)

            #if retail shop - only buy something if with profits ... only buy enough to replenish stock, or services with profits ... and don't consume your selling stock
            cBuddies = list(self.tradeBuddies)
            tradebuddy = False
            tradeType = utils.LOCALTRADESTOCK
            tradeAmtOrig = int(round(random.gauss(AVGTRADE,STDTRADE)))#AVGTRADE#
            #print ("tradeAmt: ", tradeRand, " assets:", self.nc+self.cc+self.stock+self.services+1.0+self.savings, tradeSpeedFactor)
            tradeAddition = 0#int(round(TRADESCALEFACTOR*AVGTRADE*(float(self.nc+self.cc+self.stock+self.services)/float(self.STARTNC+self.STARTCC+self.STARTSTOCK+self.STARTSERVICES)-1.0)))
            if tradeAmtOrig < MINTRADEAMT:
                tradeAmtOrig = MINTRADEAMT


            while len(cBuddies)>0:
                theTradeBuddy = self.getNextBuddy()#random.choice(cBuddies)

                if theTradeBuddy.localSelling == False or selfLocalTrading == False:
                    tradebuddy = False
                    cBuddies.remove(theTradeBuddy)

                elif theTradeBuddy.subType == utils.RETAIL or theTradeBuddy.subType == utils.FOREIGNRETAIL or theTradeBuddy.subType == utils.LOCALPRODUCER:
                    tradeType = utils.LOCALTRADESTOCK
                    if theTradeBuddy.stock >=tradeAmtOrig:
                        tradebuddy = True
                        break
                    elif theTradeBuddy.stock >=theTradeBuddy.minTradeAccepted:
                        tradeAmtOrig = theTradeBuddy.stock
                        tradebuddy = True
                        break

                    else:
                        tradebuddy = False
                        cBuddies.remove(theTradeBuddy)


                elif theTradeBuddy.subType == utils.LOCALSERVICE or theTradeBuddy.subType == utils.EXPORTSERVICE and theTradeBuddy.localSelling:
                    tradeType = utils.LOCALTRADESERVICES
                    if theTradeBuddy.services >=tradeAmtOrig:
                        tradebuddy = True
                        break
                    elif theTradeBuddy.services >=theTradeBuddy.minTradeAccepted:
                        tradeAmtOrig = theTradeBuddy.services
                        tradebuddy = True
                        break

                    else:
                        tradebuddy = False
                        cBuddies.remove(theTradeBuddy)
                else:
                    tradebuddy = False
                    cBuddies.remove(theTradeBuddy)


            dest = theTradeBuddy.rect


            if tradebuddy==True:

                tradeNCAmt = 0
                tradeCCAmt = 0
                #print (" zself NC ",self.nc, " self CC", self.cc,  "tradeRand: ",tradeRand ,  " Add: ",tradeAddition, " tradeAmt: ", tradeAmt )


                if theTradeBuddy.subType != utils.FOREIGNRETAIL:
                    tradeNCAmt = tradeAmtOrig
                    tradeCCAmt = 0

                    if self.getCCTradableValue()+self.nc >= tradeAmtOrig:

                        #Try a division of the price between CC and NC
                        if self.getCCTradableValue()> 0:#  and theTradeBuddy.defaulting == False:
                            if theTradeBuddy.subType !=utils.RETAIL: #local producer and services
                                tradeCCAmt = ccLocalPercent*tradeAmtOrig
                                tradeNCAmt = (1-ccLocalPercent)*tradeAmtOrig
                                missingAmt = 0
                                if tradeNCAmt > self.nc:
                                    missingAmt = tradeNCAmt - self.nc
                                    tradeCCAmt = tradeCCAmt + missingAmt
                                if tradeCCAmt > self.getCCTradableValue():
                                    missingAmt = tradeCCAmt - self.getCCTradableValue()
                                    tradeNCAmt = tradeNCAmt + missingAmt

                            else: #retail
                                tradeCCAmt = ccPercent*tradeAmtOrig
                                tradeNCAmt = (1-ccPercent)*tradeAmtOrig
                                if tradeNCAmt > self.nc:
                                    tradeNCAmt = 0
                                    tradeCCAmt = 0



                else: #trading with a FOREIGN RETAILER or a defaulter
                    tradeNCAmt = tradeAmtOrig
                    tradeCCAmt = 0
                    if self.nc < tradeAmtOrig:
                        tradeNCAmt = self.nc
                        tradeCCAmt = 0
                        #tradeNCAmt = 0

                if self.subType == utils.RETAIL or self.coop:
                    myProfit = self.getCCTradableValue()-(self.STARTNC-self.nc)-(self.STARTSTOCK-self.stock)-self.debt
                    if tradeNCAmt > myProfit:
                        tradeNCAmt = 0

                if tradebuddy == True:

                    tradeNCAmt = int(round(tradeNCAmt))
                    tradeCCAmt = int(round(tradeCCAmt))

                    #print ("Trades from:", traderTypeToString(self.subType), self.nc, self.cc," to: ",traderTypeToString(theTradeBuddy.subType),  self.stock, self.services, "profit: ",self.nc-(self.STARTSTOCK-self.stock), " NC: ", tradeNCAmt, " CC: ", tradeCCAmt, "orig: ",int(tradeAmtOrig))

                    if(tradeNCAmt >MAXTRADEAMT):
                        tradeNCAmt=MAXTRADEAMT

                    if(tradeCCAmt >MAXTRADEAMT):
                        tradeCCAmt=MAXTRADEAMT

                    if tradeNCAmt>=1:

                        newTrade = Trade(utils.NC,tradeNCAmt,tradeType,self,theTradeBuddy,None)
                        self.addTrade(newTrade)
                        self.lastNCTradeCycle = cycles

                    if tradeCCAmt>=1:# and theTradeBuddy.defaulting == False:
                        #choose the CCs!!!
                        newTradeCC = None
                        #if not self.coop:
                            #print("non Coop: ", tradeCCAmt, len(self.cc), self.getCCValue())
                        preferedToken = theTradeBuddy.preferedToken

                        if preferedToken is not None:

                            for cci in self.cc:
                                if cci.token.trading == True and tradeCCAmt >= 1 :
                                    #print("I'm in",cci.token.trading, "coop",self.coop)
                                    if cci.getValue() >= tradeCCAmt:
                                        if cci.token.tokenID == preferedToken.tokenID:
                                            newTradeCCa = Trade(cci.token.tokenID, tradeCCAmt, tradeType, self, theTradeBuddy,cci.token)
                                            self.addTrade(newTradeCCa)
                                            tradeCCAmt = 0
                                    elif cci.getValue() < tradeCCAmt and cci.getValue() > 1 and cci.token.tokenID == preferedToken.tokenID:
                                        newTradeCCb = Trade(cci.token.tokenID, cci.balance, tradeType, self, theTradeBuddy,cci.token)
                                        self.addTrade(newTradeCCb)
                                        #print("Trade cc 2",tradeCCAmt)
                                        tradeCCAmt = tradeCCAmt - cci.getValue()

                            if True and tradeCCAmt >= 1: #still missing
                                for cci in self.cc:
                                    if cci.token.trading == True and tradeCCAmt >= 1:
                                        #print("I'm in",cci.token.trading, "coop",self.coop)
                                        if cci.getValue() >= tradeCCAmt and cci.token.tokenID != preferedToken.tokenID:
                                            if bondingMode == False: #no conversion
                                                continue
                                            numTokens = tradeCCAmt/cci.token.price
                                            #print("pre convert a: from:",cci.balance,cci.token.price," to:",preferedToken.price,"numTokens: ",numTokens,"tradeCCAmt",tradeCCAmt)

                                            if utils.convert(numTokens,cci.token,preferedToken):


                                                newTradeCCa = Trade(preferedToken.tokenID, tradeCCAmt, tradeType, self,theTradeBuddy, preferedToken)
                                                self.addTrade(newTradeCCa)

                                                foundPref = False
                                                for ccj in self.cc:
                                                    if ccj.token.tokenID == preferedToken.tokenID:
                                                        ccj.balance += numTokens
                                                        #print("*added Balance: ", ccj.balance)
                                                        foundPref = True
                                                        #print("Found")
                                                        break
                                                if foundPref == False:
                                                    #print("Not Founda")
                                                    wToken = WalletToken(preferedToken,numTokens)
                                                    self.cc.append(wToken)

                                                cci.balance = cci.balance-numTokens
                                                tradeCCAmt = 0
                                                #print("post convert a: from:",cci.balance,cci.token.price," to:",preferedToken.price,"numTokens: ",numTokens,"tradeCCAmt",tradeCCAmt)
                                        elif cci.getValue() < tradeCCAmt and cci.getValue() >= 1 and cci.token.tokenID != preferedToken.tokenID:
                                            #print("pre convert b: from:",cci.token.price," to:",preferedToken.price)
                                            if bondingMode == False:
                                                continue

                                            if utils.convert(cci.balance,cci.token, preferedToken):
                                                newTradeCCb = Trade(preferedToken.tokenID, cci.balance, tradeType, self, theTradeBuddy, preferedToken)
                                                self.addTrade(newTradeCCb)
                                                #print("Trade cc 2",tradeCCAmt)
                                                tradeCCAmt = tradeCCAmt - cci.getValue()
                                                foundPref = False
                                                for ccj in self.cc:
                                                    if ccj.token.tokenID == preferedToken.tokenID:
                                                        ccj.balance += cci.balance
                                                        #print("added Balance -b: ", ccj.balance)
                                                        foundPref = True
                                                        #print("Found")
                                                        break

                                                if foundPref == False:
                                                    #print("Not Found1")
                                                    wToken = WalletToken(preferedToken,cci.balance)
                                                    self.cc.append(wToken)

                                                cci.balance = 0

                                                #print("Converted b: from:",cci.token.price," to:",preferedToken.price)
                        if tradeCCAmt >= 1:

                            for cci in self.cc:
                                #print("I'm inAAA",cci.token.trading,cci.token.tokenID,"coop",self.coop)
                                if cci.token.trading == True and tradeCCAmt >= 1 and preferedToken is None:
                                    #print("I'm in",cci.token.trading, "coop",self.coop)
                                    if cci.getValue() >= tradeCCAmt:
                                        newTradeCCa = Trade(cci.token.tokenID, tradeCCAmt, tradeType, self, theTradeBuddy,cci.token)
                                        self.addTrade(newTradeCCa)
                                        #print("TradeCCA1",tradeCCAmt)
                                        tradeCCAmt = 0
                                    elif cci.getValue() < tradeCCAmt and cci.getValue() >= 1 and preferedToken is None:
                                        newTradeCCb = Trade(cci.token.tokenID, cci.getValue(), tradeType, self, theTradeBuddy,cci.token)
                                        self.addTrade(newTradeCCb)
                                        #print("Trade cc 2",tradeCCAmt)
                                        tradeCCAmt = tradeCCAmt - cci.getValue()
                                    if tradeCCAmt>=1:
                                        continue



                        # Trade(utils.CC,tradeCCAmt,tradeType,self,theTradeBuddy)

                        self.lastCCTradeCycle = cycles



        #IMPORT GOODS - money goes to Market
        if importMode and self.importing == True and cycles - self.lastImportCycle >= self.waitToImportCycles and self.nc >= AVGTRADE and self.bankTrading == False and alreadyImporting == False:
            #BULK purchase as much stock as half of self.money
            importAmt = 0
            myProfit = self.getCCTradableValue()-(self.STARTNC-self.nc)-(self.STARTSTOCK-self.stock)-self.debt

            if self.nc < myProfit:
                myProfit = self.nc

            if True and self.stock>= self.STARTSTOCK and self.subType==utils.FOREIGNRETAIL and (myProfit > AVGTRADE) : #use excess money to buy services
                newImportTrade = Trade(utils.NC,myProfit,utils.EXTSERVICES,self,self.closestMarket,None)
                #print ("Buying loads of services, amt: ", myProfit)
                self.addTrade(newImportTrade)
                self.lastImportCycle = cycles
                alreadyImporting = True


            if alreadyImporting == False:
                if self.stock < self.STARTSTOCK/2: #replenish stock to start levels
                    #only restock when stock has reach 50% of start Stock
                    stockNeeded = self.STARTSTOCK-self.stock
                    importAmt = stockNeeded
                    #print ("importAmt restock :", importAmt , " nc: ",self.nc," stock: " , self.stock, "SubType: ", traderTypeToString(self.subType))


            if self.nc < importAmt:
                importAmt = self.nc

            if importAmt > 0:
                #print (importAmt)
                newImportTrade = Trade(utils.NC,importAmt,utils.EXTSTOCK,self,self.closestMarket,None)
                self.addTrade(newImportTrade)
                self.lastImportCycle = cycles
                self.bankTrading == True
                #if self.subType==FOREIGNRETAIL and self.money > STARTNC: #use excess money to buy services
                    #print (">2>2>Foreign Trader purchase  from theMarket amt: ", importAmt)
            #print ("Import Trade ", importAmt)



        #ISSUE
        #TAKE existing CC reserve and create a new Token  - only call once when profits are up
        if self.coop and clearingMode and self.getCCValue()>0 and self.ownToken==False and cycles - self.lastClearingCycle >= self.waitToClearCycles  and self.nc>= AVGTRADE and alreadyBanking==False and self.subType != utils.FOREIGNRETAIL:

            #myProfit = self.cc-(self.STARTNC-self.nc)-(self.STARTSTOCK-self.stock)-self.debt
            myProfit = self.getCCValue()-(self.STARTNC-self.nc)
            if myProfit >=0:# and self.getCCValue() <= AVGTRADE:
                if self.nc < myProfit:
                    myProfit = self.nc

                #take my total CCValue convert all tokens to parent and use it as a reserve
                valueRes = 0
                for cci in self.cc:
                    if cci.token.tokenID == utils.reserveTokenID:
                        valueRes += cci.getValue()
                    #print("value:"+str(value))
                moreCC = valueRes/(defaultCW)
                #print(">>>>>ISSUING",moreCC,utils.traderTypeToString(self.subType),self.tIndex,self.tradeNum)

                lastTokenID = lastTokenID+1

                if lastColorTokenIndex > len(colorListCC):
                    lastColorTokenIndex = 1
                #print("color:",colorListCC[lastColorTokenIndex])
                #cycle Token Colors
                newImage = pygame.image.load('nc.png').convert_alpha()
                newImage = pygame.transform.rotozoom(newImage, 0, 1.6)
                utils.fill(newImage,colorListCC[lastColorTokenIndex])
                #newImage.fill((0, 100, 200), special_flags=pygame.BLEND_MULT)
                lastColorTokenIndex = lastColorTokenIndex + 45

                newToken = Token(lastTokenID+1,moreCC,reserveToken,defaultCW,True,newImage)



                tokens.append(newToken)
                wToken = WalletToken(newToken,moreCC)
                self.cc.append(wToken)

                self.ownToken = True#False
                #if bondingMode:
                self.preferedToken = newToken

                #self.cc+4*(self.stock+self.services)
                #self.stock = self.stock+self.nc
                #self.nc=0

            self.lastClearingCycle = cycles


        #GROWSERVICES
        if self.servicesGrowthAmount > 0 and cycles - self.lastServicesGrowthCycle >= self.waitToGrowServicesCycles:
            self.services = self.servicesGrowthAmount
            self.lastServicesGrowthCycle = cycles


        if self.stockGrowthRate > 0 and cycles - self.lastStockGrowthCycle >= self.waitToGrowStockCycles:

            self.stock = self.stock + self.stockGrowthRate
            if self.stock > self.STARTSTOCK:
                self.stock = self.STARTSTOCK
            self.lastStockGrowthCycle = cycles
            #print "grow stock"
                #b.services = b.services - b.costToGrowStock
            #print "GrowStock with Services?!"

        if self.stockConsumptionRate > 0 and cycles - self.lastStockConsumptionCycle >= self.waitToConsumeStockCycles:
            if self.stock - self.stockConsumptionRate >= 0:
                self.stock = self.stock - self.stockConsumptionRate
            else:
                self.stock = 0
            self.lastStockConsumptionCycle = cycles
            #print "Consume Stock"


"""
Monitor entire market
"""
class Monitor():
    def __init__(self):
        self.tradeVolList = [] #After each $TRADEBINTICKS rounds it stores the volume of trade = the addition of each players traded amount, then wipes the trades memory
        #self.giniList = [] #After each $TRADEBINTICKS rounds it stores the Gini Index = the addition of each players money
        self.exportedList = []
        #self.importedList = []
        #self.savedList = []
        self.localTradedListNC = []
        self.localTradedListCC = []
        self.exportedList = []
        self.importedList = []


        self.monthlyLocalTradedListNC = []
        self.monthlyLocalTradedListCC = []
        self.monthlyExportedList = []
        self.monthlyImportedList = []

        self.totalNCList = []
        self.totalCCList = []
        self.oldLocalTradedList = []

    def reset(self):
        self.tradeVolList = [] #After each $TRADEBINTICKS rounds it stores the volume of trade = the addition of each players traded amount, then wipes the trades memory
        #self.giniList = [] #After each $TRADEBINTICKS rounds it stores the Gini Index = the addition of each players money
        self.exportedList = []
        #self.importedList = []
        #self.savedList = []
        self.localTradedListNC = []
        self.localTradedListCC = []
        self.exportedList = []
        self.importedList = []


        self.monthlyLocalTradedListNC = []
        self.monthlyLocalTradedListCC = []
        self.monthlyExportedList = []
        self.monthlyImportedList = []

        self.totalNCList = []
        self.totalCCList = []
        self.oldLocalTradedList = []


# set up pygame, the window, and the mouse cursor
pygame.init()
infoObject = pygame.display.Info()
#pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
#print ("WINDOW")

#WINDOWWIDTH = infoObject.current_w

#WINDOWHEIGHT = infoObject.current_h


mainClock = pygame.time.Clock()
#background = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
background = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),HWSURFACE|DOUBLEBUF,16)


HEATSUBWINDOWWIDTH = WINDOWWIDTH#SUBWINDOWWIDTH+62
HEATSUBWINDOWHEIGHT =  WINDOWHEIGHT#SUBWINDOWHEIGHT+55#SUBWINDOWHEIGHT+29  -126
print (">>>>>>>>>>>>>heat subwindow height: ", HEATSUBWINDOWHEIGHT)
HEATOFFSETWIDTH = 0#OFFSETWIDTH-8
HEATOFFSETHEIGHT = 0#OFFSETHEIGHT-34

transSurfListNC = []
heatedCells = []


tx = 0
ty = 0
my_cmapNC = cmaps.inferno#magma #2
my_cmapCC = cm.get_cmap('hsv') #2
maxColor = 255#1000#255#my_cmap.N
maxHeat = 210

norm = plt.Normalize(0, maxColor)

ccolorListNC = []
ccolorListCC = []

for i in range(0,maxColor):
    thecolorsNC=cm.ScalarMappable(norm=norm, cmap=my_cmapNC).to_rgba(i)
    ccolorListNC.append(thecolorsNC)

    thecolorsCC = cm.ScalarMappable(norm=norm, cmap=my_cmapCC).to_rgba(i)
    ccolorListCC.append(thecolorsCC)
colorListNC = []
colorListCC = []

for vals in ccolorListNC:
    #print 255*vals[0]
    valR=int(vals[0]*255)
    valG=int(vals[1]*255)
    valB=int(vals[2]*255)
    colorListNC.append((valR,valG,valB))

i = 0
for vals in ccolorListCC:
    #print 255*vals[0]
    valR=int(vals[0]*255)
    valG=int(vals[1]*255)
    valB=int(vals[2]*255)
    #colorListCC.append((valR,valG,valB))
    colorListCC.append(pygame.Color(valR, valG, valB))

    while i < 15:
        i = i +1
        continue

print ("Heat Map Generated")
startColorNC = colorListNC[0]

nIter = 0

while tx*TILESIZE<HEATSUBWINDOWWIDTH:
    tColumn = []
    transSurfListNC.append(tColumn)

    while ty*TILESIZE<HEATSUBWINDOWHEIGHT:
        tgNC = heatSurf((tx*TILESIZE,ty*TILESIZE))
        tgNC.image.fill(startColorNC)            # notice the alpha value in the color
        transSurfListNC[tx].append(tgNC)

        ty = ty+1
    tx = tx+1
    ty = 0

print ("Heatmap Surface dimensions NC: ", len(transSurfListNC), len(transSurfListNC[0]))

topTitle = 'VMS-LiquidCC-v049'

pygame.display.set_caption(topTitle)

#print (pygame.font.get_fonts())


fontSysInfo = pygame.font.Font("./Ubuntu-M.ttf", 14)
fontTrInfo = pygame.font.Font("./Ubuntu-M.ttf", 10)

monitor = Monitor()

background.fill(BACKGROUNDCOLOR)

#PLOT1WIDTH = 0
#PLOT1HEIGHT = 0
#background.blit(monitor.plot1surf, (0,0))

if displayTrade:
    pygame.display.update()

traders = []
theMarkets = []
tokens = []


lastTokenID = utils.reserveTokenID
lastColorTokenIndex = 0
reserveSupply = 100000
reserveToken = Token(utils.reserveTokenID,reserveSupply,None,None,False,ccImage)
tokens.append(reserveToken)
defaultCW = 0.5

masterWallet = WalletToken(reserveToken,reserveSupply)

aMarket = Trader(utils.EXTERNALMARKET,BOARDSIZEX+BOARDOFFSETX-60,BOARDOFFSETY,-2)
aMarket.setupMarket()
theMarkets.append(aMarket)

print ("Market Generated")

theBank = Trader(utils.BANK,OFFSETWIDTH+BORDERWIDTH/2,OFFSETHEIGHT+SUBWINDOWHEIGHT-BORDERHEIGHT/2-5,-1)
#if savingsMode:
#    theBank.color=GREEN
#else:
theBank.setupBank()

print ("Smoothing Seasonal Market Conditions")
seasonalImportSmooth, seasonalImportOrig, seasonalImportFlat, sRounds = utils.smoother(seasonalImportSmooth,seasonalImportOrig,sRounds,rounds,seasonalMarketArray,seasonalImportFlat)
#nn = 0
#for sm in seasonalImportSmooth:
#    print (nn, sm)
#    nn+=1

generateTraders(traders)
print ("Traders Generated")
generateTraderLocationsSpiral(traders)
print ("Generating Trade Partners")
generateTradeBuddies(traders)
print ("Trade Partners Generated")

#legendSprites.add(legendDude(ccImage, (legendOffsetX+5, legendOffsetY-35),utils.CC))
#legendSprites.add(legendDude(ncImage, (legendOffsetX+65, legendOffsetY-35),utils.NC))
legendSprites.add(legendDude(curveImage, (legendOffsetX+250, legendOffsetY+80),utils.EXCHANGE))

legendSprites.add(legendDude(serviceShopImage, (legendOffsetX, legendOffsetY-5),utils.LOCALSERVICE))
legendSprites.add(legendDude(productionShopImage, (legendOffsetX+65, legendOffsetY-5),utils.LOCALPRODUCER))
legendSprites.add(legendDude(workerImage, (legendOffsetX+140, legendOffsetY-5),utils.EXPORTSERVICE))
legendSprites.add(legendDude(coopServicesShopImage, (legendOffsetX, legendOffsetY+45),utils.LOCALSERVICECOOP))
legendSprites.add(legendDude(coopProductionShopImage, (legendOffsetX+65, legendOffsetY+45),utils.LOCALPRODUCERCOOP))
legendSprites.add(legendDude(retailShopImage, (legendOffsetX+135, legendOffsetY+45),utils.RETAIL))
legendSprites.add(legendDude(foreignRetailShopImage, (legendOffsetX+5, legendOffsetY+105),utils.FOREIGNRETAIL))
legendSprites.add(legendDude(marketImage, (legendOffsetX+95, legendOffsetY+105),utils.EXTERNALMARKET))

cycles = 0
pltTick = 0
heatTick = 0
tradeBinTicks = 0
totalSavings = 0
totalDebt = 0
totalExported = 0
totalImported = 0
totalPurchasedCC = 0
totalPurchasedNC = 0
totalSoldNC = 0
totalSoldCC = 0

gtotalExported = 0
gtotalImported = 0
gtotalNCNumSales = 0
gtotalCCNumSales = 0

gtotalRetailTradeNC = 0
gtotalRetailTradeCC = 0
gtotalPurchasedCC = 0
gtotalPurchasedNC = 0
gtotalSoldNC = 0
gtotalSoldCC = 0
print ("Start Trade")

toggleHeatMode(heatMode)
toggleImportMode(importMode)
toggleExportMode(exportMode)
#toggleSeasonalMode(seasonalMode)
toggleCCMode(ccMode,traders)

#if seedingMode and ccMode and loanMode and savingsMode:
#    toggleSeedingMode(traders,True)
#else:
#    toggleSeedingMode(traders,False)

runSim = True
while runSim:
    # set up the start of the game

    #trades = []

#    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    #pygame.mixer.music.play(-1, 0.0)

    while runSim: # the game loop runs while the game part is playing


        for event in pygame.event.get():
            if event.type == QUIT:
                print("<><><>Terminate on Key QUIT")
                terminate()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()
                elif event.key == pygame.K_SPACE:
                    pause = True
                    print ("PAUSE")
                    paused()
                elif event.key == pygame.K_p:
                    displayPlots = not displayPlots
                    print ("PLOTTING Mode, ", displayPlots)
                elif event.key == pygame.K_s:
                    seasonalMode = not seasonalMode
                    toggleSeasonalMode(seasonalMode)

                elif event.key == pygame.K_h:
                    heatMode = not heatMode
                    toggleHeatMode(heatMode)

                elif event.key == pygame.K_c:
                    ccMode = not ccMode
                    toggleCCMode(ccMode,traders)

                elif event.key == pygame.K_e:
                    exportMode = not exportMode #exportTrader start
                    #importMode = not importMode
                    toggleExportMode(exportMode)

                elif event.key == pygame.K_b:
                    bondingMode = not bondingMode #exportTrader start
                    #importMode = not importMode
                    toggleBondingMode(bondingMode)

                elif event.key == pygame.K_d: #defualting /// sell off CC
                    if clickedTrader<  len(traders) and clickedTrader>= 0:
                        traders[clickedTrader].convertAllCC(reserveToken,tokens,True)



                elif event.key == pygame.K_i:
                    importMode = not importMode #importers start

                    if importMode:
                        for m in theMarkets:
                            m.color=YELLOW
                    else:
                        for m in theMarkets:
                            m.color=ORANGE



                elif event.key == pygame.K_s:
                    savingsMode = not savingsMode
                    loanMode = not loanMode
                    if loanMode:
                        theBank.color=GREEN
                    else:
                        theBank.color=RED
                    print ("Savings / Loan")

                elif event.key == pygame.K_RIGHT:
                    clickedTrader = clickedTrader + 1
                    if clickedTrader> len(traders)-1:
                        clickedTrader = -2

                elif event.key == pygame.K_LEFT:
                    clickedTrader = clickedTrader - 1
                    if clickedTrader<(-2):
                        clickedTrader = len(traders)-1

                elif event.key == pygame.K_DOWN:
                    clickedTrader = clickedTrader - 5
                    if clickedTrader<(-2):
                        clickedTrader = len(traders)-1

                elif event.key == pygame.K_UP:
                    clickedTrader = clickedTrader + 5
                    if clickedTrader> len(traders)-1:
                        clickedTrader = -2

                elif event.key == pygame.K_RCTRL:
                    clientsModeB = not clientsModeB


                if  event.key == pygame.K_UP or  event.key == pygame.K_DOWN or  event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT or event.key == pygame.K_RCTRL:
                    for m in traders:
                        m.drawCon =False
                        m.drawSelf(background)

                    if clickedTrader >=0:
                        t = traders[clickedTrader]
                        if clientsModeB == True:
                            clientsMode(event,t)
                        else:
                            buddiesMode(event,t)


            if event.type == MOUSEBUTTONDOWN:
                # If the mouse moves on top of a player - set his fill and his tradebuddies
                #clickedTrader = -99998
                for m in traders:
                    m.drawCon =False
                    m.drawSelf(background)

                mouseRect = pygame.Rect(event.pos[0]-10,event.pos[1]-10 , 20, 20)

                #lRect = pygame.Rect(legendOffsetX+170, legendOffsetY+19,50,70)

                if clearBntRectal.collidepoint(event.pos):
                    print("delete all tradersw")
                    for tss in traders:
                        del tss.tradeBuddies[:]
                        tss.tradeBuddies = []
                        del tss.trades[:]
                        tss.trades = []
                        del tss.cc[:]
                        tss.cc = []


                    del traders[:]
                    traders = []
                    del tokens[:]
                    tokens = []
                    tokenSprites.empty()


                    reserveToken = Token(utils.reserveTokenID, reserveSupply, None, None, False, ccImage)
                    tokens.append(reserveToken)

                    lastColorTokenIndex = 0
                    lastTokenID = utils.reserveTokenID


                    pRETAIL = 0
                    pFOREIGNRETAIL = 0
                    pLOCALSERVICE = 0
                    pLOCALPRODUCER = 0
                    pEXPORTSERVICE = 0

                    currentDate = STARTDATE

                if tenxBntRectal.collidepoint(event.pos):
                    #print("Add 10 random dudes")
                    newDudes = 10
                    dudeList = (utils.LOCALSERVICE, utils.LOCALPRODUCER, utils.EXPORTSERVICE,utils.LOCALPRODUCERCOOP,utils.LOCALSERVICECOOP,utils.RETAIL,utils.FOREIGNRETAIL)
                    d = 0
                    while d < newDudes:

                        d=d+1
                        slegendType = random.choice(dudeList)

                        tn = Trader(utils.GENERIC,100,100,len(traders))
                        if slegendType == utils.LOCALSERVICECOOP or slegendType == utils.LOCALPRODUCERCOOP:
                            tn.coop = True
                            print("newCoop")


                        if slegendType == utils.LOCALSERVICE:
                            tn.setupLocalServices()
                            pLOCALSERVICE = pLOCALSERVICE + 1
                        elif slegendType == utils.LOCALPRODUCER:
                            tn.setupLocalProduction()
                            pLOCALPRODUCER = pLOCALPRODUCER + 1
                        elif slegendType == utils.EXPORTSERVICE:
                            tn.setupExportServiceTrader()
                            pEXPORTSERVICE = pEXPORTSERVICE + 1
                        elif slegendType == utils.LOCALPRODUCERCOOP:
                            tn.setupLocalProduction()
                            pLOCALPRODUCER = pLOCALPRODUCER + 1
                        elif slegendType == utils.LOCALSERVICECOOP:
                            tn.setupLocalServices()
                            pLOCALSERVICE = pLOCALSERVICE + 1
                        elif slegendType == utils.RETAIL:
                            tn.setupRetailShop()
                            pRETAIL = pRETAIL + 1
                        elif slegendType == utils.FOREIGNRETAIL:
                            tn.setupForeignRetailShop()
                            pFOREIGNRETAIL = pFOREIGNRETAIL + 1

                        generateTraderLocation(tn)
                        print("Generating Locations : after Add")
                        traders.append(tn)
                        TOTALSTARTINGNC=TOTALSTARTINGNC+tn.nc



                        tRETAIL = 0
                        tFOREIGNRETAIL = 0
                        tLOCALPRODUCER = 0
                        tLOCALSERVICE = 0
                        if pRETAIL >= 1:
                            tRETAIL = 1
                        if pFOREIGNRETAIL >= 1:
                            tFOREIGNRETAIL = 1
                        if pLOCALPRODUCER >= 1:
                            tLOCALPRODUCER = 1
                        if pLOCALSERVICE >= 1:
                            tLOCALSERVICE = 1

                        #diversityLevelMax requirment on the minimum number of trade partners
                        diversityLevelMax = tRETAIL +tFOREIGNRETAIL + tLOCALPRODUCER + tLOCALSERVICE

                        #MAXTRADERS = 100
                        MAXTRADERS = pRETAIL + pFOREIGNRETAIL + pLOCALSERVICE + pLOCALPRODUCER + pEXPORTSERVICE


                        if pRETAIL == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pFOREIGNRETAIL == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pLOCALPRODUCER == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pLOCALSERVICE == 1:
                            diversityLevelMax = diversityLevelMax -1



                        ai = 0
                        for tss in traders:
                            print("r2d2:",ai)
                            ai+=1
                            del tss.tradeBuddies[:]
                            tss.tradeBuddies = []
                            tss.tIndex = traders.index(tss)

                        generateTradeBuddies(traders)
                        #print("ReGenerating  Buddies 1")

                    break

                if heatBntRectal.collidepoint(event.pos):
                    print("a HEAT PICK", NCHEAT, CCHEAT, heatOn, heatMode)
                    if heatOn == False or heatMode == False:
                        heatOn = True
                        heatMode = True
                        CCHEAT = True
                        NCHEAT = False

                    elif CCHEAT == True and NCHEAT == False:
                        NCHEAT = True
                        CCHEAT = False

                    elif CCHEAT == False and NCHEAT == True:
                        NCHEAT = True
                        CCHEAT = True

                    elif CCHEAT == True and NCHEAT == True:
                        CCHEAT = False
                        NCHEAT = False
                        heatOn = False
                        heatMode = False

                    print("f HEAT PICK", NCHEAT, CCHEAT, heatOn, heatMode)

                    if heatOn:
                        for g in traders:
                            for h in g.trades:
                                if utils.isCC(h.currency) and h.dest.traderType !=  utils.EXTERNALMARKET and h.source.traderType !=  utils.EXTERNALMARKET:
                                    h.heating = CCHEAT
                                if h.currency==utils.NC and h.dest.traderType !=  utils.EXTERNALMARKET and h.source.traderType !=  utils.EXTERNALMARKET:
                                    h.heating = NCHEAT
                    break

                if tokenBntRectal.collidepoint(event.pos):

                    if clickedTrader == -998:
                        clickedTrader = 0

                    elif clickedTrader != -998:
                        clickedTrader = -998

                    break

                for t in tokenSprites:
                    if t.rect.collidepoint(event.pos) and t.legendType > utils.reserveTokenID:
                        if clickedToken ==  t.legendType:
                            clickedToken = -1
                        else:
                            clickedToken =  t.legendType
                        break



                for s in legendSprites:
                    if s.rect.collidepoint(event.pos) and s.legendType == utils.EXCHANGE:

                        bondingMode = not bondingMode #exportTrader start
                        toggleBondingMode(bondingMode)
                        print("Bonding Curve PICK")
                        break


                    elif s.rect.collidepoint(event.pos) and s.legendType != utils.EXCHANGE:
                        tn = Trader(utils.GENERIC,100,100,len(traders))

                        #zIndex = zIndex+1
                        TOTALSTARTINGNC=TOTALSTARTINGNC+tn.nc
                        if s.legendType == utils.LOCALSERVICECOOP or s.legendType == utils.LOCALPRODUCERCOOP:
                            tn.coop = True
                            print("newCoop")
                            #sCoops +=1

                        if s.legendType == utils.EXTERNALMARKET:
                            print("EXTERNALM - break")
                            break

                        elif s.legendType == utils.LOCALSERVICE:
                            tn.setupLocalServices()
                            print("LocalService PICK")
                            pLOCALSERVICE = pLOCALSERVICE + 1
                        elif s.legendType == utils.LOCALPRODUCER:
                            tn.setupLocalProduction()
                            pLOCALPRODUCER = pLOCALPRODUCER + 1
                        elif s.legendType == utils.EXPORTSERVICE:
                            tn.setupExportServiceTrader()
                            print("Export Service Trader PICK")
                            pEXPORTSERVICE = pEXPORTSERVICE + 1
                        elif s.legendType == utils.LOCALPRODUCERCOOP:
                            tn.setupLocalProduction()
                            pLOCALPRODUCER = pLOCALPRODUCER + 1
                        elif s.legendType == utils.LOCALSERVICECOOP:
                            tn.setupLocalServices()
                            print("Local Service COOP PICK")
                            pLOCALSERVICE = pLOCALSERVICE + 1
                        elif s.legendType == utils.RETAIL:
                            tn.setupRetailShop()
                            pRETAIL = pRETAIL + 1
                            print("Retail SHOP PICK")
                        elif s.legendType == utils.FOREIGNRETAIL:
                            tn.setupForeignRetailShop()
                            print("FOREIGN SHOP PICK")
                            pFOREIGNRETAIL = pFOREIGNRETAIL + 1





                        tRETAIL = 0
                        tFOREIGNRETAIL = 0
                        tLOCALPRODUCER = 0
                        tLOCALSERVICE = 0
                        if pRETAIL >= 1:
                            tRETAIL = 1
                        if pFOREIGNRETAIL >= 1:
                            tFOREIGNRETAIL = 1
                        if pLOCALPRODUCER >= 1:
                            tLOCALPRODUCER = 1
                        if pLOCALSERVICE >= 1:
                            tLOCALSERVICE = 1

                        #diversityLevelMax requirment on the minimum number of trade partners
                        diversityLevelMax = tRETAIL +tFOREIGNRETAIL + tLOCALPRODUCER + tLOCALSERVICE

                        #MAXTRADERS = 100
                        MAXTRADERS = pRETAIL + pFOREIGNRETAIL + pLOCALSERVICE + pLOCALPRODUCER + pEXPORTSERVICE


                        if pRETAIL == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pFOREIGNRETAIL == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pLOCALPRODUCER == 1:
                            diversityLevelMax = diversityLevelMax -1
                        if pLOCALSERVICE == 1:
                            diversityLevelMax = diversityLevelMax -1


                        traders.append(tn)

                        for tss in traders:
                            del tss.tradeBuddies[:]
                            tss.tradeBuddies = []
                            tss.tIndex = traders.index(tss)
                        clickedTrader = traders.index(tn)
                        moveTrader = True
                        break


                for t in traders:
                    outerLineRect = t.image.get_rect(topleft=(t.locx,t.locy))
                    if outerLineRect.collidepoint(event.pos):
                    #if t.rect.colliderect(mouseRect):
                        clickedTrader = traders.index(t)

                        if event.button == 3:
                            buddiesMode(event,t)

                        elif event.button != 3:
                            clientsMode(event,t)
                            moveTrader = True

                if clickedTrader == -99:
                    outerLineRect = aMarket.image.get_rect(topleft=(aMarket.locx,aMarket.locy))
                    if outerLineRect.collidepoint(event.pos):

                        clickedTrader = -2

            elif event.type == MOUSEBUTTONUP and moveTrader: #stop moving trader
                moveTrader = False

                #                sys.stdout.write("hello from Python %s\n" % (sys.version,))
                if traders[clickedTrader].rect.left < INFOWIDTH:
                    #print("location"+str(traders[clickedTrader].rect.left))
                    #print("b len: "+str(len(traders)))
                    traderRem =traders[clickedTrader]

                    traderRem.convertAllCC(reserveToken,tokens,True)

                    del traders[clickedTrader].trades[:]
                    traders[clickedTrader].trades = []
                    straderType = traders[clickedTrader].subType
                    print("Remove Type: "+str(straderType))
                    if straderType == utils.LOCALSERVICE:
                        pLOCALSERVICE = pLOCALSERVICE - 1
                    elif straderType == utils.LOCALPRODUCER:
                        pLOCALPRODUCER = pLOCALPRODUCER - 1
                    elif straderType == utils.EXPORTSERVICE:
                        pEXPORTSERVICE = pEXPORTSERVICE - 1
                    elif straderType == utils.LOCALPRODUCERCOOP:
                        pLOCALPRODUCER = pLOCALPRODUCER - 1
                    elif straderType == utils.LOCALSERVICECOOP:
                        pLOCALSERVICE = pLOCALSERVICE - 1
                    elif straderType == utils.RETAIL:
                        pRETAIL = pRETAIL - 1
                    elif straderType == utils.FOREIGNRETAIL:
                        pFOREIGNRETAIL = pFOREIGNRETAIL - 1




                    tRETAIL = 0
                    tFOREIGNRETAIL = 0
                    tLOCALPRODUCER = 0
                    tLOCALSERVICE = 0
                    if pRETAIL >= 1:
                        tRETAIL = 1
                    if pFOREIGNRETAIL >= 1:
                        tFOREIGNRETAIL = 1
                    if pLOCALPRODUCER >= 1:
                        tLOCALPRODUCER = 1
                    if pLOCALSERVICE >= 1:
                        tLOCALSERVICE = 1

                    #diversityLevelMax requirment on the minimum number of trade partners
                    diversityLevelMax = tRETAIL +tFOREIGNRETAIL + tLOCALPRODUCER + tLOCALSERVICE

                    #MAXTRADERS = 100
                    MAXTRADERS = pRETAIL + pFOREIGNRETAIL + pLOCALSERVICE + pLOCALPRODUCER + pEXPORTSERVICE


                    if pRETAIL == 1:
                        diversityLevelMax = diversityLevelMax -1
                    if pFOREIGNRETAIL == 1:
                        diversityLevelMax = diversityLevelMax -1
                    if pLOCALPRODUCER == 1:
                        diversityLevelMax = diversityLevelMax -1
                    if pLOCALSERVICE == 1:
                        diversityLevelMax = diversityLevelMax -1




                    traders.remove(traders[clickedTrader])
                    for tss in traders:
                        del tss.tradeBuddies[:]
                        tss.tradeBuddies = []
                        tss.tIndex = traders.index(tss)

                    #print("b len: "+str(len(traders)))
                #
                #    clickedTrader = 0
                #    print("removing "+str(clickedTrader)+" len: "+str(len(traders)))
                else:
                    traders[clickedTrader].tradeBuddies = []

                generateTradeBuddies(traders)
                #print("ReGenerating 2")

                if clickedTrader >= len(traders):
                    clickedTrader = 1




        background.fill(BACKGROUNDCOLOR)

        coolIt = False
        if cycles-heatTick > coolingFREQ:
            heatTick = cycles
            coolIt = True

        if heatOn:
            heatSprites.draw(background)
            removeSprites = []
            if True:
                #fooCells = list(heatedCells)
                for ty in heatSprites:#heatedCells:
            #for tx in transSurfListNC:
                #for ty in tx:
                    #background.blit(ty.image, (HEATOFFSETWIDTH+txi*TILESIZE,HEATOFFSETHEIGHT+tyi*TILESIZE))
                    if coolIt and ty.heat>0:#if we have reached a cooling cycle

                        heatChange = coolingAmt #cooling
                        ty.heat  = ty.heat - heatChange
                        if ty.heat <= 0:
                            ty.heat = 0
                            removeSprites.append(ty)
                            #heatSprites.remove(ty)

                        ty.image.fill(colorListNC[ty.heat])
                        #save is alist of surfaces that have changed and only blit those
                        #heatSprites = pygame.sprite.Group()
                        heatSprites.add(ty)
                        #if ty.heat==0:
                        #    fooCells.remove(ty)

            #for ty in removeSprites:
            #    heatSprites.remove(ty)
            heatSprites.remove(removeSprites)


        totalNC = 0
        totalCC = 0
        totalStock = 0
        totalServices = 0
        totalNCTraded = 0
        totalCCTraded = 0
        totalNCNumSales = 0
        totalCCNumSales = 0
        totalImported = 0
        totalExported = 0
        totalDebt = 0
        #background.blit(mapSurface,(OFFSETWIDTH,OFFSETHEIGHT))

        for m in theMarkets:
            m.marketLogistics(traders) #choose from who and how often to purchase stock or services (allow for exporting of goods and services (like labour))

        for b in traders:

            #print "drawing myself: ", b.color, b.fill
            #b.drawSelf(background)

            b.logistics()

            for trade in b.trades:
                trade.move()

                if trade.hasArrived():
                    #print "arrived"
                    if trade.validate():
                        #print "1 b.rect.width: ",b.rect.width
                        trade.completeTrade()
                        #print "completed"
                            #print "2 b.rect.width: ",b.rect.width
                            #b.drawSelf(background)
                            #trade.dest.drawSelf(background)
                        #print "Trade Completed", trade.money, currencyTypeToString(trade.currency), tradeTypeToString(trade.tradeType)
                        trade.dest.addTradeList(trade)#memory dump
                        trade.source.addTradeList(trade)#memory dump

                        if trade.tradeType !=  utils.DEPOSIT and trade.tradeType !=  utils.LOAN and trade.tradeType !=  utils.CLEARING and trade.tradeType !=  utils.DIVIDEND and trade.tradeType !=  utils.SAVINGS and trade.tradeType !=  utils.FEES:
                            if utils.isCC(trade.currency):#if trade.currency == utils.CC :
                                gtotalPurchasedCC = gtotalPurchasedCC + trade.money
                                gtotalCCNumSales = gtotalCCNumSales + 1

                                if trade.source.subType == utils.RETAIL or trade.dest.subType == utils.RETAIL:
                                    gtotalRetailTradeCC = gtotalRetailTradeCC + trade.money


                            else:

                                if trade.tradeType ==  utils.EXTSERVICES or trade.tradeType==utils.EXTSTOCK:
                                    gtotalExported = gtotalExported + trade.money
                                else:
                                    gtotalPurchasedNC = gtotalPurchasedNC + trade.money
                                    gtotalNCNumSales = gtotalNCNumSales + 1
                                    #print (gtotalPurchasedNC,gtotalNCNumSales, "WHAT?", trade.source.subType, trade.dest.subType , cycles, trade.source.lastNCTradeCycle,trade.dest.lastNCTradeCycle)
                                    if trade.source.subType == utils.RETAIL or trade.dest.subType == utils.RETAIL:
                                        gtotalRetailTradeNC = gtotalRetailTradeNC + trade.money




                    #else:
                        #print "Trade did not validate, trade money", trade.money, trade.currency,
                    b.trades.remove(trade)
                else:
                    newHead = {'x': trade.rect.centerx, 'y': trade.rect.centery}
                    trade.wormCoords.insert(0,newHead)
                    if len(trade.wormCoords) > trade.wormLength:
                        del trade.wormCoords[trade.wormLength:]

                    if displayTrade:
                        trade.drawSelf(background)

                    #update HeatMap
                    #print heatingAmtOrig,
                    #print heatingAmt, trade.money, AVGTRADE
                    if heatMode and trade.heating == True:
                        #print ("heating")

                        heatingAmt = int(float(heatingAmtOrig)*float(trade.money)/float(AVGTRADE))
                        if heatingAmt <10:
                            heatingAmt =10
                        #else:
                        #    print heatingAmt

                        acolorList = colorListNC
                        asurfList = transSurfListNC
                        #if trade.currency==CC:
                        #    acolorList = colorListCC


                        #find out where the trade is and darken the tile in the heatmap
                        #if it has reached max heat, then heat others
                        #each round cool entire heatmap
                        #print "o", trade.rect.centerx, trade.rect.centery
                        transX = int((trade.rect.centerx-HEATOFFSETWIDTH)/TILESIZE)
                        transY = int((trade.rect.centery-HEATOFFSETHEIGHT)/TILESIZE)
                        #print "c", transX, transY
                        if transX >= len(asurfList):
                            transX = len(asurfList)-1
                        currentCell = asurfList[transX][transY]


                        heatChange = heatingAmt #* trade.money#heating
                        currentCell.heat  = currentCell.heat + heatChange
                        if currentCell.heat >= maxHeat:#maxColor:
                            currentCell.heat = maxHeat-1 #maxColor-1


                        currentCell.image.fill(acolorList[currentCell.heat]) # cmap way
                        #heatedCells.append(currentCell)
                        heatSprites.add(currentCell)
                        #add to sprite Group

                        #radius of efffect
                        radiusHeat = True
                        if radiusHeat:
                            radius = 6
                            startX = transX - radius
                            endX = transX +radius
                            #startY= transY - radius
                            #endY = transY +radius
                            nTileX = startX
                            nTileY = transY#startY
                            while nTileX <= endX:
                                #check if it is inside the array
                                xOff = abs(transX-nTileX)
                                #print ">>xOff: ", xOff, " range: ",range(xOff-radius,radius-xOff+1)
                                #print ">>xOff: ", xOff, " range: ",range(-1*radius,radius+1)
                                #for yOff in range(xOff-radius,radius-xOff+1):
                                for yOff in range(-1*radius,radius+1):
                                    nTileY=transY+yOff
                                    #dist = abs(yOff)+abs(xOff)
                                    dist = abs(yOff)
                                    if abs(xOff)>abs(yOff):
                                        dist = abs(xOff)
                                    #print "xOff: ", xOff, " yOff: ", yOff, " dist: ",dist
                                    if nTileX < len(asurfList) and nTileY < len(asurfList[0]) and nTileX >=0 and nTileY >= 0 and dist != 0:
                                        nCell = asurfList[nTileX][nTileY]
                                        nCell.heat  = nCell.heat + int(heatChange/dist)
                                        if nCell.heat >= maxHeat:#maxColor:
                                            nCell.heat = maxHeat#maxColor-1
                                        nCell.image.fill(acolorList[nCell.heat])
                                        #heatedCells.append(nCell)
                                        heatSprites.add(nCell)
                                nTileX=nTileX+1

            totalNC = totalNC+b.nc
            totalCC = totalCC+b.getCCValue()
            totalStock = totalStock+b.stock
            totalServices = totalServices+b.services
            totalNCTraded = totalNCTraded + b.purchasesNC
            totalCCTraded = totalCCTraded + b.purchasesCC

            totalNCNumSales = totalNCNumSales + b.numSalesNC
            totalCCNumSales = totalCCNumSales + b.numSalesCC

            totalSavings = totalSavings + b.savings
            totalDebt = totalDebt + b.debt
            #totalExported = totalExported + b.exported
            #totalImported = totalImported + b.imported
            totalPurchasedNC = totalPurchasedNC + b.purchasesNC
            totalPurchasedCC = totalPurchasedCC + b.purchasesCC
            totalSoldNC = totalSoldNC + b.salesNC
            totalSoldCC = totalSoldCC + b.salesCC

            #gtotalPurchasedNC = gtotalPurchasedNC + b.purchasesNC
            #gtotalPurchasedCC = gtotalPurchasedCC + b.purchasesCC
            #gtotalSoldNC = gtotalSoldNC + b.salesNC
            #gtotalSoldCC = gtotalSoldCC + b.salesCC



        #borderRect = pygame.Rect(OFFSETWIDTH-BORDERWIDTH,OFFSETHEIGHT-BORDERHEIGHT, SUBWINDOWWIDTH+BORDERWIDTH, SUBWINDOWHEIGHT+BORDERHEIGHT)
        #pygame.draw.rect(background, BLACK, borderRect, 1)

        if displayTrade:
            for b in traders:
                b.drawSelf(background)
            if savingsMode == True:
                theBank.drawSelf(background)
            for m in theMarkets:
                m.drawSelf(background)
        for m in theMarkets:
            totalExported = totalExported + m.exported
            totalImported = totalImported + m.imported


        if displayPlots == True :

            cOffseting = 28
            cOffInc = 14

            background.blit(infoRect,(BORDERWIDTH,BORDERHEIGHT))

            background.blit(heatBtnRect,(legendOffsetX+250, legendOffsetY-35))
            pygame.draw.rect(background, BLUE, heatBntRectal, 1)
            drawText('HeatMap', fontSysInfo, background, legendOffsetX+253, legendOffsetY-35)


            background.blit(tokenBtnRect,(legendOffsetX+250, legendOffsetY-10))
            pygame.draw.rect(background, BLUE, tokenBntRectal, 1)
            drawText('Tokens', fontSysInfo, background, legendOffsetX+253, legendOffsetY-10)


            background.blit(clearBtnRect,(legendOffsetX+250, legendOffsetY+19))
            pygame.draw.rect(background, BLUE, clearBntRectal, 1)
            drawText('Clear', fontSysInfo, background, legendOffsetX+253, legendOffsetY+19)

            background.blit(tenxBtnRect,(legendOffsetX+250, legendOffsetY+45))
            pygame.draw.rect(background, BLUE, tenxBntRectal, 1)
            drawText('+10', fontSysInfo, background, legendOffsetX+255, legendOffsetY+45)

            #drawText('NC', fontSysInfo, background, legendOffsetX+60, legendOffsetY-30)

#legendSprites.add(legendDude(ccImage, (legendOffsetX+5, legendOffsetY-25),utils.EXTERNALMARKET))
#legendSprites.add(legendDude(ncImage, (legendOffsetX+65, legendOffsetY-25),utils.EXTERNALMARKET))


            drawText('Services', fontSysInfo, background, legendOffsetX-5, legendOffsetY+14)
            legendSprites.draw(background)

            if clickedTrader == -998:  # CC Data
                tokenSprites.draw(background)

            #background.blit(serviceShopImage, (legendOffsetX, legendOffsetY))

            drawText('Production', fontSysInfo, background, legendOffsetX+55, legendOffsetY+14)
            #background.blit(productionShopImage, (legendOffsetX+65, legendOffsetY))

            drawText('Labor', fontSysInfo, background, legendOffsetX+130, legendOffsetY+14)
            #background.blit(workerImage, (legendOffsetX+140, legendOffsetY))


            drawText('Coop S', fontSysInfo, background, legendOffsetX-5, legendOffsetY+75)
            #background.blit(coopServicesShopImage, (legendOffsetX-10, legendOffsetY+40))

            drawText('Coop P', fontSysInfo, background, legendOffsetX+60, legendOffsetY+75)
            #background.blit(coopProductionShopImage, (legendOffsetX+62, legendOffsetY+40))


            drawText('Retail', fontSysInfo, background, legendOffsetX+130, legendOffsetY+75)
            #background.blit(retailShopImage, (legendOffsetX+135, legendOffsetY+50))


            drawText('Foreign Retail', fontSysInfo, background, legendOffsetX-5, legendOffsetY+130)
            #background.blit(foreignRetailShopImage, (legendOffsetX+5, legendOffsetY+100))


            drawText('External Market', fontSysInfo, background, legendOffsetX+90, legendOffsetY+130)
            #background.blit(marketImage, (legendOffsetX+95, legendOffsetY+100))




            #background.blit(boardRect,(BOARDOFFSETX,BOARDOFFSETY))
            #pygame.draw.rect(background, BLUE, infoRect, 0)





            #clock
            drawText('Sim. Cycles: %sx%s Start Date %s' % (int(cycles),numRepeats,STARTDATE.date()), fontSysInfo, background, TOFFSETWIDTH, cOffseting)
            cOffseting = cOffseting + cOffInc

            #Businesses
            drawText('Businesses: %s Current Date %s' % (int(MAXTRADERS),cyclesToDate().date()), fontSysInfo, background, TOFFSETWIDTH, cOffseting)
            cOffseting = cOffseting + cOffInc

            #Money / Stock
            #drawText('Start Money/Stock/Services: %s/%s/%s' % (int(STARTNC*MAXTRADERS),int(STARTSTOCK*MAXTRADERS),int(STARTSERVICES*MAXTRADERS)), font, background, OFFSETWIDTH, cOffseting)
            drawText('Total Starting NC: %s ' % (int(TOTALSTARTINGNC)), fontSysInfo, background, TOFFSETWIDTH, cOffseting)

            if (totalNC+totalCC)>0:
                cOffseting = cOffseting + cOffInc

                drawText('Total NC: %s cc: %s %s%%' % (int(totalNC),int(totalCC),int(100*totalCC/(totalNC+totalCC))), fontSysInfo, background, TOFFSETWIDTH, cOffseting)

            #Imports / Exports
            #cOffseting = cOffseting + cOffInc
            #totalMImported = 0
            #for m in theMarkets:
            #    totalMImported = m.imported+totalMImported
            #drawText('Exported/Imported: %s/%s' % (int(totalImported),int(totalExported)), font, background, TOFFSETWIDTH, cOffseting)


            totalMImported = 0
            #Savings Debt
            #cOffseting = cOffseting + cOffInc

            #drawText('Savings %s, Debt %s' % (int(theBank.savings),int(theBank.debt)), fontSysInfo, background, TOFFSETWIDTH, cOffseting)

            #Savings Revenue
            #cOffseting = cOffseting + cOffInc
            #totalMImported = 0
            #pSD = 0
            #if theBank.debt >0:
            #    pSD = float(theBank.savings)/float(theBank.debt)
            #drawText('Revenue %s Costs %s Reserve: %s%%' % (int(theBank.savings-fractionalReserve*float(theBank.debt)), int(theBank.nc),int(100.0*(pSD))), fontSysInfo, background, TOFFSETWIDTH, cOffseting)

            cOffseting = cOffseting + cOffInc

            #Trade Volume
            mTl = totalPurchasedNC+totalSoldNC
            #if len(monitor.localTradedListNC)>0:
            #  mTl = monitor.localTradedListNC[len(monitor.localTradedListNC)-1]
            #drawText('Trade Volume NC per %s Cycles: %s' % (int(TRADEBINTICKS),int(mTl)), font, background, OFFSETWIDTH, cOffseting)


            cOffseting = cOffseting + cOffInc

            #Trade Volume CC
            mTlCC = totalPurchasedCC+totalSoldCC
            #if len(monitor.localTradedListCC)>0:
            #  mTl = monitor.localTradedListNC[len(monitor.localTradedListCC)-1]
            #drawText('Trade Volume CC per %s Cycles: %s' % (int(TRADEBINTICKS),int(mTl)), font, background, OFFSETWIDTH, cOffseting)


            #Gini
            cOffseting = cOffseting + cOffInc
            #drawText('Gini Index: %s' % (int(getGini(traders))), font, background, OFFSETWIDTH, cOffseting)


            #cOffseting = 30

            cOffsettingX = TOFFSETWIDTH#OFFSETWIDTH  #+920
            #clicked Trader

            if clickedTrader == -998:  # CC Data
                drawText('Tokens:', fontTrInfo, background, cOffsettingX, cOffseting)
                tokens.sort(key=lambda x: x.price, reverse=True)
                cOffsettingX = cOffsettingX +4
                cOffseting = cOffseting + 1*cOffInc
                for tt in tokens:
                    drawText('ID:%s cw: %s%% Supply: %1.0f Price: %0.2f Value: %0.1f' % (tt.tokenID,int(tt.cw*100),tt.supply,tt.price,tt.price*tt.supply), fontTrInfo, background, cOffsettingX, cOffseting)
                    foundTS = False
                    for ts in tokenSprites:
                        if ts.legendType == tt.tokenID:
                            ts.rect = ts.image.get_rect(topleft=(cOffsettingX-10, cOffseting))
                            foundTS = True
                            break
                    if foundTS == False:
                        tokenSprites.add(legendDude(tt.spriteImg, (cOffsettingX-10, cOffseting),tt.tokenID))
                    #background.blit(tt.spriteImg, (cOffsettingX-10, cOffseting))
                    cOffseting = cOffseting + cOffInc



            if clickedTrader == -1: #coop
                drawText('Cooperative: %s, %s' % (int(clickedTrader),utils.traderTypeToString(theBank.subType)),
                         fontTrInfo, background, cOffsettingX, cOffseting)

                cOffseting = cOffseting + cOffInc

                drawText('Mandatory Reserve: %s%%' % (int(fractionalReserve*100)),
                         fontTrInfo, background, cOffsettingX, cOffseting)

                cOffseting = cOffseting + cOffInc

                #drawText('Savings: %s, Debt: %s' % (int(theBank.savings),int(theBank.debt)),
                #         fontTrInfo, background, cOffsettingX, cOffseting)

                #cOffseting = cOffseting + cOffInc

                pSD = 0
                if theBank.debt >0:
                    pSD = float(theBank.savings)/float(theBank.debt)


                drawText('Above Collateral: %s Profits: %s Reserves: %s%%' % (int(theBank.savings-fractionalReserve*float(theBank.debt)), int(theBank.nc),int(100.0*(pSD))), fontTrInfo, background, cOffsettingX, cOffseting)

                cOffseting = cOffseting + cOffInc

                drawText('Transfers:', fontTrInfo, background, cOffsettingX, cOffseting)

                cOffsettingX = cOffsettingX +4
                cOffseting = cOffseting + 1*cOffInc

                for terror in theBank.tradeInfo:
                    drawText('%s' % (terror), fontTrInfo, background, cOffsettingX, cOffseting)
                    cOffseting = cOffseting + cOffInc



            if clickedTrader == -2: #market
                drawText('External Market: %s, %s' % (int(clickedTrader),utils.traderTypeToString(aMarket.subType)),
                         fontTrInfo, background, cOffsettingX, cOffseting)

                cOffseting = cOffseting + cOffInc


            if clickedTrader >= 0 and len(traders)>0 and clickedTrader < len(traders):


                cTraderSelf = traders[clickedTrader]
                nameStringTmp = utils.traderTypeToString(cTraderSelf.subType)
                #print clickedTrader

                if cTraderSelf.coop:
                    nameStringTmp += " (Cooperative)"

                drawText('Trader: #%s, %s' % (int(clickedTrader),nameStringTmp), fontTrInfo, background, cOffsettingX, cOffseting)


                cOffseting = cOffseting + cOffInc
                drawText('Starting %sNC, %scc, Stock %s, Services %s' % (int(cTraderSelf.STARTNC),int(cTraderSelf.STARTCC),int(cTraderSelf.STARTSTOCK),int(cTraderSelf.STARTSERVICES)),
                         fontTrInfo, background, cOffsettingX, cOffseting)


                cOffseting = cOffseting + cOffInc
                drawText('Current %sNC, %scc, Stock %s, Services %s (profit %s)' % (int(cTraderSelf.nc),int(cTraderSelf.getCCValue()),int(cTraderSelf.stock),int(cTraderSelf.services),int(cTraderSelf.getCCValue()-(cTraderSelf.STARTNC-cTraderSelf.nc)-(cTraderSelf.STARTSTOCK-cTraderSelf.stock)-cTraderSelf.debt)),
                         fontTrInfo, background, cOffsettingX, cOffseting)

                cOffseting = cOffseting + cOffInc


                #drawText('Savings %s, Debt %s, Days/Clearing %s' % (int(cTraderSelf.savings),int(cTraderSelf.debt),int((cTraderSelf.waitToClearCycles-cycles - cTraderSelf.lastClearingCycle)/DAILYCYCLES)),
                 #        fontTrInfo, background, cOffsettingX, cOffseting)
                #cOffseting = cOffseting + cOffInc

                #drawText('Missing stock %s, LastLoan %s, WaitToTrade %s ' % (int(cTraderSelf.STARTSTOCK-cTraderSelf.stock),int(cTraderSelf.lastLoanAmt),int(cTraderSelf.waitToTradeCycles)),
                 #        fontTrInfo, background, cOffsettingX, cOffseting)
                #cOffseting = cOffseting + cOffInc

                #for tt in cTraderSelf.trades:
                #    drawText('Trade: %s%s, type %s, to %s' % (int(tt.money),utils.currencyTypeToString(tt.currency), utils.tradeTypeToString(tt.tradeType), utils.traderTypeToString(tt.dest.subType) ), fontTrInfo, background, cOffsettingX, cOffseting)
                    #cOffseting = cOffseting + cOffInc

                if len(cTraderSelf.cc)>0:
                    drawText('Tokens', fontTrInfo, background, cOffsettingX, cOffseting)

                    cOffsettingX = cOffsettingX +4
                    cOffseting = cOffseting + 1*cOffInc

                    for tks in cTraderSelf.cc:
                        drawText('ID: %s Balance: %0.1f Price: %0.2f Value: %0.1f' % (tks.token.tokenID,tks.balance,tks.token.price,tks.token.price*tks.balance), fontTrInfo, background, cOffsettingX, cOffseting)
                        background.blit(tks.token.spriteImg, (cOffsettingX-10, cOffseting))
                        cOffseting = cOffseting + cOffInc


                if True:
                    cOffsettingX = cOffsettingX - 4
                    drawText('Outgoing Trades', fontTrInfo, background, cOffsettingX, cOffseting)

                    cOffsettingX = cOffsettingX +4
                    cOffseting = cOffseting + 1*cOffInc

                    for terror in cTraderSelf.tradeInfo:
                        drawText('%s' % (terror), fontTrInfo, background, cOffsettingX, cOffseting)
                        cOffseting = cOffseting + cOffInc


        if displayTrade:
            #pygame.display.update()
            pygame.display.flip()
        #print "total Money ", totalMoney+theBank.savings

        if False: #if saveImageMode and autoMode == True or repeatCycle >0:
            totalCy = cycles#+int(numRepeats*repeatCycle)
            #print "./plotsv43d/myfile_"+str(totalCy).zfill(5)+'.png'
            if numRepeats <=0:
                pygame.image.save(background,"./plotsv43d/myfile_"+str(totalCy).zfill(5)+'.png')
            elif numRepeats >0:
                pygame.image.save(background,"./plotsv43d/myfile"+str(int(repeatCycle))+"_"+str(totalCy).zfill(5)+'.png')

        #print(cycles)
        #mainClock.tick(FPS)
        #mainClock.tick()
        pltTick = pltTick+1
        #heatTick = heatTick+1
        cycles = cycles+1



        #if repeatCycle >0 and cycles-lastRepeatCycle > repeatCycle:
        if repeatCycle >0 and cycles > repeatCycle:
            #lastRepeatCycle = cycles
            #repeatCycleTicks = pygame.time.get_ticks() - lastRepeatCycleTicks
            #lastRepeatCycleTicks = pygame.time.get_ticks()
            repeatCycleTicks = 0
            lastRepeatCycleTicks = 0
            numRepeats = numRepeats +1
            overAllCycle+=1

            cycles = 0

            #writeVideo()
            #print "END SIMULATION >>totals"
            #print "P-NC,","P-CC,","S-NC,","S-CC,","Exp,","Imp,","ccPercent,","cycles"

            if False and overAllCycle ==1:

                print("ClearingMode","Month","All Trade","NC","CC","Export","AvgNC","AvgCC","avgExport")

                print ("clearingMode:",end='')
                print (", ccStart:",end='')
                print (", ncStart:",end='')
                print (", ncPurch",end='')
                print (", ccPurch",end='')
                print (",allLocal:",end='')
                print (", exports:",end='')
                print (",allTrade:",end='')
                print (", ccSales:",end='')
                print (", ccSales:",end='')
                print (", retailNC:",end='')
                print (", retailCC:",end='')
                print (", retailCC+NC:",end='')
                print (", nonRetailNC:",end='')
                print (", nonRetailCC:", end='')
                print (",nonRetailNC+CC:",end='')
                print (", ImportMult:")

            if False:
                print (clearingMode,end=',')
                print (ccStartAmt,end=',')
                print (ncStartAmt,end=',')
                print (int(gtotalPurchasedNC),end=',')
                print (int(gtotalPurchasedCC),end=',')
                print (str(int(gtotalPurchasedCC+gtotalPurchasedNC)),end=',')
                print (int(gtotalExported),end=',')
                print (str(int(gtotalExported+gtotalPurchasedCC+gtotalPurchasedNC)),end=',')
                print (int(gtotalNCNumSales), end=',')
                print (int(gtotalCCNumSales), end=',')
                print (int(gtotalRetailTradeNC),end=',')
                print (int(gtotalRetailTradeCC),end=',')
                print (int(gtotalRetailTradeCC+gtotalRetailTradeNC),end=',')
                print (int(gtotalPurchasedNC-gtotalRetailTradeNC),end=',')
                print (int(gtotalPurchasedCC-gtotalRetailTradeCC),end=',')
                print (str(int(gtotalPurchasedCC-gtotalRetailTradeCC+gtotalPurchasedNC-gtotalRetailTradeNC)),end=',')
                print (IMPORTMULT)




            #text_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (cclMode,ccPercent,ccStartAmt,ncStartAmt,int(gtotalPurchasedNC),int(gtotalPurchasedCC),int(gtotalPurchasedCC+gtotalPurchasedNC),int(gtotalExported),int(gtotalExported+gtotalPurchasedCC+gtotalPurchasedNC),int(gtotalNCNumSales),int(gtotalCCNumSales),int(gtotalRetailTradeNC),int(gtotalRetailTradeCC),int(gtotalRetailTradeCC+gtotalRetailTradeNC),int(gtotalPurchasedNC-gtotalRetailTradeNC),int(gtotalPurchasedCC-gtotalRetailTradeCC),int(gtotalPurchasedCC-gtotalRetailTradeCC+gtotalPurchasedNC-gtotalRetailTradeNC),repeatCycleTicks,theBank.saved,theBank.loaned,int(theBank.debt),int(theBank.savings),int(theBank.nc)))

            if numRepeats > numRepeatsTot:
                if IMPORTMULT<=IMPORTMULTMAX:
                    numRepeats = 0
                    IMPORTMULT+=IMPORTMULTSTEP
                    #print("+++IMPORTMULT: ",IMPORTMULT)
                else:
                    runSim = False
                    #text_file.close()
                    print("<><><>Terminate on STEPPING")
                    terminate()

            if False:#numRepeats > numRepeatsTot:
                #ncStartAmt> ncEndAmt:
                #if ccPercent > 1:
                #if IMPORTMULT > 10:
                runSim = False
                #text_file.close()
                print("<><><>Terminate on ", numRepeats, " Repeats")
                terminate()

            #reset all variables
            #print ("<><><>RESET ALL VARIABLES")

            currentMonthNum = STARTDATE.month
            currentMonthNum= STARTDATE.month

            gtotalExported = 0
            gtotalImported = 0
            gtotalPurchasedCC = 0
            gtotalPurchasedNC = 0

            gtotalRetailTradeCC = 0
            gtotalRetailTradeNC = 0

            gtotalNCNumSales = 0
            gtotalCCNumSales = 0

            gtotalSoldNC = 0
            gtotalSoldCC = 0

            #ccPercent = ccPercent+0.01
            #if ccStartAmt<= ccEndAmt:
            #    ccStartAmt = ccStartAmt+ccStepAmt
            #if ccStartAmt> ccEndAmt:
            #    ccStartAmt = 0
                #ccPercent = ccPercent+ccPercentStep
            clearingMode = False
            if autoMode == False:
                autoMode = True
            else:
                autoMode = False


                """
                if loanMode == False:
                #loanMode = True
                #savingsMode = True
                loanMode = True
                savingsMode = True
                        cclMode = 1
                currentRepeats = 0
                else:
                loanMode = False
                        savingsMode = False
                cclMode = 0
                ncStartAmt = ncStartAmt + ncStepAmt
                currentRepeats = 0
                """
                #else:
                    #currentRepeats = currentRepeats + 1


                #if loanMode == False:
                #    loanMode = True
                #    savingsMode = True
                #    cclMode = 1
                #elif loanMode == True:
                #    loanMode = False
                #    savingsMode = False
                #    cclMode = 0
                #    ncStartAmt = ncStartAmt + ncStepAmt


           #ncStartAmt = ncStartAmt + ncStepAmt

            #ccPercent = ccPercent+ccPercentStep

            #ccStartAmt = ccStartAmt+ccStepAmt


            #IMPORTMULT = IMPORTMULT+0.2
            #reset traders
            TOTALSTARTINGNC=0
            #monitor = Monitor()
            for b in traders:
                oldBuddies = list(b.tradeBuddies)
                #print "last trade cycle",b.lastNCTradeCycle
                b.reset()
                if b.subType==utils.RETAIL:
                    b.setupRetailShop()
                elif b.subType==utils.FOREIGNRETAIL:
                    b.setupForeignRetailShop()
                elif b.subType==utils.LOCALPRODUCER:
                    b.setupLocalProduction()
                elif b.subType==utils.LOCALSERVICE:
                    b.setupLocalServices()
                elif b.subType==utils.EXPORTSERVICE:
                    b.setupExportServiceTrader()
                else:
                    print ("Terminate on ERROR 2331")
                    terminate()

                b.tradeBuddies = oldBuddies

                TOTALSTARTINGNC=TOTALSTARTINGNC+b.nc



            for m in theMarkets:
                #print m.lastExportCycle,
                m.reset()
                m.setupMarket()
                #m = Trader(EXTERNALMARKET,OFFSETWIDTH+SUBWINDOWWIDTH-BORDERWIDTH/2+10,OFFSETHEIGHT-10)

            theBank.reset()
            theBank.setupBank()

            #if seedingMode and ccMode:# and loanMode and savingsMode:
            #    toggleSeedingMode(traders,True)
            #else:
            #    toggleSeedingMode(traders,False)

            monitor.reset()

            if heatOn:
                heatTick = 0
                txi=0
                tyi=0
                for tx in transSurfListNC:
                    for ty in tx:
                        ty.heat=0
                        #ty.surface.fill(colorListNC[ty.heat])#startColorNC
                        #heatSprites.add(ty)
                        background.blit(ty.surface, (HEATOFFSETWIDTH+txi*TILESIZE,HEATOFFSETHEIGHT+tyi*TILESIZE))
                        tyi=tyi+1
                    txi=txi+1
                    tyi=0

        if autoMode == True:
            if cycles > endCycle:
                runSim = False

                print ("END SIMULATION >>totals")
                print ("P-NC,","P-CC,","S-NC,","S-CC,","Exp,","Imp,","ccPercentUsed","ccStartAmt")
                print (gtotalPurchasedNC,",",gtotalPurchasedCC,",",gtotalSoldNC,",",gtotalSoldCC,",",gtotalExported,",",gtotalImported,",",ccPercent,ccStartAmt)
                print("<><><>Terminate on endCycle AutoMode")
                terminate()

            elif cycles > clearingModeCycle and clearingMode == False:
                toggleClearingMode(True)

            '''
            elif cycles > ccModeCycle and ccMode == False:
                toggleCCMode(True,traders)
            elif cycles > seasonalModeCycle and seasonalMode == False:
                toggleSeasonalMode(True)
            elif cycles > exportModeCycle and exportMode == False:
                toggleExportMode(True)
            elif cycles > importModeCycle and importMode == False:
                toggleImportMode(True)
            elif cycles > heatModeCycle and heatMode == False:
                toggleHeatMode(True)
            elif cycles > savingsModeCycle and savingsMode == False:
                toggleSavingsMode(True)
            elif cycles > loanModeCycle and loanMode == False:
                toggleLoanMode(True)'''

        if overAllCycle ==0 and cycles <2:

            print("ClearingMode,","Month,","All-Trade,","Avg-Trade,","NC,","CC,","Export,","AvgNC,","AvgCC,","avgExport","IMPORTMULT","today")


        tradeBinTicks = tradeBinTicks +1

        if tradeBinTicks >= DAILYCYCLES: #TRADEBINTICKS: #a day has passed
            tradeBinTicks = 0
            monitor.monthlyLocalTradedListNC.append(int(gtotalPurchasedNC))
            monitor.monthlyLocalTradedListCC.append(int(gtotalPurchasedCC))
            monitor.monthlyExportedList.append(int(gtotalExported))
            #monitor.monthlyImportedList.append(int(totalImported))

            gtotalPurchasedNC = 0
            gtotalPurchasedCC = 0
            gtotalExported = 0
            gtotalNCNumSales = 0
            gtotalCCNumSales = 0

        monthlyLocalTradedListNCLength = len(monitor.monthlyLocalTradedListNC)

        #if we are in a new month
        zdate = cyclesToDate()
        if zdate.month != currentMonthNum:
#        if monthlyLocalTradedListNCLength >= 30:
            traN=len(traders)-pEXPORTSERVICE
            if traN > 0:
                avgNC = int(sum(monitor.monthlyLocalTradedListNC)/traN)
                avgCC = int(sum(monitor.monthlyLocalTradedListCC)/traN)
                avgExport = int(sum(monitor.monthlyExportedList)/traN)
            else:
                avgNC = 0
                avgCC = 0
                avgExport = 0
            sumNC = int(sum(monitor.monthlyLocalTradedListNC))
            sumCC = int(sum(monitor.monthlyLocalTradedListCC))
            sumExport = int(sum(monitor.monthlyExportedList))
            sumAll = sumNC+sumCC+sumExport
            if traN > 0:
                avgAll = int((sumNC+sumCC+sumExport)/traN)
            else:
                avgAll = 0
            day_of_year = zdate.timetuple().tm_yday

            today = day_of_year#date.day
            seasonLen = len(seasonalImportSmooth)
            if today > seasonLen:
                print("wrong date error!:",today, seasonLen)
                today = today % seasonLen


            print (clearingMode,",",currentMonthNum, ",",sumAll, ",",avgAll,",",sumNC , ",",sumCC, ",", sumExport,",",avgNC , ",",avgCC, ",", avgExport ,",",IMPORTMULT,",",today)
            monitor.monthlyLocalTradedListNC = []
            monitor.monthlyLocalTradedListCC = []
            monitor.monthlyExportedList = []
            currentMonthNum= cyclesToDate().month
            #monitor.monthlyImportedList = []



        if displayPlots and tradeBinTicks >= TRADEBINTICKS:
            tradeBinTicks = 0
            #monitor.tradeVolList.append(totalMoneyTraded)
            #giniIndx=getGini(traders)
            #monitor.giniList.append(giniIndx)
            #monitor.exportedList.append(totalExported+totalImported)
            #monitor.importedList.append(totalImported)
            monitor.localTradedListNC.append(totalPurchasedNC+totalSoldNC)
            monitor.localTradedListCC.append(totalPurchasedCC+totalSoldCC)
            monitor.exportedList.append(totalExported)
            monitor.importedList.append(totalImported)
            monitor.totalNCList.append(totalNC)
            #monitor.savedList.append(totalSavings)
            #print totalMoney

            #print "Total: imports, exported: ", int(totalImported), int(totalExported)
            #print "Total: purchased, sold: ", int(totalPurchased), int(totalSold)
            #totalMImported = 0
            #totalMExported = 0
            #for m in theMarkets:

            #    totalMImported = m.imported + totalMImported
            #    totalMExported = m.exported + totalMExported


            #    m.imported=0
            #    m.exported=0

            #print "Market: imports, exported: ", int(totalMImported), int(totalMExported)

            for b in traders:
                b.purchasesNC=0
                b.purchasesCC=0
                b.salesNC=0
                b.salesCC=0
                b.imported=0
                b.exported=0
#                print "MarketUsers: imports, exported: ", m.imported, m.exported

            totalNC = 0
            totalCC = 0
            totalNCTraded = 0
            totalCCTraded = 0

            totalNCNumSales = 0
            totalCCNumSales = 0

            totalExported = 0
            totalImported = 0
            totalSavings = 0
            totalPurchasedNC = 0
            totalPurchasedCC = 0
            totalSoldNC = 0
            totalSoldCC = 0

            currentMonthNum = startMonth

            for m in theMarkets:
                m.exported = 0
                m.imported = 0

    waitForPlayerToPressKey()

    gameOverSound.stop()
