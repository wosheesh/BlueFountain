import pickle

# TODO: read the output pickle file
# TODO: save the data into a CSV format

def read_output(myfile):
    alumnis = pickle.load(open(myfile, "rb"))
    for