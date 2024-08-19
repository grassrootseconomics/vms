import uuid
import random
import networkx as nx
import pygame
import math
from collections import deque

# This simulation is an attempt to create a mycofi agent.
# The Mycofi Agent (MA) will have an inital amount of capital $
# MA: Will purchase nearby vouchers and place them in a pool. 

# Initialize Pygame
pygame.init()

# Initialize delay_time
delay_time = 100

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1720,880
AGENT_RADIUS = 10
POOL_WIDTH = 10
POOL_HEIGHT = 20

POOL_START_ASSETS = 10
grow_mode = False

MAX_USD_START_BALANCE = 5000
MAX_START_BALANCE = 5000
NUM_AGENTS = 41
PATH_LENGTH = 5
MAX_CONNECTORS = 4
HEALTHY_NUTRIENTS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 200, 50)
BLUE = (0, 0, 255)
BLACK = (120, 120, 120)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool Transfers")



# Set up the initial graph
Gp = nx.Graph()
pos = nx.spring_layout(Gp)
pos_init = None
    
# Create the animation
#ani = FuncAnimation(fig, update_graph, interval=1000)

class Voucher:
    def __init__(self, name, value, supply, issuer):
        self.name = name
        self.value = value
        self.supply = supply
        self.issuer = issuer
        #self.id = name #uuid.uuid4()

    def __repr__(self):
        return f"{self.name}"
        #return f"Voucher(Name: {self.name}, Value: {self.value}, Supply: {self.supply}, Issuer: {self.issuer.name})"

class Agent:
    def __init__(self, name,index):
        self.name = name
        self.vouchers = {}
        self.index = index
        self.issued_voucher = None
        self.nutrients = 0
        
    def produce_voucher(self, name, value, supply):
        v_name = name+str(self.index)
        if name == "USD":
            v_name = "USD"
        voucher = Voucher(v_name, value, supply, self)
        self.vouchers[v_name] = supply  # Store the Voucher object
        self.issued_voucher = voucher
        return voucher

    def __repr__(self):
        return f"Agent(Name: {self.name})"

class SwapPool:
    def __init__(self, name):
        self.name = name
        self.vouchers = {}
        self.exchanges = {}  # To track exchanges
        self.is_active = 1
        self.nutrients = 0

    #Adding vouchers to a pool. Note that the amount can be zero
    def deposit(self, agent, voucher, amount):
        if voucher.supply >= amount:  # Compare the supply of the voucher
            # Check if the agent has enough supply of the input voucher
            if agent.vouchers.get(voucher.name, 0) < amount:
                raise ValueError("Agent does not have enough vouchers to deposit.")

            agent.vouchers[voucher.name] -= amount
            self.vouchers.setdefault(voucher.name, 0)
            self.vouchers[voucher.name] += amount

            
            #voucher.supply -= amount  # Decrease the supply of the voucher
        else:
            raise ValueError("Insufficient voucher supply for deposit.")

    def exchange(self, agent, input_voucher, output_voucher, amount):
        #print("exch1: ",agent,agent.vouchers,input_voucher,output_voucher,amount)
        # Check if there's enough supply in the pool for the output voucher
        if self.vouchers.get(output_voucher.name, 0) < amount:
            raise ValueError("Insufficient supply in pool for exchange.")

         # Check if the agent has enough supply of the input voucher
        if agent.vouchers.get(input_voucher.name, 0) < amount:
            print("error: ",agent,agent.vouchers,input_voucher.name)
            raise ValueError("Agent does not have enough vouchers to exchange.")

        # Exchange process
        self.vouchers[output_voucher.name] -= amount
        agent.vouchers.setdefault(output_voucher.name, 0)
        agent.vouchers[output_voucher.name] += amount
        self.deposit(agent, input_voucher, amount)
        #agent tracks teh number of incomming transactions
        agent.nutrients += 2
        self.nutrients += 2
        #print("post enchange: ",agent.vouchers)

        # Update exchanges tracking
        pair = (input_voucher.name, output_voucher.name)
        if pair in self.exchanges:
            self.exchanges[pair] += 1
        else:
            self.exchanges[pair] = 1

        return f"Exchanged {amount} of {input_voucher.name} for {amount} of {output_voucher.name}"

    def empty(self,all_vouchers):
        for voucher_name in self.vouchers:
            amount = self.vouchers[voucher_name]
            agent = next(voucher.issuer for voucher in all_vouchers if voucher.name == voucher_name)
            agent.vouchers[voucher_name] += amount
            self.vouchers[voucher_name] = 0

    def fill(self,all_vouchers):
        for voucher_name in self.vouchers:
            agent = next(voucher.issuer for voucher in all_vouchers if voucher.name == voucher_name)
            amount = 0
            if agent.vouchers[voucher_name] >= 1:
                amount = random.randint(1, agent.vouchers.get(voucher_name,0))
            else:
                continue
            agent.vouchers[voucher_name] -= amount
            self.vouchers[voucher_name] += amount


    def __repr__(self):
        return f"SwapPool(Name: {self.name}, Vouchers: {self.vouchers})"

def make_graph(swap_pools):
    # Create a graph of the swap pools
    G = nx.Graph()
    if swap_pools != None:        
        for pool in swap_pools:
            if pool.is_active == 1:
                for v_id in pool.vouchers:
                    G.add_node(v_id)
                    for other_v_id in pool.vouchers:
                        if v_id != other_v_id:
                            G.add_edge(v_id, other_v_id, pool=pool.name)
    return G

def bfs_node_levels(graph, start_node):
    levels = {start_node: 0}
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        for neighbor in graph.neighbors(node):
            if neighbor not in levels:
                levels[neighbor] = levels[node] + 1
                queue.append(neighbor)
    return levels


def find_feasible_paths(G, input_voucher, output_voucher, amount, max_path_length=PATH_LENGTH):
    def dfs(current_voucher, target_voucher, path, visited):
        if len(path) > max_path_length:
            return
        if current_voucher == target_voucher:
            feasible_paths.append(list(path))
            return
        for neighbor in G[current_voucher]:
            pool_name = G[current_voucher][neighbor]['pool']
            pool = next((p for p in swap_pools if p.name == pool_name), None)
            if pool and pool.vouchers.get(neighbor, 0) >= amount and neighbor not in visited:
                if pool.is_active == 1:
                    path.append(neighbor)
                    visited.add(neighbor)
                    dfs(neighbor, target_voucher, path, visited)
                    path.pop()
                    visited.remove(neighbor)

    feasible_paths = []
    visited = set([input_voucher.name])
    dfs(input_voucher.name, output_voucher.name, [input_voucher.name], visited)
    return feasible_paths

# Example usage
#paths = find_feasible_paths(G, input_voucher, output_voucher, amount)


def old_find_feasible_paths(G, input_voucher, output_voucher, amount):
    try:
        # Find all paths using a simple path generator
        all_paths = nx.all_simple_paths(G, input_voucher.name, output_voucher.name)
        
        feasible_paths = []
        
        for path in all_paths:
            if len(path) > 5:  # Limit path length to 10
                continue
            print("a found ...... ")
        
            feasible = True
            for i in range(len(path) - 1):
                start_voucher, end_voucher = path[i], path[i + 1]
                pool_name = G[start_voucher][end_voucher]['pool']
                pool = next(pool for pool in swap_pools if pool.name == pool_name)

                # Check if the pool has enough supply
                if pool.vouchers.get(end_voucher, 0) < amount:
                    feasible = False
                    break
            
            if feasible:
                feasible_paths.append(path)

        return feasible_paths
    except nx.NetworkXNoPath:
        return []


def find_best_exchange_route(G, input_voucher, output_voucher):

    # Check if both vouchers are in the graph
    if input_voucher.name not in G or output_voucher.name not in G:
        return None

    # Use a breadth-first search to find the shortest path
    try:
        path = nx.shortest_path(G, input_voucher.name, output_voucher.name)
        return path
    except nx.NetworkXNoPath:
        return None

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


# Function to execute exchanges along the path
def execute_path_exchanges(G, path, amount,agent):
    transactions = 0
    for i in range(len(path) - 1):
        start_voucher_id, end_voucher_id = path[i], path[i + 1]
        pool_name = G[start_voucher_id][end_voucher_id]['pool']
        pool = next(pool for pool in swap_pools if pool.name == pool_name)

        start_voucher = next(voucher for voucher in all_vouchers if voucher.name == start_voucher_id)
        end_voucher = next(voucher for voucher in all_vouchers if voucher.name == end_voucher_id)

        # Find the agent who owns the start_voucher
        #agent = next(agent for agent in all_agents if start_voucher in agent.vouchers.values())
        #print("exec path: ",agent,start_voucher,end_voucher,path)
        pool.exchange(agent, start_voucher, end_voucher, amount)
        transactions += 1

    
    
    return transactions


def run_exchanges(G,agent,transactions_this_cycle):
    global all_agents, all_vouchers_inpools, swap_pools, all_agents_inpools
    # For each agent, attempt to make an exchange
    #agent = all_agents[0]
    
    path = None
    #if len(all_agents_inpools)>0:
    if True:
    #for agent in all_agents:

        agent.nutrients -= 1
        
        if random.random() < 1.25 and agent.vouchers:
            input_voucher = agent.issued_voucher#next((v for v in all_vouchers if v.issuer == agent), None)

            if agent.vouchers.get(input_voucher.name,0) < 1:
                return 0, None

            current_bal = agent.vouchers.get(input_voucher.name,0)
            #if current_bal < MAX_START_BALANCE/2:
            #    return transactions_this_cycle, path

            #per_bal = current_bal/MAX_START_BAL
            
            amount = min(5,random.randint(1, agent.vouchers.get(input_voucher.name,0)))
            #amount = random.randint(1, agent.vouchers.get(input_voucher.name,0))

            # Ensure a different Voucher object is selected
            #print(all_vouchers)
            #print("input: ",input_voucher)
            #print("all vouchers in pools len", len(all_vouchers_inpools))
            #print("all vouchers in pools", all_vouchers_inpools)

            
            output_voucher = random.choice([v for v in all_vouchers_inpools if v.name != input_voucher.name])

            #close_agents = find_closest_agents(zpos[agent.name], 8)
            #zclose_agent = next((agent for agent in all_agents_inpools if agent.name == close_agent),None)

            #output_voucher = zclose_agent.issued_voucher
            
            
            #print("tst",input_voucher,output_voucher)
            
            #output_voucher = all_vouchers[len(all_vouchers)-1]

            if input_voucher.name in G and output_voucher.name in G:
                #print("Find all feasible paths",agent.name, "(",amount,")", input_voucher.name, output_voucher.name)
                feasible_paths = find_feasible_paths(G, input_voucher, output_voucher, amount)
                if feasible_paths:
                    # Choose the best path (e.g., the shortest one)
                    best_path = min(feasible_paths, key=len)
                    #print("a Best exchange route:", best_path)
                    #print("all routes:", feasible_paths)
                    print_exchange_route(G, best_path)
                    transactions_this_cycle += execute_path_exchanges(G, best_path, amount,agent)

                    # Create a new path that starts with the agent's name and includes the swap pools
                    new_path = [agent.name]
                    for i in range(len(best_path) - 1):
                        start_voucher, end_voucher = best_path[i], best_path[i + 1]
                        pool_name = G[start_voucher][end_voucher]['pool']
                        new_path.append(pool_name)

                    final_voucher = next(voucher for voucher in all_vouchers if voucher.name == best_path[-1])
                    final_agent=final_voucher.issuer

                    #add a final transaction to the issuer of the final voucher
                    #print("a agent :", agent.vouchers, " final. agent: ", final_agent.vouchers)
                    final_agent.vouchers[final_voucher.name] += agent.vouchers[final_voucher.name]
                    agent.vouchers[final_voucher.name] = 0
                    #print("b agent :", agent.vouchers, " final. agent: ", final_agent.vouchers)

                    
                    new_path.append(final_agent.name)
                    #print("final path: ",path)

                    path = new_path
                    #print("finished exchange final path: ", path)

    if grow_mode:
        #attempt to create a small pool.
        # find the nearest with no pools or agents around
        if agent.nutrients > HEALTHY_NUTRIENTS+2:

            agent_pos = zpos[agent.name]
            #print(agent.name, " pos: ", agent_pos, " agents in pools: ", all_agents_inpools)
            
            close_agents = find_closest_agents(agent_pos, 8)
            created_new = False
            #print(" close agents: ", close_agents)
            for close_agent in close_agents:
                if created_new == False:
                    zclose_agent = next((agent for agent in all_agents if agent.name == close_agent),None)
                    if zclose_agent not in all_agents_inpools:
                        #print("close_agent not in pools: ", close_agent)
                        new_agent_pos = zpos[close_agent]

                        new_point = find_midpoint(agent_pos,new_agent_pos)

                        x1, y1 = new_point


                        collision = False

                        for node_name, (node_x, node_y) in zpos.items():
                            if is_within_circle(x1, y1, node_x, node_y, node_radius*2):
                                collision = True
                                break
                        if collision:
                            break                    

                        new_agents = [agent.name,close_agent]
                    
                        new_swap_pool = {
                            'position': new_point,
                            'connected_agents': new_agents,
                            'vouchers': {}  # Dictionary to store vouchers from each agent
                            
                        }
                        pool_name = "SP0"
                        if swap_pools != None:
                            pool_name = f"SP{len(swap_pools)}"  # Generating a unique name for the pool
                        else:
                            swap_pools = []

                        new_swap_pool = SwapPool(pool_name)

                        for zagent in new_agents:
                            agent = next(agent for agent in all_agents if agent.name == zagent)
                            voucher = agent.issued_voucher
                            amount = min(POOL_START_ASSETS,random.randint(0, agent.vouchers[voucher.name]))
                            #amount = random.randint(0, agent.vouchers[voucher.name])
                            new_swap_pool.deposit(agent, voucher, amount)
                            if agent not in all_agents_inpools:
                                all_agents_inpools.append(agent)
                            if voucher not in all_vouchers_inpools:
                                all_vouchers_inpools.append(voucher)
                            created_new = True
                            agent.nutrients = 0 #reset nutrient counter

                        swap_pools.append(new_swap_pool)

                        zpos[pool_name] = new_point
            if agent.nutrients > HEALTHY_NUTRIENTS + 2: #The agent has nutrition but can't find a new place to put a pool should add an arm to an existing pool if the pool has less than 4 vouchers already
                close_pools = find_closest_pool(agent_pos, 4)
                created_new_branch = False
                #print(" close Pools: ", close_pools)
                for close_pool in close_pools:
                    if created_new_branch == False:
                        zclose_pool = next((pool for pool in swap_pools if pool.name == close_pool),None)
                        num_branches = len(zclose_pool.vouchers)
                        if num_branches < MAX_CONNECTORS:
                            update_swap_pool(close_pool,num_branches+1,zpos[close_pool])
                            created_new_branch = True
                            agent.nutrients = agent.nutrients - 10*num_branches
                                

                    


    return transactions_this_cycle, path

# Function to create a pool between two vouchers
def create_pool(v1, v2, pool_name):
    global swap_pools
    pool = None

     # Check if a pool already exists containing both vouchers
    for existing_pool in swap_pools:
        if v1.name in existing_pool.vouchers and v2.name in existing_pool.vouchers:
            # A pool with both vouchers already exists, return None
            return None
    
    # Ensure that the deposit amount does not exceed the voucher supply
    agent_v1 = v1.issuer
    agent_v2 = v2.issuer
    amount_v1 = min(random.randint(1, 50), agent_v1.vouchers.get(v1.name, 0))
    amount_v2 = min(random.randint(1, 50), agent_v2.vouchers.get(v2.name, 0))

    # Deposit only if both agents have enough vouchers
    if amount_v1 > 0 or amount_v2 > 0:
        pool = SwapPool(pool_name)
        swap_pools.append(pool)

        if amount_v1 >= 0:
            pool.deposit(agent_v1, v1, amount_v1)
        if amount_v2 >= 0:
            pool.deposit(agent_v2, v2, amount_v2)
    return pool

def run_pool_swaps(G):
    # Performing 20 Random Exchanges by pools
    for _ in range(0):
        pool = random.choice(swap_pools)

        if len(pool.vouchers) > 1:
            v1_id, v2_id = random.sample(pool.vouchers.keys(), 2)

            # Retrieve the actual Voucher objects
            input_voucher = next(voucher for voucher in all_vouchers if voucher.name == v1_id)
            output_voucher = next(voucher for voucher in all_vouchers if voucher.name == v2_id)

            # Find the agents who own these vouchers
            agent1 = next((agent for agent in all_agents if input_voucher in agent.vouchers.values()), None)
            # Perform exchange with Voucher objects
            if agent1 and input_voucher and output_voucher:
                amount = min(min(random.randint(1, 10),agent1.vouchers.get(input_voucher.name, 0).supply),pool.vouchers[output_voucher.name])
                if amount > 0:
                    print("exchange amount:", amount, agent1, input_voucher.name,output_voucher.name)

                    path = find_best_exchange_route(G, input_voucher, output_voucher)
                    print("Best exchange route:", path)

                    print_exchange_route(G, path)



                    #print("exchange pool b:", pool)
                    pool.exchange(agent1, input_voucher, output_voucher, amount)
                    #print("exchange pool a:", pool)
    

def create_random_pools():
    # Ensure that every voucher is represented at least once
    for voucher in all_vouchers:
        agent = next((a for a in all_agents if voucher.name in a.vouchers), None)
        if agent:
            pool = random.choice(swap_pools)
            amount = random.randint(1, min(500, agent.vouchers[voucher.name]))
            pool.deposit(agent, voucher, amount)

    # Further distribute remaining vouchers randomly
    for _ in range(len(all_vouchers), len(swap_pools) * 5):
        voucher = random.choice(all_vouchers)
        agent = next((a for a in all_agents if voucher.name in a.vouchers), None)
        
        if agent:
            valid_pools = [p for p in swap_pools if len(p.vouchers) < 5 and voucher.name not in p.vouchers]
            if valid_pools:
                pool = random.choice(valid_pools)
                amount = random.randint(1, min(500, agent.vouchers[voucher.name]))
                pool.deposit(agent, voucher, amount)

                
def create_branches(voucher, depth, max_depth, chain_index, chain):
    global used_vouchers, swap_pools
    #if depth > max_depth:
    #    used_vouchers.add(voucher)
    #    return
    if max_depth < 1:
        used_vouchers.add(voucher)
        return chain
    
    #print("YYYYYYYYYYYYYY", swap_pools)
    #print("bb voucher", voucher)
    # Determine the number of branches at this level
    branch_length = max_depth#random.randint(1, 3) if depth < max_depth else random.randint(0, 2)

    branch_vouchers = []
    used_vouchers.add(voucher)
    for b in range(branch_length):

        # Select available vouchers for branching that haven't been used in this specific branch
        available_vouchers = [v for v in chain if v != voucher and v not in used_vouchers]
        if not available_vouchers:
            break

        branch_voucher = random.choice(available_vouchers)
        pool_index = len(swap_pools)+1
        branch_pool_name = f"SP{pool_index}"

        zpool = create_pool(voucher, branch_voucher, branch_pool_name)
        #print("a depth: ", depth, " vouchers a:: ",voucher.name, " b: ",branch_voucher.name, zpool)
        #print("b            pool: ", zpool)
        used_vouchers.add(branch_voucher)
        
        branch_vouchers.append(branch_voucher)

    new_chain =  [x for x in chain[1:]]        
    for bv in branch_vouchers:
        #print("old chain: ",chain)

        #new_chain =  [x for x in chain[1:]]
        # New chain is the old chain without the current voucher
        new_chain = [x for x in chain if x != voucher and x != branch_voucher and x not in branch_vouchers]
        #print("new chain: ",new_chain)
        # Recursive call to create further branches
        chain = new_chain
        chain = create_branches(branch_voucher, depth + 1, max_depth - 1, chain_index, new_chain)
    return new_chain


def create_chained_branching_pools():
    global all_vouchers, swap_pools, used_vouchers

    swap_pools = [SwapPool(f"SP{i}") for i in range(1, 6)]
    swap_pools.clear()  # Clear existing pools
    usd_vouchers = [v for v in all_vouchers if v.name == 'USD']
    usd_voucher = usd_vouchers[0]
    non_usd_vouchers = [v for v in all_vouchers if v.name != 'USD']

    # Divide non-USD vouchers into three groups for the main chains
    chain_length = len(non_usd_vouchers) // 4
    main_chains = [non_usd_vouchers[i:i + chain_length] for i in range(0, len(non_usd_vouchers), chain_length)]

    # Adjust the last main chain to include the remaining vouchers
    if len(non_usd_vouchers) % 4 != 0:
        main_chains[-1].extend(non_usd_vouchers[-(len(non_usd_vouchers) % 3):])
        
    #print("mc: ",main_chains)
    
    max_depth = 3  # Increased maximum depth for more branching
    for chain_index, chain in enumerate(main_chains, start=1):
        if used_vouchers == None:
            used_vouchers = set()
        #for i, voucher in enumerate(chain):
        main_pool_name = f"SP{chain_index}M{chain_index}"
        next_voucher = chain[0] #if i == len(chain) - 1 else chain[i + 1]
        #print("next voucher: ", next_voucher)
        create_pool(usd_voucher, next_voucher, main_pool_name)
        
        used_vouchers.add(usd_voucher)

            # Initiate branching from each voucher in the main chain
            #print("UUUUUUUUUUUUUUUUUUUUUsed_vouchers: ",used_vouchers)
            #print("swap-pool: ",swap_pools)
            
            # Recursive call to create further branches
        for voucher in enumerate(chain, start=1):
            #print("aa voucher: ",voucher)
            create_branches(voucher[1], 1, max_depth, chain_index, chain)

    return swap_pools


def create_chained_branching_pools_alt():
    global all_vouchers, swap_pools, used_vouchers
    # Additional Swap Pool with random vouchers

    # Create a new graph for Agent-Swap Pool interactions
    G_agents_pools_tmp = nx.Graph()

    # Add nodes for agents and swap pools
    G_agents_pools_tmp.add_node('b0', node_type='agent', level=0)

    # Establish connections
    for pool in swap_pools:
        # Connect pools to agents based on voucher issuers
        for voucher_name in pool.vouchers.keys():
            voucher = next(voucher for voucher in all_vouchers if voucher.name == voucher_name)
            issuer_name = voucher.issuer.name
            G_agents_pools_tmp.add_node(pool.name, node_type='pool')
            G_agents_pools_tmp.add_node(issuer_name, node_type='agent')
            G_agents_pools_tmp.add_edge(pool.name, issuer_name)
            #print("edge: ", pool.name, issuer_name)

    # Calculate node levels from the 'b0' node
    levels = nx.single_source_shortest_path_length(G_agents_pools_tmp, 'b0')

    low_level_agents = []
    for level in range(max(levels.values()) + 1):
        if level < max(levels.values()) + 1 - 3:
            continue
        level_nodes = [node for node, lvl in levels.items() if lvl == level]
        for i, node in enumerate(level_nodes):
            if G_agents_pools_tmp.nodes[node]['node_type'] == 'agent':
                low_level_agents.append(node)

    #print("low lvl: ", low_level_agents)
    #if False:
    if len(low_level_agents) >= 5:
        random_vouchers = random.sample(low_level_agents, 8)

        additional_pool_name = "uteo"
        additional_pool = SwapPool(additional_pool_name)
        for agent_name in random_vouchers:
            agent = next(zagent for zagent in all_agents if zagent.name == agent_name)
            voucher = agent.issued_voucher
            #print("agent: ",agent, agent.vouchers,voucher.name)
            amount = random.randint(1, min(500, agent.vouchers[voucher.name]))
            additional_pool.deposit(voucher.issuer, voucher, amount)
        swap_pools.append(additional_pool)
    


def draw_agent_swap_pool_grid(agents, swap_pools, screen, recent_exchange_path):
    global G_agents_pools, zpos

    # Define the area for the diagram
    diagram_width = SCREEN_WIDTH - 500
    diagram_height = SCREEN_HEIGHT - 50
    diagram_x_offset = 50
    diagram_y_offset = 50

    # Create a new graph for Agent-Swap Pool interactions
    G_agents_pools = nx.Graph()

    # Add nodes for agents and swap pools
    G_agents_pools.add_node('b0', node_type='agent', level=0)


    for agent in all_agents:
        G_agents_pools.add_node(agent.name, node_type='agent')

    # Establish connections
    if swap_pools != None:
        for pool in swap_pools:
            # Connect pools to agents based on voucher issuers
            for voucher_name in pool.vouchers.keys():
                voucher = next(voucher for voucher in all_vouchers if voucher.name == voucher_name)
                issuer_name = voucher.issuer.name
                G_agents_pools.add_node(pool.name, node_type='pool')
                G_agents_pools.add_node(issuer_name, node_type='agent')
                G_agents_pools.add_edge(pool.name, issuer_name)
                #print("edge: ", pool.name, issuer_name)

    # Calculate node positions
    if zpos is None:
        zpos = {}

        # Grid layout parameters
        grid_size = int(math.ceil(math.sqrt(len(agents))))
        grid_spacing = 100

        # Find center grid coordinates
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        start_x = center_x - (grid_size // 2) * grid_spacing
        start_y = center_y - (grid_size // 2) * grid_spacing

        # Place 'b0' in the center
        zpos['b0'] = (center_x, center_y)

        # Place other agents in the grid
        agent_index = 0
        for row in range(grid_size):
            for col in range(grid_size):
                if row == grid_size // 2 and col == grid_size // 2:
                    continue  # Skip the center for 'b0'
                if agent_index >= len(agents):
                    break

                agent_x = start_x + col * grid_spacing
                agent_y = start_y + row * grid_spacing
                zpos[agents[agent_index].name] = (agent_x, agent_y)
                agent_index += 1
    

    if toggle_mutual:
        zpos['uteo'] = (SCREEN_WIDTH / 3+20, SCREEN_HEIGHT - 2*diagram_y_offset)

            
    # Draw edges, nodes, and labels
    node_radius = 20
    voucher_radius = 5
    font = pygame.font.Font(None, 16)
    balance_font = pygame.font.Font(None, 15)


    # Draw the most recent exchange as a curved blue line
    if recent_exchange_path and len(recent_exchange_path) > 1:
        curve_points = [zpos[node] for node in recent_exchange_path if node in zpos]
        if len(curve_points) > 1:
            #print("curve points: ", curve_points) 
            #pygame.draw.lines(screen, (0, 0, 255), False, curve_points, 2)
            itter = 0
            for point in curve_points:
                if itter+1 >= len(curve_points):
                    break
                draw_curved_line(point, curve_points[itter+1], GREEN, 10)
                itter += 1

    # Draw edges (straight black lines)
    for u, v, data in G_agents_pools.edges(data=True):
        pygame.draw.line(screen, (0, 0, 0), zpos[u], zpos[v], 2)

        
    # Draw vouchers inside each pool with their amounts
    for node, (x, y) in zpos.items():
        node_color = 'red'
        node_type = G_agents_pools.nodes[node]['node_type']
        #print("node: ", node)
        #print(all_agents_inpools)

        if node_type == 'agent':
            node_color = 'red'
            agent = next((zagent for zagent in all_agents if zagent.name == node),None)
            if agent.nutrients >= HEALTHY_NUTRIENTS:
                node_color = 'green'
            pygame.draw.circle(screen, pygame.Color(node_color), (int(x), int(y)), node_radius)  
        elif node_type == 'pool':
            node_color = 'blue'
            pool = next(p for p in swap_pools if p.name == node)
            if pool and not getattr(pool, "is_active", 2):  # Check if the pool is inactive
                node_color = BLACK  # Inactive pools in black
            pygame.draw.rect(screen, pygame.Color(node_color), pygame.Rect(int(x)-POOL_WIDTH/2, int(y)-POOL_HEIGHT/2,POOL_WIDTH,POOL_HEIGHT))
            angle = 0
            angle_step = 360 / len(pool.vouchers)
            for voucher_name in pool.vouchers:
                voucher_amount = pool.vouchers[voucher_name]  # Get the amount of voucher in the pool
                voucher_x = x + (node_radius + 5) * math.cos(math.radians(angle))
                voucher_y = y + (node_radius + 5) * math.sin(math.radians(angle))

                # Render the voucher name
                voucher_name_label = font.render(voucher_name, True, (0, 0, 0))
                voucher_name_label_rect = voucher_name_label.get_rect()
                voucher_name_label_rect.center = (int(voucher_x), int(voucher_y) - 5)  # Shift upwards for vertical centering
                screen.blit(voucher_name_label, voucher_name_label_rect)

                # Render the voucher amount
                voucher_amount_label = font.render(str(voucher_amount), True, (0, 0, 0))
                voucher_amount_label_rect = voucher_amount_label.get_rect()
                voucher_amount_label_rect.center = (int(voucher_x), int(voucher_y) + 5)  # Shift downwards for vertical centering
                screen.blit(voucher_amount_label, voucher_amount_label_rect)
                
                angle += angle_step

        if node_type == 'agent':
            agent_d = next(ag for ag in agents if ag.name == node)
            total_supply = agent_d.vouchers[agent_d.issued_voucher.name]

            # Render agent's name and total supply as separate lines, centered in the red circle
            agent_label_name = font.render(agent_d.name, True, (255, 255, 255))
            agent_label_supply = font.render(str(total_supply), True, (255, 255, 255))

            # Calculate positions for both lines to center them inside the red circle
            agent_label_name_rect = agent_label_name.get_rect()
            agent_label_name_rect.center = (int(x), int(y) - 10)  # Shift name slightly above circle center

            agent_label_supply_rect = agent_label_supply.get_rect()
            agent_label_supply_rect.center = (int(x), int(y) + 10)  # Shift supply slightly below circle center

            screen.blit(agent_label_name, agent_label_name_rect)
            screen.blit(agent_label_supply, agent_label_supply_rect)


def draw_agent_swap_pool_diagram(agents, swap_pools, screen, recent_exchange_path):
    global G_agents_pools, zpos

    # Define the area for the diagram
    diagram_width = SCREEN_WIDTH - 500
    diagram_height = SCREEN_HEIGHT - 50
    diagram_x_offset = 50
    diagram_y_offset = 50

    # Create a new graph for Agent-Swap Pool interactions
    G_agents_pools = nx.Graph()

    # Add nodes for agents and swap pools
    G_agents_pools.add_node('b0', node_type='agent', level=0)

    # Establish connections
    for pool in swap_pools:
        # Connect pools to agents based on voucher issuers
        for voucher_name in pool.vouchers.keys():
            voucher = next(voucher for voucher in all_vouchers if voucher.name == voucher_name)
            issuer_name = voucher.issuer.name
            G_agents_pools.add_node(pool.name, node_type='pool')
            G_agents_pools.add_node(issuer_name, node_type='agent')
            G_agents_pools.add_edge(pool.name, issuer_name)
            #print("edge: ", pool.name, issuer_name)

    # Calculate node levels from the 'b0' node
    levels = nx.single_source_shortest_path_length(G_agents_pools, 'b0')

    # Position nodes level by level
    if zpos == None:
        zpos = {'b0': (SCREEN_WIDTH / 2, diagram_y_offset)}
    
        for level in range(max(levels.values()) + 1):
            level_nodes = [node for node, lvl in levels.items() if lvl == level]
            num_nodes = len(level_nodes)
            x_step = diagram_width / max(num_nodes, 1)
            y_position = diagram_y_offset + level * (diagram_height / (max(levels.values()) + 1))

            for i, node in enumerate(level_nodes):
                x_position = diagram_x_offset + i * x_step
                zpos[node] = (x_position, y_position)

        zpos['b0'] = (SCREEN_WIDTH / 3+20, diagram_y_offset)
    # Check if the key 'uteo' exists in the 'pos' dictionary

    if toggle_mutual:
        zpos['uteo'] = (SCREEN_WIDTH / 3+20, SCREEN_HEIGHT - 2*diagram_y_offset)

            
    # Draw edges, nodes, and labels
    node_radius = 20
    voucher_radius = 5
    font = pygame.font.Font(None, 16)
    balance_font = pygame.font.Font(None, 15)


    # Draw the most recent exchange as a curved blue line
    if recent_exchange_path and len(recent_exchange_path) > 1:
        curve_points = [zpos[node] for node in recent_exchange_path if node in zpos]
        if len(curve_points) > 1:
            #print("curve points: ", curve_points) 
            #pygame.draw.lines(screen, (0, 0, 255), False, curve_points, 2)
            itter = 0
            for point in curve_points:
                if itter+1 >= len(curve_points):
                    break
                draw_curved_line(point, curve_points[itter+1], GREEN, 10)
                itter += 1

    # Draw edges (straight black lines)
    for u, v, data in G_agents_pools.edges(data=True):
        pygame.draw.line(screen, (0, 0, 0), zpos[u], zpos[v], 2)

        
    # Draw vouchers inside each pool with their amounts
    for node, (x, y) in zpos.items():
        node_color = 'red' if G_agents_pools.nodes[node]['node_type'] == 'agent' else 'blue'
        if node_color == 'blue':
            pool = next((p for p in swap_pools if p.name == node), None)
            if pool and not getattr(pool, "is_active", 2):  # Check if the pool is inactive
                node_color = BLACK  # Inactive pools in black

            pygame.draw.rect(screen, pygame.Color(node_color), pygame.Rect(int(x)-5, int(y)-10,10,20))
        else:
            pygame.draw.circle(screen, pygame.Color(node_color), (int(x), int(y)), node_radius)
            
        if G_agents_pools.nodes[node]['node_type'] == 'pool':
            pool = next(p for p in swap_pools if p.name == node)
            angle = 0
            angle_step = 360 / len(pool.vouchers)
            for voucher_name in pool.vouchers:
                voucher_amount = pool.vouchers[voucher_name]  # Get the amount of voucher in the pool
                voucher_x = x + (node_radius + 5) * math.cos(math.radians(angle))
                voucher_y = y + (node_radius + 5) * math.sin(math.radians(angle))

                # Render the voucher name
                voucher_name_label = font.render(voucher_name, True, (0, 0, 0))
                voucher_name_label_rect = voucher_name_label.get_rect()
                voucher_name_label_rect.center = (int(voucher_x), int(voucher_y) - 5)  # Shift upwards for vertical centering
                screen.blit(voucher_name_label, voucher_name_label_rect)

                # Render the voucher amount
                voucher_amount_label = font.render(str(voucher_amount), True, (0, 0, 0))
                voucher_amount_label_rect = voucher_amount_label.get_rect()
                voucher_amount_label_rect.center = (int(voucher_x), int(voucher_y) + 5)  # Shift downwards for vertical centering
                screen.blit(voucher_amount_label, voucher_amount_label_rect)
                
                angle += angle_step

        if node_color == 'red':
            agent_d = next(ag for ag in agents if ag.name == node)
            total_supply = agent_d.vouchers[agent_d.issued_voucher.name]

            # Render agent's name and total supply as separate lines, centered in the red circle
            agent_label_name = font.render(agent_d.name, True, (255, 255, 255))
            agent_label_supply = font.render(str(total_supply), True, (255, 255, 255))

            # Calculate positions for both lines to center them inside the red circle
            agent_label_name_rect = agent_label_name.get_rect()
            agent_label_name_rect.center = (int(x), int(y) - 10)  # Shift name slightly above circle center

            agent_label_supply_rect = agent_label_supply.get_rect()
            agent_label_supply_rect.center = (int(x), int(y) + 10)  # Shift supply slightly below circle center

            screen.blit(agent_label_name, agent_label_name_rect)
            screen.blit(agent_label_supply, agent_label_supply_rect)


        
def draw_network_diagram(agents, liquidity_pools, screen):
    global G, pos
    G = Gp
    #pos = nx.spectral_layout(G)
    
    # Get the screen dimensions
    screen_width = min(500, screen.get_width())
    screen_height = min(600, screen.get_height())

    # Find the minimum and maximum positions of nodes in the layout
    min_x = min(x for x, _ in pos.values())
    max_x = max(x for x, _ in pos.values())
    min_y = min(y for _, y in pos.values())
    max_y = max(y for _, y in pos.values())

     # Calculate scaling factors and offsets to fit and center the graph on the right half
    x_scale = (screen_width - 50) / (max_x - min_x)  # 200 for left offset and 100 for right border
    y_scale = (screen_height - 50) / (max_y - min_y)  # 100 for top and bottom borders
    scale = min(x_scale, y_scale)

    x_offset = 1300+screen_width - 100 - (max_x - min_x) * scale  # 100-pixel right border
    y_offset = (screen_height - (max_y - min_y) * scale) / 2 + 100  # 100-pixel top border

    # Draw edges with weights (you may need to customize this part)
    for u, v, data in G.edges(data=True):
        u_x = (pos[u][0] - min_x) * scale + x_offset
        u_y = (pos[u][1] - min_y) * scale + y_offset
        v_x = (pos[v][0] - min_x) * scale + x_offset
        v_y = (pos[v][1] - min_y) * scale + y_offset
        pygame.draw.line(screen, (0, 0, 255), (u_x, u_y), (v_x, v_y), 2)

    # Draw nodes as larger circles with labels inside
    node_radius = 15  # Increase the radius for larger circles
    node_color = 'black'
    font = pygame.font.Font(None, 18)
    for node, (x, y) in pos.items():
        x = (x - min_x) * scale + x_offset
        y = (y - min_y) * scale + y_offset
        pygame.draw.circle(screen, pygame.Color(node_color), (int(x), int(y)), node_radius)

        # Draw label inside the circle in white font
        label = font.render(G.nodes[node]['label'], True, (255, 255, 255))
        label_rect = label.get_rect()
        label_rect.center = (int(x), int(y))
        screen.blit(label, label_rect)

# Function to draw curved lines between two points with adjustable arrow size
def draw_arrow(surface, color, start, end, size=10):
    pygame.draw.line(surface, color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(surface, color, (
        (end[0] + size * math.sin(math.radians(rotation)), end[1] + size * math.cos(math.radians(rotation))), 
        (end[0] + size * math.sin(math.radians(rotation - 120)), end[1] + size * math.cos(math.radians(rotation - 120))),
        (end[0] + size * math.sin(math.radians(rotation + 120)), end[1] + size * math.cos(math.radians(rotation + 120)))
    ))
    
    
def draw_curved_line(host, attendee, color,thickness):
    start = (host[0], host[1])
    end = (attendee[0], attendee[1])
    mx, my = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
    offset = 50
    control_point = (mx, my - offset)

    #font = pygame.font.Font(None, 18)  # Font for rendering text
    
    prev_x, prev_y = start
    for t in range(1, 101):
        t /= 100
        p0 = (1-t)*start[0] + t*control_point[0], (1-t)*start[1] + t*control_point[1]
        p1 = (1-t)*control_point[0] + t*end[0], (1-t)*control_point[1] + t*end[1]
        x = int((1-t)*p0[0] + t*p1[0])
        y = int((1-t)*p0[1] + t*p1[1])
        
        pygame.draw.line(screen, color, (prev_x, prev_y), (x, y), thickness)
        prev_x, prev_y = x, y

    draw_arrow(screen, DARK_GREEN, (prev_x, prev_y), end)    
    

    # Shift label along the line for better visibility
    #shift_factor = 0.6  # Adjust as needed
    #label_x = int((1 - shift_factor) * start[0] + shift_factor * end[0])
    #label_y = int((1 - shift_factor) * start[1] + shift_factor * end[1])

                    
    #text = font.render(f"({lp.pools[i][j][0]},{lp.pools[i][j][1]})", True, (0, 0, 0))
    #screen.blit(text, (mx - 10, my - offset - 10))  # Adjusted position
    #screen.blit(text, (label_x, label_y))


def update_graph():
    global Gp, swap_pools, pos

    Gp.clear()
    if swap_pools != None:
        for pool in swap_pools:
            if pool.is_active == 1:
                for (v1_id, v2_id), count in pool.exchanges.items():
                    # Add or update nodes with labels
                    if v1_id not in Gp:
                        Gp.add_node(v1_id, label=v1_id)
                    if v2_id not in Gp:
                        Gp.add_node(v2_id, label=v2_id)

                    # Add edges
                    Gp.add_edge(v1_id, v2_id, weight=count)

    # Recalculate positions
    pos = nx.spring_layout(Gp)

def calculate_statistics(swap_pools, all_vouchers, all_agents, transactions_this_cycle):
    # Total Transactions Per Cycle
    total_transactions_per_cycle = transactions_this_cycle

    # Total Connections
    total_connections = 0
    average_connections = 0
    if swap_pools != None:
        for pool in swap_pools:
            for pair in pool.exchanges.keys():
                total_connections += 1

        # Average Connections per Agent
        connections_per_agent = {}
        for pool in swap_pools:
            for (voucher_id, _), _ in pool.exchanges.items():
                agent_name = next(voucher.issuer.name for voucher in all_vouchers if voucher.name == voucher_id)
                connections_per_agent.setdefault(agent_name, set()).add(pool.name)

        average_connections = sum(len(connections) for connections in connections_per_agent.values()) / len(all_agents)

    return total_transactions_per_cycle, total_connections, average_connections

def render_statistics(screen, statistics, x_offset, y_offset):
    font = pygame.font.Font(None, 24)
    labels = ["Transactions/cycle", "Num Connections", "Avg Connections/Agent"]
    y_step = 30  # Vertical space between lines

    for i, stat in enumerate(statistics):
        formatted_stat = f"{stat:.2f}"
        text = f"{labels[i]}: {formatted_stat}"
        label = font.render(text, True, (0, 0, 0))
        screen.blit(label, (x_offset, y_offset + i * y_step))


def is_within_circle(mouse_x, mouse_y, center_x, center_y, radius):
    return (mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2 <= radius ** 2

def is_within_rectangle(mouse_x, mouse_y, rect_x, rect_y, rect_width, rect_height):
    return rect_x <= mouse_x <= rect_x + rect_width and rect_y <= mouse_y <= rect_y + rect_height

def find_midpoint(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    return (midpoint_x, midpoint_y)


# alive = 1
# paused = 2
# dead = 0
def toggle_pool(pool_name):
    global swap_pools
    pool = next((p for p in swap_pools if p.name == pool_name), None)
    if pool:
        ans = pool.is_active
        if ans == 1:
            pool.is_active = 2
        if ans == 2:
            pool.is_active = 0
        if ans == 0:
            pool.is_active = 1
    return ans
            

def find_closest_agents(click_pos, num_closest):
    """
    Find the closest agents to the click position, only considering agents whose names start with 'b'.

    Parameters:
    click_pos (tuple): The x, y position of the click.
    num_closest (int): Number of closest agents to find.

    Returns:
    list: A list of the closest agents.
    """
    global zpos  # Access the global variable

    # Filter agents whose names start with 'b' and calculate distances
    distances = [(name, math.hypot(pos[0] - click_pos[0], pos[1] - click_pos[1])) 
                 for name, pos in zpos.items() if name.startswith('b')]
    distances.sort(key=lambda x: x[1])  # Sort by distance

    # Return closest agent names, limited to num_closest
    return [name for name, _ in distances[:num_closest]]

def find_closest_pool(click_pos, num_closest):
    """
    Find the closest agents to the click position, only considering agents whose names start with 'b'.

    Parameters:
    click_pos (tuple): The x, y position of the click.
    num_closest (int): Number of closest agents to find.

    Returns:
    list: A list of the closest agents.
    """
    global zpos  # Access the global variable

    # Filter agents whose names start with 'b' and calculate distances
    distances = [(name, math.hypot(pos[0] - click_pos[0], pos[1] - click_pos[1])) 
                 for name, pos in zpos.items() if name.startswith('S')]
    distances.sort(key=lambda x: x[1])  # Sort by distance

    # Return closest agent names, limited to num_closest
    return [name for name, _ in distances[:num_closest]]


def create_swap_pool(click_pos,num_c):
    """
    Create a SwapPool at the click position, connecting the closest agents, and assign random vouchers.

    Parameters:
    click_pos (tuple): The x, y position of the click.

    Returns:
    dict: A dictionary representing the new SwapPool.
    """
    global zpos, swap_pools, all_agents, all_agents_inpools, all_vouchers_inpools

    closest_agents = find_closest_agents(click_pos,num_c)
    new_swap_pool = {
        'position': click_pos,
        'connected_agents': closest_agents,
        'vouchers': {}  # Dictionary to store vouchers from each agent
    }

    pool_name = "SP0"
    if swap_pools != None:
        pool_name = f"SP{len(swap_pools)}"  # Generating a unique name for the pool
    else:
        swap_pools = []
    new_swap_pool = SwapPool(pool_name)

    # Randomly allocate vouchers from each connected agent
    
    for zagent in closest_agents:
        # Assuming each agent has a 'vouchers' attribute
        # Modify this part based on how vouchers are stored and managed
        #print("zagent: ", zagent)
        agent = next(agent for agent in all_agents if agent.name == zagent)
        voucher = agent.issued_voucher
        #amount = min(POOL_START_ASSETS,random.randint(0, agent.vouchers[voucher.name]))
        amount = int(agent.vouchers[voucher.name]/2)
        #amount = random.randint(0, agent.vouchers[voucher.name])
        new_swap_pool.deposit(agent, voucher, amount)
        if agent not in all_agents_inpools:
            all_agents_inpools.append(agent)
        if voucher not in all_vouchers_inpools:
            all_vouchers_inpools.append(voucher)



    # Add the new swap pool to the global list and zpos
    swap_pools.append(new_swap_pool)

    zpos[pool_name] = click_pos

    return new_swap_pool


def update_swap_pool(clicked_pool_name,num_c,click_pos):
    """
    Revamp the current pool to have num_c connectors
    """
    global zpos, swap_pools, all_agents, all_agents_inpools, all_vouchers_inpools

    closest_agents = find_closest_agents(click_pos,num_c)
    pool_s = next(pool for pool in swap_pools if pool.name == clicked_pool_name)
    pool_name = clicked_pool_name
    updated_swap_pool = pool_s #SwapPool(pool_name)

    #print("zpool: ", pool_s)
        
    # Randomly allocate vouchers from each connected agent
    
    for zagent in closest_agents:
        # Assuming each agent has a 'vouchers' attribute
        # Modify this part based on how vouchers are stored and managed
        #print("zagent: ", zagent)
        agent = next(agent for agent in all_agents if agent.name == zagent)
        voucher = agent.issued_voucher
        #print("voucher: ", voucher)
                
        vouch = next((vo for vo in updated_swap_pool.vouchers if vo == voucher.name),None)
        if vouch != None: # don't add existing vouchers
            continue
        
        #amount = min(POOL_START_ASSETS,random.randint(0, agent.vouchers[voucher.name]))
        amount = int(agent.vouchers[voucher.name]/2)
        updated_swap_pool.deposit(agent, voucher, amount)
        if agent not in all_agents_inpools:
            all_agents_inpools.append(agent)
        if voucher not in all_vouchers_inpools:
            all_vouchers_inpools.append(voucher)



    # Add the new swap pool to the global list and zpos
    #swap_pools.append(new_swap_pool)

    #zpos[pool_name] = click_pos

def init_sim():
    global all_vouchers, all_agents, swap_pools, zpos
    cycle = 0
    num_cycles = 0
    transactions_total = 0
    transactions = 0
    del swap_pools
    swap_pools = None
    del zpos
    zpos = None

    business_agents = [Agent(f"b{i}",i) for i in range(1, 41)]
    state_agent = Agent("b0",0)
    usd_voucher = state_agent.produce_voucher("USD", 1, MAX_USD_START_BALANCE)

    all_vouchers = []
    all_vouchers_inpools = []
    all_vouchers.append(usd_voucher)
    all_agents_inpools = []
    all_agents = []
    all_agents.append(state_agent)

    used_vouchers = set()

    for agent in business_agents:
        voucher = agent.produce_voucher("v", 1, MAX_USD_START_BALANCE)
        all_vouchers.append(voucher)
        all_agents.append(agent)


                



    
# Creating Agents
business_agents = [Agent(f"b{i}",i) for i in range(1, NUM_AGENTS)]
state_agent = Agent("b0",0)
usd_voucher = state_agent.produce_voucher("USD", 1, MAX_USD_START_BALANCE)

all_vouchers = []
all_vouchers_inpools = []
all_vouchers.append(usd_voucher)
all_agents = []
all_agents_inpools = []
all_agents.append(state_agent)

used_vouchers = None

for agent in business_agents:
    start_amt = MAX_START_BALANCE #random.randint(1, MAX_START_BALANCE)
    voucher = agent.produce_voucher("v", 1, start_amt)
    all_vouchers.append(voucher)
    all_agents.append(agent)


swap_pools = None #

#create_random_pools()
#swap_pools = create_chained_branching_pools()

# Step 1: Iterate over each SwapPool
if swap_pools != None:
    for pool in swap_pools:
    # Step 2: Create all possible pairs of vouchers within the pool
        voucher_ids = list(pool.vouchers.keys())
        for i, v1_id in enumerate(voucher_ids):
            for v2_id in voucher_ids[i+1:]:
                # Step 3: Update the exchanges dictionary
                if (v1_id, v2_id) not in pool.exchanges and (v2_id, v1_id) not in pool.exchanges:
                    pool.exchanges[(v1_id, v2_id)] = 0

# Add a control state variable
simulation_state = 'stopped'  # Can be 'initial', 'stopped', 'running', or 'step'
view_mode = True
contrib_mode= False
host_mode= False
trade_mode = False
cycle = 0
total_cycles = 0
num_cycles = 0
transactions = 0
transactions_total = 0
toggle_mutual = False
zpos = None
node_radius = 5
draw_diagram = False
num_con = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the click is on a swap pool
            found_pool = False
            found_pool_name = None
            for pool_name, (pool_x, pool_y) in zpos.items():
                #if is_within_circle(mouse_x, mouse_y, pool_x, pool_y, node_radius):
                if is_within_rectangle(mouse_x, mouse_y, pool_x - POOL_WIDTH, pool_y - POOL_HEIGHT, POOL_WIDTH*2, POOL_HEIGHT*2):
                    #toggle_pool(pool_name)
                    found_pool = True
                    found_pool_name = pool_name
                    break
            # Create a new SwapPool at the click position
            if found_pool == False:
                click_pos = pygame.mouse.get_pos()
                new_pool = create_swap_pool(click_pos,num_con)
                swap_pools.append(new_pool)
            elif found_pool == True: # modify the existing pool to add more 
                update_swap_pool(found_pool_name,num_con,click_pos)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                init_sim()
                simulation_state = 'initial'
            if event.key == pygame.K_f:
                if draw_diagram == True:
                    draw_diagram = False
                else:
                    draw_diagram = True
            elif event.key == pygame.K_p:
                if simulation_state == 'running':
                    simulation_state = 'stopped'
                else:
                    simulation_state = 'running'
            elif event.key == pygame.K_s:
                simulation_state = 'step'
            elif event.key == pygame.K_r:
                simulation_state = 'running'
            elif event.key == pygame.K_g:
                if grow_mode == True:
                    grow_mode = False
                else:
                    grow_mode = True
            elif event.key == pygame.K_q:
                pygame.quit()
                exit(0)
            elif event.key == pygame.K_RIGHT:  # Right arrow key
                delay_time = max(0, delay_time // 2)  # Halve the delay time, minimum 5 ms
            elif event.key == pygame.K_LEFT:  # Left arrow key
                if delay_time == 0:
                    delay_time = 10
                else:
                    delay_time = delay_time * 2  # Double the delay time
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Increase the num_agents
                num_agents += 1
                angle = 2 * math.pi / num_agents
                init_sim()
                simulation_state = 'initial'
            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:  # Decrease the num_agents
                if num_agents > 1:  # At least one agent should remain
                    num_agents -= 1
                    angle = 2 * math.pi / num_agents
                    init_sim()
                    simulation_state = 'initial'
            elif event.key == pygame.K_2:
                num_con = 2
            elif event.key == pygame.K_3:
                num_con = 3
            elif event.key == pygame.K_4:
                num_con = 4
            elif event.key == pygame.K_5:
                num_con = 5
            elif event.key == pygame.K_6:
                num_con = 6
            elif event.key == pygame.K_7:
                num_con = 7
            elif event.key == pygame.K_8:
                num_con = 8
            elif event.key == pygame.K_9:
                num_con = 9
            elif event.key == pygame.K_d:
                if toggle_mutual == False:
                    toggle_mutual = True
                else:
                    toggle_mutual = False

                if toggle_mutual:
                    additional_pool_name = "uteo"
                    pool_s = next((pool for pool in swap_pools if pool.name == additional_pool_name),None)
                    if pool_s != None:
                        pool_s.fill(all_vouchers)
                    else:
                        create_chained_branching_pools_alt()
                # remove any extra swapools
                else:
                    additional_pool_name = "uteo"
                    pool_s = next(pool for pool in swap_pools if pool.name == additional_pool_name)
                    pool_s.empty(all_vouchers)

        
    if simulation_state == 'stopped':
        continue
    elif simulation_state == 'step':
        simulation_state = 'stopped'
        
    screen.fill(WHITE)


    G = make_graph(swap_pools)

    path = None
    transactions_per_cycle = 0
    if len(all_agents_inpools)>0:
        transactions, path = run_exchanges(G,all_agents_inpools[cycle],transactions)
        
        #transactions_total += transactions
        #transactions_per_cycle = transactions_total / (1+cycle+num_cycles*len(all_agents_inpools))
        transactions_per_cycle = transactions / (1+num_cycles)

    #print("trans :", transactions, cycle, num_cycles*len(all_agents_inpools))
    #print("trans :", transactions, " cycle: ", cycle, " total_cycles: ", total_cycles, " num_cycles: ", num_cycles, transactions_per_cycle)

    update_graph()
    if draw_diagram:
        draw_network_diagram(all_agents, swap_pools, screen)

    
    #draw_agent_swap_pool_diagram(all_agents, swap_pools, screen,path)
    draw_agent_swap_pool_grid(all_agents, swap_pools, screen,path)

    # Calculate statistics
    stats = calculate_statistics(swap_pools, all_vouchers, all_agents, transactions_per_cycle)
    
    # Define the position for the stats block
    stats_x_offset = SCREEN_WIDTH - 300  # Adjust as needed
    stats_y_offset = 50  # Adjust as needed

    # Render the statistics on the screen
    render_statistics(screen, stats, stats_x_offset, stats_y_offset)

    # Update the display

    pygame.display.flip()
    pygame.time.delay(delay_time)

    cycle = cycle + 1
    total_cycles = total_cycles + 1
    if cycle >= len(all_agents_inpools):
        cycle = 0
        num_cycles += 1
