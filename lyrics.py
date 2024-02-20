import textacy
import spacy

# import lyrics getter
from lyricsgenius import Genius

# analyzing data
from textacy import text_stats as ts 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter

# preprocessing data
from textacy import preprocessing
from functools import partial

# extra info
from textacy import extract


# basic settings
genius = Genius('hTTQgGEaUcs7hnOeq8V4mLGQOtbEWzhhmN3Gi42M2wnMPkF_jhq01gIHjplqRuoA')
genius.retries = 10
genius.verbose = False

# addaptable settings
divider = "\n*************************\n" #so information is nicely divided into sections
artist_name = 'Bruno Mars'
max_songs = 3
print_songs = 3 #Be less then 
song_list = []

# making the songs list
def create_song_list(artist_name,max_songs):
    if print_songs <= max_songs:
                print("\n\n")
                i=0
                artist = genius.search_artist(artist_name,max_songs=max_songs)
                songs = artist.songs
                # print(songs)
                for song in songs:
                    song_list.append(f'{song.lyrics}')
                    print(f"Added SONG{i} - with id: {song.id} / {song.artist} - {song.title}")
                    i+=1
                print(divider)
                    
    else:
        print(f"max_songs {max_songs} is less then the number to be printed: {print_songs}")

create_song_list(artist_name,max_songs)

# functions to analyse the text
nlp = spacy.load('en_core_web_sm')    #load the dictionary once

def flesch_score(song_text):
    doc = nlp(song_text)
    stats = ts.readability.flesch_reading_ease(doc)
    print("FLESCH SCORE: 0 is Difficult and 100 is Easy to read:")
    print(f"The lyrics has a score of {round(stats,3)}\n")

def extract_matches(song_text):
    keyword_search = 'room'
    doc = nlp(song_text)
    em = extract.matches.token_matches(doc, [{"POS":"DET","OP":"?"},{"POS":"ADJ","OP":"+"},{"POS":"NOUN","OP":"+"}])
    print(list(em))
    ek = extract.kwic.keyword_in_context(doc, keyword=keyword_search,window_width=10)
    print(f'\nThe keyword: "{keyword_search}" appears in: ')
    if ek:
        for i in ek:
            print(f'{i}')
    else:
        print("NOT!...")

def summarize(song_text):
    doc = nlp(song_text)
    lyric_length = len(list(doc))
    keywords = []
    stopwords = list(STOP_WORDS)
    post_tag=['PROPN','ADJ','NOUN','VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
                continue
        if(token.pos_ in post_tag):
                keywords.append(token.text)
    freq_word = Counter(keywords)
    freq_list = freq_word.most_common(5)
    print(f'How many time each word appears in the song: {freq_list} \n')

    

# printing the songs
def get_lyric_data(song_list,max_print=1):
    i=0
    print(f'There are {len(song_list)} songs to analyze')
    print(divider)
    for song in song_list:
        if i <= max_print:
            summarize(song)
            flesch_score(song)
            extract_matches(song)
            print(divider)
            i+=1
        
get_lyric_data(song_list,print_songs)