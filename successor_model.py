import os
import random
import pickle
from urllib.request import urlopen
class SuccessorModel(object):
    SENTENCE_LOWER_BOUND = 6
    SENTENCE_UPPER_BOUND = 15
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
    def create_options_with_bigram(self, bigram_table, prev_key, words_with_weights):
        factor = SuccessorModel.BIGRAM_MULTIPLICATIVE_FACTOR
        one_prev = prev_key[1]
        if one_prev in SuccessorModel.stop_words:
            factor = SuccessorModel.STOP_WORDS_FACTOR
        bigram_mappings = list(bigram_table[prev_key])
        for each_word in bigram_mappings:
            each_word[1] *= factor
        words_with_weights = deep_merge(words_with_weights, bigram_mappings)
        return words_with_weights

    def construct_sent(self, word, unigram_table, bigram_table, limit = None):
        result, wordcounter = '', 0
        two_prev, one_prev = '' , ''
        prev_key = (two_prev, one_prev)
        while not check_end(word):
            result += word + ' '
            words_with_weights = list(unigram_table[word])
            two_prev, one_prev = one_prev, word
            prev_key = (two_prev, one_prev)
            if (one_prev != '' and two_prev != ''):
                if prev_key in bigram_table:
                    words_with_weights = self.create_options_with_bigram(bigram_table, prev_key, words_with_weights)
            if (limit is not None) and (wordcounter == limit):
                end = check_contains_end(words_with_weights)
                if (end != ''):
                    return result + end
                else:
                    return ''
            word = find_weighted_random(words_with_weights)
            wordcounter += 1
        return result + word

##################
#####Learning#####
################## 
def build_bigram_table(tokens):
    if len(tokens) < 3:
        return {}
    table = {}
    two_prev, one_prev = tokens[0], tokens[1]
    prev_key = (two_prev, one_prev)
    for i in range(2, len(tokens)):
        word = tokens[i]
        # only make bigrams when you arne't mapping across sentences (when there's a period)
        if not (check_end(prev_key[0]) or check_end(prev_key[1])):
            if prev_key not in table:
                table[prev_key] = [[word, 1]]
            else:
                duplicate = False
                for successor in table[prev_key]:
                    if successor[0] == word:
                        successor[1] += 1
                        duplicate = True
                if (not duplicate):
                    table[prev_key].append([word, 1])
        two_prev, one_prev = one_prev, word
        prev_key = (two_prev, one_prev)
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
    path = filename
    if (os.path.exists(path)):
        preprocessed_file = open(path, 'r', encoding='utf-8')
        text = preprocessed_file.read()
        for c in text:
            if c in ['.','!', '?']:
                processed += ' ' + c + ' '
            elif c in ['"', '"', '-', '--', "''"]:
                continue
            else:
                processed += c
        new_path = filename+'.processed'
        processed_file = open(new_path, 'w', encoding='utf-8')
        processed_file.write(processed)
        preprocessed_file.close()
        processed_file.close()
        return new_path
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


