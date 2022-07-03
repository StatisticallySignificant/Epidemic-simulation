import pygame, random
from pygame.locals import * 

# People inherites from sprites
class People(pygame.sprite.Sprite):
	def __init__(self, people_group, test_collide_group, coordinate, dimensions):
		pygame.sprite.Sprite.__init__(self, [people_group])
		pygame.sprite.Group.add(test_collide_group, self)

		# People's parameters
		# Give a direction that is high enough
		self.direction = [random.randint(-100,100)/100, random.randint(-100,100)/100]
		if -0.3<self.direction[0]<=0.3 and -0.3<self.direction[1]<=0.3:
			self.direction[0]=0.8
			self.direction[1]=0.9
		self.x, self.y = coordinate
		self.dimensions = dimensions
		self.speed = 0.1
		
		self.surface = pygame.Surface(self.dimensions)
		self.rect = self.surface.get_rect(x=self.x, y=self.y)
		self.surface.fill((0,255,0))

		# Most people are healthy
		self.infected = False
		self.recovered = False
		self.dead = False
		self.lucky = False
		self.side_time = random.randint(-100,100)*15

	# Get_infected is used either to infect someone or to check if they are infected
	def get_infected(self):
		# It can't infect someone who is already ill or recovered or dead 
		if self.infected or self.recovered or self.dead :
			return False
		# It is the beginning of the infection and its color changes
		self.infected_time = 0
		self.surface.fill((255,0,0))
		self.infected = True
		return True
	
	# Draw people on screen
	def draw(self,screen):
		screen.blit(self.surface, self.rect)

	# Move people unless it is dead
	def move(self, delta_time, screen_size):
		if self.dead :
			self.direction =(0,0)
		# If it's coordinate are on the screen, they don't need to change
		if max(self.dimensions[1],120)<self.rect[1]+self.dimensions[1]<screen_size[1] and max(self.dimensions[0],160)<self.rect[0]+self.dimensions[0]<screen_size[0] :
			pass

		# Stay on the screen 
		# Top left corner
		elif self.rect[0]<=160 and self.rect[1]<=120:
			self.direction[0] = random.randint(1,100)/100
			self.direction[1] = random.randint(1,100)/100
		# Top
		elif self.rect[1]<=0:
			self.direction[1] = random.randint(1,100)/100
		# Left 
		elif self.rect[0]<=0:
			self.direction[0] = random.randint(1,100)/100
		# Botom
		elif self.rect[1]+self.dimensions[1]>=screen_size[1]:
			self.direction[1] = random.randint(-100,-1)/100
		# Right
		elif self.rect[0]+self.dimensions[0]>=screen_size[0]:
			self.direction[0] = random.randint(-100,-1)/100
		self.rect.move_ip(self.direction[0] * self.speed * delta_time,  self.direction[1] * self.speed * delta_time)

def create_people(screen_width, screen_lengh, people_group, test_collide_group):
	people_dimensions = (10,10)
	coordinate = (random.randint(0, screen_width-people_dimensions[0]), random.randint(0, screen_lengh-people_dimensions[1]))
	return People(people_group, test_collide_group, coordinate, people_dimensions)