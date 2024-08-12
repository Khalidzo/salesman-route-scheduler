from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from typing import Tuple
from scipy.spatial.distance import cdist
from geopy.distance import geodesic


def initialize_kmeans(
    data: pd.DataFrame, n_clusters: int, random_state: int = 0
) -> Tuple[KMeans, pd.Series]:
    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
        cluster_labels = kmeans.fit_predict(data[["latitude", "longitude"]])
        return kmeans, cluster_labels
    except Exception as e:
        raise e


def create_distance_matrix(data: pd.DataFrame, cluster_centers) -> np.ndarray:
    return cdist(data[["latitude", "longitude"]], cluster_centers, "euclidean")


def assign_nodes_to_clusters(
    n_locations: int, n_clusters: int, distance_matrix: np.ndarray
) -> dict:
    locations_per_cluster, extra_locations = divmod(n_locations, n_clusters)
    final_clusters = {i: [] for i in range(n_clusters)}
    remaining_nodes = list(range(n_locations))

    while remaining_nodes:
        for cluster in range(n_clusters):
            target_size = locations_per_cluster + (
                1 if cluster < extra_locations else 0
            )
            if len(final_clusters[cluster]) < target_size and remaining_nodes:
                closest_node_idx = np.argmin(distance_matrix[remaining_nodes, cluster])
                closest_node = remaining_nodes.pop(closest_node_idx)
                final_clusters[cluster].append(closest_node)
    return final_clusters


def generate_clustered_lists(visiting_data: pd.DataFrame, clusters: dict) -> list:
    visiting_data["final_cluster"] = -1
    for cluster, nodes in clusters.items():
        for node in nodes:
            visiting_data.at[node, "final_cluster"] = cluster

    clustered_lists = []
    for cluster in range(len(clusters)):
        cluster_nodes = visiting_data[visiting_data["final_cluster"] == cluster]
        cluster_info = cluster_nodes[
            ["name", "address", "place_id", "longitude", "latitude"]
        ].to_dict(orient="records")
        clustered_lists.append(cluster_info)
    return clustered_lists


def insert_home_location(clustered_lists, home):
    for cluster in clustered_lists:
        cluster.insert(0, home)
    return clustered_lists


def greedy_tsp(distance_matrix):
    num_locations = len(distance_matrix)
    visited = [False] * num_locations
    route = [0]
    visited[0] = True

    for _ in range(num_locations - 1):
        last = route[-1]
        nearest = None
        nearest_distance = float("inf")
        for i in range(num_locations):
            if not visited[i] and distance_matrix[last][i] < nearest_distance:
                nearest = i
                nearest_distance = distance_matrix[last][i]
        route.append(nearest)
        visited[nearest] = True

    route.append(0)  # Return to the starting point
    return route


def calculate_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = [[0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                coords_1 = (locations[i]["latitude"], locations[i]["longitude"])
                coords_2 = (locations[j]["latitude"], locations[j]["longitude"])
                distance_matrix[i][j] = geodesic(coords_1, coords_2).kilometers
    return distance_matrix


def optimize_routes(clustered_lists):
    optimized_routes = []
    for cluster in clustered_lists:
        distance_matrix = calculate_distance_matrix(cluster)
        optimized_route_indices = greedy_tsp(distance_matrix)
        optimized_route = [cluster[i] for i in optimized_route_indices]
        optimized_routes.append(optimized_route)
    return optimized_routes
