import os
import random
import pickle
from urllib.request import urlopen
class SuccessorModel(object):

    stop_words = ['of', 'a', 'an', 'the', 'by', 'for', 'of', 'from']
    end_punctuation = ['.', '!', '?']
    BIGRAM_MULTIPLICATIVE_FACTOR = 5
    STOP_WORDS_FACTOR = 50
    def __init__(self, filename):
        self.path = process(filename)
        self.tokens = get_tokens(self.path)
        self.unigram_table = build_unigram_table(self.tokens)
        self.bigram_table = build_bigram_table(self.tokens)
########################
#####Public Methods#####
########################
    def random_sent(self):
        sentence = ''
        while (len(sentence.split()) < 6) or (len(sentence.split()) > 15):
            sentence = self.construct_sent(find_weighted_random(self.unigram_table['.']), self.unigram_table, self.bigram_table)
        return sentence
    def generate_k_sentences(self, k):
        sentence = ''
        for x in range(k):
            sentence += self.random_sent() + '\n'
        print(sentence[:-1])
    def generate_sentence_length(self, k):
        sentence = ''
        while len(sentence.split())-1 != k:
            sentence = self.random_sent()
        return sentence
###############################
#####Sentence Construction#####
###############################
    def create_options_with_bigram(self, bigram_table, prevKey, wordsWithWeights):
        factor = SuccessorModel.BIGRAM_MULTIPLICATIVE_FACTOR
        onePrev = prevKey[1]
        if onePrev in SuccessorModel.stop_words:
            factor = SuccessorModel.STOP_WORDS_FACTOR
        biGramMappings = list(bigram_table[prevKey])
        for each_word in biGramMappings:
            each_word[1] *= factor
        wordsWithWeights = deep_merge(wordsWithWeights, biGramMappings)
        return wordsWithWeights

    def construct_sent(self, word, unigram_table, bigram_table, limit = None):
        result, wordcounter = '', 0
        twoPrev, onePrev = '' , ''
        prevKey = (twoPrev, onePrev)
        while not check_end(word):
            result += word + ' '
            wordsWithWeights = list(unigram_table[word])
            twoPrev, onePrev = onePrev, word
            prevKey = (twoPrev, onePrev)
            if (onePrev != '' and twoPrev != ''):
                if prevKey in bigram_table:
                    wordsWithWeights = self.create_options_with_bigram(bigram_table, prevKey, wordsWithWeights)
            if (limit is not None) and (wordcounter == limit):
                end = check_contains_end(wordsWithWeights)
                if (end != ''):
                    return result + end
                else:
                    return ''
            word = find_weighted_random(wordsWithWeights)
            wordcounter += 1
        return result + word
##################
#####Learning#####
################## 
def build_bigram_table(tokens):
    if len(tokens) < 3:
        return {}
    table = {}
    twoPrev, onePrev = tokens[0], tokens[1]
    prevKey = (twoPrev, onePrev)
    for i in range(2, len(tokens)):
        word = tokens[i]
        # only make bigrams when you arne't mapping across sentences (when there's a period)
        if not (check_end(prevKey[0]) or check_end(prevKey[1])):
            if prevKey not in table:
                table[prevKey] = [[word, 1]]
            else:
                duplicate = False
                for successor in table[prevKey]:
                    if successor[0] == word:
                        successor[1] += 1
                        duplicate = True
                if (not duplicate):
                    table[prevKey].append([word, 1])
        twoPrev, onePrev = onePrev, word
        prevKey = (twoPrev, onePrev)
    return table
def build_unigram_table(tokens):
    table = {}
    prev = '.'
    for word in tokens:
        if prev not in table:
            table[prev] = [[word, 1]]
        else:
            duplicate = False
            for successor in table[prev]:
                if successor[0] == word:
                    successor[1] += 1
                    duplicate = True
            if (not duplicate):
                table[prev].append([word, 1])
        prev = word
    return table
###################
#####Utilities#####
###################
def get_tokens(path):
    if (os.path.exists(path)):
        return open(path, encoding='utf-8').read().split()
    else:
        return []

def process(filename):
    processed = ''
    path = filename+'.txt'
    if (os.path.exists(path)):
        preprocessedfile = open(path, 'r', encoding='utf-8')
        text = preprocessedfile.read()
        for c in text:
            if c in ['.','!', '?']:
                processed += ' ' + c + ' '
            elif c in ['"', '"', '-', '--', "''"]:
                continue
            else:
                processed += c
        newPath = filename+'_processed.txt'
        processedfile = open(newPath, 'w', encoding='utf-8')
        processedfile.write(processed)
        preprocessedfile.close()
        processedfile.close()
        return newPath
    else:
        return ''
def check_contains_end(l):
    for punct in ['.', '!', '?']:
        for subl in l:
            if punct in subl[0]:
                return punct
    return ''
# Checks if a word contains a sentence ending character.
# Complexity: O(n) where n is char_length of the string.
def check_end(word):
    for punct in ['.','!', '?']:
        if punct in word:
            return True
    return False
# From a list of two-element lists with words and their respective weights, 
# this function finds a weighted randomized choice form them.
# Complexity: O(n) where n is number of dictionaries in wordDict.
def find_weighted_random(wordDict):
    elements = []
    weights = []
    weighted_ranges = []
    for each_word in wordDict:
        elements.append(each_word[0])
        weights.append(each_word[1])
    if (len(elements) == 0):
        return None
    if (len(elements) == 1):
        return elements[0]
    r = random.random()
    total_weight, current_range = sum(weights), 0
    for weight in weights:
        current_range += weight / total_weight
        weighted_ranges.append(current_range)
    start_range = 0
    for i in range(len(weighted_ranges)):
        end_range = weighted_ranges[i]
        if (r >= start_range and r <= end_range):
            return elements[i]
        start_range = end_range
# Deep merges 2 lists of 2-element lists to remove duplicates
# keys. Outputs a dictionary that has a sum of the keys (non-destructive) 
# Complexity: O(n^2)
def deep_merge(l1, l2):
    for sublist1 in l1:
        duplicate = False
        for sublist2 in l2:      
            if sublist1[0] == sublist2[0]:
                sublist2[1] += sublist1[1]
                duplicate = True
        if (not duplicate):
            l2.append(sublist1)
    return l2


