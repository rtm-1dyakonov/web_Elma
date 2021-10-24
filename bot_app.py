### pip install pymorphy2 ###
### pip install tensorflow ###



import tensorflow as tf
import numpy as np
import pymorphy2
import pickle
import eel

eel.init('web')

model = tf.keras.models.load_model("2drop02_lr01")

with open('dict_labels.json', 'rb') as fp:
    dict_labels = pickle.load(fp)

with open('word_index_.json', 'rb') as fp:
    word_index_ = pickle.load(fp)



def norm_converter(sentence):
    """
    Функция для приведения слов в норм.форму
    """
    morph = pymorphy2.MorphAnalyzer()
    parsed_token = morph.parse(sentence) 
    return parsed_token[0].normal_form

def encode(phrase):
  string = norm_converter(phrase)
  words = string.split(" ")
  encoded_phrase = [word_index_["<start>"]]
  for token in words:
    index = word_index_.get(token, word_index_["<UNKNOWN>"])
    encoded_phrase.append(index)
  return encoded_phrase

def expand(x, filler, gl=15):
    n = gl - len(x)
    if n > 0:
        x.extend([filler]*n)
    return np.asarray(x, dtype="int32")

# def top3_4phrase(phrase, model, dict_labels=dict_labels):
#   encoded_phrase = expand(encode(phrase), 0)
#   predictions = model.predict(np.array(encoded_phrase)[None, :]).ravel()
#   top_lbl_index = np.argsort(-predictions)[:3]
#   print("ТОП-3 намерения для введённое фразы:")
#   for index in top_lbl_index:
#     print(dict_labels[index], ", вероятность: ", round(100*predictions[index], 4), "%", sep="")

def top_indexes(phrase, model):
  encoded_phrase = expand(encode(phrase), 0)
  predictions = model.predict(np.array(encoded_phrase)[None, :]).ravel()
  top_lbl_index = np.argsort(-predictions)[:3]
  return predictions, top_lbl_index

@eel.expose
def intent(phrase):
  predictions, indexes = top_indexes(phrase, model);
  obj = []
  for index in indexes:
    obj.append(dict_labels[index])
  return obj

@eel.expose
def score(phrase):
  predictions, indexes  = top_indexes(phrase, model);
  obj = []
  for index in indexes:
    obj.append(round(100*predictions[index], 4))
  return obj
  

# if __name__ == "__main__":
#   phrase = input("Введите фразу длиной до 14 слов:\n")
#   top3_4phrase(phrase, model)
#   k=input("Для выхода нажмите любую клавишу")

eel.start('index.html', size=(1200, 800))