import requests
import json
from lxml import etree
from pyquery import PyQuery as pq

def dining_links():
    dining_halls = {}
    res = requests.get("http://dining.uconn.edu/nutrition")
    doc = pq(res.content)
    links = doc('a')
    for item in links.items():
        if 'nutritionanalysis.dds.uconn.edu' in str(item.attr('href')):
            dining_halls[item.text()] = item.attr('href')
    return dining_halls

def dining_menu(link):
    dining_hall = {}
    time = None
    meals = []

    res = requests.get(link, timeout=15)
    doc = pq(res.content)

    divs = doc('div')
    divs.remove('script')
    for item in divs.items():
        if str(item.attr('class')) in 'shortmenumeals':
            if not time:
                time = item.text()
            else:
                meal_temp = meals
                dining_hall[time] = meal_temp
                meals = []
                time = item.text()
        elif str(item.attr('class')) in 'headlocation':
            dining_hall['name'] = item.text()
        elif str(item.attr('class')) in 'shortmenutitle':
            dining_hall['date'] = item.text()
        elif str(item.attr('class')) in 'shortmenurecipes':
            meals.append(item.text())

    meal_temp = meals
    dining_hall[time] = meal_temp

    return json.dumps(dining_hall)

def search_menu(link, items, meal_time=None):
    dining_hall = {}
    time = None
    meals = []

    res = requests.get(link, timeout=15)
    doc = pq(res.content)

    divs = doc('div')
    divs.remove('script')
    for item in divs.items():
        if str(item.attr('class')) in 'shortmenumeals':
            #print time in meal_time
            #print 'Time:',time,' meal_time: ',meal_time
            if not time:
                time = item.text()
            else:
                meal_temp = meals
                dining_hall[time] = meal_temp
                meals = []
                time = item.text()
        elif str(item.attr('class')) in 'headlocation':
            dining_hall['name'] = item.text()
        elif str(item.attr('class')) in 'shortmenutitle':
            dining_hall['date'] = item.text()
        elif str(item.attr('class')) in 'shortmenurecipes':
            for food in items:
                if food in str(item.text()):
                    meals.append(item.text())

        meal_temp = meals
        dining_hall[time] = meal_temp

    return json.dumps(dining_hall, indent=2, sort_keys=False)
