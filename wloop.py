

#import libs
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import os
import sys
HOME_DIR = os.path.expanduser("~/")
sys.path.insert(0, HOME_DIR+'Documents/zwiebel/')
import jkf

dims = [16,16,1,16]
Lx, Ly, Lz, Lt = dims
Ncut = 500
Nstep = 10
Nconf_tot = 2000
Nconf = int((Nconf_tot - Ncut)/Nstep) # configurations actually considered
N_jkf = 10

DIR = "./data/runs/X16Y16Z1T16/beta1.0_PureGauge_heat1_nmeas2000_nsteps500/"
base_FILE = "wilsonloop.00"


def get_jkf(x, Nj):
  """ jackknifes from list of configurations x """
  N = len(x) # number of measures
  n = int(N/Nj)
  Nc = len(x[0]) # number of elements of each x_i
  M = np.zeros((Nj, Nc))
  for j in range(Nj):
    aj = 0
    for i1 in range(0, j*n):
      aj += x[i1]
    ##
    for i2 in range((j+1)*n, N):
      aj += x[i2]
    ##
    aj /= (N-n) # average
    M[j] = aj
  ##
  return M
##


def get_avr_jkf(x):
  """ averages of jackknifes """
  Nj = len(x)
  Nc = len(x[0]) # number of elements of each x_i
  M = np.zeros(Nc)
  for j in range(Nj):
    M += x[j]
  ##
  M /= Nj
  return M
##


def get_err_jkf(x):
  """ jackknifes error """
  av = get_avr_jkf(x)
  Nj = len(x)
  Nc = len(x[0]) # number of elements of each x_i
  eM = 0#np.zeros(Nc)
  for j in range(Nj):
    eM += (x[j]-av)**2
  ##
  A0 = (Nj-1)/Nj
  eM *= A0
  return np.sqrt(eM)
##

from io import StringIO
def get_df_conf_Wr(i):
  F = DIR+base_FILE+"{:04d}".format(i)+".dat"
  sF = open(F, "r").read()
  sF = sF.replace(" \n", "\n").replace(4*" ", " ").replace(3*" "," ")
  #
  TESTDATA = StringIO(sF)
  return pd.read_csv(TESTDATA, sep=" ")
##  

def get_list_df_conf_Wr():
  L_Wr = []
  for i in range(1, Nconf+1):
    Wr = get_df_conf_Wr(i*Nstep).drop(['t'], axis=1) # no need for time
    L_Wr.append(Wr)
  ##
  return L_Wr
##

LIST_df_Wr = get_list_df_conf_Wr() # list of gauge config data frame for W_r(t)

def get_conf_Wr(r):
  cWr = np.zeros((Lt-1, Nconf))
  for g in range(Nconf):
    cWr[:, g] = LIST_df_Wr[g]["r={r}".format(r=r)].to_numpy()
  ##
  return cWr
##

def get_jkf_Wr(r):
  return jkf.confs_to_jkf(get_conf_Wr(r), N_jkf)
##

def get_jkf_Vr_eff(r):
  Wr = get_jkf_Wr(r)
  return Wr.M_eff_no_back()
##

def add_time_series(Fig, y, ey, lbl, tstart=1):
  """ add plot of planar W_r(t) to the Fig """
  #
  x = [i for i in range(tstart, len(y)+1)]
  #
  trace_name = lbl
  Fig.add_trace(
    go.Scatter(
      x=x, y=y, 
      error_y = dict(
        type = 'data',
        array = ey,
        visible=True
      ),
      mode="lines+markers+text",
      name=trace_name
    )
  )
  #
  return None
##

def gen_plot_obs_r(fun_Mr, name):
  Fig = go.Figure()
  for r in range(1, Lx):
    y  = fun_Mr(r).ae()["av"]
    ey = fun_Mr(r).ae()["err"] 
    add_time_series(Fig, y, ey, "{name}_{r}(t)".format(name=name, r=r))
  ##
  dir = "./plots/"
  if not os.path.exists(dir):
    os.makedirs(dir)
  ##
  Fig.write_html(dir+"{name}.html".format(name=name))
  return
##  

gen_plot_obs_r(get_jkf_Wr, "W")
gen_plot_obs_r(get_jkf_Vr_eff, "V")


