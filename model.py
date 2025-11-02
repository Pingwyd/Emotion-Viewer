import os
import cv2
import numpy as np
import os
import cv2
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


train_dir = '/root/.cache/kagglehub/datasets/samithsachidanandan/human-face-emotions/versions/2/Data'
# test_dir = '/root/.cache/kagglehub/datasets/msambare/fer2013/versions/1/train'

print("Train folders:", os.listdir(train_dir))
# print("Test folders:", os.listdir(test_dir))



def load_data(data_dir):
    X, y = [], []
    classes = os.listdir(data_dir)
    classes.sort() # Sort classes to ensure consistent labeling
    class_to_label = {c: i for i, c in enumerate(classes)}

    for emotion in classes:
        emotion_dir = os.path.join(data_dir, emotion)
        for img_name in os.listdir(emotion_dir):
            img_path = os.path.join(emotion_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (48, 48))
            X.append(img.flatten())   # flatten for scikit-learn
            y.append(class_to_label[emotion])

    return np.array(X), np.array(y), classes

X_train, y_train, train_class_names = load_data(train_dir)
# X_test, y_test, test_class_names = load_data(test_dir)

print("Training samples:", len(X_train))
# print("Test samples:", len(X_test))
print("Train Classes:", train_class_names)
# print("Test Classes:", test_class_names)


X_train = X_train / 255.0
# X_test = X_test / 255.0

mlp = MLPClassifier(
    hidden_layer_sizes=(256, 128),
    activation='relu',
    solver='adam',
    batch_size=300,
    learning_rate_init=0.002,
    max_iter=80,
    verbose=True,
    random_state=42
)

mlp.fit(X_train, y_train)

# y_pred = mlp.predict(X_test)

# print("Accuracy:", accuracy_score(y_test, y_pred))
# print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=test_class_names))

joblib.dump(mlp, "model.pkl")

from google.colab import files
files.download("model.pkl")