from successor_model import SuccessorModel
import pickle
print('Type in the name of the file (without the file extension) from which we are learning the language model')
file_name = str(input())
model = SuccessorModel(file_name)
canon = file_name.split('.')[0]

with open(canon+'_model.ml', 'wb') as output:
	pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)