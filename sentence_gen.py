import successor_model
import pickle
print('Please enter the filename: ')
filename = str(input())
print('Enter the length of the random sentence you want:')
n_words = int(input())
with open(filename+'_model.ml', 'rb') as inFile:
	model = pickle.load(inFile)
print(model.generate_sentence_length(n_words))