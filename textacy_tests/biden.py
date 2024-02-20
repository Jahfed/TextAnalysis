import textacy
import spacy

# analyzing data
from textacy import text_stats as ts 

# preprocessing data
from textacy import preprocessing
from functools import partial

# extra info
from textacy import extract

# The sources to use as an example
basepath = '../text_data/'
file = basepath + 'bidenspeech.txt'
sentence = 'this! is: www.jahfed.com #@'

########STATISTICAL ANALYSIS OF TEXT#############
# A function to calculate the readability (complexity) of a text in the The Flesch–Kincaid readability test.
def flesch(filename):
    with open(file,  'r') as f:
        text = f.read()
        text = text.replace('\n','')

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # doc = textacy.make_spacy_doc(text, lang="en_core_web_sm")
    stats = ts.readability.flesch_reading_ease(doc)
    print(f"The text has a readability score of {round(stats,3)}")

flesch(file)



###########PREPROCESSING TEXT############
preproc = preprocessing.make_pipeline(
    preprocessing.remove.html_tags,
    preprocessing.replace.urls,
    preprocessing.normalize.unicode,
    partial(preprocessing.remove.punctuation, only=["$","//","!",'"']),
    preprocessing.replace.emojis,
    preprocessing.normalize.whitespace,
)

clean_text = preproc(sentence)
print(clean_text)



###########EXTRACT INFO###########