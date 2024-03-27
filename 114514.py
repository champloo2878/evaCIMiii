import pickle as pk
import matplotlib.pyplot as plt

with open("dse1.pk","rb") as f:
    dse_res = pk.load(f)

num_point = len(dse_res)

x = [0 for i in range(num_point)]
y = [0 for i in range(num_point)]

print(dse_res)

for i in range(num_point):
    x[i] = dse_res[i][0]
    y[i] = dse_res[i][1]
    plt.scatter(x[i], y[i])
plt.show()


