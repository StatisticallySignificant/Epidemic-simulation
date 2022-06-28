import pygame, random
from pygame.locals import * 
# People inherites from sprites
class People(pygame.sprite.Sprite):
	def __init__(self, people_group, test_collide_group, coordinate, dimensions):
		pygame.sprite.Sprite.__init__(self, [people_group])
		pygame.sprite.Group.add(test_collide_group, self)

		# Give a direction that is high enough
		self.direction = [random.randint(-100,100)/100, random.randint(-100,100)/100]
		if -0.3<self.direction[0]<=0.3 and -0.3<self.direction[1]<=0.3:
			self.direction[0]=0.8
			self.direction[1]=0.9

		self.x, self.y = coordinate
		self.dimensions = dimensions

		self.surface = pygame.Surface(self.dimensions)
		self.rect = self.surface.get_rect(x=self.x, y=self.y)
		self.surface.fill((0,255,0))

		# Most people are healthy
		self.infected = False
		self.recovered = False
		self.dead = False
		if random.random() <= 0.1:
			self.get_infected()
		#self.infected = random.choices([True, False],[1,20]) (another way to do it)


	def get_infected(self):
		infection_probability = random.randint(1,100)
		# It can infect someone who is already ill or recovered or dead 
		# The person has 20% chance to not get ill
		if self.infected or self.recovered or self.dead or infection_probability<=20:
			return False

		self.infected_time = 0
		self.surface.fill((255,0,0))
		self.infected = True
		return True
	
	def draw(self,screen):
		screen.blit(self.surface, self.rect)

	def move(self, speed, delta_time, screen_size):
		if self.dimensions[1]<self.rect[1]+self.dimensions[1]<screen_size[1] and self.dimensions[0]<self.rect[0]+self.dimensions[0]<screen_size[0] :
			pass
		# Stay on the screen 
		# Top
		elif 0>=self.rect[1]:
			self.direction[1] = random.randint(1,100)/100
		# Left
		elif 0>=self.rect[0]:
			self.direction[0] = random.randint(1,100)/100
		# Botom
		elif self.rect[1]+self.dimensions[1]>=screen_size[1]:
			self.direction[1] = random.randint(-100,-1)/100
		# Right
		elif self.rect[0]+self.dimensions[0]>=screen_size[0]:
			self.direction[0] = random.randint(-100,-1)/100
		self.rect.move_ip(self.direction[0] * speed * delta_time,  self.direction[1] * speed * delta_time)

def create_people(screen_width, screen_lengh, people_group, test_collide_group, dimensions):
	coordinate = (random.randint(0, screen_width-dimensions[0]), random.randint(0, screen_lengh-dimensions[1]))
	return People(people_group, test_collide_group, coordinate, dimensions)