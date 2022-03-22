import os
import tempfile
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def tsne_plot(data, classification, path = None):
	if (not path):
		tmp_dir = tempfile.gettempdir()
		path = os.path.join(tmp_dir, ".gmm-demux")
	if (not os.path.exists(path)):
		os.makedirs(path)
	y = classification["Cluster_id"]
	y[y >= 5] = 5
	tsne = TSNE(n_components = 2, random_state = 0)
	X_reduced = tsne.fit_transform(data)
	# plt.figure(figsize=(13, 7))
	plt.clf()
	plt.scatter(X_reduced[:, 0], 
		X_reduced[:, 1],
		c = y, 
		cmap = 'Set1',
		s = 2, 
		alpha = 0.5
	)
	# plt.axis('off')
	plt.xlabel("tSNE1")
	plt.xticks([])
	plt.ylabel("tSNE2")
	plt.yticks([])
	# plt.colorbar()
	plt.savefig(os.path.join(path, "tsne.png"))