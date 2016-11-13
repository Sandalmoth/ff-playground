# Read the work vector from a file
args <- commandArgs(trailingOnly = TRUE)
print("Trying to open:")
print(args[1])
wtable = read.table(args[1], sep=",", strip.white=TRUE, header=TRUE)

wtable
str(wtable)

# lets start with a timescale
weeks = 6
days = 7*weeks
dayparts = 24 # 1h resolution seems reasonable
timesteps = days*dayparts

# this way every integer-shift is a day-shift
t = 0:(timesteps-1) / dayparts

# so t 1/2 are the fitness/fatigue decay parameters
# and k 1/2 are parameters for their linear combination into performance
t1 = 3
t2 = 1
kq = 0.5 # k1 / k2
k1 = kq / (1 + kq)
k2 = 1 - k1

# make decay rate independent of time resolution
t1 = t1 * dayparts
t2 = t2 * dayparts

# since this is the supersimple version, lets just define the work-vector manually
w = vector(length = timesteps, mode="numeric")
# trying out some various workload distributions

# calculate timesteps and add them to wtable
wtable$Timestep = wtable$Day*dayparts + wtable$Timepoint

# also calculate workload
# first, we need a function

epley = function(I) {
	return((1/I - 1)*30 + 1)
}

# and then the simple calculation
# R is suprisingly convenient
wtable$Workload = wtable$Sets * wtable$Reps / epley(wtable$Intensity)

wtable

for (i in 1:length(wtable$Day)) {
	w[wtable$Timestep[i]] = w[wtable$Timestep[i]] + wtable$Workload[i]
}
# w[wtable$Timestep] = wtable$Workload

# get a plot for easy overview
plot(w~t)

# g is the fitness function, h is the fatigue function

# Function calculating fitness (or fatigue) at timestep n
ff = function(w, n, t) {
	f = 0.0
	for (i in 1:(n-1)) {
		f = f + w[i] * exp(-(n-i)/t)
	}
	return(f)
}

# compute fitness and fatigue
g = vector("numeric", timesteps)
for (i in 2:timesteps) {
	g[i] = ff(w, i, t1)
}
h = vector("numeric", timesteps)
for (i in 2:timesteps) {
	h[i] = -ff(w, i, t2)
}

# plot(g~t)
# plot(h~t)

# calculate the performance
p = k1 * g + k2 * h

# plot(p~t)

# making a plot of fitness, fatigue and performance
plot(p~t, cex=0, ylim=c(min(h), max(g)))
# lines(w~t)
lines(g~t, col="blue")
lines(h~t, col="red")
lines(p~t)

# because it would be nice to see overall trends, lets make a weekly p average
# seems sensible to plot it from the middle of the week
tmidweeks = (0:(weeks-1) * dayparts * 7 + dayparts * 3.5) / dayparts
pavg = vector("numeric", weeks)
for (i in 0:(weeks-1)) {
	prange = 1:(7*dayparts) + i*7*dayparts
	pavg[i+1] = mean(p[prange]) # Oh how it annoys me that R stuff starts from index 1.
}

# add it to the big plot
lines(pavg~tmidweeks, lty="dotted")