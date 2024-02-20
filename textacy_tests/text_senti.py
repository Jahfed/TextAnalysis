from textblob import TextBlob

basepath = '../text_data/'
file = basepath + 'bidenspeech.txt'

with open(file,'r') as f:
    text = f.read()

blob = TextBlob(text)
sentiment = blob.sentiment.polarity
print(sentiment)
