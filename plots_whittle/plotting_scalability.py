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
TPT = {'Scenario1':{'embb':{'maxwt': [60/(6*p['embb'])],'maxCQI':[159/(6*p['embb'])],'propfair':[202/(6*p['embb'])], 'RR': [280/(6*p['embb'])], 'whittle':[66/(6*p['embb'])]},
                    'XR':{'maxwt':[-176/(6*p['xr'])],'maxCQI':[2007/(6*p['xr'])], 'propfair':[3109/(6*p['xr'])], 'RR': [2939/(6*p['xr'])], 'whittle':[1060/(6*p['xr'])]}},
        'Scenario2':{'embb':{'maxwt':[734/(15*p['embb'])],'maxCQI':[1413/(15*p['embb'])], 'propfair':[2320/(15*p['embb'])], 'RR': [1928/(15*p['embb'])], 'whittle':[503/(15*p['embb'])]},
                    'XR':{'maxwt':[1856/(15*p['xr'])],'maxCQI':[6847/(15*p['xr'])], 'propfair':[9490/(15*p['xr'])], 'RR': [10750/(15*p['xr'])], 'whittle':[6957/(15*p['xr'])]}},
        'Scenario3':{'embb':{'maxwt':[-24/(30*p['embb'])],'maxCQI':[2442/(30*p['embb'])], 'propfair':[4478/(30*p['embb'])], 'RR': [16097/(30*p['embb'])], 'whittle':[1688/(30*p['embb'])]},
                    'XR':{'maxwt':[-1108/(30*p['xr'])],'maxCQI':[12083/(30*p['xr'])], 'propfair':[18819/(30*p['xr'])], 'RR': [2518/(30*p['xr'])], 'whittle':[7710/(30*p['xr'])]}}}

TSLS = {'Scenario1':{'URLLC':{'maxwt':[137/6],'maxCQI':[35/6], 'propfair':[9/6], 'RR': [-1/6], 'whittle':[35/6]},
                    'XR':{'maxwt':[32/6],'maxCQI':[79/6],'propfair':[31/6], 'RR': [1/6], 'whittle':[63/6]}},
        'Scenario2':{'URLLC':{'maxwt':[2224/15],'maxCQI':[112/15], 'propfair':[49/15], 'RR': [14/15], 'whittle':[31/15]},
                    'XR': {'maxwt':[123/15],'maxCQI':[258/15], 'propfair':[122/15], 'RR': [24/15], 'whittle':[787/15]}},
        'Scenario3':{'URLLC':{'maxwt':[4957/30],'maxCQI':[182/30], 'propfair':[53/30], 'RR': [89/30], 'whittle':[217/30]},
                    'XR':{'maxwt':[132/30],'maxCQI':[421/30], 'propfair':[165/30], 'RR': [-25/30], 'whittle':[351/30]}}}

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
         x = np.arange(3)
         xlabels = ['Scenario $4$', 'Scenario $5$','Scenario $6$']
    else:
         x = np.arange(3)
         xlabels = ['Scenario $4$', 'Scenario $5$','Scenario $6$']
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
         x = np.arange(3)
         xlabels = ['Scenario $4$', 'Scenario $5$','Scenario $6$']
    else:
         x = np.arange(3)
         xlabels = ['Scenario $4$', 'Scenario $5$','Scenario $6$']
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
    #plt.xticks(rotation=45)
    if key == "XR":
        plt.legend(["maxwt", "maxCQI", "PF", "RR", "whittle"], fontsize=18)

        #plt.legend(["maxwt", "maxCQI", "Proportional Fairness", "Round Robin", "whittle"])
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='black')
    #plt.yticks(fontsize=14)
    #plt.xlabel("Throughput Constraint")
    #plt.ylabel("Mean TSLS violation", fontsize = 22)
    
    #plt.title("Traffic model: "+key, fontsize=26, fontweight='bold')
    plt.savefig("Traffic model: "+key+"tsls.pdf")
    plt.show()