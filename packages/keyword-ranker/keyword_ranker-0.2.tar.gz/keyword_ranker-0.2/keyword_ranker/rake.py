# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
# Automatic keyword extraction from individual documents.
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and
# Theory.unknown: John Wiley and Sons, Ltd.
#
# NOTE: The original code can be found here:
# https://github.com/zelandiya/RAKE-tutorial
# has been extended by sbadecker to support lemmatization using
# WordNetLemmatizer from NLTK.


from __future__ import absolute_import
from __future__ import print_function
import re
import operator
import six
from six.moves import range
from nltk.stem import WordNetLemmatizer
import nltk


try:
    _ = nltk.corpus.wordnet
except Exception:
    nltk.download('wordnet')


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stopwords(stopword_file):
    '''
    Utility function to load stop words from a file and return as a list of
    words.

    Parameters
    ----------
    stopword_file : str
        Path and filename of a file containing stop words.


    Returns
    ------
    stopwords :  list
        A list of stop words.

    '''
    stopwords = []
    for line in open(stopword_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stopwords.append(word)
    return stopwords


def lemmatize_phrases(phraselist):
    lemmatizer = WordNetLemmatizer()
    phraselist_lemmatized = []
    for phrase in phraselist:
        words = phrase.split(' ')
        phrase_temp = []
        for word in words:
            word = lemmatizer.lemmatize(word)
            phrase_temp.append(word)
        phraselist_lemmatized.append(' '.join(phrase_temp))
    return phraselist_lemmatized


def separate_words(text, min_word_return_size):
    '''
    Utility function to return a list of all words that are have a length
    greater than a specified number of characters.

    Parameters
    ----------
    text : str
        The text that must be split in to words.
    min_word_return_size : int
        The minimum number of characters a word must have to be included.


    Returns
    ------
    words :  list
        A list of words.

    '''
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to
        # invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' \
        and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    '''
    Utility function to return a list of sentences.

    Parameters
    ----------
    text : str
        The text that must be split in to sentences.

    Returns
    ------
    words :  list
        A list of sentences.

    '''
    sentence_delimiters = re.compile(u'[\\[\\]\n.!?,;:\t\\-\\"\\(\\)\\\'\u2019\u2013]')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stopword_regex(stopword_file_path):
    stopword_list = load_stopwords(stopword_file_path)
    stopword_regex_list = []
    for word in stopword_list:
        word_regex = '\\b' + word + '\\b'
        stopword_regex_list.append(word_regex)
    stopword_pattern = re.compile('|'.join(stopword_regex_list), re.IGNORECASE)
    return stopword_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern,
    min_char_length=1, max_words_length=3, lemmatize=True):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        if lemmatize:
            phrases = lemmatize_phrases(phrases)
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "" and is_acceptable(phrase, min_char_length,
            max_words_length):
                phrase_list.append(phrase)
    return phrase_list


def is_acceptable(phrase, min_char_length, max_words_length):

    # a phrase must have a min length in characters
    if len(phrase) < min_char_length:
        return 0

    # a phrase must have a max number of words
    words = phrase.split()
    if len(words) > max_words_length:
        return 0

    digits = 0
    alpha = 0
    for i in range(0, len(phrase)):
        if phrase[i].isdigit():
            digits += 1
        elif phrase[i].isalpha():
            alpha += 1

    # a phrase must have at least one alpha character
    if alpha == 0:
        return 0

    # a phrase must have more alpha than digits characters
    if digits > alpha:
        return 0
    return 1


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score,
                                    min_keyword_frequency=1):
    keyword_candidates = {}

    for phrase in phrase_list:
        if min_keyword_frequency > 1:
            if phrase_list.count(phrase) < min_keyword_frequency:
                continue
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stopwords_path, min_char_length=1, max_words_length=5,
                min_keyword_frequency=1, lemmatize=False):
        self.__stopwords_path = stopwords_path
        self.__stopwords_pattern = build_stopword_regex(stopwords_path)
        self.__min_char_length = min_char_length
        self.__max_words_length = max_words_length
        self.__min_keyword_frequency = min_keyword_frequency
        self.__lemmatize = lemmatize

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stopwords_pattern, self.__min_char_length, self.__max_words_length, self.__lemmatize)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores, self.__min_keyword_frequency)

        sorted_keywords = sorted(six.iteritems(keyword_candidates), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords
