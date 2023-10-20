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
    def __init__(self, x, y, service,index):
        self.x = x
        self.y = y
        self.service = service
        self.promises = 30  # Start with 100 promises (vouchers)
        self.last_promises = 30  # Initialize the last_promises to track changes
        self.starting_promises = 30  # Initial promises to track risk
        self.risk = 0  # Initialize risk
        self.work_done_for = 0  # New variable: Work done for this agent by others
        self.work_done_by = 0  # New variable: Work done by this agent for others
        self.index = index


    def give(self,amt_out):
        self.promises -= amt_out
        self.work_done_for += amt_out

    def receive(self,amt_in):
        self.promises += amt_in
        self.work_done_by += amt_in

        
    def calculate_multiplier(self):
        if self.work_done_by == 0:  # Avoid division by zero
            return 0
        mult = math.sqrt(self.work_done_for) * (self.work_done_for / self.work_done_by)  # Multiplier formula
        print(f"{self.index} work_done_for: {self.work_done_for}, work_done_by: {self.work_done_by} mult: {mult}\n")
        return mult
    
    # In the Agent class
    
    def draw(self, is_host=False, attending=True):
        alpha = int(max(0, min(255, 255 * (1 - self.risk))))
        color = GREEN if is_host else (BLUE if attending else RED)
        pygame.draw.circle(screen, color + (alpha,), (self.x, self.y), AGENT_RADIUS)
        font = pygame.font.Font(None, 24)
        
        text = font.render(str(self.promises), True, (0, 0, 0))
        screen.blit(text, (self.x - 6, self.y + AGENT_RADIUS + 5))
        
        # Calculate and show the change in promises
        change = self.promises - self.last_promises
        if change != 0:
            fontsm = pygame.font.Font(None, 16)
            change_text = f"{'+ ' if change > 0 else ''}{change}"
            change_surface = fontsm.render(change_text, True, (0, 0, 0))
            screen.blit(change_surface, (self.x + AGENT_RADIUS, self.y - AGENT_RADIUS))

        self.last_promises = self.promises  # Update last_promises for the next cycle


def initialize_simulation():
    global common_pool, total_volume, cycle_count, agents, attendees, total_multiplier_effect, liquidity_pools
    common_pool = 0
    total_volume = 0
    cycle_count = 0
    attendees = []
    total_multiplier_effect = 0

    agents = []
    for i in range(num_agents):
        x = int(center_x + radius * math.cos(i * angle))
        y = int(center_y + radius * math.sin(i * angle))
        service = f"Service {i+1}"
        agent = Agent(x, y, service,i)
        agent.risk = random.random()  # Initialize risk randomly
        agents.append(agent)
    # Initialize liquidity_pools to zero
    liquidity_pools = [[[0, 0] for _ in range(len(agents))] for _ in range(len(agents))]



# Function to calculate value created (Multiplier Effect)
def calculate_value_created(attendees):

    total_work_done = sum(agent.work_done_by for agent in attendees)
    num_people = len(attendees)
    return math.sqrt(num_people) * total_work_done


def draw_liquidity_pool(agent1, agent2, promises1, promises2):
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
    pygame.draw.line(surface, color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(surface, color, ((end[0] + 5*math.sin(math.radians(rotation)), end[1] + 5*math.cos(math.radians(rotation))), 
                                          (end[0] + 5*math.sin(math.radians(rotation-120)), end[1] + 5*math.cos(math.radians(rotation-120))),
                                          (end[0] + 5*math.sin(math.radians(rotation+120)), end[1] + 5*math.cos(math.radians(rotation+120)))))

def draw_curved_line(start, end, color,thickness):
    mx, my = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
    offset = 50
    control_point = (mx, my - offset)
    
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

def gini_coefficient(x):
    # Based on bottom eq: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    n = len(x)
    s = 0
    for i in range(n):
        xi = x[i]
        for j in range(n):
            xj = x[j]
            s += abs(xi - xj)
    return s / (2.0 * n ** 2 * sum(x))


def draw_stats(cycles_count):
    # Calculate statistics for Promise Theory
    total_risk = 0
    for agent in agents:
        risk_from_balance = 1 - (agent.promises / agent.starting_promises)
        risk_from_attendance = 0 if agent in attendees else 1
        agent.risk = 0.5 * (risk_from_balance + risk_from_attendance)
        total_risk += agent.risk
        
    avg_risk = total_risk / num_agents
    total_equity = sum(agent.promises for agent in agents)
    avg_equity = total_equity / num_agents
    gini = gini_coefficient([agent.promises for agent in agents])


    
    # Create a font object
    font = pygame.font.Font(None, 24)

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
    
    risk_text = font.render(f"Average Risk: {avg_risk:.2f}", True, (0, 0, 0))
    screen.blit(risk_text, (20, 80))
    
    equity_text = font.render(f"Average Equity: {avg_equity:.2f}", True, (0, 0, 0))
    screen.blit(equity_text, (20, 110))
    
    gini_text = font.render(f"Gini Coefficient: {gini:.2f}", True, (0, 0, 0))
    screen.blit(gini_text, (20, 140))

    total_volume_text = font.render(f"Total Volume: {total_volume}", True, (0, 0, 0))
    screen.blit(total_volume_text, (20, 170))
    

 # Function to save the current Pygame screen as an image
def save_screen_to_file(screen, filename):
    pygame.image.save(screen, filename)

# Function to create an animated GIF from saved images
def create_gif(image_folder, gif_filename, duration=1000):
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
num_agents = 28
angle = 2 * math.pi / num_agents
radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3
center_y = SCREEN_HEIGHT // 2
center_x = 2 * SCREEN_WIDTH // 4

agents = []
for i in range(num_agents):
    x = int(center_x + radius * math.cos(i * angle))
    y = int(center_y + radius * math.sin(i * angle))
    service = f"Service {i+1}"
    agent = Agent(x, y, service,i)
    agent.risk = random.random()  # Initialize risk randomly
    agents.append(agent)

# Initialize liquidity_pools to zero
liquidity_pools = [[[0, 0] for _ in range(len(agents))] for _ in range(len(agents))]
    
# Initialize other variables
common_pool = 0
total_volume = 0
cycle_count = 0
attendees = []  
total_multiplier_effect = 0

# Add a control state variable
simulation_state = 'initial'  # Can be 'initial', 'stopped', 'running', or 'step'

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

    if simulation_state == 'initial':
        screen.fill(WHITE)
    
        # Draw agents with their initial promises
        for agent in agents:
            agent.draw()

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

    # Run the Mwerya cycle
    agent_index = cycle_count % num_agents
    host = agents[agent_index]
    attendees = []
    for agent in agents:
        if agent.promises >= 1:
            common_pool += 1
            agent.promises -= 1

    transfers = []
    
    # Random member to member transfers
    for i in range(5):  # 5 random transfers per turn
        sender, receiver = random.sample(agents, 2)
        if sender.promises >= 1:
            sender.give(1)
            receiver.receive(1)
            transfers.append((sender, receiver))
            total_volume += 1

    host.promises += common_pool
    for agent in agents:
        attending = random.random() > 0.2  # 20% chance of not attending
        if attending and (agent.index != host.index):
            agent.receive(1)
            host.give(1)
            attendees.append(agent)
            total_volume += 1

    common_pool = 0  # Reset common pool


    # Assuming liquidity_pools is a 2D array where liquidity_pools[i][j]
    # contains the promises between agent[i] and agent[j]
    for i in range(len(agents)):
        for j in range(i+1, len(agents)):
            draw_curved_line((agents[i].x, agents[i].y), (agents[j].x, agents[j].y),BLACK,1)
            #draw_liquidity_pool(agents[i], agents[j], liquidity_pools[i][j][0], liquidity_pools[i][j][1])

    # Draw agents
    for agent in agents:
        attending = agent in attendees
        agent.draw(is_host=(agent == host), attending=attending)

        
    # Draw transfer lines
    for sender, receiver in transfers:
        draw_curved_line((sender.x, sender.y), (receiver.x, receiver.y), BLUE,3)

    # Draw Mwerya payment lines
    for attendee in attendees:
        draw_curved_line((host.x, host.y), (attendee.x, attendee.y), GREEN,3)

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

    cycle_count += 1

    # Indicate the end of a full Mwerya Cycle
    if cycle_count % num_agents == 0:
        print(f"A full Mwerya Cycle has completed. Total Volume: {total_volume}")
        total_volume = 0

    complete_cycles = cycle_count // num_agents
    if complete_cycles >= args.gif_cycles and args.gif_cycles > 0:
        gif_filename = f'./mwerya_simulation_{current_date_and_time}.gif'
        create_gif(image_folder, gif_filename, duration=300)  # 1/3 speed
        csv_file.close()
        pygame.quit()
        exit(0)
        
