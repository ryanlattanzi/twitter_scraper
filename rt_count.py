# -----------------------------------------------------------------------------

#                           rt_count.py

# This script will build a model to try to predict the retweet_count for a tweet.
# It will include all steps of data preprocessing and model building, since it is a
# unique task that I don't think is generalizable.

# -----------------------------------------------------------------------------

import pandas as pd
from sklearn.utils import shuffle
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import Model
from keras import layers, models, Input, regularizers
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt


# LOAD IN THE DATA
data   = pd.read_csv(filepath_or_buffer = '../data/big_data.csv')

# SHUFFLE, EXTRACT THE LABEL, EXTRACT THE TEXT DATA FOR PREPROCESSING PURPOSES, EXTRACT TIME VARIABLE IF WE WANT TO INCLUDE IT LATER
data   = shuffle(data)
x_text = data['full_text']
x_reg  = data.drop(columns = ['full_text', 'retweet_count', 'date_time'])
time   = data['date_time']
y      = data['retweet_count']

# We will use NLTK to clean up our text data a little bit to get rid of stop words

x_text_filtered = []
stop_words      = stopwords.words('english')

# Getting rid of 'rt' because it is redundant, since we have a column of that indication in the dataframe
stop_words.append('rt')

for sentence in list(x_text):
    sentence      = sentence.lower()
    sentence_list = sentence.split()
    x_text_filtered.append([w for w in sentence_list if not w in stop_words])
    
x_text = x_text_filtered

# EXPLORING THE DATA (X_REG)

# How many nan values in each column?
print('\nNumber of nans in each column:')
print(x_reg.isna().sum())
print('\nNumber of non - nans in each column: ')
print(x_reg.count(), '\n')

for i in range(x_reg.shape[1]):
    print('Proportion of nan values for column', x_reg.columns[i], ': ', x_reg.isna().sum()[i]/len(x_reg))

# How many unique values in each column that have missing values?

print('\nThere are ', len(data.in_reply_to_screen_name.unique()), ' unique values in column: in_reply_to_screen_name')
print('There are ', len(data.hashtags.unique()), ' unique values in column: hashtags')
print('There are ', len(data.user_mentions.unique()), ' unique values in column: user_mentions')
print('There are ', len(data.url.unique()), ' unique values in column: url')

print('\nProportions calculated as number_unique_vals/non_nan_vals for each column: ')
print('in_reply_to_screen_name: ', len(data.in_reply_to_screen_name.unique())/x_reg.count()[1])
print('hashtags               : ', len(data.hashtags.unique())/x_reg.count()[5])
print('user_mentions          : ', len(data.user_mentions.unique())/x_reg.count()[6])
print('url                    : ', len(data.url.unique())/x_reg.count()[7])

# There are two issues here: there is a lot of missing data, and when the data is not missing,
# there are many unique values. Data of this nature does not give a lot of consistant
# information, since each observation is essentially unique or missing. How can a model learn from this?
# So, to take care of this, I would like to replace the 'hashtags' and 'user_mentions' columns
# to be the number of hashtags or user mentions, replacing 'nan' values with 0 obviously. For
# 'screen_name' and 'url', I think it would be best to have a binary structure, with 1 indicating
# a reply or url is present, and 0 if not. This makes the data more consistant with information.

# I decided to go back and change this in the 'parse_entities' function in parse.py, since it is not
# good practice or efficient to keep lists as elements of Pandas dataframe. Maybe I should do some more
# research in multi indexing to make this storage more efficient.

# Fill nans with 0s
x_reg = x_reg.fillna(0)

# Change 'reply_to_screen_name' values to 1s
x_reg['in_reply_to_screen_name'] = np.where(x_reg['in_reply_to_screen_name'] != 0, 1, 0)

# Now, we one-hot-encode the 'type' and 'day' columns
x_reg = pd.get_dummies(x_reg, columns = ['type', 'day'])

# Now, let's split the data into training and testing
x_reg_train  = x_reg[:6207]
x_reg_test   = x_reg[6207:]
x_text_train = x_text[:6207]
x_text_test  = x_text[6207:]
y_train      = y[:6207]
y_test       = y[6207:]

# Scaling the x_reg_train and x_reg_test because the column 'favorite_count' has much larger values than
# compared to the other columns. So, we will divide every element in the 'favorite_count' column by the max
# value so that we can change the scale to be between 0-1. However, we want this column to dominate a little,
# so we will multiply them by 10 afterwards because many values will be very tiny. The columns 'hashtags' 
# and 'user_mentions' are of a scale that does not render our data heterogeneous, so we leave them.

max_fave_cnt = max(x_reg_train['favorite_count'])

x_reg_train['favorite_count'] = (x_reg_train['favorite_count']/max_fave_cnt)*15
x_reg_test['favorite_count']  = (x_reg_test['favorite_count']/max_fave_cnt)*15

# Preprocessing the text data by turning them into sequences of integers to be fed into an Embedding layer
# later.

vocab_size  = 900
tokenizer   = Tokenizer(vocab_size)
tokenizer.fit_on_texts(x_text_train)
x_seq_train = tokenizer.texts_to_sequences(x_text_train)
x_seq_test  = tokenizer.texts_to_sequences(x_text_test)

# Now, we must pad the sequences so that they are all of the same length to be fed into the model
# To find the appropriate max length, we will find the lengths of each sequence in the data.

lengths = []
for seq in x_seq_train:
    lengths.append(len(seq))
    
# The average length is about 14, so we will pad using a maxlen of 15.

x_seq_train = sequence.pad_sequences(x_seq_train, maxlen = 15)
x_seq_test  = sequence.pad_sequences(x_seq_test , maxlen = 15)


# Changing x_seq_train and x_seq_test into np array of arrays instead of list of lists
x_seq_train = np.array([np.array(seq) for seq in x_seq_train])
x_seq_test  = np.array([np.array(seq) for seq in x_seq_test])


# Debugging by building separate models at first to see if the data is in the right format
'''
# This works just fine
reg_model = models.Sequential()
reg_model.add(layers.Dense(32, activation = 'relu', input_shape = (19,)))
reg_model.add(layers.Dense(1))
reg_model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae'])

reg_model.fit(x_reg_train, y_train, epochs = 30, batch_size = 64)

text_model = models.Sequential()
text_model.add(layers.Embedding(vocab_size, 64))
text_model.add(layers.LSTM(32))
text_model.add(layers.Dense(1))
text_model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae'])

text_model.fit(x_seq_train, y_train, epochs = 30, batch_size = 64)
'''



# Now, I think we are ready to build the models. We will use Keras functional API because we have two
# disparate types of input data: text and regular numbers. The architecture will be relatively simple,
# having a fully connected neural net for x_reg, and running an LSTM on x_text.

text_input    = Input(shape = (15,), dtype = 'int32', name = 'text')
embedded_text = layers.Embedding(vocab_size, 64)(text_input)
encoded_text  = layers.LSTM(32, return_sequences = True)(embedded_text)
encoded_text1 = layers.LSTM(32)(encoded_text)

reg_input     = Input(shape = (19,), dtype = 'float32', name = 'reg')
x1            = layers.Dense(64, activation = 'relu')(reg_input)
x2            = layers.Dense(64, activation = 'relu')(x1)
x3            = layers.Dense(32, activation = 'relu')(x2)
x4            = layers.Dense(32, activation = 'relu')(x3)
x5            = layers.Dense(32, activation = 'relu')(x4)

concatenated  = layers.concatenate([encoded_text1, x5], axis = -1)

dense1        = layers.Dense(32)(concatenated)
dense2        = layers.Dense(16)(dense1)
output        = layers.Dense(1)(dense2)

model         = Model([text_input, reg_input], output)
model.compile(optimizer = 'rmsprop',
              loss      = 'mse',
              metrics   = ['mae'])

history       = model.fit({'text': x_seq_train, 'reg': x_reg_train}, 
                          y_train,
                          epochs           = 19,
                          batch_size       = 64,
                          validation_split = 0.1)

train_acc     = history.history['mae']
val_acc       = history.history['val_mae']
epochs        = np.arange(len(train_acc))

plt.plot(epochs, train_acc , 'bo', label = 'Training MAE')
plt.plot(epochs, val_acc   , 'o' , label = 'Val MAE')
plt.title('MAE Vs. Epoch')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()

plt.show()

plt.plot(epochs, history.history['val_loss'] , 'bo', label = 'Validation Loss')
plt.title('Loss Vs. Epoch')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.show()

# results gives a list of two things: loss and mae, respectively
results = model.evaluate([x_seq_test, x_reg_test], y_test)

# Now, let's take a peak at predictions
predictions = model.predict([x_seq_test, x_reg_test])
predictions = np.array(np.where(predictions < 0, 0, predictions)).reshape((len(predictions),))
predictions = np.around(predictions)
#y_test      = np.array(y_test)

df = pd.DataFrame({'true': y_test, 'pred': predictions})

df['abs_log_diff'] = np.log(abs(y_test-predictions))

 