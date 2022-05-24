
from ctypes import LittleEndianStructure
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

from io import StringIO


g_Druns = "./data/runs/" #directory of runs
g_nstep = 100 # measure after each 100 configurations
g_N_conf = 200 # 200 # number of gauge configurations considered
g_N_therm = 500 # number of configurations before thermalization
g_N_jkf = 10  # 20 # number of jackknifes
g_L, g_T = 8, 32 # spatial and temporal sizes of the lattice
g_plateau = [7, 14]


def dir_path_pattern(beta, L, T):
    return g_Druns+"X{X}Y{Y}Z{Z}T{T}/".format(X=L,Y=L,Z=1,T=T)+"beta{beta}".format(beta=beta)+"_PureGauge_heat0/quenched/"

class pion_corr:
  """ class for the analysis of the pion correlator """
  def __init__(self, beta, N_jkf, L, T):
    self.beta = beta
    self.L, self.T, self.T_half = L, T, int(T/2)
    self.N_jkf = N_jkf
    self.DIR = dir_path_pattern(beta, L, T)
    #
    C_conf = np.zeros((T, g_N_conf))
    for ig in range(g_N_conf):
        idx = g_N_therm + ig*g_nstep
        C_conf[:,ig] = pd.read_csv(self.DIR+"C_pion.{:06d}".format(idx), sep=" ")["C(t)"]
    ##
    self.C_jkf = jkf.confs_to_jkf(C_conf, N_jkf)
    self.C_jkf.apply_time_symmetry(+1)
    self.plateau = g_plateau
  ##
  def plot_Corr(self, yscale, path):
    fig, ax = plt.subplots()
    ax.set_title("${L}^2$x{T} - $\\beta=${beta}".format(L=self.L, T=self.T, beta=self.beta))
    ax.set_xlabel("t/a")
    ax.set_ylabel("C(t)")    
    ax.set_yscale(yscale)
    ax.errorbar(x=[t for t in range(self.T_half)], y=self.C_jkf.avrs(), yerr=self.C_jkf.errs(), linestyle="--", capsize=0.5)
    plt.savefig(path)
    plt.close()
  ##
  def get_M_eff(self):
    return (self.C_jkf).M_eff_bkw(+1)
  ##
  def get_fit_M_eff(self):
    E = Meff(self.get_M_eff())
    t1, t2 = self.plateau
    E.fit_to_const(t1=t1, t2=t2)
    return E.get_M0()
  ##
  def plot_M_eff(self, path):
    fig, ax = plt.subplots()
    ax.set_title("${L}^2$x{T} - $\\beta=${beta}".format(L=self.L, T=self.T, beta=self.beta))
    ax.set_xlabel("t/a")
    ax.set_ylabel("M_eff(t)")    
    M_eff = self.get_M_eff()
    ax.errorbar(x=[t for t in range(self.T_half-1)], y=M_eff.avrs(), yerr=M_eff.errs(), linestyle="--", capsize=1.5)
    M0 = self.get_fit_M_eff()
    #
    n_dense = 100
    t1, t2 = self.plateau[0], self.plateau[1]
    t_fit = np.linspace(t1, t2, num=n_dense)
    M_fit_best = [M0.avrs()[0] for i in range(n_dense)]
    M_fit_down = [M0.avrs()[0]-M0.errs()[0] for i in range(n_dense)]
    M_fit_up = [M0.avrs()[0]+M0.errs()[0] for i in range(n_dense)]
    #
    plt.plot(t_fit, M_fit_best, linestyle="--")
    plt.fill_between(t_fit, M_fit_down, M_fit_up, alpha=0.5, color="orange")
    #
    plt.savefig(path)
    plt.close()
##

beta_list = ["3.0"] # ["1.0", "1.5", "2.0", "2.5", "3.0"]
for beta in beta_list:
  print("beta =", beta)
  PC = pion_corr(beta, g_N_jkf, g_L, g_T)
  # plots
  dir = "./plots/beta{beta}/".format(beta=beta)
  if not os.path.exists(dir):
    os.makedirs(dir)
  ##
  PC.plot_Corr("linear", dir+"Corr.pdf")
  PC.plot_Corr("log", dir+"Corr_log.pdf")
  PC.plot_M_eff(dir+"M_eff.pdf")
#   # effective mass fitting
#   PC.fit_Meff()
##
