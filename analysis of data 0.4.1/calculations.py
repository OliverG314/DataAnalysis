from math import *

class calculations():
    def __init__(self, data):
        self.data = data

    #Function to find pmcc of data
    def pmcc(self):
        #Define x and y as corresponding data sets
        x = self.data[0]
        y = self.data[1]

        #Calculate length of data, and the mean of each data set
        n = len(self.data[0])
        xBar = sum(self.data[0])/n
        yBar = sum(self.data[1])/n

        #Calculates (sum of x_i * y_i) - (length of data * mean of x * mean of y)
        Sxy = sum([x[i]*y[i] for i in range(n)]) - n*xBar*yBar

        #Calculates (sum of x_i ** 2) - (length of data * mean of x ** 2)
        Sxx = sum([x[i]**2 for i in range(n)]) - n*xBar**2
        
        #Calculates (sum of y_i ** 2) - (length of data * mean of y ** 2)
        Syy = sum([y[i]**2 for i in range(n)]) - n*yBar**2

        return Sxy/sqrt(Sxx*Syy)

    #Function to find srcc of data
    def srcc(self):
        #Define x and y as corresponding data sets
        x = self.data[0]
        y = self.data[1]

        #Order data and store in new lists
        orderedX = sorted(x)
        orderedY = sorted(y)

        #Create empty lists for x and y ranks
        xRank = []
        yRank = []

        #Loop through data
        for i in range(len(x)):

            #Append the index in the ordered list of the original list to new lsits
            xRank.append(orderedX.index(x[i])+1)
            yRank.append(orderedY.index(y[i])+1)

        #Calculate length of data and square of differences of ranks
        n  = len(xRank)
        d2 = sum([(xRank[i] - yRank[i])**2 for i in range(n)])

        return 1 - (6*d2)/(n*(n**2 - 1))
