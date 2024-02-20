from textblob import TextBlob
from newspaper import Article

url = 'https://www.solike.review/post/how-to-respond-to-negative-reviews'
article = Article(url)

article.download()
article.parse()
article.nlp()

text = article.summary
print(text)

blob = TextBlob(text)
sentiment = blob.sentiment.polarity
print(sentiment)
