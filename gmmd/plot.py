import sys
import os
import tempfile
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import subprocess
from logging import getLogger
logger = getLogger(__name__)

def tsne_plot(data, classification, path = None):
	if (not path):
		logger.info(f"No path provided, use temp path instead.")
		tmp_dir = tempfile.gettempdir()
		path = os.path.join(tmp_dir, ".gmm-demux")
	if (not os.path.exists(path)):
		logger.info(f"Temp path not found, {path} created.")
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


def openImage(path):
	if (not path):
		logger.error(f"Empty path {path}.")
		return
	try:
		imageViewerFromCommandLine = {'linux':'xdg-open',
									'win32':'explorer',
									'darwin':'open'}[sys.platform]
	except:
		logger.error(f"Platform {sys.platform} not supported.")
		return
	try:
	    subprocess.run([imageViewerFromCommandLine, path])
	except Exception as e:
		logger.error(e)
		return
