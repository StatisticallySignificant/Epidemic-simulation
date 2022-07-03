import pygame, random
from pygame.locals import *
from People_interactif import create_people
from matplot_interacitf import *
from matplotlib import pyplot as plt

pygame.init()
running = True
displaying = False

# Colors
white = (255,255,255)
light_grey = (245,245,245)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

# Screen, size, title, background color
total_screen_size = [1200,600]
screen = pygame.display.set_mode(total_screen_size)
pygame.display.set_caption("Epidemic is running")
screen.fill(white)

# Create 2 groups of sprites
people_group = pygame.sprite.Group()
test_collide_group = pygame.sprite.Group()

# Handle time and time counters
clock = pygame.time.Clock()
time_in_game, last_data_collect, last_display = 0,0,0

# Population
population_size = 250

# Epidemic parameters
standard_infection_duration = 4000
standard_time_before_death = 3000
probability_to_die = 3 # in percent
initial_infection_probability = 1 # in percents
contact_infection_probability = 80 # in percents

# Differents counters 
infected_count, healthy_count, recovered_count, death_count = 0,0,0,0
# List of the people's status at different timings
list_infected, list_healthy, list_dead, list_recovered =[], [], [], []

# Handle display of the people's status
def display_counts(infected_count, healthy_count, recovered_count, death_count):
	# The rectangle in which the text is, is a surface
	font_surface = pygame.Surface((160,120))
	font_rect = font_surface.get_rect(x=0,y=0)
	font_surface.fill(light_grey)
	screen.blit(font_surface, font_rect)

	# Same font for every text
	font = pygame.font.SysFont(None, 35)

	healthy_text = font.render(" Sains "+str(healthy_count), True, green)
	infected_text = font.render(" Malades "+str(infected_count), True, red)
	dead_text = font.render(" Morts "+str(death_count), True, black)
	recovered_text = font.render(" Guéris "+str(recovered_count), True, blue)
	# Display at different places
	screen.blit(healthy_text, (0,0))
	screen.blit(infected_text, (0,30))
	screen.blit(dead_text, (0,60))
	screen.blit(recovered_text, (0, 90))

def draw_start_button():
	surface_size = [150,30]
	button_surface = pygame.Surface(surface_size)
	button_rect = button_surface.get_rect(x=450, y=260)
	button_surface.fill(black)
	screen.blit(button_surface, button_rect)
	font = pygame.font.SysFont(None, 35)
	start_text = font.render(" Start", True, white)
	screen.blit(start_text, (455,265))
	return(surface_size, button_rect)

surface_size, button_rect = draw_start_button()
Initial_screen = True
pygame.display.flip()
i=0
while Initial_screen : 
	# quit events
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			Initial_screen = False
			pygame.quit()
			break
		elif event.type == MOUSEBUTTONDOWN :
			position = pygame.mouse.get_pos()
			if button_rect[0] <= position[0] <= button_rect[0]+surface_size[0] and button_rect[1] <= position[1] <= button_rect[1]+surface_size[1] :
				Initial_screen = False

# Create people (at least 1 is already ill)
# Get_infected is used either to infect someone or to check if they are infected
create_people(total_screen_size[0], total_screen_size[1], people_group, test_collide_group).get_infected()
infected_count+=1
for i in range(population_size-1):
	if random.randint(0,100) <= initial_infection_probability:
		create_people(total_screen_size[0], total_screen_size[1], people_group, test_collide_group).get_infected()
		infected_count+=1

	else :
		create_people(total_screen_size[0], total_screen_size[1], people_group, test_collide_group)
		healthy_count +=1

# Initial list values
list_infected.append(infected_count)
list_healthy.append(healthy_count)
list_dead.append(death_count)
list_recovered.append(recovered_count)
ii = True

# Gaming loop
while running : 
	if ii :
		ii = False
		print('start')
	delta_time = clock.tick(30)
	time_in_game += delta_time
	last_data_collect+=delta_time
	last_display+=delta_time

	# quit events
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			running = False
			break

	if not displaying :
		# Actualize list of sprites and screen
		population = pygame.sprite.Group.sprites(people_group)
		screen.fill(white)
		
		# Append values to list every 0.5 second
		if last_data_collect>=500 :
			list_infected.append(infected_count)
			list_healthy.append(healthy_count)
			list_dead.append(death_count)
			list_recovered.append(recovered_count)

		# Tests for each sprite 
		for people in population :
			if people.infected :
				# Count time infected
				people.infected_time += delta_time

				# After a time (that is different for every people)
				if standard_time_before_death + people.side_time < people.infected_time and not people.lucky :
					hasard = random.randint(0,100)
					# If the person is unlucky, it dies
					if hasard <= probability_to_die :
						people.infected=False
						people.dead = True
						people.lucky = False
						people.surface.fill(black)
						# the people wont move anymore
						infected_count-=1
						death_count+=1
						people.draw(screen)
						continue

					# the people has one (unique) chance to die
					else :
						people.lucky = True

				# The person recovers
				elif  people.side_time + standard_infection_duration < people.infected_time and not people.recovered and not people.dead: 
					# he is no longer infected and changes color
					people.infected=False
					people.recovered = True
					people.surface.fill(blue)

					infected_count-=1
					recovered_count+=1

				# The people is still infectious
				else :
					# Test if the sprite collides with another sprite (not himself)
					test_collide_group.remove(people)
					collide_list = pygame.sprite.spritecollide(people, test_collide_group, False)
					if len(collide_list) != 0 :
						for collided in collide_list :
							# The person has a chance to not get infected
							if contact_infection_probability>=random.randint(1,100):
							# Test if the other is healthy
								if collided.get_infected() : 
									infected_count +=1
									healthy_count-=1

			people.move(delta_time, total_screen_size)
			people.draw(screen)
		# Reset the group for the next loop
		pygame.sprite.Group.empty(test_collide_group)
		test_collide_group = people_group.copy()

		# Actualize counts and screen
		display_counts(infected_count, healthy_count, recovered_count, death_count)
		pygame.display.flip()

		# When the epidemic is over, the graph are displayed
		if infected_count ==0 and time_in_game>10000:
			# The data is collected for the last values
			list_infected.append(infected_count)
			list_healthy.append(healthy_count)
			list_dead.append(death_count)
			list_recovered.append(recovered_count)

			raw_data, canvas = graphic_display(time_in_game, list_infected, list_healthy, list_dead, list_recovered)
			size = canvas.get_width_height()
			image_of_graphic = pygame.image.fromstring(raw_data, size, "RGB")
			last_display = 0
			screen.blit(image_of_graphic, (250,0))
			pygame.display.flip()

			plt.close('all')
			displaying = True

pygame.display.flip()
pygame.quit()