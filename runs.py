# runs.py

import os
import libs

EXE = libs.g_EXE 
nsave = libs.g_nsave

runs_in_progress = libs.g_runs_in_progress # output file of runs in progress 
open(runs_in_progress, "w+").close() # create file if it doesn't exist
runs_done = libs.g_runs_done # output file of previous successful runs 
#open(runs_done, "w+").close() # create file if it doesn't exist

g_FLD = libs.g_FLD
R_done = [r.strip() for r in open(runs_done, "r").readlines()] # list of lines

str_runs_done = open(runs_done, "r").read()
open(runs_done+".bkp", "w").write(str_runs_done) # saving a backup copy

# open(runs_done, "w").write("") # erasing content
FILE_done = open(runs_done, "a") # append mode

def gen_run(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  geometry = "-X {X} -Y {Y} -Z {Z} -T {T} --ndims {ndims}".format(
    X=Lx, Y=Ly, Z=Lz, T=Lt, ndims=3)
  action  = ""
  outdir  = g_FLD + libs.get_outdir_pattern(Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, beta=beta, mass=mass, heat=heat, nmeas=nmeas, nsteps=nsteps)
  if(mass=="-1"):
    action = "--beta {beta} --no_fermions 1".format(beta=beta)
  else:
    action = "--beta {beta} --mass {mass}".format(beta=beta, mass=mass)
  ##
  hmc_par = "--heat {heat} --nmeas {nmeas} --nsteps {nsteps} --nsave {nsave}".format(
    heat=heat, nmeas=nmeas, nsteps=nsteps, nsave=nsave)
  #
  if outdir in R_done:
    return
  else:
    print("Output: ", outdir)
    #
    cmd = EXE+" "+geometry+" "+action+" "+hmc_par+" "+"--outdir"+" "+outdir
    stream = os.popen(cmd)
    s = stream.read()
    #
    FILE_done.write(outdir+"\n")
    FILE_done.flush()
    return
##

libs.loop_runs(gen_run)
