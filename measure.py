# runs.py

import os
import libs


EXE = os.path.abspath("./u1-measure")
nsave = libs.g_nsave

g_FLD = libs.g_FLD

def offline_meas(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  geometry = "-X {X} -Y {Y} -Z {Z} -T {T} --ndims {ndims}".format(
    X=Lx, Y=Ly, Z=Lz, T=Lt, ndims=3)
  confdir  = g_FLD + libs.get_outdir_pattern(Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, beta=beta, mass=mass, heat=heat, nmeas=nmeas, nsteps=nsteps)
  ##
  action = "--beta {beta}".format(beta=beta)
  hmc_par = "--nmeas {nmeas} --nsteps {nsteps} --nstep {nsave}".format(
    heat=heat, nmeas=nmeas, nsteps=nsteps, nsave=nsave)
  #
  Wloops = "--Wloops 1"
  cmd = EXE+" "+geometry+" "+action+" "+hmc_par+" "+Wloops+" --confdir "+confdir
  stream = os.popen(cmd)
  s = stream.read()
  #
  return
##

libs.loop_offline(offline_meas)
