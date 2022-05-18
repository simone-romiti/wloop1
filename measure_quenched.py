# runs.py

import os
#from threading import get_native_id
import yaml

import libs

EXE = os.path.abspath("./u1-measure")
nsave = libs.g_nsave

g_FLD = libs.g_FLD
ndims = libs.Ndims

g_omeas_scripts_dir = "./omeas_scripts/"

def generate_yaml(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  geometry = {"X": Lx, "Y": Ly, "Z": Lz, "T": Lt, "ndims": ndims}
  monomials = {"gauge":{"beta": float(beta)}}
  #
  outdir = g_FLD + libs.get_quenched_confdir_pattern(
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
    beta=beta, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
    )
  measurements = {
    "conf_dir": outdir,
    "beta_str_width": 2,
    "n_meas": nmeas,
    "nstep": nsteps,
    "Wloop": True,
    "pion_staggered": {"mass": mass }
    }
  #
  nd1 = {"geometry": geometry, "monomials": monomials, "measurements": measurements}
  dmp1 = yaml.dump(nd1)
  #
  scr_path = g_omeas_scripts_dir + '/beta{beta}_chiral.yaml'.format(beta=beta)
  with open(scr_path, 'w') as f:
    f.write(dmp1)
  ##
  return scr_path
##


def offline_meas(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  scr_path = generate_yaml(Lx, Ly, Lz, Lt, beta, 0.1, heat, nmeas, nsteps)
  scr_log = g_omeas_scripts_dir + '/beta{beta}_0.1.log'.format(beta=beta)
  cmd = EXE+" -f "+scr_path
  print("running: ", cmd)
  stream = os.popen(cmd)
  s = stream.read()
  with open(scr_log, 'w') as f:
    f.write(s)
  #
  return
##

libs.loop_offline(offline_meas)
