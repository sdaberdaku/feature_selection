from sklearn.linear_model import RandomizedLogisticRegression
from loadSamples import loadSamples
import matplotlib.pyplot as plt
import numpy as np

X, y, labels = loadSamples("./descriptors/", "*_descriptors.txt")

feature_selector = RandomizedLogisticRegression(n_jobs=1, selection_threshold=0.05, n_resampling=1000, verbose=10) 
X_reduced = feature_selector.fit_transform(X, y)

with open("total_indices_list.txt", "r") as in_indices : 
    indices_list = in_indices.read().strip().split("\n")
    
x = np.arange(len(indices_list))

print "loaded %d features" % len(indices_list)
extracted_features = feature_selector.get_support(indices=True)
print len(extracted_features)

print extracted_features
print [indices_list[ii] for ii in extracted_features]
print feature_selector.scores_

feature_scores_by_index = zip(x, feature_selector.scores_)
feature_scores_by_index.sort(key=lambda a : a[1], reverse=True)
y = np.array([a[1] for a in feature_scores_by_index])
plt.figure(num=1, figsize=(150, 10), facecolor='w', edgecolor='k')
my_xticks = [indices_list[a[0]] for a in feature_scores_by_index]
plt.xticks(x, my_xticks)
plt.xticks(rotation=-70)
plt.plot(x, y, 'b-')
plt.tight_layout()
plt.savefig("plot.pdf", dpi=1200)
