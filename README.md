# ff-playground
Messing around with the fitness-fatigue model in R.

Note that I'm pretty much new to R, so don't expect anything exemplary :P

Anyway, the fitness fatigue model is a pretty cool model for predicting the effects of training on performance. I'm gonna be using it pretty much the way it is formulated in:

Mark Pfeiffer, Modeling the Relationship between Training and Perfomance - A Comparison of Two Antagonistic Concepts

supersimple.R --
simple calculation and plotting of performance function using preset workload and arbitrary units

simplewithparsing.R --
same as supersimple but reads workload vector from a .csv (see example)

Well. I'm mostly interested in strength training, so lets implement a basic way of turning sets and reps into a workload. The somewhat common
tonnage = weight * sets * reps
kinda sucks, since it obviously favours high rep sets. Instead, Im gonna base it on the more recent idea of counting hard sets to near failure. Though, this is a bit inflexible. Instead, consider a formula for calculating the 1RM given a number of reps and a weight

1RM = w(1 + r/30)		(Epley)

Intensity is defined as

I = w / 1RM

so

1/I = 1 + r/30
1/I - 1 = r/30
r = (1/I - 1)*30

Although this formula doesn't handle maxes brilliantly so lets remake it into

r = (1/I - 1)*30 + 1

So we have a formula that calculates the expected number of maximum reps, that is the number of reps that should equate failure, at a given intensity. (There are many other possible variants, which I might include. Just check wikipedia).

A suitable way of determining workload might then be:

w = sets * reps / maxreps



...Add some descriptions of scripts when they are done :P
for now, just run stuff with Rscript or something and see for yourself
