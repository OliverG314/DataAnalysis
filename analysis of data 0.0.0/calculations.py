from math import *

class calculations():
    def __init__(self, data):
        self.data = data

    def pmcc(self, data=None):
        if data == None: data = self.data
        
        n = len(self.data[0])
        xBar = sum(self.data[0])/n
        yBar = sum(self.data[1])/n
        
        Sxy = sum([self.data[0][i]*self.data[1][i] for i in range(n)]) - n*xBar*yBar

        Sxx = sum([self.data[0][i]**2 for i in range(n)]) - n*xBar**2
        Syy = sum([self.data[1][i]**2 for i in range(n)]) - n*yBar**2

        print(Sxy, Sxx, Syy)

        return Sxy/sqrt(Sxx*Syy)

    def srcc(self):
        x = self.data[0]
        y = self.data[1]

        orderedX = sorted(x)
        orderedY = sorted(y)

        xRank = []
        yRank = []

        for i in range(len(x)):
            xRank.append(orderedX.index(x[i])+1)
            yRank.append(orderedY.index(y[i])+1)

        print(xRank, yRank)
        
        n  = len(xRank)
        d2 = sum([(xRank[i] - yRank[i])**2 for i in range(n)])

        print(n, d2)

        return 1 - (6*d2)/(n*(n**2 - 1))
