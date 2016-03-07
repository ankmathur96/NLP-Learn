from successor_model import SuccessorModel
import pickle
print('Type in the name of the file (without the file extension) from which we are learning the language model')
filename = str(input())
model = SuccessorModel(filename)

with open(filename+'_model.ml', 'wb') as output:
	pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)