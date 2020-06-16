#!/usr/bin/env python3

"""1_example_neutron_spectra_tokamak.py: plots neutron spectra."""

import openmc
import plotly.graph_objects as go
from neutronics_material_maker import Material

# MATERIALS

my_material = Material(material_name='eurofer').openmc_material
mats = openmc.Materials([my_material])


# GEOMETRY

# surfaces
vessel_inner_surface = openmc.Sphere(r=500)
vessel_rear_surface = openmc.Sphere(r=600)
outer_surface = openmc.Sphere(r=650, boundary_type='vacuum')

# cells
inner_vessel_cell = openmc.Cell(region=-vessel_inner_surface)
# this is filled with a void / vauum by default

blanket_cell = openmc.Cell(region=-vessel_rear_surface & +vessel_inner_surface)
blanket_cell.fill = my_material

outer_vessel_cell = openmc.Cell(region=+vessel_rear_surface & -outer_surface)
# this is filled with a void / vauum by default

universe = openmc.Universe(cells=[inner_vessel_cell,blanket_cell, outer_vessel_cell])
geom = openmc.Geometry(universe)


# SIMULATION SETTINGS

# Instantiate a Settings object
sett = openmc.Settings()
sett.batches = 10
sett.inactive = 0 # the default is 10, which would be wasted computing for us
sett.particles = 100_000
sett.run_mode = 'fixed source'

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
sett.source = source

# setup the  filters for the tallies
neutron_particle_filter = openmc.ParticleFilter(['neutron'])
surface_filter = openmc.SurfaceFilter(vessel_rear_surface) # detects particles across a surface
cell_filter = openmc.CellFilter(blanket_cell) # detects particles across a cell / volume
energy_bins = openmc.mgxs.GROUP_STRUCTURES['CCFE-709']
energy_filter = openmc.EnergyFilter(energy_bins)
spectra_tally = openmc.Tally(name='energy_spectra')
spectra_tally.scores = ['flux']
spectra_tally.filters = [cell_filter, neutron_particle_filter, energy_filter]

# the following two lines will need uncommenting
spectra_tally.scores = ['current']
spectra_tally.filters = [surface_filter, neutron_particle_filter, energy_filter]

tallies = openmc.Tallies()
tallies.append(spectra_tally)


# combine all the required parts to make a model
model = openmc.model.Model(geom, mats, sett, tallies)
# Run OpenMC!
results_filename = model.run()

# open the results file
results = openmc.StatePoint(results_filename)

#extracts the tally values from the simulation results
cell_tally = results.get_tally(name='energy_spectra')
cell_tally = cell_tally.get_pandas_dataframe()
cell_tally_values = cell_tally['mean']
cell_tally_std_dev = cell_tally['std. dev.']


# this section plots the results
fig = go.Figure()

# adds a line for the upper stanadard deviation bound
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values+cell_tally_std_dev,
                         line=dict(shape='hv', width=0)
                        )
              )

# adds a line for the lower stanadard deviation bound
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values-cell_tally_std_dev,
                         name='std. dev.',
                         fill='tonext',
                         line=dict(shape='hv', width=0)
                        )
              )

# adds a line for the tally result
fig.add_trace(go.Scatter(x=energy_bins,
                         y=cell_tally_values,
                         name='breeder_blanket_spectra',
                         line=dict(shape='hv')
                        )
              )

fig.update_layout(title='Neutron energy spectra',
                  xaxis={'title': 'Energy (eV)',
                         'type': 'log'},
                  yaxis={'title': 'Neutrons per cm2 per source neutron',
                         'type': 'log'}
                 )

fig.write_html("blanket_neutron_spectra.html")
try:
    fig.write_html("/my_openmc_workshop/blanket_neutron_spectra.html")
except (FileNotFoundError, NotADirectoryError):  # for both inside and outside docker container
    pass

fig.show()
