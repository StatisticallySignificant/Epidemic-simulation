import pygame, random
from pygame.locals import *
from People import create_people
from matplot import *

pygame.init()
running = True

# Screen, size, title, background color
screen_size = [800,600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Epidemic is running")
screen.fill((255,255,255))

# Create 2 groups of sprites
people_group = pygame.sprite.Group()
test_collide_group = pygame.sprite.Group()

# Handle time
clock = pygame.time.Clock()
time_in_game, last_data_collect = 0,0

# People's attribute
people_speed = 0.1
people_dimensions = (10,10)

# Differents counters 
infected_count, healthy_count, recovered_count, death_count = 0,0,0,0
# List of the number of infected person at differents timings
list_infected_count = []

# Handle display of the number of infected and non infected people
def display_counts(infected_count, healthy_count, recovered_count, death_count):
	# Same font for every text
	font = pygame.font.SysFont(None, 35)
	healthy_text = font.render(" Sains "+str(healthy_count), True, (0,255,0))
	infected_text = font.render(" Malades "+str(infected_count), True, (255,0,0))
	dead_text = font.render(" Morts "+str(death_count), True, (0,0,0))
	recovered_text = font.render(" Guéris "+str(recovered_count), True, (0,0,255))
	screen.blit(healthy_text, (0,0))
	screen.blit(infected_text, (0,30))
	screen.blit(dead_text, (0,60))
	screen.blit(recovered_text, (0, 90))

# Create people (some are already ill)
for i in range(150):
	if create_people(screen_size[0], screen_size[1], people_group, test_collide_group, people_dimensions).infected:
		infected_count+=1
	else :
		healthy_count +=1
# Initial infected person 
list_infected_count.append(infected_count)

# Gaming loop
while running : 
	delta_time = clock.tick(30)
	time_in_game += delta_time
	last_data_collect+=delta_time
	for event in pygame.event.get():
		# quit events
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			running = False
			break
	# Actualize list of sprites
	population = pygame.sprite.Group.sprites(people_group)
	screen.fill((255,255,255))
	
	# Append a value to list
	if last_data_collect>=1000 :
		list_infected_count.append(infected_count)
		last_data_collect = 0

	# Tests for each sprite 
	for people in population :
		# If the person is sick
		if people.infected :
			# Count time infected
			people.infected_time += delta_time
			# After 4 secs, the person has one (unique) chance to die
			if 4000<people.infected_time and not people.lucky :
				hasard = random.randint(0,100)
				# If the person is unlucky, it dies
				if hasard <=3 :
					people.infected=False
					people.dead = True
					people.surface.fill((0,0,0))

					infected_count-=1
					death_count+=1
					
					# Note for later : maybe it should stop moving
					people.move(people_speed, delta_time, screen_size)
					people.draw(screen)
					continue
				# If the person is lucky, it can't die anymore
				else :
					people.lucky = True

			# After 6secs, the person can recover
			elif people.infected_time>6000 and not people.recovered and not people.dead: 
				# he is no longer infected and changes color
				people.infected=False
				people.recovered = True
				people.surface.fill((0,0,255))

				infected_count-=1
				recovered_count+=1

			# If it is still infectious
			else :
				# Test if the sprite collides with another sprite (not himself)
				test_collide_group.remove(people)
				collide_list = pygame.sprite.spritecollide(people, test_collide_group, False)
				if len(collide_list) != 0 :
					for collided in collide_list :
						# If the other is healthy (get_infect only works if it is the first time, and return True if so)
						if collided.get_infected() : 
							infected_count +=1
							healthy_count-=1

		people.move(people_speed, delta_time, screen_size)
		people.draw(screen)
	pygame.sprite.Group.empty(test_collide_group)
	test_collide_group = people_group.copy()
	# Actualize counts and screen
	display_counts(infected_count, healthy_count, recovered_count, death_count)
	pygame.display.flip()
	# Display graph at the end of the epidemic 
	if time_in_game>=10000 and infected_count==0 and running :
		graphic_display(time_in_game, list_infected_count)

pygame.quit()