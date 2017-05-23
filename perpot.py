#!/usr/bin/python3


import math
from matplotlib import pyplot as plt


class PerPot:
    def __init__(self):
        self.t = 0
        self.sr = 0.0
        self.rr = 0.0
        self.ofr = 0.0
        self.pp = 0.0
        self.trace = {}
        self.trace['pp'] = [self.pp]
        self.trace['sr'] = [self.sr]
        self.trace['rr'] = [self.rr]
        self.trace['ofr'] = [self.ofr]

    def set_delays(self, ds, dr, dsof):
        self.ds = ds
        self.dr = dr
        self.dsof = dsof

    def set_starting_potentials(self, sp, rp):
        self.sp = sp
        self.rp = rp
        self.trace['sp'] = [self.sp]
        self.trace['rp'] = [self.rp]

    def step(self, lr):
        # raise potentials
        self.sp += lr
        self.rp += lr
        # recompute rates
        self.sr = min(min(1.0, self.sp), max(0.0, self.pp)) / self.ds
        self.rr = min(min(1.0, self.rp), min(1.0, 1.0 - self.pp)) / self.dr
        self.ofr = max(0.0, self.sp - 1.0) / self.dsof
        # update potentials
        self.sp -= self.sr + self.ofr
        self.rp -= self.rr
        self.pp += self.rr - self.sr - self.ofr
        # store results
        self.trace['sp'].append(self.sp)
        self.trace['rp'].append(self.rp)
        self.trace['pp'].append(self.pp)
        self.trace['sr'].append(self.sr)
        self.trace['rr'].append(self.rr)
        self.trace['ofr'].append(self.ofr)

        self.t += 1

    def follow(self, prog):
        for w in prog:
            self.step(w)

    def plot(self, prog):
        fig, ax = plt.subplots(nrows=3, sharex=True)
        xaxis = list(range(self.t))
        ax[0].plot(xaxis, prog)
        ax[1].plot(self.trace['pp'], label='pp')
        ax[1].plot(self.trace['sp'], label='sp')
        ax[1].plot(self.trace['rp'], label='rp')
        ax[1].legend(loc='upper right')
        ax[2].plot(self.trace['sr'], label='sr')
        ax[2].plot(self.trace['rr'], label='rr')
        ax[2].plot(self.trace['ofr'], label='ofr')
        ax[2].legend(loc='upper right')
        plt.show()

def main():
    pp = PerPot()
    pp.set_delays(2, 1.8, 2)
    pp.set_starting_potentials(0, 0)
    W = [0.01*math.sqrt(x) if x%1 == 0 else 0.0 for x in range(1000)]
    pp.follow(W)
    pp.plot(W)



if __name__ == '__main__':
    main()
