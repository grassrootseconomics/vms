"""
Mwerya Simulation with Promise Theory

This script simulates an economic system based on Promise Theory, visualizing interactions between agents within a Mwerya (community). It uses Pygame for rendering the simulation and allows user interaction through command-line arguments. The simulation models economic activities, including exchanges and contributions, within a community of agents. Each agent has a set of promises (vouchers) and can exchange them with others, contributing to the community's liquidity pool. The simulation also includes statistical calculations like Gini coefficient and equity distribution.

Classes:
    Agent: Represents an individual in the Mwerya simulation.
    LP: Represents the liquidity pool in the Mwerya community.

Functions:
    initialize_simulation(): Initializes the simulation with agents and settings.
    calculate_value_created(attendees): Calculates the value created in the community.
    draw_liquidity_pool(agent1, agent2, promises1, promises2): Draws liquidity pools between agents.
    draw_arrow(surface, color, start, end): Draws an arrow between two points.
    draw_curved_line(lp, host, attendee, color, thickness): Draws curved lines representing transactions.
    gini_coefficient(x): Calculates the Gini coefficient for inequality measurement.
    draw_stats(cycle_count): Draws statistical information on the Pygame screen.
    save_screen_to_file(screen, filename): Saves the current screen to a file.
    create_gif(image_folder, gif_filename, duration): Creates a GIF from saved images.

Command-line Arguments:
    -g/--gif_cycles: Specifies the number of full Mwerya cycles for GIF creation.

Usage:
    Run the script with Python and optionally use the -g argument to specify the number of cycles for GIF creation.
    Interact with the simulation using keyboard inputs to control various modes and states.
"""
# Import required modules
import pygame
import random
import math
from PIL import Image
import os
from datetime import datetime
import glob
import argparse
import csv

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Mwerya Simulation with Promise Theory")
parser.add_argument("-g", "--gif_cycles", type=int, help="Number of full Mwerya cycles for GIF creation", default=0)
args = parser.parse_args()

# Get the current date and time
current_date_and_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Initialize Pygame
pygame.init()

# Initialize delay_time
delay_time = 100

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
AGENT_RADIUS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (120, 120, 120)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mwerya Simulation with Promise Theory")


# Agent class

class Agent:
    """
    Represents an individual agent in the Mwerya simulation.

    Each agent has a position, a set of services, liabilities, promises, and other attributes that define its role and actions in the economic simulation.

    Attributes:
        x (int): X-coordinate of the agent's position.
        y (int): Y-coordinate of the agent's position.
        service (str): The service provided by the agent.
        liabilities (int): The amount of liabilities held by the agent.
        promises (list): List of promises (vouchers) held for other agents.
        starting_promises (int): The initial number of promises for tracking risk.
        work_done_for (int): The amount of work done for this agent by others.
        work_done_by (int): The amount of work done by this agent for others.
        confidence (int): A measure of the agent's confidence in the economic system.
    """
    DEFICIT_THRESHOLD = 25.5
    INDIFFERENCE_THRESHOLD = 55.5

    def __init__(self, x, y, service,index,num_agents):
        self.x = x
        self.y = y
        self.service = service
        self.liabilities = 0
        self.promises = [0]*num_agents
        self.promises[index] = 30  # Start with own promises (vouchers)
        self.starting_promises = 30  # Initial promises to track risk
        self.work_done_for = 0  # New variable: Work done for this agent by others
        self.work_done_by = 0  # New variable: Work done by this agent for others
        self.index = index
        self.confidence = 50
        self.transaction_history = []

    def check_confidence(self):
        """ Vérifie le niveau de confiance et renvoie le statut correspondant. """
        if self.confidence <= Agent.DEFICIT_THRESHOLD:
            return 'defiance'
        elif self.confidence <= Agent.INDIFFERENCE_THRESHOLD:
            return 'indifference'
        else:
            return 'confidence'

    def give(self,agent,amt_out):
       """
        Process the action of giving a specified amount of promises to another agent.
       """
       if self.check_confidence() == 'defiance':
            return 

       if amt_out > 0:
            self.promises[agent.index] -= amt_out
            self.work_done_for += amt_out
            self.transaction_history.append(('give', agent.index, amt_out))

    def receive(self,agent,amt_in):
       """
        Process the action of receiving promises from another agent.
       """
       if self.check_confidence() == 'defiance':
            return

       if amt_in > 0:
            self.promises[agent.index] += amt_in
            self.work_done_by += amt_in
            self.transaction_history.append(('receive', agent.index, amt_in))
            self.confidence = min(100, self.confidence + 5)

    def update_confidence(self, delta):
        """
        Updates the confidence level of the agent with bounds.
        """
        self.confidence = max(0, min(100, self.confidence + delta))

    


    def calculate_multiplier(self):
        """
        Calculates a multiplier based on the work done by and for the agent.

        Returns:
            float: The calculated multiplier value.
        """
        if self.work_done_by == 0:  # Avoid division by zero
            return 0
        mult = math.sqrt(self.work_done_for) * (self.work_done_for / self.work_done_by)  # Multiplier formula
        #print(f"{self.index} work_done_for: {self.work_done_for}, work_done_by: {self.work_done_by} mult: {mult}\n")
        return mult
    
    # In the Agent class
    
    def draw(self, is_host=False, attending=True, zBlack=True):
        """
        Draws the agent on the screen.

        Args:
            is_host (bool): Indicates if the agent is the host.
            attending (bool): Indicates if the agent is attending an event.
            zBlack (bool): Determines the color scheme for the drawing.
        """
        alpha = int(max(0, min(255, 255 * (1))))
        color = BLACK
        if is_host:
            color = GREEN
        if zBlack==False:
            color = GREEN if is_host else (BLUE if attending else RED)
        pygame.draw.circle(screen, color + (alpha,), (self.x, self.y), AGENT_RADIUS)
        font = pygame.font.Font(None, 24)
        
        #text = font.render(str(self.promises), True, (0, 0, 0))
        text = font.render(str(self.promises[self.index]), True, (0, 0, 0))
        screen.blit(text, (self.x - 6, self.y + AGENT_RADIUS + 5))
        



# LiquidityPool  class
class LP:
    """
    Represents the liquidity pool in the Mwerya community.

    Manages the deposits and exchanges between agents, tracking the promises and transactions within the community.

    Attributes:
        pools (list): A 2D list representing the liquidity pools between each pair of agents.
    """
    def __init__(self,num_agents):
        """
        Initializes the liquidity pool with given number of agents.

        Args:
            num_agents (int): The number of agents in the simulation.
        """
        self.pools = [[[0, 0] for _ in range(num_agents)] for _ in range(num_agents)]



    def deposit(self,zagent,i,j,amt_i, amt_j):
        """
        Handles the deposit of promises between two agents in the liquidity pool.

        Args:
            zagent (Agent): The agent making the deposit.
            i (int): Index of the first agent in the transaction.
            j (int): Index of the second agent in the transaction.
            amt_i (int): The amount deposited by the first agent.
            amt_j (int): The amount deposited by the second agent.
        """
        self.pools[i][j][0] += amt_i
        self.pools[i][j][1] += amt_j

        self.pools[j][i][1] += amt_i
        self.pools[j][i][0] += amt_j
        
        
        zagent.promises[i] -= amt_i
        zagent.promises[j] -= amt_j

    def exchange(self,zagent,i,j,amt_i, amt_j):
        """
        Facilitates the exchange of promises between two agents in the liquidity pool.

        Args:
            zagent (Agent): The agent initiating the exchange.
            i (int): Index of the first agent in the exchange.
            j (int): Index of the second agent in the exchange.
            amt_i (int): The amount of promises the first agent wants to exchange.
            amt_j (int): The amount of promises the second agent wants to exchange.

        Returns:
            int: The amount exchanged.
        """
        amount = 0
        if amt_i > 0:
            if amt_i <= self.pools[i][j][1]: #enough to remove from other side
                amount = amt_i
                self.pools[i][j][0]  += amt_i
                self.pools[i][j][1]  -= amt_i

                self.pools[j][i][1]  += amt_i
                self.pools[j][i][0]  -= amt_i

                
                zagent.promises[i] -= amt_i
                zagent.promises[j] += amt_i
        elif amt_j > 0:
            if amt_j <= self.pools[i][j][0]:
                amount = amt_j
                self.pools[i][j][0]  -= amt_j
                self.pools[i][j][1]  += amt_j

                self.pools[j][i][1]  -= amt_j
                self.pools[j][i][0]  += amt_j
                
                zagent.promises[j] -= amt_j
                zagent.promises[i] += amt_j
        if amt_j > 0 and amt_i >0:
                    print(f"error in exchange {amt_i}, {amt_j}\n")
        
        return amount

    # Liquidity Pool class draw
    
    def draw_all(self,agents):
        """
        Draws all the liquidity pools between agents on the screen.

        Args:
            agents (list): List of Agent objects in the simulation.
        """
        color = BLACK
        thickness = 1
        font = pygame.font.Font(None, 24)  # Font for rendering text
        #print(f"zz|||||||")

        for i in range(len(agents)):
            for j in range(i+1, len(agents)):
                if i != j and (self.pools[i][j][0]  >0 or self.pools[i][j][1] >0 ):
                    
                    #print(f"mmmm{i},{j}: {self.pools[i][j][0]},{self.pools[i][j][1]}")
                            
                    start = (agents[i].x, agents[i].y)
                    end = (agents[j].x, agents[j].y)


                    mx, my = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
                    offset = 50
                    control_point = (mx, my - offset)

                    # Shift label along the line for better visibility
                    shift_factor = 0.5  # Adjust as needed
                    label_x = int((1 - shift_factor) * start[0] + shift_factor * end[0])
                    label_y = int((1 - shift_factor) * start[1] + shift_factor * end[1])

                    
                    text = font.render(f"({self.pools[i][j][0]},{self.pools[i][j][1]})", True, (0, 0, 0))
                    #screen.blit(text, (mx - 10, my - offset - 10))  # Adjusted position
                    screen.blit(text, (label_x, label_y))

                    
                    prev_x, prev_y = start
                    for t in range(1, 101):
                        t /= 100
                        p0 = (1-t)*start[0] + t*control_point[0], (1-t)*start[1] + t*control_point[1]
                        p1 = (1-t)*control_point[0] + t*end[0], (1-t)*control_point[1] + t*end[1]
                        x = int((1-t)*p0[0] + t*p1[0])
                        y = int((1-t)*p0[1] + t*p1[1])
        
                        pygame.draw.line(screen, color, (prev_x, prev_y), (x, y), thickness)


                        prev_x, prev_y = x, y
    

    def print(self,agents):
        """
        Prints the details of the liquidity pools for debugging purposes.

        Args:
            agents (list): List of Agent objects to print information about.
        """
        color = BLACK
        thickness = 1
        print(f"|||||||\n")    

        for i in range(len(agents)):
            for j in range(i+1, len(agents)):
                if self.pools[i][j][0]  >0 or self.pools[i][j][1] >0:
                    print(f"a {i}, {j}: {self.pools[i][j][0]},{self.pools[i][j][1]}\n")
                if self.pools[j][i][1]  >0 or self.pools[j][i][0] >0:
                    print(f"b {j}, {i}: {self.pools[j][i][0]},{self.pools[j][i][1]}\n")    


                    
def initialize_simulation():
    """
    Initializes the simulation with a set number of agents and default settings.

    Sets up the agents in a circular formation and initializes the liquidity pools and other relevant variables.
    """
    global total_volume, cycle_count, agents, attendees, total_multiplier_effect, liquidity_pools, num_agents
    total_volume = 0
    cycle_count = 0
    attendees = []
    total_multiplier_effect = 0
    view_mode = True
    contrib_mode = False
    host_mode= False
    trade_mode = False
    
    agents = []
    for i in range(num_agents):
        x = int(center_x + radius * math.cos(i * angle))
        y = int(center_y + radius * math.sin(i * angle))
        service = f"Service {i+1}"
        agent = Agent(x, y, service,i,num_agents)
        agents.append(agent)
    # Initialize liquidity_pools to zero
    liquidity_pools = LP(num_agents)



# Function to calculate value created (Multiplier Effect)
def calculate_value_created(attendees):
    """
    Calculates the total value created in the community based on the work done by the attendees.

    Args:
        attendees (list): List of agents who have attended and contributed to the community.

    Returns:
        float: The total value created in the community.
    """
    total_work_done = sum(agent.work_done_by for agent in attendees)
    num_people = len(attendees)
    return math.sqrt(num_people) * total_work_done


def draw_liquidity_pool(agent1, agent2, promises1, promises2):
    """
    Draws the liquidity pool between two agents.

    Args:
        agent1 (Agent): The first agent in the liquidity pool.
        agent2 (Agent): The second agent in the liquidity pool.
        promises1 (int): The amount of promises held by the first agent.
        promises2 (int): The amount of promises held by the second agent.
    """
    # Calculate the center point between the two agents
    center_x, center_y = (agent1.x + agent2.x) // 2, (agent1.y + agent2.y) // 2
    
    # Calculate radius and angles for the arcs
    radius = int(math.sqrt((agent2.x - agent1.x)**2 + (agent2.y - agent1.y)**2)) // 2
    angle1 = math.atan2(agent1.y - center_y, agent1.x - center_x)
    angle2 = math.atan2(agent2.y - center_y, agent2.x - center_x)
    
    # Convert angles to degrees
    angle1, angle2 = math.degrees(angle1), math.degrees(angle2)
    
    # Sort the angles to draw arcs correctly
    if angle1 > angle2:
        angle1, angle2 = angle2, angle1
    
    # Draw full capacity arc (black, thickness = 4)
    pygame.draw.arc(screen, (0, 0, 0), (center_x - radius, center_y - radius, 2 * radius, 2 * radius), math.radians(angle1), math.radians(angle2), 4)
    
    # Calculate the proportion of the pool filled by agent1's promises
    total_promises = promises1 + promises2
    if total_promises > 0:
        filled_angle = angle1 + (angle2 - angle1) * (promises1 / total_promises)
        
        # Draw filled arc (white, thickness = 2)
        pygame.draw.arc(screen, (255, 255, 255), (center_x - radius, center_y - radius, 2 * radius, 2 * radius), math.radians(angle1), math.radians(filled_angle), 2)

        
        
# Function to draw curved lines between two points
def draw_arrow(surface, color, start, end):
    """
    Draws an arrow between two points.

    Args:
        surface (pygame.Surface): The surface on which to draw the arrow.
        color (tuple): The color of the arrow.
        start (tuple): The starting point of the arrow.
        end (tuple): The ending point of the arrow.
    """
    pygame.draw.line(surface, color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(surface, color, ((end[0] + 5*math.sin(math.radians(rotation)), end[1] + 5*math.cos(math.radians(rotation))), 
                                          (end[0] + 5*math.sin(math.radians(rotation-120)), end[1] + 5*math.cos(math.radians(rotation-120))),
                                          (end[0] + 5*math.sin(math.radians(rotation+120)), end[1] + 5*math.cos(math.radians(rotation+120)))))

def draw_curved_line(lp,host, attendee, color,thickness):
    """
    Draws a curved line between a host and an attendee to represent transactions.

    Args:
        lp (LP): The liquidity pool object.
        host (Agent): The host agent.
        attendee (Agent): The attendee agent.
        color (tuple): The color of the line.
        thickness (int): The thickness of the line.
    """
    if host.index == attendee.index:
        return
    start = (host.x, host.y)
    i = host.index
    end = (attendee.x, attendee.y)
    j = attendee.index
    mx, my = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
    offset = 50
    control_point = (mx, my - offset)

    font = pygame.font.Font(None, 18)  # Font for rendering text
    
    prev_x, prev_y = start
    for t in range(1, 101):
        t /= 100
        p0 = (1-t)*start[0] + t*control_point[0], (1-t)*start[1] + t*control_point[1]
        p1 = (1-t)*control_point[0] + t*end[0], (1-t)*control_point[1] + t*end[1]
        x = int((1-t)*p0[0] + t*p1[0])
        y = int((1-t)*p0[1] + t*p1[1])
        
        pygame.draw.line(screen, color, (prev_x, prev_y), (x, y), thickness)
        prev_x, prev_y = x, y
    
    draw_arrow(screen, color, (prev_x, prev_y), end)

    # Shift label along the line for better visibility
    shift_factor = 0.6  # Adjust as needed
    label_x = int((1 - shift_factor) * start[0] + shift_factor * end[0])
    label_y = int((1 - shift_factor) * start[1] + shift_factor * end[1])

                    
    text = font.render(f"({lp.pools[i][j][0]},{lp.pools[i][j][1]})", True, (0, 0, 0))
    #screen.blit(text, (mx - 10, my - offset - 10))  # Adjusted position
    screen.blit(text, (label_x, label_y))


def gini_coefficient(x):
    """
    Calculates the Gini coefficient for a set of values.

    Args:
        x (list): A list of values (e.g., incomes, wealth) for which to calculate the Gini coefficient.

    Returns:
        float: The Gini coefficient, representing the inequality among the values.
    """
    # Based on bottom eq: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    n = len(x)
    s = 0
    for i in range(n):
        xi = x[i]
        for j in range(n):
            xj = x[j]
            s += abs(xi - xj)
    if (2.0 * n ** 2 * sum(x)) >0:
        return s / (2.0 * n ** 2 * sum(x))
    else:
        return 0


def draw_stats(cycles_count):
    """
    Draws statistical information such as total equity, average equity, Gini coefficient, etc., on the screen.

    Args:
        cycle_count (int): The current cycle count in the simulation.
    """
    total_equity = sum(sum(agent.promises[i] for i in range(num_agents)) for agent in agents)
    avg_equity = total_equity / num_agents
    gini = gini_coefficient([sum(agent.promises[i] for i in range(num_agents)) for agent in agents])
    total_liable = sum(agent.liabilities for agent in agents)
    avg_liable = total_liable/num_agents
    per_liable = 100*total_liable / total_equity
    
    # Create a font object
    font = pygame.font.Font(None, 24)

    confidence_text = font.render(f"Confiance : {agent.confidence}%", True, (0, 0, 0))
    text_rect = confidence_text.get_rect()
    text_rect.bottomleft = (20, SCREEN_HEIGHT - 20)  # Position en bas à gauche
    screen.blit(confidence_text, text_rect)

    # Calculate and display the individual and average multipliers
    individual_multipliers = [agent.calculate_multiplier() for agent in agents]
    average_multiplier = sum(individual_multipliers) / num_agents if num_agents > 0 else 0

    # Append data to CSV
    csv_writer.writerow([cycle_count, average_multiplier])

    font = pygame.font.Font(None, 24)
    avg_multiplier_text = font.render(f"Avg. Mult: {average_multiplier:.2f}", True, (0, 0, 0))
    screen.blit(avg_multiplier_text, (20, 230))
        
    cycle_count_text = font.render(f"Weeks Past: {cycles_count}", True, (0, 0, 0))
    screen.blit(cycle_count_text, (20, 20))
    
    complete_cycles = cycles_count // num_agents
    complete_cycles_text = font.render(f"Complete Cycles: {complete_cycles}", True, (0, 0, 0))
    screen.blit(complete_cycles_text, (20, 50))
    
    tot_text = font.render(f"Total. Equity: {total_equity:.0f}", True, (0, 0, 0))
    screen.blit(tot_text, (20, 80))

    equity_text = font.render(f"Avg. Equity: {avg_equity:.2f}", True, (0, 0, 0))
    screen.blit(equity_text, (20, 110))
    
    gini_text = font.render(f"Gini Coefficient: {gini:.2f}", True, (0, 0, 0))
    screen.blit(gini_text, (20, 140))

    total_volume_text = font.render(f"Total Volume: {total_volume}", True, (0, 0, 0))
    screen.blit(total_volume_text, (20, 170))

    num_agents_text = font.render(f"Members: {num_agents}", True, (0, 0, 0))
    screen.blit(num_agents_text, (20, 200))

    total_liabilities_text = font.render(f"Total Oblig.: {total_liable}", True, (0, 0, 0))
    screen.blit(total_liabilities_text, (20, 260))  # Adjust the position as needed

    total_liabilities_text = font.render(f"% Oblig.: {per_liable:.0f}%", True, (0, 0, 0))
    screen.blit(total_liabilities_text, (20, 290))  # Adjust the position as needed

    avg_liabilities_text = font.render(f"Avg. Oblig.: {avg_liable:.2f}", True, (0, 0, 0))
    screen.blit(avg_liabilities_text, (20, 320))  # Adjust the position as needed

    

 # Function to save the current Pygame screen as an image
def save_screen_to_file(screen, filename):
    """
    Saves the current state of the Pygame screen to a file.

    Args:
        screen (pygame.Surface): The Pygame screen to be saved.
        filename (str): The name of the file where the screen will be saved.
    """
    pygame.image.save(screen, filename)

# Function to create an animated GIF from saved images
def create_gif(image_folder, gif_filename, duration=1000):
    """
    Creates an animated GIF from a series of images saved in a folder.

    Args:
        image_folder (str): The folder containing the images.
        gif_filename (str): The filename for the created GIF.
        duration (int): The duration for each frame in the GIF.
    """
    images = [Image.open(os.path.join(image_folder, f)) for f in sorted(os.listdir(image_folder))]
    images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=duration, loop=0)


csv_filename = f'mwerya_simulation_metrics_{current_date_and_time}.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Current Round', 'Average Multiplier'])

    
# Example of how to use these functions in your Pygame loop
image_folder = './mwerya_images'
if args.gif_cycles > 0:
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    else:
        # Delete existing PNG files
        for existing_file in glob.glob(f'{image_folder}/*.png'):
            os.remove(existing_file)
        
# Create agents and place them in a circle
num_agents = 31
angle = 2 * math.pi / num_agents
radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3
center_y = SCREEN_HEIGHT // 2
center_x = 2 * SCREEN_WIDTH // 4

agents = []
for i in range(num_agents):
    x = int(center_x + radius * math.cos(i * angle))
    y = int(center_y + radius * math.sin(i * angle))
    service = f"Service {i+1}"
    agent = Agent(x, y, service,i,num_agents)
    agents.append(agent)

# Initialize liquidity_pools to zero
liquidity_pools = LP(num_agents)
    
# Initialize other variables
total_volume = 0
cycle_count = 0
attendees = []  
total_multiplier_effect = 0

# Add a control state variable
simulation_state = 'initial'  # Can be 'initial', 'stopped', 'running', or 'step'
view_mode = True
contrib_mode= False
host_mode= False
trade_mode = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            csv_file.close()
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                initialize_simulation()
                simulation_state = 'initial'
            elif event.key == pygame.K_p:
                if simulation_state == 'running':
                    simulation_state = 'stopped'
                else:
                    simulation_state = 'running'
            elif event.key == pygame.K_s:
                simulation_state = 'step'
            elif event.key == pygame.K_r:
                simulation_state = 'running'
            elif event.key == pygame.K_q:
                if args.gif_cycles > 0:
                    gif_filename = f'./mwerya_simulation_{current_date_and_time}.gif'
                    create_gif(image_folder, gif_filename)
                csv_file.close()
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
                initialize_simulation()
                simulation_state = 'initial'
            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:  # Decrease the num_agents
                if num_agents > 1:  # At least one agent should remain
                    num_agents -= 1
                    angle = 2 * math.pi / num_agents
                    initialize_simulation()
                    simulation_state = 'initial'

    if simulation_state == 'initial':
        screen.fill(WHITE)
    
        # Draw agents with their initial promises
        for agent in agents:
            agent.draw(zBlack=True)

        # Display initial stats
        draw_stats(cycle_count)

        pygame.display.flip()
    
        # Change state to 'stopped' after drawing the initial state
        simulation_state = 'stopped'



    if simulation_state == 'stopped':
        continue
    elif simulation_state == 'step':
        simulation_state = 'stopped'
        
    screen.fill(WHITE)
    #print(f"{cycle_count}xxxxxx|||||||\n")    



    agent_index = cycle_count % num_agents
    host = agents[agent_index]


    if contrib_mode == True:
        host_mode = False
        # Contribute to the Mwerya    
        for agent in agents:
            if agent.index != host.index:
                if agent.promises[agent.index] >= 1 and liquidity_pools.pools[host.index][agent.index][1] == 0: #add this promise to the pool for the host
                    i = host.index
                    j = agent.index
                    #print(f"before:m{i},{j}: {liquidity_pools.pools[i][j][0]},{liquidity_pools.pools[i][j][1]}")

                    if liquidity_pools.pools[host.index][agent.index][0] > 0: # perform an exchange instead (clearing)
                        amt = liquidity_pools.exchange(agent,host.index,agent.index,1,0)
                        if amt > 0 and host.promises[agent.index] >= 1:
                            agent.give(host,1)
                            host.receive(host,1)
                            #attendees.append(agent)
                            total_volume += 1
                            agent.liabilities += 1
                            host.liabilities -= 1
                    elif liquidity_pools.pools[host.index][agent.index][0] == 0: # deposit
                        liquidity_pools.deposit(agent,host.index,agent.index,0,1)
                        agent.liabilities += 1

                    #print(f"after:m{i},{j}: {liquidity_pools.pools[i][j][0]},{liquidity_pools.pools[i][j][1]}")
            

    attendees = []
    transfers = []
    
    
    if host_mode == True:
        #Host Mwerya: now host pushes into the pools pulls out their vouchers and gives them back
        for agent in agents:
            attending = random.random() > 0.2  # 20% chance of not attending
            if attending and (agent.index != host.index):
                if host.promises[host.index]>=1:
                    amt = liquidity_pools.exchange(host,host.index,agent.index,1,0)
                    if amt > 0 and host.promises[agent.index] >= 1:
                        host.give(agent,1)
                        agent.receive(agent,1)
                        attendees.append(agent)
                        agent.liabilities -= 1
                        host.liabilities += 1
                        total_volume += 1
                        
    if trade_mode == True:
        #Random member to member transfers
        for i in range(int(num_agents/2)):  # num_agent/2 random transfers per turn
            sender, receiver = random.sample(agents, 2)
            if sender.promises[sender.index] >= 1 and liquidity_pools.pools[sender.index][receiver.index][1] >= 1: #there is something to pull
                amt = liquidity_pools.exchange(agent,sender.index,receiver.index,1,0)
                sender.give(receiver,1)
                receiver.receive(receiver,1)
                transfers.append((sender, receiver))
                sender.liabilities += 1
                receiver.liabilities -= 1

                total_volume += 1



    # Draw Mwerya payment lines
    colorz = BLACK
    for a in agents:
        if a in attendees:
            draw_curved_line(liquidity_pools,host,a, GREEN,3)
        else:
            draw_curved_line(liquidity_pools,host,a, BLACK,2)



    
    # Assuming liquidity_pools is a 2D array where liquidity_pools[i][j]
    # contains the promises between agent[i] and agent[j]
    #for i in range(len(agents)):
    #    for j in range(i+1, len(agents)):
    #        draw_curved_line((agents[i].x, agents[i].y), (agents[j].x, agents[j].y),BLACK,1)
    
    #liquidity_pools.draw_all(agents)
    #liquidity_pools.print(agents)

    #liquidity_pools.draw_host(host,attendees)
    #liquidity_pools.print(attendees)

    
    # Draw agents
    for agent in agents:
        attending = agent in attendees
        if view_mode == True or contrib_mode == True or trade_mode == True:
            agent.draw(is_host=(agent == host), attending=attending, zBlack=True)
        elif host_mode:
            agent.draw(is_host=(agent == host), attending=attending, zBlack=False)

        
    # Draw transfer lines
    if trade_mode == True:
        for sender, receiver in transfers:
            draw_curved_line(liquidity_pools,sender,receiver, BLUE,3)



    # Display metrics
    draw_stats(cycle_count)  # Add this line to draw the statistics

    #font = pygame.font.Font(None, 36)
    #text = font.render(f'Total Volume: {total_volume}', True, (0, 0, 0))
    #screen.blit(text, (20, 20))

    pygame.display.flip()
    pygame.time.delay(delay_time)

    # Uncomment these lines to save the screen to a file
    #filename = os.path.join(image_folder, f'screen_{cycle_count}.png')
    if args.gif_cycles > 0:
        filename = os.path.join(image_folder, f'screen_{str(cycle_count).zfill(4)}.png')
        save_screen_to_file(screen, filename)


    if view_mode == True:
        contrib_mode = True
        host_mode = False
        view_mode = False
        trade_mode = False
    elif contrib_mode == True:
        contrib_mode = False
        host_mode = True
        view_mode = False
        trade_mode = False
    elif host_mode == True:
        contrib_mode = False
        host_mode = False
        view_mode = False
        trade_mode = True
    elif trade_mode == True:
        contrib_mode = False
        host_mode = False
        view_mode = True
        trade_mode = False
        cycle_count += 1

    # Indicate the end of a full Mwerya Cycle
    #if cycle_count % num_agents == 0:
    #    print(f"A full Mwerya Cycle has completed. Total Volume: {total_volume}")
        #total_volume = 0

    complete_cycles = cycle_count // num_agents
    if complete_cycles >= args.gif_cycles and args.gif_cycles > 0:
        gif_filename = f'./mwerya_simulation_{current_date_and_time}.gif'
        create_gif(image_folder, gif_filename, duration=300)  # 1/3 speed
        csv_file.close()
        pygame.quit()
        exit(0)
        
