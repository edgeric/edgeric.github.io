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
TPT = {'Scenario1':{'embb':{'maxwt': [840/p['embb']],'maxCQI':[736/p['embb']],'propfair':[381/p['embb']], 'RR': [682/p['embb']], 'whittle':[1794/p['embb']]},
                    'XR':{'maxwt':[549/p['xr']],'maxCQI':[983/p['xr']], 'propfair':[376/p['xr']], 'RR': [713/p['xr']], 'whittle':[-34/p['xr']]}},
        'Scenario2':{'embb':{'maxwt':[-1431/p['embb']],'maxCQI':[-915/p['embb']], 'propfair':[296/(p['embb'])], 'RR': [-83/p['embb']], 'whittle':[-794/p['embb']]},
                    'XR':{'maxwt':[1894/p['xr']],'maxCQI':[2024/p['xr']], 'propfair':[497/p['xr']], 'RR': [-10/p['xr']], 'whittle':[-689/p['xr']]}},
        'Scenario3':{'embb':{'maxwt':[198/p['embb']],'maxCQI':[1481/p['embb']], 'propfair':[1069/p['embb']], 'RR': [405/p['embb']], 'whittle':[788/p['embb']]},
                    'XR':{'maxwt':[1809/p['xr']],'maxCQI':[1869/p['xr']], 'propfair':[967/p['xr']], 'RR': [473/p['xr']], 'whittle':[-307/p['xr']]}},
        'Scenario4':{'embb':{'maxwt': [713/p['embb']],'maxCQI':[1059/p['embb']],'propfair':[1813/p['embb']], 'RR': [1932/p['embb']], 'whittle':[1659/p['embb']]},
                    'XR':{'maxwt':[1370/p['xr']],'maxCQI':[1083/p['xr']], 'propfair':[1227/p['xr']], 'RR': [780/p['xr']], 'whittle':[1408/p['xr']]}},
        'Scenario5':{'embb':{'maxwt': [-756/p['embb']],'maxCQI':[585/p['embb']],'propfair':[186/p['embb']], 'RR': [-130/p['embb']], 'whittle':[-135/p['embb']]},
                    'XR':{'maxwt':[-605/p['xr']],'maxCQI':[-1489/p['xr']], 'propfair':[-75/p['xr']], 'RR': [-381/p['xr']], 'whittle':[-381/p['xr']]}}}


TSLS = {'Scenario1':{'URLLC':{'maxwt':[785],'maxCQI':[5], 'propfair':[46], 'RR': [-1], 'whittle':[-1]},
                    'XR':{'maxwt':[38],'maxCQI':[-2],'propfair':[52], 'RR': [-1], 'whittle':[16]}},
        'Scenario2':{'URLLC':{'maxwt':[460],'maxCQI':[6], 'propfair':[16], 'RR': [-1], 'whittle':[-2]},
                    'XR':{'maxwt':[1994],'maxCQI':[2490],'propfair':[32], 'RR': [-1], 'whittle':[15]}},
        'Scenario3':{'URLLC':{'maxwt':[387],'maxCQI':[16], 'propfair':[32], 'RR': [-1], 'whittle':[-2]},
                    'XR':{'maxwt':[513],'maxCQI':[2266],'propfair':[29], 'RR': [-1], 'whittle':[45]}},
        'Scenario4':{'URLLC':{'maxwt':[1680],'maxCQI':[1922], 'propfair':[49], 'RR': [-1], 'whittle':[531]},
                    'XR':{'maxwt':[136],'maxCQI':[13],'propfair':[33], 'RR': [-1], 'whittle':[917]}},
        'Scenario5':{'URLLC':{'maxwt':[507],'maxCQI':[27], 'propfair':[22], 'RR': [-1], 'whittle':[-2]},
                    'XR':{'maxwt':[71],'maxCQI':[28],'propfair':[26], 'RR': [-1], 'whittle':[-1]}}}
        
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
         x = np.arange(5)
         xlabels = ['Trace $1$', 'Trace $2$','Trace $3$', 'Trace $4$', 'Trace $5$']
    else:
         x = np.arange(5)
         #xlabels = ['Scenario $1$', 'Scenario $2$']
         xlabels = ['Trace $1$', 'Trace $2$','Trace $3$', 'Trace $4$', 'Trace $5$']
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
    plt.xticks(x,xlabels, fontsize=14)
    #plt.xticks(rotation=45)
    plt.ylim(-30, 100)

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
         x = np.arange(5)
         #xlabels = ['Scenario $1$', 'Scenario $3$']
         xlabels = ['Trace $1$', 'Trace $2$','Trace $3$', 'Trace $4$', 'Trace $5$']
    else:
         x = np.arange(5)
         #xlabels = ['Scenario $1$', 'Scenario $2$']
         xlabels = ['Trace $1$', 'Trace $2$','Trace $3$', 'Trace $4$', 'Trace $5$']
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
    plt.xticks(x,xlabels, fontsize=14)
    #plt.xticks(rotation=45)
    if key == "XR":
        plt.legend(["maxwt", "maxCQI", "PF", "RR", "whittle"], fontsize=16)

        #plt.legend(["maxwt", "maxCQI", "Proportional Fairness", "Round Robin", "whittle"])
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='black')
    #plt.yticks(fontsize=14)
    #plt.xlabel("Throughput Constraint")
    #plt.ylabel("Mean TSLS violation", fontsize = 22)
    
    #plt.title("Traffic model: "+key, fontsize=26, fontweight='bold')
    plt.savefig("Traffic model: "+key+"tsls.pdf")
    plt.show()