#!/usr/bin/env python

##############
#### Modified image classification code to help Cozmo identify objects in the arena.
##############

#import matplotlib.pyplot as pyplot
import numpy as np
import re
from skimage import color, exposure, feature, filters, io, morphology, segmentation, transform
from sklearn import metrics, model_selection, svm

class ImageClassifier:
    
    def __init__(self):
        self.classifer = None

    def imread_convert(self, f):
        return io.imread(f).astype(np.uint8)

    def load_data_from_folder(self, dir):
        # read all images into an image collection
        ic = io.ImageCollection(dir+"*.bmp", load_func=self.imread_convert)
        
        #create one large array of image data
        data = io.concatenate_images(ic)
        
        #extract labels from image names
        labels = np.array(ic.files)
        for i, f in enumerate(labels):
            m = re.search("_", f)
            labels[i] = f[len(dir):m.start()]

        type(data)
        type(labels)

        return(data,labels)

    def extract_image_features(self, data):
        # Please do not modify the header above

        # extract feature vector from image data
        feature_data = []

        for img in data:
            img = color.rgb2gray(img)

            img = segmentation.inverse_gaussian_gradient(img, alpha=75.0, sigma=3.0)

            img = transform.resize(img, (100, 200),
                       anti_aliasing=True, anti_aliasing_sigma=0.5)

            hog = feature.hog(img, orientations=12, pixels_per_cell=(24, 24), cells_per_block=(3, 3),
                                    transform_sqrt=True, block_norm="L1-sqrt", feature_vector=True,
                                    visualize=False, multichannel=False)

            feature_data.append(hog)

        feature_data = np.asarray(feature_data)

        # Please do not modify the return type below
        return(feature_data)

    def train_classifier(self, train_data, train_labels):
        # Please do not modify the header above

        # train model and save the trained model to self.classifier
        self.classifer = svm.LinearSVC(C=1.0, penalty="l2", loss= "squared_hinge", dual=False, tol=0.0001,
                                        multi_class="ovr", fit_intercept=True, intercept_scaling=1000,
                                        class_weight="balanced", max_iter=1000)\
                                        .fit(train_data, train_labels)

    def predict_labels(self, data):
        # Please do not modify the header

        # predict labels of test data using trained model in self.classifier
        # the code below expects output to be stored in predicted_labels
        predicted_labels = self.classifer.predict(data)

        # Please do not modify the return type below
        return predicted_labels

def main():
    img_clf = ImageClassifier()

    # load images
    (train_raw, train_labels) = img_clf.load_data_from_folder('./imgs/')

    # convert images into features
    train_data = img_clf.extract_image_features(train_raw)

    # train model
    img_clf.train_classifier(train_data, train_labels)



    # predict images
    predicted_labels = img_clf.predict_labels(train_data)


    ''' Architecture for training and testing classifier
    # load images
    (train_raw, train_labels) = img_clf.load_data_from_folder('./train/')
    (test_raw, test_labels) = img_clf.load_data_from_folder('./test/')

    # convert images into features
    train_data = img_clf.extract_image_features(train_raw)
    test_data = img_clf.extract_image_features(test_raw)

    # train model and test on training data
    img_clf.train_classifier(train_data, train_labels)
    predicted_labels = img_clf.predict_labels(train_data)
    print("\nTraining results")
    print("=============================")
    print("Confusion Matrix:\n",metrics.confusion_matrix(train_labels, predicted_labels))
    print("Accuracy: ", metrics.accuracy_score(train_labels, predicted_labels))
    print("F1 score: ", metrics.f1_score(train_labels, predicted_labels, average='micro'))

    # test model
    predicted_labels = img_clf.predict_labels(test_data)
    print("\nTest results")
    print("=============================")
    print("Confusion Matrix:\n",metrics.confusion_matrix(test_labels, predicted_labels))
    print("Accuracy: ", metrics.accuracy_score(test_labels, predicted_labels))
    print("F1 score: ", metrics.f1_score(test_labels, predicted_labels, average='micro'))
    '''

# if __name__ == "__main__":
#     main()
