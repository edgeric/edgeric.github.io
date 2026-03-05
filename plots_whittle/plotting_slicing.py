# creating the data
import numpy as np
import matplotlib.pyplot as plt
TPT = {}
TSLS = {}
# TPT = {'Scenario1':{'embb':{'maxwt':[-74,121,540,647,993,1238],'maxCQI':[-158,330,306,615,1059,1340],'whittle':[80,-544,-57,430,393,977]},
#                     'XR':{'maxwt':[360,685,895,1134,1478,1727],'maxCQI':[738,1029,1396,1717,1884,2245],'whittle':[316,726,-926,69,-278,13]}},
#         'Scenario2':{'embb':{'maxwt':[304,1439,1928,2521],'maxCQI':[718,1286,1900,2385],'whittle':[1386,2004,2523,3103]},
#                     'XR':{'maxwt':[-1746,-1181,-1109,2],'maxCQI':[-1871,-1336,-623,-85],'whittle':[-2069,-1719,-855,-37]}},
#         'Scenario3':{'embb':{'maxwt':[180,1339,1943,2327],'maxCQI':[704,1243,1827,2611],'whittle':[357,906,1489,1334]}}}
# TSLS = {'Scenario1':{'URLLC':{'maxwt':[2,2,6,40,2,148],'maxCQI':[7,6,6,7,7,7],'whittle':[1,12,2,-2,1,2]},
#                     'XR':{'maxwt':[349,206,216,267,447,442],'maxCQI':[2490,2490,2490,2490,2490,2263],'whittle':[89,76,5,41,6,7]}},
#         'Scenario2':{'XR': {'maxwt':[432,540,760,978],'maxCQI':[628,752,714,882],'whittle':[86,100,88,156]}},
#         'Scenario3':{'URLLC':{'maxwt':[611,860,678,789],'maxCQI':[601,630,1255,1530],'whittle':[7,3,4,260]}}}
####################### Figure 1 ###################################
p = {'embb': 0.9*3304.74/100, 'xr': 0.9*4922.09/100}
TPT = {'Scenario1':{'embb':{'maxwt': [745/(10*p['embb'])],'maxCQI':[2226/(10*p['embb'])],'propfair':[4355/(10*p['embb'])], 'RR': [9578/(10*p['embb'])], 'whittle':[1688/(10*p['embb'])]},
                    'XR':{'maxwt':[14575/(10*p['xr'])],'maxCQI':[14657/(10*p['xr'])], 'propfair':[18859/(10*p['xr'])], 'RR': [21985/(10*p['xr'])], 'whittle':[7710/(10*p['xr'])]}},
        'Scenario2':{'embb':{'maxwt':[-1266/(10*p['embb'])],'maxCQI':[-191/(10*p['embb'])], 'propfair':[-780/(10*p['embb'])], 'RR': [4080/(10*p['embb'])], 'whittle':[1688/(10*p['embb'])]},
                    'XR':{'maxwt':[9767/(10*p['xr'])],'maxCQI':[9968/(10*p['xr'])], 'propfair':[13194/(10*p['xr'])], 'RR': [16352/(10*p['xr'])], 'whittle':[7710/(10*p['xr'])]}},
        'Scenario3':{'embb':{'maxwt':[-1002/(10*p['embb'])],'maxCQI':[780/(10*p['embb'])], 'propfair':[1180/(10*p['embb'])], 'RR': [6129/(10*p['embb'])], 'whittle':[1688/(10*p['embb'])]},
                    'XR':{'maxwt':[1002/(10*p['xr'])],'maxCQI':[2443/(10*p['xr'])], 'propfair':[5569/(10*p['xr'])], 'RR': [10845/(10*p['xr'])], 'whittle':[7710/(10*p['xr'])]}},
        'Scenario4':{'embb':{'maxwt':[-1287/(10*p['embb'])],'maxCQI':[-135/(10*p['embb'])], 'propfair':[-977/(10*p['embb'])], 'RR': [3329/(10*p['embb'])], 'whittle':[1688/(10*p['embb'])]},
                    'XR':{'maxwt':[4168/(10*p['xr'])],'maxCQI':[4900/(10*p['xr'])], 'propfair':[8912/(10*p['xr'])], 'RR': [13640/(10*p['xr'])], 'whittle':[7710/(10*p['xr'])]}}}

TSLS = {'Scenario1':{'URLLC':{'maxwt':[11/10],'maxCQI':[136/10], 'propfair':[38/10], 'RR': [-1/10], 'whittle':[217/10]},
                    'XR':{'maxwt':[314/10],'maxCQI':[417/10],'propfair':[127/10], 'RR': [13/10], 'whittle':[351/10]}},
        'Scenario2':{'URLLC':{'maxwt':[228/10],'maxCQI':[367/10], 'propfair':[224/10], 'RR': [15/10], 'whittle':[217/10]},
                    'XR': {'maxwt':[310/10],'maxCQI':[426/10], 'propfair':[127/10], 'RR': [13/10], 'whittle':[351/10]}},
        'Scenario3':{'URLLC':{'maxwt':[632/10],'maxCQI':[433/10], 'propfair':[268/10], 'RR': [21/10], 'whittle':[217/10]},
                    'XR':{'maxwt':[98/10],'maxCQI':[158/10], 'propfair':[32/10], 'RR': [-6/10], 'whittle':[351/10]}},
        'Scenario4':{'URLLC':{'maxwt':[642/10],'maxCQI':[485/10], 'propfair':[268/10], 'RR': [21/10], 'whittle':[217/10]},
                    'XR':{'maxwt':[174/10],'maxCQI':[258/10], 'propfair':[62/10], 'RR': [4/10], 'whittle':[351/10]}}}

ylabels = {'embb':[],'XR':[]}
for key in TPT.keys():
    for key2 in TPT[key]:
            ylabels[key2].append(np.concatenate(list(TPT[key][key2].values())))
print(ylabels)
plt.rcParams['font.size'] = 16
for key in ylabels:
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for item in ylabels[key]:
        y1.append(item[0])
        y2.append(item[1])
        y3.append(item[2])
        y4.append(item[3])
        y5.append(item[4])
    print(y1,y2,y3)
    if key == "embb":
         x = np.arange(4)
         xlabels = ['Config $1$', 'Config $2$','Config $3$', 'Config $4$']
    else:
         x = np.arange(4)
         xlabels = ['Config $1$', 'Config $2$','Config $3$', 'Config $4$']
    # for key in ylabels:
    width = 0.1
    plt.figure(figsize=(6, 4))
    #plt.figure()
    ax = plt.axes()
    # Setting the background color of the plot
    # using set_facecolor() method
    #ax.set_facecolor("powderblue")
    ax.set_alpha(0.1)
    plt.bar(x-width, y1, width, color='blue',alpha=0.7)
    plt.bar(x, y2, width, color='red',alpha=0.7)
    plt.bar(x+width, y3, width, color='orange',alpha=0.7)
    plt.bar(x+(2*width), y4, width, color='green',alpha=0.7)
    plt.bar(x+(3*width), y5, width, color='purple',alpha=0.7)
    plt.xticks(x,xlabels)
    plt.xticks(x,xlabels)
    #plt.xticks(rotation=45)
    plt.ylim(-10, 100)
    if key == "embb":
        plt.legend(["maxwt", "maxCQI", "PF", "RR", "Windex"], fontsize=18)

    #plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='black')

    #plt.yticks(fontsize=14)
    #plt.xlabel("Throughput Constraint")
    #plt.ylabel("% Throughput violation", fontsize=22)
    #plt.legend(["maxwt", "maxCQI", "Proportional Fairness", "Round Robin", "whittle"])
    #plt.title("Traffic model: "+key, fontsize=26, fontweight='bold')
    plt.savefig("Traffic model: "+key+"tpt.pdf")
    plt.show()
ylabels = {'URLLC':[],'XR':[]}
for key in TSLS.keys():
    for key2 in TSLS[key]:
            ylabels[key2].append(np.concatenate(list(TSLS[key][key2].values())))
print(ylabels)
for key in ylabels:
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for item in ylabels[key]:
        y1.append(item[0])
        y2.append(item[1])
        y3.append(item[2])
        y4.append(item[3])
        y5.append(item[4])
    print(y1,y2,y3)
    if key == "urllc":
         x = np.arange(4)
         xlabels = ['Config $1$', 'Config $2$','Config $3$', 'Config $4$']
    else:
         x = np.arange(4)
         xlabels = ['Config $1$', 'Config $2$','Config $3$', 'Config $4$']
    # for key in ylabels:
    width = 0.1
    plt.figure(figsize=(6, 4))
    #plt.figure()
    ax = plt.axes()
    # Setting the background color of the plot
    # using set_facecolor() method
    #ax.set_facecolor("powderblue")
    ax.set_alpha(0.1)
    plt.bar(x-width, y1, width, color='blue',alpha=0.7)
    plt.bar(x, y2, width, color='red',alpha=0.7)
    plt.bar(x+width, y3, width, color='orange',alpha=0.7)
    plt.bar(x+(2*width), y4, width, color='green',alpha=0.7)
    plt.bar(x+(3*width), y5, width, color='purple',alpha=0.7)
    plt.xticks(x,xlabels)
    plt.ylim(-10, 100)
    #plt.xticks(rotation=45)
    

        #plt.legend(["maxwt", "maxCQI", "Proportional Fairness", "Round Robin", "whittle"])
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='black')
    #plt.yticks(fontsize=14)
    #plt.xlabel("Throughput Constraint")
    #plt.ylabel("Mean TSLS violation", fontsize = 22)
    
    #plt.title("Traffic model: "+key, fontsize=26, fontweight='bold')
    plt.savefig("Traffic model: "+key+"tsls.pdf")
    plt.show()