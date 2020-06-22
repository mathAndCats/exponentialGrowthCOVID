# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:35:22 2020

@author: lhatc
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

###############################################################################
def extractData(filename='data.txt'):

    rows = [] 
    with open(filename,'r',encoding="ASCII") as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile, delimiter='\t') 
          
        # extracting field names through first row 
        #fields = next(csvreader) 
      
        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row) 
     
        return rows;
    
###############################################################################
rows = extractData();

stateWideString = rows[len(rows)-1];
stateWideString = stateWideString[1:];
stateWideFloat = np.array([float(i) for i in stateWideString]);
numDays = len(stateWideFloat)

averageStateWide = np.zeros(numDays-6);
sumArray = np.zeros(numDays-6);

for ii in range(7,numDays+1):
    sumArray[ii-7] = sum(stateWideFloat[ii-7:ii])
    averageStateWide[ii-7] = sumArray[ii-7] / 7;

N = len(averageStateWide);

avgOffset = 3;
xArrayAvg = np.array(range(avgOffset,N+avgOffset));

# data
fig = plt.figure();
ax = fig.add_subplot(1, 1, 1);
ax.plot(stateWideFloat, "o-");
ax.plot(xArrayAvg, averageStateWide, "o-");
labelArray = ("# of hospitalized COVID-19 patients","7-day average");
ax.legend(labelArray);
ax.grid();
ax.set_xlabel("Day since April 8");
ax.set_ylabel("# Hospitalized");    

# exponential fit

startNum = 47;
logYData = np.log(averageStateWide[startNum-avgOffset:]);
xArrayExpFit = np.array(range(0,len(logYData)));
curveFit = np.polyfit(xArrayExpFit, logYData, 2);

expFit = np.exp(curveFit[2]) * np.exp(curveFit[1]*xArrayExpFit) * np.exp(curveFit[0]*xArrayExpFit**2);

fig = plt.figure();
ax = fig.add_subplot(1, 1, 1);
ax.plot(stateWideFloat, "o-");
ax.plot(xArrayAvg, averageStateWide, "o-");
ax.plot(xArrayExpFit+startNum, expFit, "o-", Color="Green");
labelArray = ("# of hospitalized COVID-19 patients","7-day average","Exponential fit");
ax.legend(labelArray);
ax.grid();
ax.set_xlabel("Day since April 8");  
ax.set_ylabel("# Hospitalized");  

# extend exponential fit
xArrayExpExtrap = np.array(range(0,len(logYData)+27));
extrapData = np.exp(curveFit[2]) * np.exp(curveFit[1]*xArrayExpExtrap) * np.exp(curveFit[0]*xArrayExpExtrap**2)

fig = plt.figure();
ax = fig.add_subplot(1, 1, 1);
ax.plot(stateWideFloat, "o-");
ax.plot(xArrayAvg, averageStateWide, "o-");
ax.plot(xArrayExpFit+startNum, expFit, "o-");
labelArray = ("# of hospitalized COVID-19 patients","7-day average","Exponential fit");
ax.legend(labelArray);
ax.grid();
ax.set_xlabel("Day since April 8");  
ax.set_ylabel("# Hospitalized");  
ax.plot(xArrayExpExtrap+startNum, extrapData, "o-", Color="Green");

#xArray = np.array(range(0,len(logYData)+30));
#extrapData = np.exp(curveFit[2]) * np.exp(curveFit[1]*xArray) * np.exp(curveFit[0]*xArray**2)
#ax.plot(xArray+startNum+1, extrapData, "o-");