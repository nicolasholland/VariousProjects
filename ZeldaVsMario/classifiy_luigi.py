#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pickle
from pathlib import Path
import random
import luigi
import numpy as np
from scipy.misc import imread, imsave, imresize
from sklearn.cluster import KMeans
from sklearn import tree
import matplotlib.pyplot as plt


def cluster_image(img_fn, n_clusters=3):
    """
    Computes kmeans of an image.

    Parameters
    ----------
    fn : string, image filename

    Returns
    -------
    cluster : tuple, cluster centers
    """
    img = imread(img_fn)
    img = np.array(img, dtype=np.float64) / 255

    w, h, d = tuple(img.shape)
    image_array = np.reshape(img, (w * h, d))
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(image_array)
    return tuple(kmeans.cluster_centers_.reshape((3 * n_clusters)))

def resize_write(fin, fout, resize=(300, 300)):
    """
    Redas file, resizes it and writes result.

    Parameters
    ----------
    fin : string, input image
    fout : string, output image
    resize : tuple, default (300, 300)
    """
    img = imread(fin)
    img = imresize(img, resize)
    imsave(fout, img)

def train_tree(path='training/'):
    """
    Train a Tree.

    Returns
    -------
    clf : sklearn.tree.DecisionTreeClassifier
    """
    X = []
    Y = [0, 1]
    for filename in os.listdir(path):
        img = imread(os.path.join(path, filename))
        img = imresize(img, (300, 300))
        img = np.array(img, dtype=np.float64) / 255

        w, h, d = tuple(img.shape)
        image_array = np.reshape(img, (w * h, d))

        kmeans = KMeans(n_clusters=3, random_state=0).fit(image_array)
        X.append(kmeans.cluster_centers_.reshape(9))

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    return clf

def predict(cluster_fn, clf_fn):
    """
    Reads a cluster file and a classifier file and applys predict.

    Paramters
    ---------
    cluster_fn : string, file containing cluster centers
    clf_fn : string, file containing pickled tree.DecisionTreeClassifier

    Returns
    -------
    predict : np.array, containing prediction
    """
    clf = pickle.load(open(clf_fn, 'rb'))
    cluster_file = open(cluster_fn, 'r')
    cluster_line = cluster_file.readlines()
    cluster = np.array([float(val) for val in cluster_line[0].split()])

    return clf.predict(cluster)

class GetImage(luigi.Task):
    path = 'raw_input'
    output_fnp = os.path.join('tmp', 'img.png')

    def requires(self):
        return []

    def run(self):
        raw_images = os.listdir(self.path)
        img_fn = raw_images[random.randint(0, len(raw_images)) - 1]
        resize_write(os.path.join(self.path, img_fn), self.output_fnp)

    def output(self):
        return luigi.LocalTarget(self.output_fnp)

class ClusterImage(luigi.Task):
    output_fnp = os.path.join('tmp', 'cluster.txt')

    def requires(self):
        return [GetImage()]

    def run(self):
        clusters = cluster_image(self.input()[0].path)

        with self.output().open('w') as fout:
            fout.write("%f %f %f %f %f %f %f %f %f" % (clusters))

    def output(self):
        return luigi.LocalTarget(self.output_fnp)

class TrainClassifier(luigi.Task):
    output_fnp = os.path.join('tmp', 'clf.pkl')

    def requires(self):
        return []

    def run(self):
        clf = train_tree()

        pickle.dump(clf, open(self.output_fnp, "wb"))

    def output(self):
        return luigi.LocalTarget(self.output_fnp)

class PredictLabel(luigi.Task):
    output_fnp = os.path.join('tmp', 'label.txt')

    def requires(self):
        return [ClusterImage(), TrainClassifier()]

    def run(self):
        label = predict(self.input()[0].path, self.input()[1].path)

        with self.output().open('w') as fout:
            fout.write("%f " % (label[0]))

    def output(self):
        return luigi.LocalTarget(self.output_fnp)

class CleanAll(luigi.Task):

    def requires(self):
        return [GetImage(), ClusterImage(), TrainClassifier(), PredictLabel()]

    def run(self):
        for it in range(len(self.input())):
            os.remove(self.input()[it].path)

    def complete(self):
        for it in range(len(self.input())):
            if not Path(self.input()[it].path).is_file():
                return False

        self.run()
        return True


def train():
    """
    Train a Tree and test on an image.
    """
    clf = train_tree()

    img = imread(sys.argv[1])
    img = imresize(img, (300, 300))
    img = np.array(img, dtype=np.float64) / 255

    w, h, d = tuple(img.shape)
    image_array = np.reshape(img, (w * h, d))
    kmeans = KMeans(n_clusters=3, random_state=0).fit(image_array)

    print("Predicted: ", clf.predict(kmeans.cluster_centers_.reshape(9)))


def main():
    """
    main for plotting kmeans clustered images.
    """
    img = imread(sys.argv[1])
    img = imresize(img, (300, 300))
    img = np.array(img, dtype=np.float64) / 255

    w, h, d = tuple(img.shape)
    image_array = np.reshape(img, (w * h, d))

    kmeans = KMeans(n_clusters=3, random_state=0).fit(image_array)
    labels = kmeans.predict(image_array)

    d = kmeans.cluster_centers_.shape[1]
    print("Kmeans cluster centers: ", kmeans.cluster_centers_)
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = kmeans.cluster_centers_[labels[label_idx]]
            label_idx += 1

    plt.imshow(image)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 2 :
        if sys.argv[1] == 'GetImage':
            raw_images = os.listdir(sys.argv[2])
            img_fn = raw_images[random.randint(0, len(raw_images)) - 1]
            resize_write(os.path.join(sys.argv[2], img_fn),
                         os.path.join(sys.argv[3], 'img.png'))
            print("Image written to ", sys.argv[3])
        elif sys.argv[1] == 'ClusterImage':
            clusters = cluster_image(sys.argv[2])
            fout = open(os.path.join(sys.argv[3], 'cluster.txt'), 'w')
            fout.write("%f %f %f %f %f %f %f %f %f" % (clusters))
            fout.close()
            print("Clusterfile written to ", sys.argv[3])
        elif sys.argv[1] == 'TrainClassifier':
            clf = train_tree(sys.argv[2])
            pickle.dump(clf, open(os.path.join(sys.argv[3], 'clf.pkl'), "wb"))
            print("Classifier written to ", sys.argv[3])
        elif sys.argv[1] == 'PredictLabel':
            label = predict(os.path.join(sys.argv[2], 'cluster.txt'),
                            os.path.join(sys.argv[2], 'clf.pkl'))
            fout = open(os.path.join(sys.argv[2], 'label.txt'), 'w')
            fout.write("%f " % (label[0]))
            fout.close()
            print("Label written to ", sys.argv[2])
    else:
        main()