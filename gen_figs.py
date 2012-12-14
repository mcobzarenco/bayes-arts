#!/usr/bin/python
from __future__ import print_function, division

import time

from pylab import *
from numpy import random
from scipy.stats import beta

N = 100
GROUND_THETA = 0.60

random.seed(int(time.clock() * 100))
rets = random.rand(N) < GROUND_THETA


def plot_beta(name, a, b, ret=None, n=None):
    print(a, b)
    theta = linspace(0, 1, 300)
    pdf = beta.pdf(theta, a, b)

    ax = axes()
    ax.plot(theta, pdf / max(pdf))
    if n is not None:
        ax.text(0.025, 0.9, 'TRADE IDEA %d' % n)
    if ret is not None:
        ax.text(0.025, 0.85, 'RETURN %s 0' % ('>' if ret else '<'))
    ax.set_title('P(hit rate | ideas so far)')
    ax.yaxis.set_ticks([])
    ax.grid()
    ax.legend()
    ax.xaxis.set_label_text('Hit Rate')
    ax.xaxis.set_ticks(linspace(0, 1, 11))
    s, e = (beta.ppf(0.025, a, b), beta.ppf(0.975, a, b))
    ax.fill([s, s, e, e, s], [0, 1, 1, 0, 0], color='0.9')

    gcf().set_size_inches(10, 6)
    savefig(name, bbox_inches='tight')

    plt.close()
    return


a, b = 7, 7

f = open('hitrate.tex', 'w')
name = 'figs/0.pdf'
plot_beta(name, a, b)
f.write("""\\begin{frame}\\frametitle{Hit Rate (Initial Prior)}\\begin{figure}
            \\begin{centering}\includegraphics[scale=0.5]{%s}\\end{centering}\\end{figure}\\end{frame}\n""" % name)

for i, ret in enumerate(rets):
    name = 'figs/%d.pdf' % (i + 1)
    a, b = a + ret, b + 1 - ret
    plot_beta(name, a, b, ret, i + 1)
    f.write("""\\begin{frame}\\frametitle{Hit Rate (Posterior)}\\begin{figure}
                \\begin{centering}\includegraphics[scale=0.5]{%s}\\end{centering}\\end{figure}\\end{frame}\n""" % name)

f.close()

print('mle=%.3f' % (sum(rets) / float(N)))
