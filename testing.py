import random
class Bush:
    def __init__(self, x, y, size, aphid_count):
        self.x = x
        self.y = y
        self.color = (0, 200, 0)
        self.size = size
        self.aphids = []
        self.aphid_count = len(self.aphids)

    def regrow(self):
        self.aphids.append(Aphid(random.uniform(0, self.size), random.uniform(0, self.size), self, 10, False))

class Aphid:
    def __init__(self, x, y, parent, life, drawn):
        self.x = x
        self.y = y
        self.parent = parent
        self.life = life
        self.drawn = drawn
    
    def draw(self):
        self.drawn == True
    
    def delete(self):
        for aphid in self.parent.aphids:
            if (aphid.x == self.x) and (aphid.y == self.y):
                self.parent.aphids.remove(aphid)
            print(self.parent.aphids)

bush = Bush(5, 5, 5, 5)
bush.regrow()
bush.regrow()
bush.regrow()
