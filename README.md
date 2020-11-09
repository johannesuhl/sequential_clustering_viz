# Visualizing sequential clustering results

<img width="1000" alt="java 8 and prio java 8  array review example" src="https://github.com/johannesuhl/sequential_clustering_viz/blob/main/img7.jpg">

Various applications require cluster analysis applied to sequential or longitudinal data. While there are numerous approaches for sequential clustering, visual-analytical methods to illustrate clustering results are sparse.
The script sequential_cluster_flows.py reads longitudinal data, and exemplarily generates clusters for each temporal cross-section of the data.
The number of instances per cluster and per point in time, as well as the number of clusters transitioning between clusters in subsequent points in time are then visualized using a network-based visualization technique, based on matplotlib.

The data used for demonstration of the visualization are 19 demographic characteristics reported for approx. 200 countries, from 1950 to present, and projected up to the year 2100, in 5-year intervals (see United Nations 2019, https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_Period_Indicators_Medium.csv).
BIRCH clustering was used to derive the clusters (and number of clusters) for each cross-section, using a range of thresholds dictating the granlarity of the cluster sequences (i.e., 0.1,0.2,0.3):

<img width="300" alt="java 8 and prio java 8  array review example" src="https://github.com/johannesuhl/sequential_clustering_viz/blob/main/cluster_sequence_map_birch_threshold_0.1.jpg"><img width="300" alt="java 8 and prio java 8  array review example" src="https://github.com/johannesuhl/sequential_clustering_viz/blob/main/cluster_sequence_map_birch_threshold_0.2.jpg"><img width="300" alt="java 8 and prio java 8  array review example" src="https://github.com/johannesuhl/sequential_clustering_viz/blob/main/cluster_sequence_map_birch_threshold_0.3.jpg">

# References:

United Nations, Department of Economic and Social Affairs, Population Division (2019). World Population Prospects 2019, Online Edition. Rev. 1. https://population.un.org/wpp/Download/Standard/CSV/

Zhang, T., Ramakrishnan, R., & Livny, M. (1996). BIRCH: an efficient data clustering method for very large databases. ACM sigmod record, 25(2), 103-114.

# Cluster sequences for BIRCH threshold of 0.2 enlarged:

<img width="300" alt="java 8 and prio java 8  array review example" src="https://github.com/johannesuhl/sequential_clustering_viz/blob/main/cluster_sequence_map_birch_threshold_0.2.jpg">
