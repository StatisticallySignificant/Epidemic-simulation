# Need to install scipy first
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends import backend_agg as agg
import pygame
from pygame.locals import *
from scipy.interpolate import make_interp_spline 

pygame.init()

def graphic_display(time_in_game, list_infected, list_healthy, list_dead, list_recovered):
	# X axis : Time in seconds
	x_values = np.linspace(1,time_in_game/1000, len(list_infected))
	# Values converted as array (1D)
	# There are 4 list of values
	y_infected_counts = np.array(list_infected)
	y_healthy_counts = np.array(list_healthy)
	y_deaths_counts = np.array(list_dead)
	y_recovered_counts = np.array(list_recovered)

	# Curves are smooth
	Infected_Spline = make_interp_spline(x_values, y_infected_counts)
	Healthy_Spline =  make_interp_spline(x_values, y_healthy_counts)
	Deaths_Spline =  make_interp_spline(x_values, y_deaths_counts)
	Recovered_Spline =  make_interp_spline(x_values, y_recovered_counts)
	X_values = np.linspace(x_values.min(), x_values.max())

	infected_values = Infected_Spline(X_values)
	healthy_values = Healthy_Spline(X_values)
	death_values = Deaths_Spline(X_values)
	recovered_values = Recovered_Spline(X_values)

	fig, ax = plt.subplots()
	# Differents titles and parameters
	fig.set_figwidth(7)
	fig.set_figheight(6)
	ax.set_title(" Progression des états en fonction du temps") 
	ax.set_xlabel(" Temps (jours fictifs)") 
	ax.set_ylabel(" Nombre de personnes ")

	# Create a graph
	ax.plot(X_values, infected_values, color="red", label='infectés', linewidth=1.8)
	ax.plot(X_values, healthy_values, color='green', label='sains',  linewidth=1.8)
	ax.plot(X_values, death_values, color='black', label='morts', linewidth=1.7)
	ax.plot(X_values, recovered_values, color='blue', label='guéris', linewidth=1.8)
	plt.legend() 
	# We can export data in png 
	#plt.savefig('graph.png')

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	return raw_data, canvas
