from operator import add
from matplotlib import pyplot as plt
a = (255, 180, 60)
b = (0, 150, 255)

# vector addition
c = list(map(add, a, b))
print(c)

# scalar multiplication
d = list(map(lambda x: x * (1/2), c))
print(d)

plt.figure()
colors = [a, b, d]
for i, color in enumerate(colors):
    plt.bar(i, 1, color=[x/255 for x in color])
plt.axis('off')
plt.show()