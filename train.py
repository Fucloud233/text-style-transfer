import fasttext

class Classifier:
    def __init__(self, output_path: str):
        self.model = None
        self.output_path = output_path


    def train(self, train_dataset: str, epoch: int=25):
        self.model = fasttext.train_supervised(input=train_dataset, epoch=epoch)
    
    def test(self, test_dataset: str):
        return self.model.test(test_dataset)
    
    def predict(self, sentence: str):
        return self.model.predict(sentence)

    def save(self):
        self.model.save_model(self.output_path)

    def load(self):
        self.model = fasttext.load_model(self.output_path)

MODEL_PATH = 'model/fastText.bin'

def main():
    train_dataset_path = 'data/yelp/sentiment.train'
    test_dataset_path = 'data/yelp/sentiment.test'

    classifier = Classifier(MODEL_PATH)
    
    classifier.train(train_dataset_path)
    classifier.save()

    classifier.load()
    print(classifier.test(test_dataset_path))

def predict():
    classifier = Classifier(MODEL_PATH)
    classifier.load()

    while True:
        sentence = input("input:\t")
        if sentence == 'exit':
            break

        kind = classifier.predict(sentence)
        print("kind:\t{}".format(kind))

if __name__ == '__main__':
    # main()
    predict()
    