import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data.csv")
le_X = LabelEncoder()
le_Y = LabelEncoder()
train, test = train_test_split(df, test_size=0.2)

le_X.fit(np.unique(train.drop('Move', axis=1)))

x_train = np.array([le_X.transform(samp) for samp in train.drop('Move', axis=1).values])
y_train = pd.get_dummies(train["Move"])

x_test = np.array([le_X.transform(samp) for samp in test.drop('Move', axis=1).values])
y_test = pd.get_dummies(test["Move"])

# Settings
input_dim = len(x_train[0])
neurons = 64
epochs = 500

# Model
model = Sequential()
model.add(Dense(neurons, input_dim=input_dim, activation="relu"))
model.add(Dense(9, activation='softmax'))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(x_train, y_train, epochs=epochs, shuffle=True, batch_size=32, verbose=2)

model.save("tictacModel")

scores = model.evaluate(x_test, y_test, batch_size=32)

print(model.metrics_names[0] + ": " + str(scores[0]) + "\n" + model.metrics_names[1] + ": " + str(scores[1]))
