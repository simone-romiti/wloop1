# acc.py

from doctest import master
import matplotlib.pyplot as plt

import libs

import plotly.graph_objects as go
Fig = go.Figure()


f_acc = lambda x: x # identity
def plot_acc(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  libs.plot_obs(
    Fig=Fig, NAME="rho", F=f_acc, ncut=0, 
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
    beta=beta, mass=mass, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
  )
####

def gen_html_acc(dims):
  libs.gen_html(Fig, "acc", dims)
####

libs.loop_2(plot_acc, gen_html_acc)


