import json
import random
import pickle
import tensorflow as tf
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

lem = WordNetLemmatizer()

intents = json.loads(open("data.json").read())

words = pickle.load(open("words.pk1", "rb"))
classes = pickle.load(open("classes.pk1", "rb"))
model = tf.keras.models.load_model("chatbot_model.model")

ignore_letters = ["!", "?", ",", ".", "-", "_", "/", "\"", "£", "$", "#", "@", "(", ")", ":", ";" ]
user_name = ""

def clean_up_sentence(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words = [lem.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for i in sentence_words:
        for x, word in enumerate(words):
            if word == i:
                bag[x] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    THRESHOLD = 0.50
    results = [[i, r] for i, r, in enumerate(res) if r >= THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent" : classes[r[0]], "probability" : str(r[1])})
    tag = return_list[0]["intent"]
    global user_name
    if tag == "introduce":
        for word in clean_up_sentence(sentence):
            if word not in words and word not in ignore_letters:
                user_name = word
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["response"])
            break
    return result

def name_replace(res):
    res = res.replace("<name>", user_name.capitalize())
    return res




# print("Chatbot is running come and say Hi. ")   Just for testing purposes in the terminal
# while True:
#     message = input("")
#     message = message.lower()
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)


# print(predict_class("Hello World"))