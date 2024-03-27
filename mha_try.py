import numpy as np
import pickle as pk


a = np.array([1,1.3,2])
print(a*23)

with open("a.pk", "wb") as f:
    pk.dump(a,f)



