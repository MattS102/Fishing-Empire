# Import Random (for testing)
import random
import pygame
import os

#src path
ImgPath = 'C:\\Users\\owenc\\Documents\\GitHub\\tufts_project\\src\\img'
# Define Main function
def main():
	#load images 
	cod = pygame.image.load(os.path.join(ImgPath,'cod.png'))
	mb = pygame.image.load(os.path.join(ImgPath,'_MB_.png'))
	bass = pygame.image.load(os.path.join(ImgPath,'bass.png'))
	salmon =  pygame.image.load(os.path.join(ImgPath,'salmon.png'))
	trout =  pygame.image.load(os.path.join(ImgPath,'trout.png'))
	tuna =  pygame.image.load(os.path.join(ImgPath,'tuna.png'))
	wincon =  pygame.image.load(os.path.join(ImgPath,'Wincon.png'))

	aa = pygame.image.load(os.path.join(ImgPath,'aquatic_abuductor.png'))
	ch =  pygame.image.load(os.path.join(ImgPath,'captain_hooker.png'))
	ss =  pygame.image.load(os.path.join(ImgPath,'salmon_slayer.png'))
	tt =  pygame.image.load(os.path.join(ImgPath,'trout_terminator.png'))

	dock =  pygame.image.load(os.path.join(ImgPath,'dock.gif'))#GIF will not be animated TODO
	menu =  pygame.image.load(os.path.join(ImgPath,'menu.png'))
	player =  pygame.image.load(os.path.join(ImgPath,'player.png'))
	longBut =  pygame.image.load(os.path.join(ImgPath,'longbutton.png'))
	smallBut =  pygame.image.load(os.path.join(ImgPath,'smallbutton.png'))


	# initialize the pygame module
	pygame.init()
	# load and set the logo
	'''
	logo = pygame.image.load("logo32x32.png") TODO
	pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")
	'''
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((240,180))

	# define a variable to control the main loop
	running = True
	# main loop
	while running:
		# event handling, gets all event from the event queue
		for event in pygame.event.get():
		# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
	# Set up starting variables
	mainRod = "Fish Stick"
	mainPowerUp = ""
	totalPoints = 0
	usableItems = []

	# Variable to check how many uses the user has for their power up
	powerUpCounter = 0

	# Set up a list/dictioanry for the fishes, fishing rods, and power ups (Point values may change).
	fishesList = ["Cod", "Bass", "Trout", "Salmon", "Tuna"]
	fishingRodDic = {"Captain Hooker" : 50, "The Salmon Slayer" : 150, "The Trout Terminator" : 400, "The Aquatic Abductor" : 1000}
	powerUpsDic = {"Slow-Time" : 50, "1 in a Million" : 80, "Double Down" : 100}

	# Set up a list of all the fishing rod and power up options
	var1 = fishingRodDic.keys()
	var2 = powerUpsDic.keys()
	fishingRods = []
	powerUps = []

	for char in var1:
		fishingRods.append(char)

	for i in var2:
		powerUps.append(i)

	welcome_message()

	# Use a while loop to check if the user wants to throw the fishing line
	while (input("Throwing Fishing Line: ") == "y"):

		# Check if the user has any current power ups being used
		if (powerUpCounter > 0):
			powerUpCounter -= 1
			print("You have " + str(powerUpCounter) + " uses for your power up left.")

		# Get a random number between 0 and 4 (This will be changed so it is weighted by rarity)
		fishType = fishesList[random.randint(0,4)]

		# Call the function to calculate how many points the user should have
		totalPoints = get_points(fishType, totalPoints)

		print()
		# Ask the user what thy would like to do (3 options)
		userChoice = input("What would you like to do: \n1. Show Shop\n2. Show Inventory\n3. Throw Fishing Line\n")

		# Check if the answer is 1, 2 or 3
		if (userChoice == "1"):
			# Call 2 functions to shop the shop and prompt the user to buy an item
			show_shop(fishingRods, powerUps)
			totalPoints, usableItems = get_items(totalPoints, fishingRods, powerUps, usableItems, fishingRodDic, powerUpsDic)

		elif (userChoice == "2"):
			# Show the user their inventory and use any items in it (if possible)
			usableItems, mainRod, mainPowerUp, powerUpCounter = show_inventory(fishingRods, powerUps, totalPoints, mainRod, usableItems, mainPowerUp, powerUpCounter)

		elif (userChoice != "3"):
			# Tell the user their input was not an option
			print("That is not an option.")

		# Tell the user their current rod, power up, and total points (FOR TESTING PURPOSES)
		print()
		print ("Main Rod: " + mainRod)
		print("Main Power Up: " + mainPowerUp)
		print("Total Points: " + str(totalPoints))

		print()

def welcome_message():
	print("Welcome to FISHING EMPIRE!")
	print("\n")
	print("Fishing Empire is a game all about FISH! The aim of the game is to\n\ncatch the rarest and most valuable fish that you can, and then using\n\nthem to buy upgrades. It won’t be easy though: each cast of your rod is\n\nfollowed by a tricky reaction-based challenge in order to secure\n\nthe fish.")
	print("\n")
	print("You will start with a level 1 fishing rod called Fish Stick, but, as\n\nyou progress, the shop will offer better rods and some cool power-ups! ")
	print("\n")
	print("Good Luck!")
	print("\n")

# Define a function which shows the user the fishing shop
def show_shop(fishingRods, powerUps):

	print("--------------")
	print("FISHING SHOP")
	print("--------------")


	# Print all of the available fishing rods
	print("FISHING RODS")
	for i in range (1, len(fishingRods) + 1):
		print(str(i) + ". " + fishingRods[i-1])

	print()
	print()

	# Print all of the available power ups
	print("POWER-UPS")
	for i in range (1, len(powerUps) + 1):
		print(str(i) + ". " + powerUps[i-1])

	print()

# Define a function which lets the user buy an item from the chop
def get_items(totalPoints, fishingRods, powerUps, usableItems, fishingRodDic, powerUpsDic):
	
	# Ask the user what they would like to buy
	userItem = input("What would you like to buy today? ")

	# Check if the item is a fishing rod in the shop
	# Check if the item is not already owned by the user
	if (userItem in fishingRods):	
		if (userItem not in usableItems):

			# Get the cost of the item
			cost = fishingRodDic[userItem]

			# Check if the user has enough points to buy the item
			# Take away the cost from totalPoints and add the item to usable items.
			if (totalPoints >= cost):
				totalPoints -= cost
				usableItems.append(userItem)
				print("You have bought " + userItem)

			else:
				# Tell the user they don't have enough points
				print("You don't have enough points")
		else:
			# Tell the user they already have the item
			print("You already have this item.")

	# Check if the item is a power up in the shop
	# Check if the item is not already owned by the user
	elif (userItem in powerUps):
		if (userItem not in usableItems):

			# Get the cost of the item
			cost = powerUpsDic[userItem]

			# Check if the user has enough points to buy the item
			# Take away the cost from totalPoints and add the item to usable items
			if (totalPoints >= cost):
				totalPoints -= cost
				usableItems.append(userItem)

			else:
				# Tell the user they don't have enough points
				print("You don't have enough points")

		else:
			# Tell the user they already have the item
			print("You already have this item.")

	else:
		# Tell the user that the item is not in the store
		print("That item is not in the store.")

	# Return the user's total points and usable items
	return totalPoints, usableItems

# Define a function to calculate how many points the user should have
def get_points(fishType, totalPoints):

	# Create a dictionary which contains each type of fish and their point value
	fishDic = {"Cod" : 100, "Bass" : 300, "Trout" : 800, "Salmon" : 1500, "Tuna" : 3000, "DHpupfish" : 100000}

	# Add the fish's point value to the user's total points
	totalPoints += fishDic[fishType]

	# Return the total points
	return totalPoints

#Define a function which shows the user their inventroy and lets them use an item (if possible)
def show_inventory(fishingRods, powerUps, totalPoints, mainRod, usableItems, mainPowerUp, powerUpCounter):

	# Print the total points
	# Print the user's fishing rods and power ups (if they have them)
	print()
	print("Total Points: " + str(totalPoints))

	print()

	print("Fishing Rods and Power Ups: ")

	if (len(usableItems) != 0):

		for i in range (1, len(usableItems) + 1):
			print(str(i) + ". " + usableItems[i-1])
		usableItems, mainRod, mainPowerUp, powerUpCounter = use_item(fishingRods, powerUps, totalPoints, mainRod, usableItems, mainPowerUp, powerUpCounter)
	else:
		print("You have no fishing rods or power ups to use.\n")

	return usableItems, mainRod, mainPowerUp, powerUpCounter

def use_item(fishingRods, powerUps, totalPoints, mainRod, usableItems, mainPowerUp, powerUpCounter):

	# Ask if they would like to use a fishing rod or neither
	userInput = input("Would you like to use a fishing rod or power up? (Enter fishing rod, power up, or no) ")
		
	# Check if the user typed fishing rod, power up, or no
	if (userInput == "fishing rod"):
		# Ask the user what rod they want to use
		userRod = input("What rod would you like to use? ")

		# Check if the user owns the rod and set it to their main rod if True
		if (userRod in usableItems):
			mainRod = userRod
			print(userRod + " is your main rod now.")
		else:
			print("You can not use that rod.")

	elif (userInput == "power up"):
		# Ask the user what power up they want to use
		userPowerUp = input("What power up would you like to use? ")

		# Check if the user owns the power up and set it to their main power up
		# Delete the item from usableItems
		# Set the powerUpCounter to 10
		if (userPowerUp in usableItems):
			mainPowerUp = userPowerUp
			del usableItems[usableItems.index(userPowerUp)]
			powerUpCounter = 10
			print(userPowerUp + " is your power up now. You have 10 uses.")
		else:
			print("You do not own that power up.")

	# Return the user's usable items, main rod/powerup, and the powerUpCounter
	return usableItems, mainRod, mainPowerUp, powerUpCounter

# Call main
main()
