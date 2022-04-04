# dH.py

from doctest import master
import math
import libs

import plotly.graph_objects as go
Fig_dH = go.Figure()

f_dH = lambda x: x # identity
def plot_dH(Lx, Ly, Lz, Lt, beta, heat, nmeas, nsteps, mass):
    libs.plot_obs(
      Fig_dH, "dH", f_dH, ncut=0, 
      Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
      beta=beta, mass=mass, 
      heat=heat, nmeas=nmeas, nsteps=nsteps
      )
####

def gen_html_dH(dims):
  libs.gen_html(Fig_dH, "dH", dims)
####

libs.loop_2(plot_dH, gen_html_dH)

#---------------------------

Fig_exp_m_dH = go.Figure()

f_exp_m_dH = lambda x: math.exp(-x) # e^{-dH}
def plot_exp_m_dH(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps) -> None:
  libs.plot_obs(
    Fig_exp_m_dH, "dH", f_exp_m_dH, ncut=15, 
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt,
    beta=beta, mass=mass, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
  )
  return None
####

def gen_html_exp_m_dH(dims):
  libs.gen_html(Fig_exp_m_dH, "exp_m_dH", dims)
####

libs.loop_2(plot_exp_m_dH, gen_html_exp_m_dH)

#---------------------------

Fig_mod_dH = go.Figure()

f_mod_dH = lambda x: math.fabs(x) # |dH|
def plot_mod_dH(Lx, Ly, Lz, Lt, beta, heat, nmeas, nsteps, mass):
  libs.plot_obs(
    Fig_mod_dH, "dH", f_mod_dH, ncut=15, 
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt,
    beta=beta, mass=mass, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
  )
####

def gen_html_mod_dH(dims):
  libs.gen_html(Fig_mod_dH, "mod_dH", dims)
####

libs.loop_2(plot_mod_dH, gen_html_mod_dH)
