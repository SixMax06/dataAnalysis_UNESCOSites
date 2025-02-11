# -*- coding: utf-8 -*-
"""datasetUNESCO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WghANynHFejoJIftp8GaSmyI9MOyMfRG

[Kaggle Source Dataset](https://www.kaggle.com/datasets/rishabhbhartiya/unesco-world-heritage-updated-2024) / [Github Repository](https://github.com/SixMax06/progettoTPI_analisiDati_UNESCOSites)

[MathPlot Documentation](https://matplotlib.org/) / [Folium Documentation](https://python-visualization.github.io/folium/latest/)

Libraries downloading

(run this if you're not using Colab)
"""

!pip install matplotlib
!pip install folium
!pip install requests

"""**WARNING**

The following code works only with the dataset in the repository linked above and will not work with any other dataset

Feel free to use this code as inspiration for your own work :)

---

Dataset import from Github repository

(Run this before running the other cells, otherwise they won't work)
"""

import requests

#function to download a .json dataset given a url as a parameter
def download_dataset(url):
  try:
    response = requests.get(url)
    response.raise_for_status()

  except requests.exceptions.HTTPError as err:
    print(err)
    return None

  data = response.json()
  print("Dataset imported correctly")
  return data

#dataset import inside two variables (dictionaries)
UNESCO_dataset_url = "https://raw.githubusercontent.com/SixMax06/progettoTPI_analisiDati_UNESCOSites/refs/heads/main/datasets/UNESCO_WORLD_HERITAGE.json"
data = download_dataset(UNESCO_dataset_url)

StatesLocation_dataset_url = "https://raw.githubusercontent.com/SixMax06/dataAnalysis_UNESCOSites/refs/heads/main/datasets/COUNTRIES_LATLONG.json"
StatesLocation = download_dataset(StatesLocation_dataset_url)

"""Data Analysis"""

#general information about the dataset

oldest, newest, Lrank, Hrank, Lrating, Hrating = 2025, 0, 2000, 0, 5, 0   #initializing all variables needed

#search for the values
for site in data:
  if site["Nomination Year"] > newest:
    newest = site["Nomination Year"]
  if site["Nomination Year"] < oldest:
    oldest = site["Nomination Year"]

  if site["Rank"] > Hrank:
    Hrank = site["Rank"]
  if site["Rank"] < Lrank:
    Lrank = site["Rank"]

  if site["Rating"] > Hrating:
    Hrating = site["Rating"]
  if site["Rating"] < Lrating:
    Lrating = site["Rating"]


#putting the sites needed into lists
list_oldest, list_newest, list_Lrank, list_Hrank, list_Lrating, list_Hrating = [], [], [], [], [], []   #lists initialization

#filling the lists
for site in data:
  if site["Nomination Year"] == oldest:
    list_oldest.append(site["Site Name"])
  if site["Nomination Year"] == newest:
    list_newest.append(site["Site Name"])

  if site["Rank"] == Lrank:
    list_Lrank.append(site["Site Name"])
  if site["Rank"] == Hrank:
    list_Hrank.append(site["Site Name"])

  if site["Rating"] == Lrating:
    list_Lrating.append(site["Site Name"])
  if site["Rating"] == Hrating:
    list_Hrating.append(site["Site Name"])

#printing information on screen

print(f'Number of sites: {len(data)}\n')    #printing sites number

print(f'Oldest site(s) ({oldest}): {list_oldest}')     #printing oldest site(s)
print(f'Newest site(s) ({newest}): {list_newest}\n')   #printing newest site(s)

print(f'Lowest rank ({Lrank}): {list_Lrank}')         #printing lowest ranked site
print(f'Highest rank ({Hrank}): {list_Hrank}\n')      #printing highest ranked site

print(f'Lowest rating ({Lrating}): {list_Lrating}')     #printing lowest rated site
print(f'Highest rating ({Hrating}): {list_Hrating}\n')  #printing highest rated site

#site search with state

#user inputs the state name
state = input("Insert state name: ")
found = False

#search for needed site: if found prints info, else prints an error message
for site in data:
  if site["Country"] == state:
    print(f'Site No.{site["ID"] + 1} : "{site["Site Name"]}", nominated in {site["Nomination Year"]}, ranked {site["Rank"]} in the world and rated a {site["Rating"]} out of 5')
    found = True

if not found:
  print("ERROR: Site not found")

#site search with nomination year

#user inputs the nomination year
year = int(input("Insert year: "))
found = False

#search for needed site: if found prints info, else prints an error message
for site in data:
  if site["Nomination Year"] == year:
    print(f'Site No.{site["ID"] + 1} : "{site["Site Name"]}" located in {site["Country"]}, ranked {site["Rank"]}^ in the world and rated a {site["Rating"]} out of 5')
    found = True

if not found:
  print("ERROR: Site not found")

#site search with name

#user inputs the name of the site
name = input("Insert site name: ")
found = False

#search for needed site: if found prints info, else prints an error message
for site in data:
  if site["Site Name"] == name:
    print(f'Site No.{site["ID"] + 1} : Located in {site["Country"]}, nominated in {site["Nomination Year"]}, ranked {site["Rank"]}^ in the world and rated a {site["Rating"]} out of 5')
    found = True

if not found:
  print("ERROR: Site not found")

#site search with rank

#user inputs the rank
rank = int(input("Insert rank: "))
found = False

#search for needed site: if found prints info, else prints an error message
for site in data:
  if site["Rank"] == rank:
    print(f'Site No.{site["ID"] + 1} : "{site["Site Name"]}" located in {site["Country"]}, nominated in {site["Nomination Year"]} and rated a {site["Rating"]} out of 5')
    found = True

if not found:
  print("ERROR: Site not found")

#site search with rating range (from 0 to 5)

#user inputs the rating range
Rmin, Rmax = float(input("Insert minimun rank: ")), float(input("Insert maximun rank: "))
found = False

#search for needed site: if found prints info, else prints an error message
for site in data:
  if Rmin <= site["Rating"] <= Rmax:
    print(f'Site No.{site["ID"] + 1} : "{site["Site Name"]}" located in {site["Country"]}, nominated in {site["Nomination Year"]} and ranked {site["Rank"]}^ in the world')
    found = True

if not found:
  print("ERROR: Site not found")

"""Data Analysis with Graphs and Maps"""

#graph representing sites based on rating (range)

#imporing graph library
import matplotlib.pyplot as plt

counts = [0 for i in range(0, 5)]   #initializing counting list

#filing counting list
for site in data:
  rating = site["Rating"]
  counts[int(rating)] += 1

lables = [(str(i) + " - " + str(i + 0.99)) for i in range(0,5)]   #labels initialization

#graph initialization
fig, ax = plt.subplots()
ax.bar(lables, counts)
ax.bar_label(ax.containers[0])

#graph lables declaration
plt.xlabel("Rating")
plt.ylabel("Number of sites")
plt.title("Sites based on rating")

#graph print
plt.show()

#graph representing sites based on nomination year (range)

#imporing graph library
import matplotlib.pyplot as plt

#initializing counting list and lables
lables_old = [i//5 for i in range(1975, 2025, 5)]
counts = [0 for i in range(0, 10)]

#filling counting list
for site in data:
  year = site["Nomination Year"]
  i = lables_old.index(year//5)
  counts[i] += 1

lables = [(str(i) + " - " + str(i + 4)) for i in range(1975, 2025, 5)]   #labels correction (for printing)

#graph initialization
fig, ax = plt.subplots()
ax.barh(lables, counts)
ax.bar_label(ax.containers[0])

#graph lables declaration
plt.ylabel("Nomination year")
plt.xlabel("Number of sites")
plt.title("Sites based on nomination year")

#graph print
plt.show()

#graph rapresenting states based on number of sites in them (top 10)

#imporing graph library
import matplotlib.pyplot as plt

top_range = 10  #change this variable to set the leaderboard range

states_list = []   #initializing list of countries

#filling countries list
for site in data:
  if site["Country"] not in states_list:
    states_list.append(site["Country"])

counts = [0 for i in range(0, len(states_list))]   #initializing counting list

#filling counting list
for site in data:
  counts[states_list.index(site["Country"])] += 1

#sorting countries by number of sites
states_counts = list(zip(counts, states_list))
states_counts.sort(reverse=True)

#picking only the "top_range" of the lists
top_states = [state[1] for state in states_counts[:top_range]]
top_counts = [state[0] for state in states_counts[:top_range]]

#graph initialization
fig, ax = plt.subplots()
ax.barh(top_states, top_counts)
ax.invert_yaxis()
ax.bar_label(ax.containers[0])

#graph lables declaration
plt.ylabel("State")
plt.xlabel("Number of sites")
plt.title(f"Top {top_range} states with most sites")

#graph print
plt.show()

#map that rappresents all states that have UNESCO sites (with the number of them)

#importing map library
import folium as fl

#importing random library
import random as rnd

#function to search countries names between the two datasets
def search_state_location(name):
  location = []
  for state in StatesLocation:
    if state["name"] == name:
      location = [state["latitude"], state["longitude"]]
      break
  return location

states_list = []    #countries list initialization

#filling countries list
for site in data:
  if site["Country"] not in states_list:
    states_list.append(site["Country"])

counts = [0 for i in range(0, len(states_list))]    #counting list intialization

#filling counting list
for site in data:
  counts[states_list.index(site["Country"])] += 1

states_counts = list(zip(states_list, counts))

#map and marker feature group decloaration
map = fl.Map([0.0, 0.0], zoom_start = 2)
marker_group = fl.FeatureGroup(name = "States Markers").add_to(map)

#color list declaration
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

#markers declaration and adding in the map
for state in states_counts:
  location = search_state_location(state[0])

  if location != []:    #declares the marker only if it finds the location in the other dataset (it also gives it a random color from the "colors" list)
    popup = fl.Popup(f"{state[0]} - {state[1]} site(s)", parse_html=True, max_width=200)
    fl.Marker(location = location, popup = popup, icon = fl.Icon(color = colors[rnd.randint(0, len(colors) - 1)])).add_to(marker_group)

#adding layer control to map
fl.LayerControl().add_to(map)

#map print
map