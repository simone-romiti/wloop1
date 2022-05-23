# runs.py

from email import message
import os
import yaml

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

g_nsave = 100
g_icounter_omeas = 0#libs.n_thermalize
g_nstep_omeas = 100

def get_yaml(Lx, Ly, Lz, Lt, beta, m_sea, m_val, heat, nmeas, nsteps):
  geometry = {"X": Lx, "Y": Ly, "Z": Lz, "T": Lt, "ndims": libs.Ndims}
  monomials = {"gauge":{"beta": float(beta)}}
  #
  outdir = g_FLD + libs.get_quenched_confdir_pattern(
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
    beta=beta, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
    )
  #
  hmc = {"heat": bool(heat), "n_meas": nmeas, "n_save": g_nsave, "conf_dir": outdir}
  integrator = {"n_steps": nsteps}
  #
  omeas = {
    "verbosity": 1,
    "icounter": g_icounter_omeas,
    "nstep": g_nstep_omeas,
    "Wloop": True,
    "pion_staggered": {"mass": float(m_val) }
    }
  #
  nd1 = {
    "geometry": geometry, 
    "monomials": monomials, 
    "hmc": hmc, "integrator": integrator, 
    "omeas": omeas
    }
  dmp1 = yaml.dump(nd1, default_flow_style=False)
  #
  yaml_dir = outdir
  #
  if not os.path.exists(yaml_dir):
    os.makedirs(yaml_dir)
  ##
  yaml_path = yaml_dir+'m_val{m_val}.yaml'.format(m_val=m_val)
  of = open(yaml_path, 'w') 
  of.write(dmp1)
  ##
  return yaml_path
##


def gen_run(Lx, Ly, Lz, Lt, beta, m_sea, m_val, heat, nmeas, nsteps):
  yaml_input = get_yaml(Lx, Ly, Lz, Lt, beta, m_sea, m_val, heat, nmeas, nsteps)
  if yaml_input in R_done:
    return
  else:
    print("Output: ", yaml_input)
    #
    cmd = EXE+" -f "+yaml_input
    stream = os.popen(cmd)
    s = stream.read()
#    open('run.log', "w").write(s)
    #
    FILE_done.write(yaml_input+"\n")
    FILE_done.flush()
    return
##

libs.loop_runs(gen_run)
