import pickle


class Composer:
    def load(self, name: str):
        with open(str(name) + '.pickle', 'rb') as data:
            return pickle.load(data)

    def save(self, name: str, data):
        with open(str(name) + '.pickle', 'wb') as f:
            pickle.dump(data, f)
