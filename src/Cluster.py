import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1. Import your brand new clustering pipeline function
try:
    from data_preprocess_and_visualization import get_clustering_data
except ModuleNotFoundError:
    from data_preprocess_and_visualization import get_clustering_data

print("Loading data for Unsupervised Segment Analysis...")
filepath=r"D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

X_clust = get_clustering_data(filepath)

# 2. Run the Elbow Loop to find the optimal number of clusters
wcss = []
cluster_range = range(1, 11)

print("Calculating inertia across different cluster sizes...")
for k in cluster_range:
    # n_init=10 runs the initialization 10 times to find the optimal starting centroids
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(X_clust)
    wcss.append(kmeans.inertia_)

print("\nLoop completed successfully!")

# 3. Plot the Elbow Curve
plt.figure(figsize=(10, 6))
plt.plot(cluster_range, wcss, marker='o', linestyle='--', color='#8e44ad', linewidth=2)
plt.title('The Elbow Method for Optimal Employee Segments (K)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Clusters (K)', fontsize=12)
plt.ylabel('WCSS / Inertia (Internal Variance)', fontsize=12)
plt.xticks(cluster_range)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()

