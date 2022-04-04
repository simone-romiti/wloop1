from io import StringIO
from sys import path
import pandas as pd
#import matplotlib.pyplot as plt
import os

Ndims = 3 # number of spacetime dimensions

g_EXE = "./u1-hmc" # global executable (or symbolic link to it)
g_nsave = 1 # period of saving configurations
g_FLD = "./data/runs/" 

g_runs_done = "./runs_done.txt" # output file of previous successful runs 
g_runs_in_progress = "./runs_in_progress.txt" # output file of runs in progress 


def get_outdir_pattern(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  """ Name patterns of the output directory for both runs and data analysis """
  outdir  = "X{X}Y{Y}Z{Z}T{T}/".format(X=Lx, Y=Ly, Z=Lz, T=Lt)
  outdir += "beta{beta}_".format(beta=beta)
  if(mass=="-1"):
    outdir += "PureGauge_"
  else:
    outdir += "mass{mass}_".format(mass=mass)
  ##
  outdir += "heat{heat}_nmeas{nmeas}_nsteps{nsteps}/".format(heat=heat, nmeas=nmeas, nsteps=nsteps)
  return outdir
## 

def get_plots_dir(Lx, Ly, Lz, Lt):
  """ Output directory of plots corresponding to the same volume """
  return "./plots/"+"X{X}Y{Y}Z{Z}T{T}/".format(X=Lx, Y=Ly, Z=Lz, T=Lt)

def get_output_dir_hmc(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  """ path of the output directory of the HMC """
  return g_FLD + get_outdir_pattern(Lx,Ly,Lz,Lt, beta, mass, heat, nmeas, nsteps)
##

def get_output_path_hmc(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  """ path of the output file of the HMC """
  dir = get_output_dir_hmc(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps)
  return dir + "output.hmc.data"
##

def get_data(Lx,Ly,Lz,Lt, beta, mass, heat, nmeas, nsteps):
  path_file = get_output_path_hmc(
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
    beta=beta, mass=mass, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
    )
  #
  F = open(path_file, "r")
  content = F.read()
  # content = content.split("## Acceptance rate parcentage: rho = rate/(i+1)\n")[1]
  # content = content.split("## Acceptance rate:")[0]
  TESTDATA = StringIO(content)
  #
  return pd.read_csv(TESTDATA, sep=" ", dtype=str)
##

# label for plots
def get_label(beta, mass, heat, nmeas, nsteps):
  lbl = "h="+str(heat)+" , "
  lbl += "$\\beta$="+beta+" , "
  lbl += "Nm="+str(nmeas)+" , "
  lbl += "Ns="+str(nsteps)+" , "
  lbl += "m="+str(mass)
  return lbl
##

def get_V_str(Lx, Ly, Lz, Lt):
  """ Volume info for plot titles"""
  return str(Lx) + "$\\times$" + str(Ly) + "$\\times$" + str(Lz) + "$\\times$" + str(Lt)
##

import plotly.graph_objects as go

def plot_obs(Fig, NAME, F, ncut, Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  """ Plot the column NAME to which the function F is applied """
  #
  df = get_data(Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, beta=beta, mass=mass, heat=heat, nmeas=nmeas, nsteps=nsteps)
  df = df.loc[df['getaccept'] == "1"]
  #
  x = [float(xi) for xi in df["i"]][ncut:]
  y = [F(float(yi)) for yi in df[NAME]][ncut:]
  #
  lbl = get_label(beta=beta, heat=heat, nmeas=nmeas, nsteps=nsteps, mass=mass)
  # plt.plot(x, y, label=lbl)
  trace_name = ""
  if (mass == "-1"):
    trace_name += "beta={beta} PureGauge".format(beta=beta) 
  else:
    trace_name += "beta={beta} mass={mass}".format(beta=beta, mass=mass)
  ##      
  trace_name += " heat: " + str(heat) + " nmeas: " + str(nmeas) + " nsteps: " + str(nsteps) 
  Fig.add_trace(
    go.Scatter(x=x, y=y,
      mode="lines+markers+text",
      name=trace_name
    )
  )
  #
  return None
##

import os
def gen_html(Fig, name, dims):
    Lx, Ly, Lz, Lt = dims
    plots_dir = get_plots_dir(Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt)
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    ##
    Fig.write_html(plots_dir+name+".html")


R_runs_done = [l.strip() for l in open(g_runs_done, "r").readlines()]
def loop_dims_fixed(dims, Fun, skip_missing_file) -> None:
  Lx, Ly, Lz, Lt = dims
  for beta in ["1.0", "2.0", "3.0"]:
    for mass in ["-1", "0.100", "0.000", "0.010"]:
      for heat in [1]:
        for nsteps in [500]:
          for nmeas in [2000]:
            dir_file = get_output_dir_hmc(
              Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
              beta=beta, mass=mass, 
              heat=heat, nmeas=nmeas, nsteps=nsteps
              )
            #
            if not dir_file in R_runs_done:
              if(skip_missing_file):
                print("MISSING FILE:", dir_file)
                continue
            ##
            Fun(
              Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
              beta=beta, mass=mass, 
              heat=heat, nmeas=nmeas, nsteps=nsteps
            )
  ##
  return None
##


def loop_1(dims, Fun) -> None:
  loop_dims_fixed(dims, Fun, True)
##


List_dims = [[16,16,1,16]]

def loop_runs(F_data) -> None:
  for dims in List_dims:
    loop_dims_fixed(dims, F_data, False)
  ##
  return None
##

def loop_offline(F_data) -> None:
  """ Loop for offline operations on the gauge configurations """
  for dims in List_dims:
    loop_dims_fixed(dims, F_data, True)
  ##
  return None
##

def loop_2(F_data, F_geom) -> None:
  for dims in List_dims:
    loop_1(dims, F_data)
    F_geom(dims)
    ##
  return None
##



