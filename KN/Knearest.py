import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib import style
import warnings
from collections import Counter
style.use("fivethirtyeight")

# plot = [1,3]
# goalplot = [2,5]
# plt.scatter(goalplot[0], goalplot[1], s=150)

# def eucdist(plot, goalplot):
#     euc = sqrt((plot[0] - goalplot[0])**2 + (plot[1] - goalplot[1])**2)
#     print(euc)
#     plt.scatter(plot[0], plot[1], s=150)
#     return euc

# euc = eucdist(plot, goalplot)
# print("euc", euc)

# plot2 = [4,7]

# euc = eucdist(plot2, goalplot)


# plt.scatter(goalplot[0], goalplot[1], s=150)
# plt.show()

dataset = {"k": [[2,5],[4,1],[6,5]],"g": [[3,2],[6,3],[4,5]],"r": [[5,5],[7,7],[8,6]]}
newFeature = [42,23]

dataset = {
    "Husr": [[35,35],[37,37],[42,32],[60,34],[63,36],[61,35],[65,22],[76,16]],
    "Hyresrättg": [[23,12], [26,33], [28,20], [19,6], [97,9]],
    "BostadsRättb": [[57,45],[24,28],[26,30]],
    "Radhusy": [[37,21],[45,47],[32,42],[55,24],[61,25]]
}

def Knearest(dataset, predict, k=3):
    if len(dataset) >= k:
        warnings.warn("K is too high")
    distance = []
    for group in dataset:
        for feature in dataset[group]:
            eucdist = np.linalg.norm(np.array(feature) - np.array(predict))
            distance.append([eucdist, group])
    votes = [i[1] for i in sorted(distance)[:k]]
    votesResutlt = Counter(votes).most_common(1)
    print(votesResutlt)
    return votesResutlt

result = Knearest(dataset, newFeature, k=4)
print(result[0][0])

[[plt.scatter(ii[0], ii[1], color=i[-1]) for ii in dataset[i]] for i in dataset]

plt.scatter(newFeature[0], newFeature[1], s=100)
plt.ylabel = "inkomst" 
plt.ylabel = "ålder"

plt.show()