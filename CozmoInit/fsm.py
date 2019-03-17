#!/usr/bin/env python3

import cozmo
import datetime
import imgClassification
import numpy as np
import sys
import time
import actions

def get_trained_classifier(image_directory):
    image_classifier = imgClassification.ImageClassifier()

    # load images
    (train_raw, train_labels) = image_classifier.load_data_from_folder(image_directory)

    # convert images into features
    train_data = image_classifier.extract_image_features(train_raw)

    # train model
    image_classifier.train_classifier(train_data, train_labels)

    return image_classifier

def image_identifier(classifier, data):
    features = classifier.extract_image_features(data)
    print(np.shape(features))
    image_predictions = classifier.predict_labels(features)
    print(image_predictions)
    image_predictions.reshape(1,-1)
    print(image_predictions)
    image_predictions = image_predictions.tolist()
    print("type", type(image_predictions))
    match = 0
    prediction = None
    print(len(image_predictions))
    for x in range (0,len(image_predictions) - 1):
        print(x)
        labelA = image_predictions[x]
        labelB = image_predictions[x + 1]
        print("prediction",prediction)
        print("labelA=", labelA)
        print("labelB=", labelB)

        if labelA == labelB:
            match += 1
            prediction = labelB
        else:
            match = 0
        print(match)
 
    return prediction if match >= 2 else None

def fsm(robot: cozmo.robot.Robot):
    #Create a trained classifier object.
    trained_classifier = get_trained_classifier('imgs/')

    #Take six raw images.
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled  = False
    robot.camera.enable_auto_exposure()

    robot.set_head_angle(cozmo.util.degrees(0)).wait_for_completed()

    while(1):
        picture_array = []
        for i in range (0, 4):
            time.sleep(2)
            latest_image = robot.world.latest_image
            if latest_image is not None:
                raw_image = np.array(latest_image.raw_image)
                picture_array.append(raw_image)
                print("Took a pic. Here's the raw image: ", raw_image)
                time.sleep(0.1)
                

        picture_array = np.asarray(picture_array)
        print("picture array = ", np.shape(picture_array))
        imageName = image_identifier(trained_classifier, picture_array)
        print("image name =", imageName)
        print(type(imageName))
        if imageName == 'drone':
            actions.drone(robot)
        elif imageName == 'order':   
            actions.order(robot)
        elif imageName == 'inspection':
            actions.inspection(robot) 











if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.run_program(fsm)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)

