from model import Persistence
from parsers import tokenize

class Classifier(Persistence):
    def train(self, item, category):
        for feature in tokenize(item):
            self.incf(feature, category)

        self.incc(category)

    def fprob(self, feature, category):
        ''' Probability of finding feature in samples of given category '''
        if self.catcount(category) == 0:
            return 0

        return self.fcount(feature, category) / self.catcount(category)

    def weightedprob(self, feature, category):
        basic_prob = self.fprob(feature, category)

        # count of samples with feature in all categories
        totals = sum(self.fcount(feature, c) for c in self.categories())

        return (0.5 + totals * basic_prob) / (1.0 + totals)
