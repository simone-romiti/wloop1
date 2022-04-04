# energy.py

from doctest import master
import matplotlib.pyplot as plt

import libs

import plotly.graph_objects as go
Fig = go.Figure()


f_E = lambda x: x # identity
def plot_energy(Lx, Ly, Lz, Lt, beta, mass, heat, nmeas, nsteps):
  libs.plot_obs(
    Fig=Fig, NAME="E*A", F=f_E, ncut=0, 
    Lx=Lx, Ly=Ly, Lz=Lz, Lt=Lt, 
    beta=beta, mass=mass, 
    heat=heat, nmeas=nmeas, nsteps=nsteps
  )
####

def gen_html_energy(dims):
  libs.gen_html(Fig, "energy", dims)
####

libs.loop_2(plot_energy, gen_html_energy)


