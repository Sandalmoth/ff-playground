#!/usr/bin/python3


from ff import FF
from perpot import PerPot
import math
from matplotlib import pyplot as plt


if __name__ == '__main__':
    ff = FF()
    ff.set_decays(20, 7)
    ff.set_combination_functions(lambda x: math.log(x+0.01), lambda x: x)
    pp = PerPot()
    pp.set_delays(14, 12, 14)
    pp.set_starting_potentials(0, 0)

    W = [0.01*math.sqrt(x) if x%7 == 0 else 0.0 for x in range(1000)]
    pp.follow(W)
    ff.follow(W)

    fig, ax = plt.subplots(nrows = 3, sharex = True)
    xaxis = list(range(len(W)))
    ax[0].plot(xaxis, W)
    ax[1].plot(pp.trace['pp'], label='pp')
    ax[1].plot(pp.trace['sp'], label='sp')
    ax[1].plot(pp.trace['rp'], label='rp')
    ax[1].legend(loc='upper right')
    ax[2].plot(ff.trace['performance'], label='performance')
    ax[2].plot(ff.trace['fitness'], label='fitness')
    ax[2].plot(ff.trace['fatigue'], label='fatigue')
    ax[2].legend(loc='upper right')

    plt.show()
