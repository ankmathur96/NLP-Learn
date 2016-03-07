import successor_model
import pickle, sys, os
from successor_model import SuccessorModel
def random_sentence_gen(model):
	response = ''
	print('**************************************************************************************************')
	print("Language model is loaded. To quit sentence generation, input 'quit' as the random sentence length")
	print('**************************************************************************************************')
	while 1:
		print('Enter the length of the random sentence you want:')
		response = input()
		if response == "quit":
			break
		n_words = int(response)
		if n_words < SuccessorModel.SENTENCE_LOWER_BOUND or n_words >= SuccessorModel.SENTENCE_UPPER_BOUND:
			print("USAGE: Enter a sentence length that is not lower than " + str(SuccessorModel.SENTENCE_LOWER_BOUND) \
				+ " or bigger than " + str(SuccessorModel.SENTENCE_UPPER_BOUND))
			print()
		else:
			print()
			print('"' + model.generate_sentence_length(n_words) + '"')
			print()

if len(sys.argv) < 2:
	print("USAGE: python sentence_gen.py [text file to learn from]")
else:
	file_name = sys.argv[1]
	if os.path.exists(file_name):
		canon = file_name.split('.')[0]
		if os.path.exists(canon + '_model.ml'):
			with open(canon+'_model.ml', 'rb') as inFile:
				model = pickle.load(inFile)
		else:
			model = SuccessorModel(file_name)
			with open(canon + '_model.ml', 'wb') as model_out:
				pickle.dump(model, model_out, pickle.HIGHEST_PROTOCOL)
		random_sentence_gen(model)
	else:
		print("ERROR: File was not found at that path. Check to make sure the file is still there.")
