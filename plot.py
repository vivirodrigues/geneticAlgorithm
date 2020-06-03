import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import json

 #  _____          _____  _______      _______ _______ _______ _______ _____ _______ _______ _____ _______ _______
 # |_____] |      |     |    |         |______    |    |_____|    |      |   |______    |      |   |       |______
 # |       |_____ |_____|    |         ______|    |    |     |    |    __|__ ______|    |    __|__ |_____  ______|
                                                                                                                

x = []
y1 = []
y2 = []
y3 = []

y1_std = []
y2_std = []
y3_std = []


fname="trace.csv"
f = open(fname, 'r')
num_cols = len(f.readline().split(';'))
f.seek(0)
lines = f.read().splitlines()
f.close()

print("Plotting Statistics")

for line in lines:
	data = line.split(';')
	x.append(float(data[0].replace(',', '.')))
	y1.append(float(data[1].replace(',', '.')))
	y2.append(float(data[2].replace(',', '.')))
	y3.append(float(data[3].replace(',', '.'))) 
	y1_std.append(0)
	y2_std.append(0)
	y3_std.append(0)
								
fig = plt.figure(1)

yMax = max(y2) + 2
yMim = min(y2) - 1
plt.ylim(yMim, yMax)

xMax = len(x) + len(x)*0.02
xMim =  len(x)*-0.02
plt.xlim(xMim, xMax)
#plt.xticks(x, rotation = "horizontal")

plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    												

plt.errorbar(x,y1, ls="solid", label='Best', color='black', yerr=y1_std, zorder=3)			
plt.errorbar(x,y2, ls="solid", label='Worst', color='c', yerr=y2_std, zorder=3)						
plt.errorbar(x,y3, ls="solid", label='Average', color='m', yerr=y3_std, zorder=3)			

nameFile = 'results'
ylabel = 'Pairs of non-Attacking Queens'
xlabel = 'Number of generations'
title = "8-Queens Problem"

plt.ylabel(ylabel, fontweight="bold")
plt.xlabel(xlabel, fontweight="bold") 	
#plt.title(title, fontweight="bold")

plt.legend(numpoints=1, loc="upper left", ncol=3, bbox_to_anchor=(-0.02, 1.15))

fig.savefig(nameFile+'.png', bbox_inches='tight')
plt.close(fig) 			
print("End")

 #  _____          _____  _______      _______ _     _  ______  _____  _______  _____  _______  _____  _______ _______
 # |_____] |      |     |    |         |       |_____| |_____/ |     | |  |  | |     | |______ |     | |  |  | |______
 # |       |_____ |_____|    |         |_____  |     | |    \_ |_____| |  |  | |_____| ______| |_____| |  |  | |______
                                                                                                                    

print("Plotting Chromosome")
fig = plt.figure(2)
fname="solution.csv"
f = open(fname, 'r')
num_cols = len(f.readline().split(';'))
f.seek(0)
lines = f.read().splitlines()
f.close()
x = []
y = []
for line in lines:
	data = line.split(';')
	x.append(float(data[0].replace(',', '.')))
	y.append(float(data[1].replace(',', '.')))

plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)    												
plt.plot(x, y, 'ro', markersize=10)
plt.axis([-0.2, 7.2, -0.2, 7.2])



ylabel = 'Rows'
xlabel = 'Columns'
title = "8 Queens Puzzle"

plt.ylabel(ylabel, fontweight="bold")
plt.xlabel(xlabel, fontweight="bold") 	
plt.title(title, fontweight="bold")

fig.savefig('map.png', bbox_inches='tight')
print("End")