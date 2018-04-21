import pandas as pd
from keras.backend import sparse_categorical_crossentropy
from keras.layers import Dense
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from keras.models import Sequential

names = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'free sulfur dioxide',
         'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'quality']
dataset = pd.read_csv('data/winequality-red.csv', names=names)

examples = dataset.drop(['quality'], axis=1).values
truths = dataset['quality'].get_values()

train_examples, test_examples, train_truths, test_truths = train_test_split(examples, truths, test_size=0.33)

model = Sequential()
model.add(Dense(units=22, activation='relu', input_dim=11))
model.add(Dense(units=10, activation='softmax'))

model.compile(loss=sparse_categorical_crossentropy,
              optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

model.fit(train_examples, train_truths, epochs=20, batch_size=32)

loss_and_metrics = model.evaluate(test_examples, test_truths, batch_size=128)
print("loss and metrics: ", loss_and_metrics)

prediction = model.predict(test_truths, batch_size=128)
prediction = prediction.argmax(1)

print("accuracy score: ", accuracy_score(test_truths, prediction))