

#import libs
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import matplotlib.pyplot as plt

import os
import sys

HOME_DIR = os.path.expanduser("~/")
sys.path.insert(0, HOME_DIR+'Documents/zwiebel/')
import jkf
from eff_curve import Meff as Meff

dims = [16,16,1,16]
Lx, Ly, Lz, Lt = dims
Ncut = 500
Nstep = 50
Nconf_tot = 10000
Nconf = int((Nconf_tot - Ncut)/Nstep) # configurations actually considered
N_jkf = 10

DIR_data = "./data/"
DIR_analysis = DIR_data + "analysis/"
DIR_runs = DIR_data + "runs/"
DIR_geom = "X16Y16Z1T16/"

def get_DIR_hmc(beta):
  return "beta{b}_PureGauge_heat0_nmeas{Nconf_tot}_nsteps1000/".format(b=beta, Nconf_tot=Nconf_tot)
##

base_FILE = "wilsonloop.00"

from io import StringIO

class static_potential:
  """ class for the analysis of the static potential """
  def __init__(self, beta):
    self.beta = beta
    self.DIR = DIR_runs + DIR_geom + get_DIR_hmc(self.beta)
    self.LIST_df_Wr = self.get_list_df_conf_Wr() # list of gauge config data frame for W_r(t)
    self.plateau = pd.read_csv(DIR_analysis+DIR_geom+"plateau.txt", sep=" ", dtype={'beta': str})
  ##
  def get_df_conf_Wr(self, i):
    F = self.DIR+base_FILE+"{:04d}".format(i)+".dat"
    sF = open(F, "r").read()
    sF = sF.replace(" \n", "\n").replace(4*" ", " ").replace(3*" "," ")
    #
    TESTDATA = StringIO(sF)
    return pd.read_csv(TESTDATA, sep=" ")
  ##  
  def get_list_df_conf_Wr(self):
    L_Wr = []
    for i in range(1, Nconf+1):
      Wr = self.get_df_conf_Wr(i*Nstep).drop(['t'], axis=1) # no need for time
      L_Wr.append(Wr)
    ##
    return L_Wr
  ##
  def get_conf_Wr(self, r):
    cWr = np.zeros((Lt-1, Nconf))
    for g in range(Nconf):
        cWr[:, g] = self.LIST_df_Wr[g]["r={r}".format(r=r)].to_numpy()
    ##
    return cWr
  ##
  def get_jkf_Wr(self, r):
    return jkf.confs_to_jkf(self.get_conf_Wr(r), N_jkf)
  ##
  def get_jkf_Vr(self, r):
    Wr = self.get_jkf_Wr(r)
    return Wr.M_eff_no_bkw()
  ##
  def add_time_series(self, Fig, y, ey, lbl, type="linear", tstart=1):
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
  def gen_plot_obs_r(self, fun_Mr, name, type="linear"):
    """ Generate the plots from the jkf matrix obtained with fun_Mr(r), for all r
        type = One of the following enumeration values:
            ['-', 'linear', 'log', 'date', 'category',
            'multicategory']
    """
    Fig = go.Figure()
    for r in range(1, Lx):
      y  = fun_Mr(r).ae()["av"]
      ey = fun_Mr(r).ae()["err"] 
      self.add_time_series(Fig, y, ey, "{name}_{r}(t)".format(name=name, r=r))
    ##
    Fig.update_xaxes(title_text="t")
    Fig.update_yaxes(title_text=name, type=type)
    Fig.update_layout()
    ##
    dir = "./plots/"+DIR_geom+"beta"+self.beta+"/"
    if not os.path.exists(dir):
      os.makedirs(dir)
    ##
    outfile = dir+"{name}".format(name=name)
    if(type !=  "linear"):
      outfile += "({tp}_plot)".format(tp=type)
    ##
    outfile += ".html"
    Fig.write_html(outfile)
    return
  ##
  def gen_plot_Wr(self, type):
    self.gen_plot_obs_r(self.get_jkf_Wr, "W", type=type)
  ##
  def gen_plot_Vr(self):
    self.gen_plot_obs_r(self.get_jkf_Vr, "V_eff")
  ##
  def get_fit_V(self, r):
    E = Meff(self.get_jkf_Vr(r))
    ib = list(self.plateau["beta"]).index(self.beta)
    t1, t2 = self.plateau.iloc[ib][["t1", "t2"]]
    E.fit_to_const(t1=t1, t2=t2)
    return E.get_M0()
  ##
  def fit_all_V(self, rlist) -> None:
    nr = len(rlist)
    V = jkf.matrix(nr, N_jkf)
    print("Fitting V(r):")
    for i in range(nr):
      print("r=", i)
      V[i] = self.get_fit_V(rlist[i])
    ##
    columns = ["j={j}".format(j=j) for j in range(N_jkf)]
    V.to_DataFrame(columns=columns).to_csv(DIR_analysis+DIR_geom+"/Vr.dat")

    V.ae().to_csv(DIR_analysis+DIR_geom+"/Vr(ae).dat")
    plt.title("{X}x{Y}x{Z}x{T} - $\\beta=${beta}".format(X=Lx,Y=Ly,Z=Lz,T=Lt,beta=self.beta))
    plt.xlabel("r")
    plt.ylabel("V(r)")    
    plt.errorbar(x=[r for r in range(1,nr+1)], y=V.ae()["av"], yerr=V.ae()["err"])
    plt.savefig("./plots/"+DIR_geom+"beta"+beta+"/Vr.pdf")
    plt.close()

    return None
##

beta_list = ["1.0", "1.5", "2.0", "2.5", "3.0"]
for beta in beta_list:
  print("beta =", beta)
  Si = static_potential(beta)
  # plots
  Si.gen_plot_Wr("linear")
  Si.gen_plot_Wr("log")
  Si.gen_plot_Vr()
  # effective mass fitting
  Si.fit_all_V([1,2,3])
##

