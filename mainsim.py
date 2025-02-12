import pygame as pg
import numpy as np
import random
import time
import matplotlib.pyplot as plt

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

    def regrow(self):
        self.aphids.append(Aphid(random.uniform(0, self.size), random.uniform(0, self.size), self, 10))

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
    def __init__(self, x, y, color, size, hunger, thirst, sight, hunger_max, thirst_max, hunger_thresh, thirst_thresh):
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
        self.sight = sight
        self.hunger_max = hunger_max
        self.thirst_max = thirst_max
        self.hunger_thresh = hunger_thresh
        self.thirst_thresh = thirst_thresh
        self.state = "idle"
        self.target = None
        self.distance = sight

    def move(self):
        if self.state == "idle":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.hunger -= 1
            self.thirst -= 1
        elif self.state == "hungry":
            if self.detect_nearby_objects(bushes, self.sight):
                self.eat()
            else:
                self.x += self.vx
                self.y += self.vy
        elif self.state == "thirsty":
            if self.detect_nearby_objects(lakes, self.sight):
                self.drink()
            else:
                self.x += self.vx
                self.y += self.vy
        elif self.state == "both":
            if self.detect_nearby_objects(lakes, self.sight):
                self.drink()
            if self.detect_nearby_objects(bushes, self.sight):
                self.eat()
            if not self.detect_nearby_objects(bushes, self.sight) or not self.detect_nearby_objects(lakes, self.sight):
                self.x += self.vx
                self.y += self.vy
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
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

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
        if self.hunger <= 0 or self.thirst <= 0:
            self.state = "dead"
            return self.state
        if self.hunger < self.hunger_thresh:
            self.state = "hungry"
            nearby_bushes = self.detect_nearby_objects(bushes, self.sight)
            if nearby_bushes:
                self.target = nearby_bushes[0]
            else:
                self.target = None
            return self.state
        if self.thirst < self.thirst_thresh:
            self.state = "thirsty"
            nearby_lakes = self.detect_nearby_objects(lakes, self.sight)
            if nearby_lakes:
                self.target = nearby_lakes[0]
            else:
                self.target = None
            return self.state
        if self.thirst < self.thirst_thresh and self.hunger < self.hunger_thresh:
            self.state = "both"
            nearby_bushes = self.detect_nearby_objects(bushes, self.sight)
            nearby_lakes = self.detect_nearby_objects(lakes, self.sight)
            nearby_objects = {**nearby_bushes, **nearby_lakes}
            if nearby_objects:
                self.target = min(nearby_objects, key = nearby_objects.get)
            if self.target in nearby_bushes:
                self.state = "hungry"
            elif self.target in nearby_lakes:
                self.state = "thirsty"
        if self.thirst >= self.thirst_thresh and self.hunger >= self.hunger_thresh:
            self.state = "idle"
            return self.state

    def eat(self):
        self.distance = np.sqrt((self.x - self.target.x)**2 + (self.y - self.target.y)**2)
        if self.distance <= self.sight:
            self.hunger = self.hunger_max
            self.target = None
    
    def drink(self):
        self.distance = np.sqrt((self.x - self.target.x)**2 + (self.y - self.target.y)**2)
        if self.distance <= self.sight:
            self.thirst = self.thirst_max
            self.target = None

def is_overlapping(x, y, size, entities):
    for entity in entities:
        distance = np.sqrt((x - entity.x)**2 + (y - entity.y)**2)
        if distance < (size + entity.size) / 2:
            return True
    return False

entities = []

# Add Junebugs
for _ in range(10):
    while True:
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 20)
        if not is_overlapping(x, y, size, entities):
            entities.append(Junebug(x, y, random.choice(list(colors.keys())), size, 10, 10, 10, 10, 10, 5, 5))
            break

# Add Bushes
for _ in range(3):
    while True:
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = 50
        if not is_overlapping(x, y, size, entities):
            entities.append(Bush(x, y, size, 3))
            break

# Add Lakes
for _ in range(3):
    while True:
        size = random.randint(50, 100)
        x = random.randint(size // 2, width - size // 2)
        y = random.randint(size // 2, height - size // 2)
        if not is_overlapping(x, y, size, entities):
            entities.append(Lake(x, y, size))
            break

running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))

    bushes = [entity for entity in entities if isinstance(entity, Bush)]
    lakes = [entity for entity in entities if isinstance(entity, Lake)]

    for entity in entities[:]:
        if isinstance(entity, Junebug):
            entity.update_state(bushes, lakes)
            if entity.state == "dead":
                entities.remove(entity)
            else:
                entity.move()
        entity.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()