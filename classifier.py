from model import Persistence
from parsers import tokenize

class Classifier(Persistence):
    def check(self, item):
        print list(self.categories())
        return
        res = []
        for cat in self.categories():
            res.append((cat, self.test(item, cat)))
        res.sort(key=lambda x: x[1])
        return res

    def test(self, item, category):
        print 'testing', category
        # probability of finding all features of sample in given category
        total = reduce(
            lambda a, b: a * b, 
            (
                self.weightedprob(feature, category)
                for feature in tokenize(item)
            )
        )
        return total * (
            # probability of that some random sample goes into that category
            self.catcount(category) / self.totalcount()
        )

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
        ''' Probability of finding feature in samples of given category,
        starting from 1/2 '''
        basic_prob = self.fprob(feature, category)

        # count of samples with feature in all categories
        totals = sum(self.fcount(feature, c) for c in self.categories())

        return (0.5 + totals * basic_prob) / (1.0 + totals)
