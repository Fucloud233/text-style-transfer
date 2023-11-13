from nltk.translate import bleu

# https://stackoverflow.com/questions/32395880/calculate-bleu-score-in-python

bleu(
    ['The candidate has no alignment to any of the references'.split()],
    'John loves Mary'.split(),
    (1,),
)