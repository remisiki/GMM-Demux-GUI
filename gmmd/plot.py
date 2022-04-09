import sys
import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import subprocess
from logging import getLogger
logger = getLogger(__name__)

def tsne_plot(data, classification, class_name_ary, path = None):
	if (not path):
		logger.info(f"No path provided, use temp path instead.")
		tmp_dir = tempfile.gettempdir()
		path = os.path.join(tmp_dir, ".gmm-demux")
	if (not os.path.exists(path)):
		logger.info(f"Temp path not found, {path} created.")
		os.makedirs(path)
	sample_num = data.shape[1]
	tsne = TSNE(n_components = 2, random_state = 0)
	X_reduced = tsne.fit_transform(data)
	X = pd.DataFrame(X_reduced)
	y = list(classification["Cluster_id"])
	y = list(map(lambda x: x if (x <= sample_num) else (sample_num + 1), y))
	X["class"] = y
	df_split_by_class = []
	for i in range(sample_num + 2):
		df = X[X["class"] == i]
		df_split_by_class.append(df)
	colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666']
	plt.clf()
	fig, ax = plt.subplots()
	for i in range(sample_num + 2):
		df = df_split_by_class[i]
		sc = ax.scatter(
			df.iloc[:, 0],
			df.iloc[:, 1],
			color = colors[i % len(colors)],
			label = class_name_ary[i] if (i <= sample_num) else "MSM",
			s = 2,
			alpha = 0.5
		)
	plt.draw()
	plt.legend(fontsize = 9, loc = 'upper right')
	plt.xlabel("tSNE1")
	plt.xticks([])
	plt.ylabel("tSNE2")
	plt.yticks([])
	plt.savefig(os.path.join(path, "tsne.png"))

def pdfPlot(x, pdf, hto_name, path = None):
	if (not path):
		logger.info(f"No path provided, use temp path instead.")
		tmp_dir = tempfile.gettempdir()
		path = os.path.join(tmp_dir, ".gmm-demux")
	if (not os.path.exists(path)):
		logger.info(f"Temp path not found, {path} created.")
		os.makedirs(path)
	plt.clf()
	fig, ax = plt.subplots()
	pdf_transpose = pdf.T
	low_plot = ax.plot(x, pdf_transpose[0], label = "low")
	high_plot = ax.plot(x, pdf_transpose[1], label = "high")
	plt.draw()
	plt.legend(fontsize = 9, loc = 'upper right')
	plt.savefig(os.path.join(path, f"pdf_{hto_name}.png"))
