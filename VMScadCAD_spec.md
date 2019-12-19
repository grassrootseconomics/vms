# Village Market Simulator (VMS) 


## -> vmsCADcad


[TOC]



# Background:  {#background}

The Village Market Simulator – approximates economic interactions in various Kenyan settings through agent-based modeling and it is used as a way of testing parameters of community currencies.

The original code used several types of agents which could be placed on the fly (during market running) and interact with the other agents buying or selling stock or services as a teaching tool.

A video of various versions of this code running can be found here: [https://www.youtube.com/watch?v=_559D4yxONo&list=PLPUExzwZAUpbEInJy_8Wj_c_mDsw7-qXe](https://www.youtube.com/watch?v=_559D4yxONo&list=PLPUExzwZAUpbEInJy_8Wj_c_mDsw7-qXe)

The source code those older models can be found here:[ https://github.com/GrassrootsEconomics/vms](https://github.com/GrassrootsEconomics/vms)


# Hopes: {#hopes}

This document seeks to simplify the above model and modularize it so it is easy to build on. 

**Overall we wish to simulate:**



1. Basic market conditions in underserved communities
2. The introduction of a community currency (CC) and look at various impacts on the community
3. Multiple currencies interacting, created by agents.
4. Bonding curves that connect these currencies together as well as national currencies together
    1. The currently proposed method of using Kenyan Shillings (via DAI) as a reserve 
    2. Various community currency creation and price stability models: 
        1. Eg: The exchange rate for each CC to reserve should oscillate around 1.
            1. (+) As people outside a community currency buy goods (or save) with/from a CC_a holders they adds more reserve and mints new CC_a’s - and increases their value. 
            2. (-) As people convert CC_a for its underlying national currency reserve or use them to buy from other CC_b+ holders the exchange price will fall.


## Sim/Visualization {#sim-visualization}



1. Seeing the seasonality of the External Market and resulting local trade
    1. The simulation without CC involved could show that when seasons are bad and the external market is not pumping in cash the local market is often stagnate.
    2. The introduction of a CC increases local trade in various circumstances - such as enough local producers and service providers compared to retail shops. Can appear counter cyclic to National Currency
    3. The introduction of multiple connected CCs creates larger stable markets
2. Visualizing the network of agents and trade (National Currency and CC)
    4. Overall trade volume
    5. Gini Index - Balance and trade distributions
3. Visualizing the relative value of all the CCs over time
4. Agent Views: Being able to see who is trading with who as well as their balances and trades
5. Hot Spots: Seeing hot spots of trade using a heatmap
6. Agent Parameters: Adjusting agent types, numbers and parameters
7. Currency Parameters: Adjusting currency creation rules and parameters
8. System: Parameters: Adjusting the overall economic environment


# Logistics {#logistics}

Agents (who are various types of local businesses) are placed randomly and choose 5 other agents to trade with (typical shops)- keeping in mind they must have at least 1 stock and service provider.

In each turn of an agent it simulates a typical day. Each agent needs to feed a family and needs to buy roughly 300/= of food. The list of things each agent buys and sells is stored in their Class.

So they shop at their ~5 typical shops and if they can’t find a shop with stock they will search farther and farther.

The external market buys services from the community on monthly (seasonal) intervals and retail shops send national currency back to the external market to restock.

Agents will have a balance in a ‘Group Token’ there may be several Group Tokens in one simulation but each agent can only hold 1 Group Token.

An Agent who needs to buy from another agent but is missing National Currency can use CC if accepted or convert CC into National Currency (at a ‘fee’) (lowering the value of the CC by removing reserve see equation (3))


## Token Creation {#token-creation}

**CC Creator:** An agent that has a balance of at least 10,000 National currency can ‘save’ it in a smart contract and use it as leverage (25% reserve ratio) to create a local credit (community currency CC) with 40,000 units of a **‘Group Token’. **

An Agent can only create one Group token it is then assigned that Group Token as his own.

Some agents don’t accept the local currency including the external market. Retail shop’s acceptance of a Group Token will vary _(for instance only accepting 50% of their profit margin)_. 

The local currency (Group Token) has a value of 1:1 with National currency as long as it maintains 25% reserve. (see bonding curve)

A CC Creator forces other agents to convert into his CC to buy his goods. (This adds more reserve and increases its value - see equation (2))

Any agent that buys from a CC Creator is assigned that **Group Token** if they have never before been assigned a **‘Group Token’. **Eventually all agents - except the external market and foreign retailers should have a group token.


### Group Accounts: {#group-accounts}

Group Token Creator as a group savings and loan account. Agents save in the group account and create a token and airdrop this token to each-other and give loans in the token. *This is closer to reality in Kenya and can be a stage 2 in simulation. For the purposes of this doc - An individual agent can be approximated with a group account. In Kenya this is often the case where a single account could have many users (family ex. wife, husband, kids).


## Auto Convert {#auto-convert}

Whenever two normal users trade with each other that have different ‘Group Tokens’ the recipient must convert the other Group Token to his own. 

Ex. Someone in Group Token A that sends A’s to someone with Group Token B will 1st convert to the reserve (burning some A’s and removing reserve from A’s reserve) then 2nd place that Reserve into B’s and mint new B’s. As a result B will have a higher exchange rate than A (given they started equal).


## Conversion {#conversion}

Each Group Token created has a reserve (in National currency) and a supply of Group Tokens.

The exchange rate of the Group Token is given by equation (1) P= R/(S.F) = Reserve / Supply . a Target Reserve Ratio



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Village-Market0.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Village-Market0.png "image_tooltip")




<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Village-Market1.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Village-Market1.png "image_tooltip")


Each time a conversion take place between a CC and it’s reserve there is an adjustment to the exchange price of that token - along the bonding curve based on equations 2 and 3.


## Group Dynamics {#group-dynamics}

Any agent if they get 10k+ national currency they can create a Group Token. In reality these are savings accounts for a group of Women who meet weekly and save about 100 Kenyan Shillings each. These shillings can go into the reserve and increase their token’s value. As they value goes up they give out loans to each other or use the CC for local projects. When they cash it out to reserve - the value drops again.

In the simulation we approximate this by the users buying from that agent (forced conversion to that Group Token) and if they are out of national currency and need to make a purchase (or are purchasing from a retailer) they can convert their CC back to reserve (which lowers the value).


### Price Stability Model {#price-stability-model}



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Village-Market2.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Village-Market2.png "image_tooltip")


The exchange rate for each Group Token to reserve should oscillate around 1.



        2. (+) As people outside a community currency buy goods (or save) with/from a CC_a holders they adds more reserve and mints new CC_a’s - and increases their value. 
        3. (-) As people convert CC_a for it’s underlying national currency reserve or use them to buy from other CC_b+ holders the exchange price will fall.


# Agents {#agents}

The below represent a single agent with 3 primarily different characteristics, namely:



1. External market – are a source of National currency for the village– generally buying labor from the community on a seasonal period. It has an infinite amount of National Currency and the injections of this money into the other agents is the external source of money as well as retail goods.
2. Local producer (services or stocks) – Sources their services and stock locally (their service / stock supply autogenerates on some time period). They buy and sell locally.
3. Retailer – Buy stock from the external market and sells it locally. They may also buy local goods and food. (A ‘Foreign Retailer never buys anything locally)

*Note that these agent dynamics could be trained to mimic the trade data from actual trade data in Kenya.


## Agent/System Variables: {#agent-system-variables}

Agent.wants = a list of dicts. Each dict says what that agent buys, on what frequency, from where and if that item expires (is consumed or resold). The frequency adjusts that amount wanted in that period.

Agent.offers = a list of dicts. Each dict says what that agent sells, on what frequency, from where and if that item expires (is consumed or resold).

Location = Random GPS coordinates (allowing a user to select and place agents make this an interesting teaching tool). Coordinates could match actual GPS coordinates of users

Trade partners list = Generated list of (5) other agents this agent trades with - note a trade will see out more if those 5 don’t have the stock/services needed in their wants list

Balance in National Currency

Balance of Group Token (given auto-convert there should be only one token available) 

Group Token = this is the token an agent will always convert to when receiving another token (see Group Token Creation below)

Min Purchase Size = 20 (what is the minimum bought of goods and services)

Target Reserve Ratio = (see equation 1) 25%

Minimum reserve balance = 10,000 #Minimum to start a Group Token

Price Elasticity = False #DO item prices vary based on the exchange value of the tokens? False = indicated that the CCs are always used locally at the same value as a KSH. (Hence arbitrage is possible)


## External Market {#external-market}

**agent.wants** = [{‘item’:‘services’, ’where’:’local’, ‘want-freq’: [0.1,0.3,0.5,0.6,0.7,0.3,0.5,0.7,0.7,0.7,1],’ amount’:1000’, ‘expiration’:’daily’, ‘resold’:’false’}]

Ex. Purchases as much as 10,000 ‘labor’ (from as many agents as possible) at the end of the month. On a seasonal basis that multiplies how much that will be purchased (Jan:0.1, Feb:0.3, March: 0.5, April: 0.6: May: 0.7: June: 0.7: July: 0.3: August: 0.5: September: 0.7, Oct: 0.7, November:0.7, December:1)= [0.1,0.3,0.5,0.6,0.7,0.3,0.5,0.7,0.7,0.7,1]

This money goes to local service producers and in the absence of National Currency it limits the amount of trade.

**agent.offers** = [{‘item’:goods, ’where’:’retail’, ‘source’:’self’, ‘source-freq’:’daily’,’source-amount’:1000’, sell-freq’:’always’, ‘price:’1 ‘expiration’:’never’}]

 The Market offers goods to retail shops


## Local Producer (Services) {#local-producer-services}

**agent.offers** = [{‘item’:‘services’, ’where’:’any’, ‘source’:’self’, ‘source-freq’:’daily’,’source-amount’:300’, sell-freq’:’always’, ‘price:’1 ‘expiration’:’daily’}]

This agent sells ‘labor’ to anyone (external markets or other local agents). 300 units (a day of labor) is created and expires daily.

**agent.wants** = [{‘item’:‘goods’, ’where’:’local’, ‘want-freq’:’daily’,’ amount’:200’, ‘expiration’:’daily’, ‘resold’:’false’},


      {‘item’:‘services’, ’where’:’local’, ‘want-freq’:’weekly’,’ amount’:500’, ‘expiration’:’daily’, ‘resold’:’false’}]


## Local Producer (Goods) {#local-producer-goods}

**agent.offers** = [{‘item’:‘goods’, ’where’:’any’, ‘source’:’self’, ‘source-freq’:’monthly’,’source-amount’:10000’, source-freq’: [0,0,1,0,0,0,0,0,0.6,0,0,], ‘price:’1 ‘expiration’:’monthly’}]

This agent sells ‘goods’ to anyone they are seasonal - hence the source frequency - this is a 2 rain season market.

**agent.wants** = [{‘item’:‘goods’, ’where’:’local’, ‘want-freq’:’daily’,’ amount’:200’, ‘expiration’:’daily’, ‘resold’:’false’},


      {‘item’:‘services’, ’where’:’local’, ‘want-freq’:’weekly’,’ amount’:500’, ‘expiration’:’daily’, ‘resold’:’false’}]


## Retailer {#retailer}

**agent.offers** = [{‘item’:‘goods’, ’where’:’local’, ‘source’:’market’, ‘source-freq’:’daily’,’source-amount’:1000’, ‘sell-freq’: ‘daily’, ‘price:’1.2 ‘expiration’:’never’}]

#retailer sells goods bought from the market and starts with 1000. There is a 20% markup from purchase

**agent.wants** = [{‘item’:‘goods’, ’where’:’external’, ‘want-freq’:’restocking’,’ amount’:’restock’, ‘expiration’:’never’, ‘resold’:’true’}, _#note this is restocking and should happen when stock is out_


    {‘item’:‘goods’, ’where’:’external’, ‘want-freq’:’daily’,’ amount’:200’, ‘expiration’:’daily’, ‘resold’:’false’},


    {‘item’:‘services’, ’where’:’external’, ‘want-freq’:’weekly’,’ amount’:500’, ‘expiration’:’daily’, ‘resold’:’false’}]


# Data {#data}

Post running a simulation for a time period (say 1 year) the output should be a transaction list similar to actual data:

[https://github.com/GrassrootsEconomics/TransactionDatasets](https://github.com/GrassrootsEconomics/TransactionDatasets) - this is data from running in Kenya


<!-- Docs to Markdown version 1.0β17 -->
