import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#import scipy
import math
import pygame
from astropy import constants, units
import copy

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DEFAULTSCALE = 39 #pixels per AU

pygame.init()
font = pygame.font.Font(None, 32)
#L_sun solar luminosity
#pygame.image.load('bg.jpg') loads image to background

def planetSim():
	class CelestialBody(object):
		TIMESTEP =  3600*24 #the game will be sped up by this number (1 day per second)
		def __init__(self, displayRadius, color, m, actualRadius):
			self.d = 0*units.m #distance from sun to sun = 0
			self.scale = DEFAULTSCALE
			self.x = 0 * units.m #x position; only changes with camera movement and orbits
			self.y = HEIGHT/2 * constants.au / self.scale # y position
			self.displayRadius = displayRadius
			self.actualRadius = actualRadius.to(units.m)
			self.color = color
			self.m = m
			self.x_vel = 0
			self.y_vel = 0
			self.distance_to_sun = 0
			self.radiusToScale = False
			self.r = displayRadius
		
		def draw(self):
			x = (self.x * self.scale/constants.au).value
			y = (self.y * self.scale/constants.au).value
			if self.radiusToScale:
				r = (self.actualRadius * self.scale/constants.au).value
			else:
				r = self.r
			pygame.draw.circle(screenPlanets, self.color, (x, y), r)

		def toggleRadius(self): #toggle the radii to scale or to display
			self.radiusToScale = not self.radiusToScale

		def increaseScale(self):
			planetScale = self.scale * 1.1 #1.1 is an arbitrary increase of the scale
			if planetScale < 20000000:
				self.scale = planetScale

		def decreaseScale(self):
			planetScale = self.scale / 1.1
			if planetScale > 0.5:
				self.scale = planetScale

		def increaseRadius(self):
			planetR = self.r * 1.1
			if planetR < HEIGHT/4:
				self.r = planetR

		def decreaseRadius(self):
			planetR = self.r / 1.1
			if planetR >= 1:
				self.r = planetR

		def centralize(self):
			self.x = self.d.copy()
			self.y = HEIGHT/2 * constants.au / self.scale

		def toRight(self):
			self.x -= 50*constants.au/self.scale

		def toLeft(self):
			self.x += 50*constants.au/self.scale
		
		def toUp(self):
			self.y += 50*constants.au/self.scale
		
		def toDown(self):
			self.y -= 50*constants.au/self.scale

	class Planet(CelestialBody):
		def __init__(self, d, displayRadius, color, m, actualRadius):
			CelestialBody.__init__(self, displayRadius, color, m, actualRadius)
			self.d = d.to(units.m) #distance from the sun; doesn't change with camera movement
			self.x = self.d.copy()

		def calcForceGravity(self, otherCelestialBody):
			d_x = otherCelestialBody.x - self.x #distance between two bodies in m; negative distances will be squared
			d_y = otherCelestialBody.y -self.y
			d = math.sqrt(d_x**2 + d_y**2)
			if otherCelestialBody.d == 0: #if otherCelestialBody is the sun
				self.d = d

			f = constants.G * self.m * otherCelestialBody.m / d**2
			theta = math.atan2(d_y, d_x)
			f_x = f * math.cos(theta)
			f_y = f * math.sin(theta)
			return f_x, f_y

		def updatePosition(self, planets):
			pass


	run = True
	clock = pygame.time.Clock() #otherwise, the game runs at the speed of the processor
	WIDTH, HEIGHT = 1300, 500
	screenPlanets = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Planet simulation")
	sun = CelestialBody(30, YELLOW, constants.M_sun, constants.R_sun)
	mercury = Planet(57.9e9*units.m, 1, (100,100,100), 0.33e4*units.kg, 4879/2*units.km)
	venus = Planet(108.2e9*units.m, 3, YELLOW, 4.87e4*units.kg, 12104/2*units.km)
	earth = Planet((1*units.au).to(units.m), 3, BLUE, constants.M_earth, constants.R_earth)
	mars = Planet(228e9*units.m, 2, RED, 0.642e24*units.kg,6792/2*units.km)
	jupiter = Planet(778.5e9*units.m, 35, (120,40, 0), constants.M_jup, constants.R_jup)
	saturn = Planet(1432e9*units.m, 30, (255,255,102), 568e24*units.kg, 120536/2*units.km)
	uranus = Planet(2867e9*units.m, 14, (0, 120, 125), 86.8e24*units.kg, 51118/2*units.km)
	neptune = Planet(4515e9*units.m, 13, BLUE, 102e24*units.kg, 49528/2*units.km)
	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				'''
				if event.key == pygame.K_j:
					centralizeOnPlanet(earth, planets)'''
				for planet in planets:
					if event.key == pygame.K_z:
						planet.toggleRadius()
					if event.key == pygame.K_c:
						for planet in planets:
							planet.centralize()

		
		userInput = pygame.key.get_pressed()
		for planet in planets:
			if userInput[pygame.K_KP_PLUS]:
				planet.increaseScale()
			
			elif userInput[pygame.K_KP_MINUS]:
				planet.decreaseScale()
			
			if userInput[pygame.K_RIGHT]:
				planet.toRight()
			
			elif userInput[pygame.K_LEFT]:
				planet.toLeft()
			
			if userInput[pygame.K_UP]:
				planet.toUp()
			
			elif userInput[pygame.K_DOWN]:
				planet.toDown()
			
			if userInput[pygame.K_r]:
				planet.increaseRadius()
			
			elif userInput[pygame.K_e]:
				planet.decreaseRadius()

			'''
		if userInput[pygame.K_UP]:
			changeScale(planets, 1.1)
		elif userInput[pygame.K_DOWN]:
			changeScale(planets, 1/1.1)'''
		screenPlanets.fill((0, 0, 0))
		for planet in planets:
			planet.draw()
		auPerPixel = round(((1*units.au).to(units.m)/planets[0].scale).value, 2) #How many aus a pixel represents
		scaleTxt = font.render("Scale: 1 pixel =  {:e}m".format(auPerPixel), True, (255,255,255))
		screenPlanets.blit(scaleTxt, (10, HEIGHT - 30))
		if planets[0].radiusToScale:
			radiiToScaleStr = "Radii and distances to scale."
		else:
			radiiToScaleStr = "Radii not to scale, but distances to scale."
		screenPlanets.blit(font.render(radiiToScaleStr, True, (255,255,255)), (10, HEIGHT - 60))
		pygame.display.flip()
	pygame.quit()

#print(constants.G.value)
#print(constants.au)
planetSim()
#print(constants.M_sun)