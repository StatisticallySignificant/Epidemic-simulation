from matplotlib import pyplot as plt
import numpy as np

def graphic_display(time_in_game, list_infected):
	# Values that we want to display as an array (1D)
	x_values = np.linspace(1,time_in_game/1000, len(list_infected))
	y_values = np.array(list_infected)#np.cos(4*x_values)

	ax = plt.subplots()[1]
	# Differents titles
	ax.set_title(" Nombre de malades en fonction du temps") 
	ax.set_xlabel(" Temps (secondes)") 
	ax.set_ylabel(" Personnes infectées ")
	# Create a graph
	ax.plot(x_values, y_values, color="red")
	# Color between 0 and y_value
	ax.fill_between(x_values, y_values, 0, color='red')
	# Display graph and its legend (there is no legend right now)
#	plt.legend() 
	plt.show()
