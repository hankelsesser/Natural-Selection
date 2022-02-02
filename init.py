import pygame, sys, random, math
pygame.init()

size = width, height =  800, 800
black = 0, 0, 0

pygame.font.init()
speed_display = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode(size)

def signus(x):
    if x<0:
        return(-1)
    elif x>0: return(1)
    else:
        return(0)

def sigmoid(x):
    return(1/(1+math.exp(-x)))

class Food:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
class Water:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Agent:
    def __init__(self, speed, x, y):
        self.speed = speed
        self.x = x
        self.y = y
        self.hunger = 0
        self.thirst = 0
        self.objective = [None, None]
        self.food_left = True
        self.water_left = True
        self.fitness = 0
        self.color = int(sigmoid(self.speed*0.25)*255)
        self.energy = 1
    def find_objective(self):
        if self.food_left == False:
            if self.water_left == False:
                print("all done")
                return (None, None)
            else:
                print("only water left")
                return(water_nodes, "W")
        elif self.water_left == False:
            print("only food left")
            return(food_nodes, "F")
        else:
            if self.hunger < self.thirst:
                print("hungry")
                return(food_nodes, "F")
            else: 
                print("thrisy")
                return(water_nodes, "W")
        print("objective found")
        
    def get_fitness(self):
        self.fitness = self.hunger + self.thirst
        return(self.fitness)

    def objective_exsists(self):
         if self.objective_type == "W":
                if self.objective_id in water_nodes:
                    return True
         elif self.objective_type == "F":
                if self.objective_id in food_nodes:
                    return True
         else: return False

    def move(self):
        if self.energy > 0.25:
            self.energy -= self.speed/1000
        if self.food_left == self.water_left == False:
            self.fitness = self.hunger + self.thirst
            #round_over = True
            #print(round_over)
        else:
            if self.objective[0] == None:
                self.objective_dict, self.objective_type = self.find_objective()
                if len(self.objective_dict) > 0:#there are objectives left
                    self.objective_id, self.objective = self.closest(self.objective_dict)
                else:
                    if self.objective_type == "F":
                        self.food_left = False
                    if self.objective_type == "W":
                        self.water_left = False

                    #print("new objective")
            elif self.objective_exsists() != True:
                self.objective[0], self.objective[1] = None, None
                
                        
            elif abs(self.x - self.objective[0]) < self.speed*self.energy and abs(self.y - self.objective[1]) < self.speed*self.energy:
                if self.objective_type == "W":
                    if self.objective_id in water_nodes:
                        del water_nodes[self.objective_id]
                        self.thirst += 20
                        #self.energy += 0.09
                elif self.objective_type == "F":
                    if self.objective_id in food_nodes:
                        del food_nodes[self.objective_id]
                        self.hunger += 20
                        #self.energy += 0.5



                #remove node and reset objective
                self.objective[0] = None
                self.objective[1] = None
                print("objective_reset")
            else:
                #print(self.speed)
                #print(signus(self.x - self.objective[0]))
                #print("moving")
                self.x += self.energy * self.speed * signus(self.objective[0]- self.x)
                #print(signus(self.x - self.objective[0]))
                self.y += self.energy * self.speed * signus(self.objective[1]- self.y)

            
    def closest(self, objectives_dict):
        distances = {}
        closest_distance = 1000
        closest_id = None
        
        for objective in objectives_dict:
            distancex = self.x - objectives_dict[objective].x
            distancey = self.y - objectives_dict[objective].y
            distances[objective] = [math.sqrt(distancex**2+distancey**2), objectives_dict[objective].x, objectives_dict[objective].y]
        for key in distances:
            if closest_distance>distances[key][0]:
                closest_distance = distances[key][0]
                closest_id = key
        return(closest_id, distances[closest_id][1:])

# test_list= [Food(10, 10), Food(20, 20)]
# test_agent = Agent(10, 1, 1)
# print(test_agent.closest(test_list))

        
        #returns the  closest objective from the list

def best_agents(agents, change):
    ranking = []
    #sorted(lst, key=lambda x: x[1], reverse=True)
    for agent in agents:
        ranking.append([agent.get_fitness(), agent])
    ranking = sorted(ranking, key=lambda x: x[0], reverse=True)
    print(ranking)
    best = []
    for i in range(int(inital_agents_num/3)):
        best.append(Agent(ranking[i][1].speed, random.randint(0, 800), random.randint(0,800)))
        if ranking[i][1].speed > change:
            for i in range(3):
                best.append(Agent(ranking[i][1].speed +random.randint(-1*change, change), random.randint(0, 800), random.randint(0,800)))
        else:
            for i in range(3):
                best.append(Agent(ranking[i][1].speed +random.randint(-1*ranking[i][1].speed, ranking[i][1].speed), random.randint(0, 800), random.randint(0,800)))
    
    # for agent in agents:
    #     if agent.get_fitness() >= 60:
    #         best.append(Agent(agent.speed, random.randint(0, 800), random.randint(0,800)))
    #         for i in range(3):
    #             best.append(Agent(agent.speed + random.randint(-2, 2), random.randint(0, 800), random.randint(0,800)))
    return(best)

def average_speed(agents):
    speed_sum = 0
    for agent in agents:
        speed_sum += agent.speed
    return(speed_sum/len(agents))

inital_agents_num = 15
nodes_num = 25
agents = []
food_nodes = {}
water_nodes = {}


for i in range(inital_agents_num):
    agents.append(Agent(random.randint(50, 100), random.randint(0, 800), random.randint(0,800)))
for i in range(nodes_num):
    food_nodes[i] = Food(i, random.randint(0, 800), random.randint(0, 800))
    water_nodes[i] = Water(i, random.randint(0, 800), random.randint(0, 800))
    
clock = pygame.time.Clock()
round_over = False
while 1:
    #lock.tick(10)

    while round_over == False:
        #clock.tick(60)
        screen.fill(black) 
        textsurface = speed_display.render(str(average_speed(agents)), False, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        
        for agent in agents:
            pygame.draw.ellipse(screen,(agent.color, 0, 0), pygame.Rect(agent.x,agent.y, 10, 10))
            agent.move()
        for node in food_nodes:
            pygame.draw.ellipse(screen,(100, 200, 100), pygame.Rect(food_nodes[node].x,food_nodes[node].y, 10, 10))
        for node in water_nodes:
            pygame.draw.ellipse(screen,(100, 100, 200), pygame.Rect(water_nodes[node].x,water_nodes[node].y, 10, 10))
            #print("water, x",water_nodes[node].x)
        
        if len(water_nodes) == len(food_nodes) == 0:
            round_over = True

        screen.blit(textsurface,(0,0))
        pygame.display.flip()
    else:
        print("new gen")
        agents = best_agents(agents, 2)
        for i in range(nodes_num):
            food_nodes[i] = Food(i, random.randint(0, 800), random.randint(0, 800))
            water_nodes[i] = Water(i, random.randint(0, 800), random.randint(0, 800))
        round_over = False



       