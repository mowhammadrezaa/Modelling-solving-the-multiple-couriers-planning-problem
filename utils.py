import numpy as np
from sklearn.cluster import KMeans


def compute_lower_bound(dist_matrix, item_sizes, max_capacities):
    # Compute k-Means clustering
    clusters = k_means_clustering(dist_matrix, item_sizes, max_capacities)

    # Compute lower bound based on clusters
    lower_bound_ = 0
    for cluster in clusters:
        cluster_distances = [np.array(dist_matrix)[i, j] for i in cluster for j in cluster]
        max_distance_in_cluster = np.max(cluster_distances)
        lower_bound_ = max(lower_bound_, max_distance_in_cluster)

    return lower_bound_


def k_means_clustering(dist_matrix, item_sizes, max_capacities):
    m = len(max_capacities)

    # Initialize clusters
    clusters = [[] for _ in range(m)]

    # Initialize centroids
    kmeans = KMeans(n_clusters=m, random_state=0).fit(np.array(dist_matrix)[:-1, :-1])
    labels = kmeans.labels_

    # Assign each item to the closest centroid
    for j, label in enumerate(labels):
        i = label
        if max_capacities[i] >= item_sizes[j]:
            clusters[i].append(j + 1)  # Adjust index to exclude the dummy location

    return clusters