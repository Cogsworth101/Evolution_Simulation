import pygame as pg
import numpy as np
import random
import time
import matplotlib.pyplot as plt
from math import log2
from operator import add

game_speed = 120 # in fps

# make a basic pygame window and runtime
pg.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Evolution Simulation")

colors = {
    (255, 0, 0): "red",
    (0, 255, 0): "green",
    (0, 0, 255): "blue",
    (255, 255, 0): "yellow",
    (0, 255, 255): "cyan",
    (255, 0, 255): "magenta",
    (255, 255, 255): "white",
    (0, 0, 0): "black"
}

class Bush:
    def __init__(self, x, y, size, aphid_count):
        self.x = x
        self.y = y
        self.color = (0, 200, 0)
        self.size = size
        self.aphids = []
        self.aphid_count = len(self.aphids)
        self.max_aphid_count = 3
        for i in range(self.max_aphid_count):
            self.regrow()
            print(self.aphids[i].x)

    def regrow(self):
        self.aphids.append(Aphid(random.uniform(0, self.size), random.uniform(0, self.size), self, 10, False))

    def draw(self, screen):
        rect = pg.Rect(self.x, self.y, self.size, self.size)
        pg.draw.ellipse(screen, self.color, rect)
        for aphid in self.aphids:
            if aphid.drawn == False:
                aphid.draw()

class Aphid:
    def __init__(self, x, y, parent, life, drawn):
        self.x = x
        self.y = y
        self.parent = parent
        self.life = life
        self.drawn = drawn
    
    def draw(self):
        pg.draw.circle(screen, (255, 0, 0), (int(self.parent.x + random.uniform(0, self.parent.size)), int(self.parent.y) + random.uniform(0, self.parent.size)), 2)
        self.drawn = True
    
    def delete(self):
        for aphid in self.parent.aphids:
            if (aphid.x == self.x) and (aphid.y == self.y):
                self.parent.aphids.remove()

class Lake:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.color = (0, 30, 200)
        self.size = size

    def draw(self, screen):
        rect = pg.Rect(self.x, self.y, self.size, self.size)
        pg.draw.ellipse(screen, self.color, rect)

class Junebug:
    """The Junebug class.
        Args:
            x (Integer): x position of the Junebug.
            y (Integer): y position of the Junebug.
            color (Tuple): RGB color of the Junebug.
            size (Integer): Size of the Junebug.
            hunger (Integer): Current hunger of the Junebug.
            thirst (Integer): Current thirst of the Junebug.
            sight (Integer): Sight radius of the Junebug.
            hunger_max (Integer): Maximum capable hunger of Junebug.
            thirst_max (Integer): Maximum capable thirst of Junebug.
            hunger_thresh (Integer): The threshold of hunger to be considered hungry.
            thirst_thresh (Integer): The threshold of thirst to be considered thirsty.
        """
    def __init__(self, x, y, color, size, hunger, thirst, hunger_max, thirst_max, hunger_thresh, thirst_thresh):
        """The Junebug class.
        Args:
            x (Integer): x position of the Junebug.
            y (Integer): y position of the Junebug.
            color (Tuple): RGB color of the Junebug.
            size (Integer): Size of the Junebug.
            hunger (Integer): Current hunger of the Junebug.
            thirst (Integer): Current thirst of the Junebug.
            sight (Integer): Sight radius of the Junebug.
            hunger_max (Integer): Maximum capable hunger of Junebug.
            thirst_max (Integer): Maximum capable thirst of Junebug.
            hunger_thresh (Integer): The threshold of hunger to be considered hungry.
            thirst_thresh (Integer): The threshold of thirst to be considered thirsty.
        """
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.hunger = hunger
        self.thirst = thirst
        self.sight = 50 + self.size * 2
        self.hunger_max = hunger_max
        self.thirst_max = thirst_max
        self.hunger_thresh = hunger_thresh
        self.thirst_thresh = thirst_thresh
        self.state = "idle"
        self.target = None
        self.target2 = None
        self.partner = None
        self.distance = self.sight
        self.life_max = 50 # How many times it's eaten/drank
        self.life = self.life_max

    def move(self):
        fps = clock.get_fps()
        if fps == 0:
            fps = 60
        
        frame_target = 120
        move_duration = 60

        if not hasattr(self, "move_timer"):
                self.move_timer = 0

        if self.state == "idle":
            if self.move_timer < move_duration:
                self.x += self.vx
                self.y += self.vy

            elif self.move_timer >= frame_target:
                self.move_timer = 0
                for i, j in enumerate(self.detect_nearby_objects(junebugs, self.sight * 5)):
                    dx = j.x - self.x
                    dy = j.y - self.y
                    dist = (dx**2 + dy**2) ** 0.5 or 1
                    speed = 2
                    self.vx = (dx / dist) * speed
                    self.vy = (dy / dist) * speed
                    break
                self.mate(self.partner)

            self.move_timer += 1

        elif self.state == "hungry":
            if self.move_timer < move_duration:
                self.x += self.vx
                self.y += self.vy
            
            elif self.move_timer >= frame_target:
                self.move_timer = 0
                for i, j in enumerate(self.detect_nearby_objects(bushes, self.sight * 5)):
                    dx = j.x - self.x
                    dy = j.y - self.y
                    dist = (dx**2 + dy**2) ** 0.5 or 1
                    speed = 2
                    self.vx = (dx / dist) * speed
                    self.vy = (dy / dist) * speed
                    break
            
            if is_overlapping(self.x, self.y, self.sight, self.target):
                self.eat()

            self.move_timer += 1
        
        elif self.state == "thirsty":
            if self.move_timer < move_duration:
                self.x += self.vx
                self.y += self.vy
            
            elif self.move_timer >= frame_target:
                self.move_timer = 0
                for i, j in enumerate(self.detect_nearby_objects(lakes, self.sight * 5)):
                    dx = j.x - self.x
                    dy = j.y - self.y
                    dist = (dx**2 + dy**2) ** 0.5 or 1
                    speed = 2
                    self.vx = (dx / dist) * speed
                    self.vy = (dy / dist) * speed
                    break
            
            if is_overlapping(self.x, self.y, self.sight, self.target2):
               self.drink()

            self.move_timer += 1

        elif self.state == "both":
            if self.move_timer < move_duration:
                self.x += self.vx
                self.y += self.vy

            elif self.move_timer >= frame_target:
                self.move_timer = 0
                for i, j in enumerate(self.detect_nearby_objects(lakes + bushes, self.sight * 5)):
                    dx = j.x - self.x
                    dy = j.y - self.y
                    dist = (dx**2 + dy**2) ** 0.5 or 1
                    speed = 2
                    self.vx = (dx / dist) * speed
                    self.vy = (dy / dist) * speed
                    break
            
            if is_overlapping(self.x, self.y, self.sight, self.target):
                self.eat()
            if is_overlapping(self.x, self.y, self.sight, self.target2):
                self.drink()

            self.move_timer += 1

        # Boundary checks
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
        if self.x > width:
            self.x = width
            self.vx = -self.vx
        if self.y < 0:
            self.y = 0
            self.vy = -self.vy
        if self.y > height:
            self.y = height
            self.vy = -self.vy
    
    def mate(self, partner):
        """Mates one Junebug with another.

        Args:
            partner (Junebug): The Junebug to mate with.
        """
        if self.state == "idle" and partner.state == "idle":
            if is_overlapping(self.x, self.y, self.sight, partner):
                combo = list(map(add, self.color, partner.color))
                child_color = list(map(lambda x: x * (1/2), combo))
                child_size = (self.size + partner.size) / 2
                for i in range(random.randint(1, 3)):
                    entities.append(Junebug(self.x, self.y, child_color, child_size, 10, 10, 10, 10, 5, 5))
                self.partner = None
                partner.partner = None
                print("Mated")
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
        transparent_color = (20, 20, 20, 128)
        transparent_surface = pg.Surface((self.sight * 2, self.sight * 2), pg.SRCALPHA)
        pg.draw.circle(transparent_surface, transparent_color, (self.sight, self.sight), self.sight, width=2)
        screen.blit(transparent_surface, (int(self.x - self.sight), int(self.y - self.sight)))

    def detect_nearby_objects(self, objects, radius):
        """Creates a dictionary of nearby objects in the format of {obj: self.distance}.

        Args:
            Objects (List): The list of objects to check on.
            Radius (Integer): The sight radius to check for objects in.

        Returns:
            Dictionary: {obj: self.distance} Gives an object and it's distance from the Junebug.
        """
        nearby_objects = {}
        for obj in objects:
            if obj is not self:
                self.distance = np.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)
                if self.distance <= radius:
                    nearby_objects.update({obj: self.distance})
        return nearby_objects
    
    def update_state(self, bushes, lakes):
        """Updates the state machine.

        Args:
            Bushes (List): List of the bushes.
            Lakes (List): List of the lakes.

        Returns:
            String: The state of the current Junebug.
        """

        if (self.hunger <= 0 or self.thirst <= 0) or (self.life <= 0):
            self.state = "dead"
            return self.state
        elif self.thirst < self.thirst_thresh and self.hunger < self.hunger_thresh:
            self.state = "both"
            nearby_bushes = self.detect_nearby_objects(bushes, self.sight * 5)
            nearby_lakes = self.detect_nearby_objects(lakes, self.sight * 5)
            nearby_objects = {**nearby_bushes, **nearby_lakes}
            if nearby_objects:
                if nearby_bushes and nearby_lakes:
                    self.state = "both"
                    for i, j in enumerate(nearby_bushes):
                        self.target = j
                        break
                    for i, j in enumerate(nearby_lakes):
                        self.target2 = j
                        break
                elif nearby_bushes:
                    self.state = "hungry"
                    for i, j in enumerate(nearby_bushes):
                        self.target = j
                        break
                elif nearby_lakes:
                    self.state = "thirsty"
                    for i, j in enumerate(nearby_lakes):
                        self.target2 = j
                        break
            return self.state
        elif self.hunger < self.hunger_thresh:
            self.state = "hungry"
            nearby_bushes = self.detect_nearby_objects(bushes, self.sight * 5)
            if nearby_bushes:
                for i, j in enumerate(nearby_bushes):
                    self.target = j
                    break
            else:
                self.target = None
            return self.state
        elif self.thirst < self.thirst_thresh:
            self.state = "thirsty"
            nearby_lakes = self.detect_nearby_objects(lakes, self.sight * 5)
            if nearby_lakes:
                for i, j in enumerate(nearby_lakes):
                    self.target2 = j
                    break
            else:
                self.target2 = None
            return self.state
        elif self.thirst >= self.thirst_thresh and self.hunger >= self.hunger_thresh:
            self.state = "idle"
            nearby_mates = self.detect_nearby_objects(junebugs, self.sight * 5)
            if nearby_mates:
                for i, j in enumerate(nearby_mates):
                    self.partner = j
                    break
            else:
                self.partner = None
            return self.state

    def eat(self):
        """Tries to make Junebug eat, no attributes, just checks if it's overlapping and eats if it is.
        """
        if is_overlapping(self.x, self.y, self.sight, self.target):
            if self.target.aphids != []:
                self.hunger = self.hunger_max
                self.target = None
                self.life -= 1
                self.target.aphids[0].delete()
                print(self.target.aphids)
    
    def drink(self):
        """Tries to make Junebug drink, no attributes, just checks if it's overlapping and drinks if it is.
        """
        if is_overlapping(self.x, self.y, self.sight, self.target2):
            self.thirst = self.thirst_max
            self.target2 = None
            self.life -= 1

def is_overlapping(x, y, size, entities):
    """
    Use case (1/2)
    
        Detects whether an entity and all entities from a list are overlapping.

    Args:
        x (Integer): The x position of the first entity.
        y (Integer): The y position of the first entity.
        size (Integer): The size of the first entity
        entities (List): List of entities which could be overlapped with.

    Returns:
        Boolean: Whether or not the entity is overlapping any of the list.
    
    Use case (2/2)
    
        Detects whether 2 entities are overlapping with one another.

    Args:
        x (Integer): The x position of the first entity.
        y (Integer): The y position of the first entity.
        size (Integer): The size of the first entity
        entities (Entity): Single entity which could be overlapped with.
        
    Returns:
        Boolean: Whether or not the entity is overlapping the other.
    """
    if type(entities) is list:
        for entity in entities:
            distance = np.sqrt((x - entity.x)**2 + (y - entity.y)**2)
            if distance < (size + entity.size) / 2:
                return True
        return False
    elif type(entities) is Junebug or type(entities) == Lake or type(entities) == Bush:
        distance = np.sqrt((x - entities.x)**2 + (y - entities.y)**2)
        if distance < (size + entities.size) / 2:
            return True
        return False
        

entities = []

# Add Junebugs
for _ in range(5):
    while True:
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 20)
        if not is_overlapping(x, y, size, entities):
            entities.append(Junebug(x, y, random.choice(list(colors.keys())), size, 10, 10, 10, 10, 5, 5))
            break

# Add Bushes
for _ in range(3):
    while True:
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = 100
        if not is_overlapping(x, y, size, entities):
            entities.append(Bush(x, y, size, 3))
            break

# Add Lakes
for _ in range(3):
    while True:
        size = random.randint(150, 250)
        x = random.randint(size // 2, width - size // 2)
        y = random.randint(size // 2, height - size // 2)
        if not is_overlapping(x, y, size, entities):
            entities.append(Lake(x, y, size))
            break
            
running = True
clock = pg.time.Clock()

i = 0 # Counter for hunger and thirst
j = 0
fps = clock.get_fps() if clock.get_fps() > 0 else game_speed

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((200, 255, 200))

    bushes = [entity for entity in entities if isinstance(entity, Bush)]
    lakes = [entity for entity in entities if isinstance(entity, Lake)]
    junebugs = [entity for entity in entities if isinstance(entity, Junebug)]

    for entity in entities[:]:
        if isinstance(entity, Junebug):
            entity.update_state(bushes, lakes)
            if entity.state == "dead":
                # print("Junebug died with " + str(entity.thirst) + " thirst and " + str(entity.hunger) + " hunger.")
                entities.remove(entity)
            else:
                entity.move()
                if i == 120:
                    i = 0
                    entity.hunger -= 1
                    entity.thirst -= 1
                    # print(entity.state, entity.hunger, entity.thirst)
                if j == 240:
                    j = 0
                    entity.
                else:
                    i += 1
                    j += 0
        entity.draw(screen)

    pg.display.flip()
    clock.tick(game_speed)

pg.quit()