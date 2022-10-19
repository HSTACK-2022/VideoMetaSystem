# tensorflow/ImageSeperate/test.py
#
# 이미지 폴더의 경로를 받아 그 안에 있는 이미지들을 분류합니다.
# 기본적으로 imageTraining.h5 모델을 이용하여 분류하나,
# 다시 학습이 필요한 경우 101번째 줄의 train()의 주석을 삭제하면
# 학습 데이터를 기반으로 다시 학습할 수 있습니다.
#
# 이미지는 아래 5개의 기준으로 분류됩니다.
# N (News) : 뉴스 형식의 이미지
# L (Leceture) : 강의, 강연 이미지
# P (PPT) : PPT와 같이 정적인 자료를 사용한 이미지
# A (Application) : N, L, P가 아닌 이미지
# E (Error) : 이미지 분류가 불가능한 경우


import os
import numpy as np
import tensorflow as tf
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=512, activation='relu'),
        tf.keras.layers.Dense(units=4, activation='softmax')
    ])
    model.compile(optimizer='adam',
                loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
    return model


def train():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAIN_DIR = os.path.join(BASE_DIR, 'train')
    VALIDATION_DIR = os.path.join(BASE_DIR, 'validation')

    TRAIN_PPT_DIR = os.path.join(TRAIN_DIR, 'ppt')
    TRAIN_PP_DIR = os.path.join(TRAIN_DIR, 'pp')
    TRAIN_LECTURE_DIR = os.path.join(TRAIN_DIR, 'lecture')
    TRAIN_NEWS_DIR = os.path.join(TRAIN_DIR, 'news')

    VALIDATION_PPT_DIR = os.path.join(VALIDATION_DIR, 'ppt')
    VALIDATION_PP_DIR = os.path.join(VALIDATION_DIR, 'pp')
    VALIDATION_LECTURE_DIR = os.path.join(VALIDATION_DIR, 'lecture')
    VALIDATION_NEWS_DIR = os.path.join(VALIDATION_DIR, 'news')

    # check imgs
    nrows, ncols = 4,4
    pic_index = 0
    fig = plt.gcf()
    fig.set_size_inches(ncols*3, nrows*3)
    pic_index+=8

    model = create_model()

    model.summary()
    model.compile(optimizer=RMSprop(learning_rate=0.001), loss='categorical_crossentropy',metrics = ['accuracy'])

    # 이미지 전처리
    train_datagen = ImageDataGenerator(rescale = 1.0/255.)
    test_datagen = ImageDataGenerator(rescale = 1.0/255.)

    train_datagen = ImageDataGenerator( rescale = 1.0/255. )
    test_datagen  = ImageDataGenerator( rescale = 1.0/255. )

    train_generator = train_datagen.flow_from_directory(TRAIN_DIR, batch_size=20, class_mode='categorical', target_size=(150, 150))
    validation_generator =  test_datagen.flow_from_directory(VALIDATION_DIR, batch_size=20, class_mode  = 'categorical', target_size = (150, 150))

    history = model.fit(train_generator, validation_data=validation_generator, steps_per_epoch=100, epochs=50, validation_steps=50, verbose=2)

    model.save("imageTraining.h5")


def predict(model, path):
    img = image.load_img(path, target_size=(150,150))
    x= image.img_to_array(img)
    x=np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images,batch_size=10)
    if classes[0][0] == 1.0:    return "L"      #lecture
    elif classes[0][1] == 1.0:  return "N"      #news
    elif classes[0][2] == 1.0:  return "A"      #application
    elif classes[0][3] == 1.0:  return "P"      #ppt
    else :                      return "E"      #error


if __name__ == "__main__":
    # load the saved model (after training)
    # model = pickle.load(open("result/mlp_classifier.model", "rb"))
    # train()
    import argparse, sys
    parser = argparse.ArgumentParser(description="""Scene recognition script, this will load the model you trained, 
                                and perform inference on a sample you provide""")
    parser.add_argument("-f", "--file", help="The path to the file, preferred to be in image format (.jpg, .png)")
    args = parser.parse_args()
    dirs = args.file
    images = os.listdir(dirs)
    # load the saved/trained weights
    model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imageTraining.h5")
    new_model = tf.keras.models.load_model(model_path)

    for file in images:
        absfilepath = os.path.join(dirs, file)
        type = predict(new_model, absfilepath)
        if type != "E" :
            newName = type + file
            os.rename(absfilepath, os.path.join(dirs, newName))

    sys.exit(0)