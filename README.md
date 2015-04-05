NLPRandomSentenceLearn
=============
SentenceLearn generates a alignment-based language model from a document by mapping individual words and two-word phrases to their successors in the text from which the model is learning. It can then generate random sentences using the lexicon and the grammar learned from the language model.

API
---
There are 3 important files included - successor_model.py, process.py, and sentence_gen.py. The latter 2 serve as the way to interact with the successor model, and successor_model contains the source code for the creation of the model and the generation of random sentence from that model. 

1. <b>process.py</b>

	Before running this file, any text can be put into a text file and placed in the same directory as process.py. 
	When run from STDin, process.py will ask for the filename as the input in the Terminal, construct the word model, and save that as a file in the same directory. Another pre-processed text file for the original text file will also appear in the same directory.

2. <b>sentence_gen.py</b>
	After running process.py, there should be a .ml file that contains the model stored as a file. When running sentence_gen, it will request a filename from STDin in the same way as process.py. Then, it will request a number of random sentences to generate, and it will output those sentences (as a quick note: it takes some time to read in the file (around 3-4 seconds on my machine) and then some time to run through the model and compute the probabilities. For 10 sentences generated from the text of the Mary Shelley novel, Frankenstein, it took about 8 seconds total.

3. <b>successor_model.py</b>

	<b>Public Methods:</b>
	
	a. random_sent() - Generates a random sentence
	
	b. generate_k_sentences(int k) - Generates k random sentences.
	
	c. generate_sentence_length(int k) - Generates a sentence of length k



Description of the model
------------------------

I built a successor table with each word being mapped into a dictionary that maps any word to all of the words that have followed that word in the learning text. From there, the random sentence generator picks randomly from any words that start a sentence (words that follow a period) and for every word, it randomly picks the next word from the list of successors of the current word. This model selects using a weighted probability because the table also keeps track of how many times a word has succeeded another word. This process continues until a period. I called the successors table a unigram table.

This model is actually surprisingly successful, although not perfect. Frequently, the sentences produced by this model lose their "train of thought" or start devolving into strange and incorrect sentences. I felt like, in general, the problem was a lack of context.

Therefore, I also constructed a bigram model, which maps two-word phrases to successors. Then, when generating the random sentences, the previous 2 words can be taken into context, and, if we also search the bigram set, then we can find a successfor the sentence that might make more sense. 

I integrated the bigram set with the unigram set and set a constant by which I increased the probabilistic weight of a bigram result. 

In terms of data structures, I used a dictionary to map words to their successors, and for each successor word, I put it in a 2-element list with its weight. Therefore, the primary data structure is a dictionary with strings as keys and a list of 2-element lists. 
Random Notes
------------
There are a few more tweaks in the model:

1. I increased the factor by which I preferred the bigram results if I am looking for a successor of a "stop" word (of, in, etc.) because context is especially useful in those contexts.

2. I eliminated quotation marks and dashes, which were creating bizzarre sentences.

3. I kept tweaking the value for the factor by which I prefer bigrams to generate better sentences until I found a happy middle. 
4. I throw out random sentences that are longer than 15 words (these tend to be sentences that started well intentioned but devolved).
