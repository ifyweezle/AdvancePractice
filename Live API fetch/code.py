# Importing necessary modules and libraries
import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder

# Free API endpoint to get information about astronauts on the ISS
astros_url = "http://api.open-notify.org/astros.json"

# Fetching astronaut data from the API
astros_response = urllib.request.urlopen(astros_url)
astros_result = json.loads(astros_response.read())

# Creating and writing astronaut information to a text file
with open("iss_astronauts.txt", "w") as file:
    file.write("There are currently " +
               str(astros_result["number"]) + " astronauts on the ISS: \n\n")
    astronauts = astros_result["people"]
    for astronaut in astronauts:
        file.write(f"{astronaut['name']} - on board\n")

    # Retrieving the user's current latitude and longitude using geocoder
    user_location = geocoder.ip('me')
    file.write("\nYour current lat / long is: " + str(user_location.latlng))

# Opening the text file in the default web browser
webbrowser.open("iss_astronauts.txt")

# Setting up the world map in the turtle module
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)

# Loading the world map image and ISS icon
screen.bgpic("map.gif")
screen.register_shape("iss.gif")

# Creating a turtle for the ISS icon
iss_turtle = turtle.Turtle()
iss_turtle.shape("iss.gif")
iss_turtle.setheading(45)
iss_turtle.penup()

# Real-time tracking of the ISS location on the world map
while True:
    # Fetching the current location of the ISS
    iss_location_url = "http://api.open-notify.org/iss-now.json"
    iss_location_response = urllib.request.urlopen(iss_location_url)
    iss_location_result = json.loads(iss_location_response.read())

    # Extracting latitude and longitude from the ISS location data
    iss_latitude = float(iss_location_result["iss_position"]['latitude'])
    iss_longitude = float(iss_location_result["iss_position"]['longitude'])

    # Outputting ISS coordinates to the console
    print("\nLatitude: " + str(iss_latitude))
    print("Longitude: " + str(iss_longitude))

    # Updating the ISS location on the world map
    iss_turtle.goto(iss_longitude, iss_latitude)

    # Refreshing the location every 5 seconds
    time.sleep(5)
