from datasets import load_dataset

def main():
    dataset_id = 'ag_news'
    
    dataset = load_dataset(dataset_id)
    
    class_label = dataset['train'].features['label']
    
    print(class_label.num_classes)
    print(class_label.names)
    # output: 4 ['World', 'Sports', 'Business', 'Sci/Tech']


if __name__ == '__main__':
    main()