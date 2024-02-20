import textacy
import spacy
from my_modules.loader import loader

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
genius.retries = 10 #increase the number if time-out fails, standard is no retries not advisable
genius.verbose = False

# ask userinput
artist_request = input("\n\nWhich artist do you want to analyse? ")
songs_request = int(input("And how many songs? "))
keyword_request = input("Is there a keyword that you are interested in? ")

if len(artist_request.strip()) < 2:
    artist_name = 'Bruno Mars'
else:
    artist_name = artist_request.strip()

if len(keyword_request.strip()) < 3:
    keyword = ''
else:
    keyword_search = keyword_request.strip()

if songs_request < 1 or songs_request > 20:
    max_songs = 3
    print_songs = 3 #Be less then max_songs, it is being checked
else:
    max_songs = songs_request
    print_songs = songs_request

# initializing a divider and a songlist
divider = "\n*************************\n"
song_list = []
nlp = spacy.load('en_core_web_sm')    #languag is english (en)

# making the songs list
def create_song_list(artist_name,max_songs):
    loader()
    if print_songs <= max_songs:
                i=0
                artist = genius.search_artist(artist_name,max_songs=max_songs)
                songs = artist.songs
                print('\r\033[K\033[92mLoaded Songs succesfully...\033[0m\n\n', end='')
                for song in songs:
                    song_list.append(f'{song.lyrics}')
                    print(f"\033[93mAdded SONG {i+1} - with id: {song.id} / {song.artist} - {song.title}\033[0m")
                    i+=1
                print(divider)
    else:
        print(f"max_songs {max_songs} is less then the number to be printed: {print_songs}")
create_song_list(artist_name,max_songs)

def flesch_score(song_text):
    doc = nlp(song_text)
    stats = ts.readability.flesch_reading_ease(doc)
    print("FLESCH SCORE: 0 is Difficult and 100 is Easy to read (only english-language):")
    print(f"The lyrics has a score of \033[92m{round(stats,3)}\033[0m\n")

def extract_matches(song_text):
    doc = nlp(song_text.replace('\n', ' '))
    em = extract.matches.token_matches(doc, [{"POS":"DET","OP":"?"},{"POS":"ADJ","OP":"+"},{"POS":"NOUN","OP":"+"}])
    print(list(em))

    if len(keyword_search) > 2:
        ek = extract.kwic.keyword_in_context(doc, keyword=keyword_search,window_width=10)
        print(f'\nThe keyword: \033[92m"{keyword_search}"\033[0m appears in: ')
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
    print(f'How many time each word appears in the song: \n\033[95m{freq_list}\033[0m \n')

# printing the songs
def get_lyric_data(song_list,max_print=1):
    i=0
    print(f'There are \033[92m{len(song_list)}\033[0m songs to analyze')
    print(divider)
    for song in song_list:
        if i <= max_print:
            summarize(song)
            flesch_score(song)
            extract_matches(song)
            print(divider)
            i+=1
        
get_lyric_data(song_list,print_songs)