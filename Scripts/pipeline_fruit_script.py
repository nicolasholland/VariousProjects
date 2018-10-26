"""
We play with sklearns pipeline feature.
First we downloaded kaggles fruit dataset.
Then we make a pipeline using opencv sift features and a support vector classifier.
We train and test our pipeline (just on random parts of the dataset, no splitting)
And finally we store the svc predictions in a redis db using redis' pipeline feature :D

Before running the script, you have to check the path to the dataset...
And make sure to start a redis db or disable the redis code if you dont need it.
"""
import os
from os.path import join, basename, isdir
from glob import glob
import numpy as np
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import cv2
import redis
import imageio

# Prepare data set
samplesize = 100
base = '/home/dutchman/kaggle/fruits/original_data_set'
datafolders = [join(base, f) for f in os.listdir(base) if isdir(join(base, f))]
data_dict = {basename(path):glob(join(path, '*.png')) for path in datafolders}
training_images = [np.random.choice(data_dict[key]) for c in range(samplesize)
                   for key in data_dict.keys()]
labels = np.array(list(data_dict.keys()) * samplesize)
images = np.array([imageio.imread(f) for f in training_images])

# Define pipeline and Train on data
sift = cv2.xfeatures2d.SIFT_create()
def man_pip(img, noffeat=5):
    """ manual pipeline """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(gray,None)
    assert des.shape[0] >= noffeat
    return des[:noffeat,:].flatten()

data = np.array([man_pip(img) for img in images])

clf = SVC(gamma='auto')
clf.fit(data, labels)


# Build sklearn pipeline
class Gray(object):
    def fit(self, *args, **kwargs):
        pass

    def transform(self, X, **kwargs):
        return cv2.cvtColor(X, cv2.COLOR_BGR2GRAY)

class Sift(object):
    def __init__(self, k):
        self.nofp = k
        self.sift = cv2.xfeatures2d.SIFT_create()

    def fit(self, *args, **kwargs):
        pass

    def transform(self, X, **kwargs):
        kp, des = self.sift.detectAndCompute(X,None)
        assert des.shape[0] >= self.nofp
        return des[:self.nofp,:].flatten().reshape(1, -1)

pipe = Pipeline([('gray', Gray()), ('sift', Sift(5)), ('svc', clf)])

# Evaluate on Test set and store in database
testset = [data_dict[key][50+c] for c in range(50) for key in data_dict.keys()]
db = redis.StrictRedis(host='localhost', port=6379, db=0)
db_pipe = db.pipeline()

def test():
    acc = 0
    for c in range(len(testset)):
        inp = testset[c]
        pred = pipe.predict(imageio.imread(inp))
        acc += int(pred == labels[c])
        db_pipe.set(inp, pred[0])
    db_pipe.execute()
    acc /= len(testset)
    return acc

print(test())
