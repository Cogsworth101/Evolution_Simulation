class guy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

sup = guy(5, 5)

randomdict = {sup: "hi", 
              5: "ho", 
              2: "sup"
}
for i, j in enumerate(randomdict):
    print(j)
    break