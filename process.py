from successor_model import SuccessorModel
import pickle
print('Type in the filename to create the language model')
filename = str(input())
model = SuccessorModel(filename)

with open(filename+'_model.ml', 'wb') as output:
	pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)