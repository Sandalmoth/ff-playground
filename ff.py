#!/usr/bin/python3


import math
from matplotlib import pyplot as plt


class FF:
    def __init__(self):
        self.t = 0
        self.fitness = 0
        self.fatigue = 0
        self.performance = 0
        self.work = []
        self.trace = {}
        self.trace['fitness'] = [self.fitness]
        self.trace['fatigue'] = [self.fatigue]
        self.trace['performance'] = [self.performance]

    def set_decays(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def set_combination_functions(self, g, h):
        self.g = g
        self.h = h

    def step(self, lr):
        # calculate fitness/fatigue
        self.work.append(lr)
        self.fitness = sum([self.work[i] * math.exp((i - len(self.work)) / self.t1) for i in range(len(self.work))])
        self.fatigue = sum([self.work[i] * math.exp((i - len(self.work)) / self.t2) for i in range(len(self.work))])
        self.performance = self.g(self.fitness) - self.h(self.fatigue)
        # store results
        self.trace['fitness'].append(self.g(self.fitness))
        self.trace['fatigue'].append(self.h(self.fatigue))
        self.trace['performance'].append(self.performance)

        self.t += 1

    def follow(self, prog):
        for w in prog:
            self.step(w)

    def plot(self, prog):
        fig, ax = plt.subplots(nrows=2, sharex=True)
        xaxis = list(range(self.t))
        ax[0].plot(xaxis, prog)
        ax[1].plot(self.trace['performance'], label='performance')
        ax[1].plot(self.trace['fitness'], label='fitness')
        ax[1].plot(self.trace['fatigue'], label='fatigue')
        ax[1].legend(loc='upper left')
        plt.show()

def main():
    ff = FF()
    ff.set_decays(2, 1)
    ff.set_combination_functions(lambda x: math.sqrt(x), lambda x: x)
    W = [0.01*math.sqrt(x) if x%1 == 0 else 0.0 for x in range(1000)]
    ff.follow(W)
    ff.plot(W)



if __name__ == '__main__':
    main()
