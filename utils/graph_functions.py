import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def gmm_plot(gmm, data, times):
    print(f"BIC for 3 components: {gmm.bic(data):.2f}")
    
    # Step 3: Extract parameters (sort by mean to assign clusters logically)
    means = gmm.means_.flatten()
    stds = np.sqrt(gmm.covariances_.flatten())
    weights = gmm.weights_
    order = np.argsort(means)
    means = means[order]
    stds = stds[order]
    weights = weights[order]
    print(f"Cluster means: {means}")
    print(f"Cluster std devs: {stds}")
    print(f"Cluster weights: {weights}")
    
    # Step 4: Find thresholds where weighted densities cross
    x = np.linspace(0, max(times), 1000).reshape(-1, 1)
    density0 = weights[0] * norm.pdf(x, means[0], stds[0])
    density1 = weights[1] * norm.pdf(x, means[1], stds[1])
    density2 = weights[2] * norm.pdf(x, means[2], stds[2])
    
    # Find crossings between adjacent components
    diff01 = density0 - density1
    diff12 = density1 - density2
    sign_change01 = np.diff(np.sign(diff01.flatten())) != 0
    sign_change12 = np.diff(np.sign(diff12.flatten())) != 0
    cross_indices01 = np.where(sign_change01)[0]
    cross_indices12 = np.where(sign_change12)[0]
    
    thresholds = []
    if len(cross_indices01) > 0:
        thresholds.append(x[cross_indices01].flatten()[0])  # First crossing for 0-1
    if len(cross_indices12) > 0:
        thresholds.append(x[cross_indices12].flatten()[0])  # First crossing for 1-2
    if thresholds:
        print(f"Approximate thresholds: {thresholds[0]:.2f} and {thresholds[1]:.2f} seconds")
    else:
        print("No clear crossings; clusters may not overlap meaningfully.")
    
    # Optional: Visualize
    plt.hist(times, bins=40, density=True, alpha=0.5, color='gray')
    plt.plot(x, density0, 'r--', label='Cluster 1 (short)')
    plt.plot(x, density1, 'g--', label='Cluster 2 (medium)')
    plt.plot(x, density2, 'b--', label='Cluster 3 (long)')
    for thresh in thresholds:
        plt.axvline(thresh, color='k', linestyle='-', label=f'Threshold at {thresh:.2f}' if thresh == thresholds[0] else "")
    plt.xlabel('Visitation duration (seconds)')
    plt.ylabel('Density')
    plt.legend()
    return plt


def plot_elbow_and_silhouette_side_by_side(
    X_pca,
    k_range=range(2, 11),
    figsize=(14, 6),
    random_state=42
):

    inertia = []
    silhouette_scores = []
    
    print("Calculating metrics for k =", end=" ")
    for k in k_range:
        print(k, end=" ")
        
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(X_pca)
        
        inertia.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_pca, kmeans.labels_))
    print()  # newline
    
    # ────────────────────────────────────────────────
    # Create side-by-side subplots
    # ────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, sharey=False)
    
    # Left plot: Elbow Method
    ax1.plot(k_range, inertia, 'bo-', markersize=8, linewidth=2)
    ax1.set_xlabel('Number of Clusters (k)')
    ax1.set_ylabel('Inertia')
    ax1.set_title('Elbow Method for Optimal k')
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Silhouette Score
    ax2.plot(k_range, silhouette_scores, 'go-', markersize=8, linewidth=2)
    ax2.set_xlabel('Number of Clusters (k)')
    ax2.set_ylabel('Silhouette Score')
    ax2.set_title('Silhouette Score for Different k')
    ax2.grid(True, alpha=0.3)
    
    # Final touches
    fig.suptitle('K-means Clustering Evaluation', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    return plt