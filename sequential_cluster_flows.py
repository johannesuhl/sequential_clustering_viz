# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 14:21:07 2020

@author: Johannes
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans,AgglomerativeClustering,Birch
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['font.size'] = 24

### read some country level statistics 
#Source: United Nations, 
#Department of Economic and Social Affairs, Population Division (2019). 
#World Population Prospects 2019 - Special Aggregates, Online Edition. Rev. 1.) 
datadf=pd.read_csv(r'https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_Period_Indicators_Medium.csv')

id_col='LocID' #id column of each instance
time_col='MidPeriod' # date column
interval=5 ### temporal granularity
lw_factor=0.6 ### line width of the flow lines. to be adjusted depending on total number of instances
bubble_factor=0.4 ### size of the nodes. to be adjusted depending on total number of instances
threshs=[0.1,0.2,0.3,0.4,0.5] #using a range of stopping criteria when estimating number of clusters.
## the columns in the dataframe used for clustering:
cluster_cols=[u'TFR', u'NRR', u'CBR', u'Births', u'LEx', u'LExMale', u'LExFemale',
       u'IMR', u'Q5', u'CDR', u'Deaths', u'DeathsMale', u'DeathsFemale',
       u'CNMR', u'NetMigrations', u'GrowthRate', u'NatIncr', u'SRB', u'MAC']

#some cleaning:
datadf=datadf[datadf.LocID<900]
datadf=datadf.dropna()
datadf=datadf.sort_values(by=time_col)

#scaling each feature to (0,1)
scaler = MinMaxScaler(feature_range=(0, 1))
for col in datadf[cluster_cols]:                
    X = datadf[col].values
    Xres = X.reshape(-1, 1)
    scaler.fit(Xres)
    Xtrans = scaler.transform(Xres)  
    rescaled = Xtrans.reshape(1, -1)[0]
    datadf[col]= rescaled                

for thresh in threshs:
    
    allLabels=[]
    periodcount=0
    for period,perioddf in datadf.groupby(time_col):
        periodcount+=1
        ids = perioddf[id_col].values
        X = perioddf[cluster_cols].values
        clust =  Birch(branching_factor=50, n_clusters=None, threshold=thresh, compute_labels=True).fit(X)     
        cluster_labels = clust.labels_
        print period,cluster_labels     
        allLabels.append(list(cluster_labels))
        
    allLabels=np.array(allLabels)
    
    #cluster labels are used as x-coordinates. subtracing mean for symmetry purposes.
    means = allLabels.mean(axis=1, keepdims=True)
    dataarr = np.subtract(allLabels,means)
    
    ### create node coordinates:
    xs = []
    ys = []
    y=datadf[time_col].min()
    for row in dataarr:
        y+=5
        currxs = np.unique(row)
        currys = np.full((1,np.unique(row).shape[0]),y)[0]    
        for x in currxs:
            xs.append(x)
        for y in currys:
            ys.append(y)
    
    ### calculate cluster sizes:
    freqs=[]
    for row in dataarr:
        unique_elements, counts_elements = np.unique(row, return_counts=True)
        print(np.asarray((unique_elements, counts_elements)))
        freqs+=(list(counts_elements))
    
    ## plot:
    fig, ax = plt.subplots(figsize=(8,40))
    colors = np.random.rand(len(freqs))
    for x in range(1,dataarr.shape[0]):
        trajects_curr_transition=[]
        for y in range(1,dataarr.shape[1]):
            traject = [dataarr[x-1,y],dataarr[x,y]]
            trajects_curr_transition.append(traject)
        
        #get the number of instances "flowing" between the current and previos point in time.    
        trajects_curr_transition = np.array(trajects_curr_transition)
        unique_elements, counts_elements = np.unique(trajects_curr_transition, return_counts=True,axis=0)
        print(unique_elements, counts_elements)
    
        for ix in range(0,unique_elements.shape[0]):
            lineStarty = sorted(np.unique(datadf[time_col].values))[1]+(x-1)*interval
            lineEndy = sorted(np.unique(datadf[time_col].values))[1]+x*interval
            lineStartx = unique_elements[ix][0]
            lineEndx = unique_elements[ix][1]
            ax.plot([lineStartx, lineEndx], [lineStarty, lineEndy], linewidth = lw_factor*counts_elements[ix], color = 'grey',zorder=2,alpha=0.25)
    ax.scatter(xs, ys, s=bubble_factor*np.array(freqs)*np.array(freqs),zorder=1,alpha=0.8)    
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('black')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('black')
    ax.set_ylabel('Year')    
    ax = plt.gca()
    ax.set_xticks([])
    plt.ylim(sorted(np.unique(datadf[time_col].values))[0]-interval,sorted(np.unique(datadf[time_col].values))[-1]+2*interval)
    plt.show()
    fig.savefig('cluster_sequence_map_birch_threshold_%s.jpg' %thresh,dpi=150)