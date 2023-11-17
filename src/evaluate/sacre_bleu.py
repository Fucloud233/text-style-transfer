import evaluate as hf_evaluate

sacrebleu = hf_evaluate.load('sacrebleu')

def evaluate(src: str, tgt: str):
    results = sacrebleu.compute(predictions=[tgt], references=[[src]])

    return results['score']

def evaluate_batch(sentences: str):
    predications, references = [], []
    for sentence in sentences:
        predications.append(sentence['1'])
        references.append([sentence['0']])

    results = sacrebleu.compute(predictions=predications, references=references)

    return results['score']
    
if __name__ == '__main__':
    
    predications = [ "hello the general kenobi", "foo bar foobar"]
    references = [ 
        ["hello there general kenobi", "hello there !"],
        ["foo bar foobar", "foo bar foobar"]
    ]

    sacrebleu = hf_evaluate.load('sacrebleu')

    results = sacrebleu.compute(predictions=predications, references=references)

    print(list(results.keys()))
    print(results['score'])
