"""
MIT License

Copyright (c) 2020-present phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time

import discord
import redbot
from redbot.core import commands
import requests
import json
from bs4 import BeautifulSoup
import discord
import os
import urllib
import requests_html
import re
import math
import xml.etree.ElementTree as ET
import xmltodict

class equipment:
	head = ""
	Neck = ""
	Shoulders = ""
	Cloak = ""
	Chest = ""
	Shirt = ""
	Tabard = ""
	Bracer = ""
	Gloves = ""
	Belt = ""
	Legs = ""
	Boots = ""
	Ring_1 = ""
	Ring_2 = ""
	Trinket_1 = ""
	Trinket_2 = ""
	Main_hand = ""
	Off_hand = ""
	Ranged = ""


class item:
	itemID = ""
	name = ""
	ilvl = ""
	gs = ""
	gem_slots = 0
	gem_fit = 0
	ench_slots = 0
	ench_fit = 0
	int = 0
	stam = 0
	str = 0
	agi = 0
	spr = 0
	arpen = 0
	crit = 0
	haste = 0
	mp5 = 0
	sp = 0
	hit = 0
	bv = 0
	dodge = 0
	parry = 0
	block = 0
	exp = 0
	atk = 0


class character:
	name = ""
	realm = "Icecrown"
	online = False
	level = 1
	faction = "Neutral"
	gender = ""
	game_class = ""
	honorablekills = 0
	guild = ""
	achievementpoints = 0
	equipment = equipment()
	race = ""
	talents = ""
	professions = ""


rawr_attr_correlation = {"ItemLevel": "", "Armor": "Armor", "Stamina": "Stamina", "Intellect": "Intellect",
						 "Strength": "Strength",
						 "Agility": "Agility", "Spirit": "Spirit", "SpellPower": "spell power",
						 "CritRating": "critical strike rating",
						 'HasteRating': "haste", "ArmorPenetrationRating": "armor penetration",
						 "HitRating": "hit rating", 'AttackPower': "attack power",
						 "ExpertiseRating": "expertise rating",
						 "DefenseRating": "defense rating", "ParryRating": "parry rating", "bv": "block value",
						 "BlockValue": "Block", "BlockRating": "shield block rating",
						 "DodgeRating": "dodge", "Resilience": "resilience rating", "Mp5": "mana per 5 sec"}

GS_Rarity = {
	0: {"Red": 0.55, "Green": 0.55, "Blue": 0.55},
	1: {"Red": 1.00, "Green": 1.00, "Blue": 1.00},
	2: {"Red": 0.12, "Green": 1.00, "Blue": 0.00},
	3: {"Red": 0.00, "Green": 0.50, "Blue": 1.00},
	4: {"Red": 0.69, "Green": 0.28, "Blue": 0.97},
	5: {"Red": 0.94, "Green": 0.09, "Blue": 0.00},
	6: {"Red": 1.00, "Green": 0.00, "Blue": 0.00},
	7: {"Red": 0.90, "Green": 0.80, "Blue": 0.50},
}

GS_Formula = {
	"A": {
		4: {"A": 91.4500, "B": 0.6500},
		3: {"A": 81.3750, "B": 0.8125},
		2: {"A": 73.0000, "B": 1.0000}
	},
	"B": {
		4: {"A": 26.0000, "B": 1.2000},
		3: {"A": 0.7500, "B": 1.8000},
		2: {"A": 8.0000, "B": 2.0000},
		1: {"A": 0.0000, "B": 2.2500}
	}
}

GS_Quality = {
	6000: {
		"Red": {"A": 0.94, "B": 5000, "C": 0.00006, "D": 1},
		"Green": {"A": 0.47, "B": 5000, "C": 0.00047, "D": -1},
		"Blue": {"A": 0, "B": 0, "C": 0, "D": 0},
		"Description": "Legendary"
	},
	5000: {
		"Red": {"A": 0.69, "B": 4000, "C": 0.00025, "D": 1},
		"Green": {"A": 0.28, "B": 4000, "C": 0.00019, "D": 1},
		"Blue": {"A": 0.97, "B": 4000, "C": 0.00096, "D": -1},
		"Description": "Epic"
	},
	4000: {
		"Red": {"A": 0.0, "B": 3000, "C": 0.00069, "D": 1},
		"Green": {"A": 0.5, "B": 3000, "C": 0.00022, "D": -1},
		"Blue": {"A": 1, "B": 3000, "C": 0.00003, "D": -1},
		"Description": "Superior"
	},
	3000: {
		"Red": {"A": 0.12, "B": 2000, "C": 0.00012, "D": -1},
		"Green": {"A": 1, "B": 2000, "C": 0.00050, "D": -1},
		"Blue": {"A": 0, "B": 2000, "C": 0.001, "D": 1},
		"Description": "Uncommon"
	},
	2000: {
		"Red": {"A": 1, "B": 1000, "C": 0.00088, "D": -1},
		"Green": {"A": 1, "B": 000, "C": 0.00000, "D": 0},
		"Blue": {"A": 1, "B": 1000, "C": 0.001, "D": -1},
		"Description": "Common"
	},
	1000: {
		"Red": {"A": 0.55, "B": 0, "C": 0.00045, "D": 1},
		"Green": {"A": 0.55, "B": 0, "C": 0.00045, "D": 1},
		"Blue": {"A": 0.55, "B": 0, "C": 0.00045, "D": 1},
		"Description": "Trash"
	},
}
GS_ItemTypes = {
	"INVTYPE_RELIC": {"SlotMOD": 0.3164, "ItemSlot": 18, "Enchantable": False},
	"INVTYPE_TRINKET": {"SlotMOD": 0.5625, "ItemSlot": 33, "Enchantable": False},
	"INVTYPE_2HWEAPON": {"SlotMOD": 2.000, "ItemSlot": 16, "Enchantable": True},
	"INVTYPE_WEAPONMAINHAND": {"SlotMOD": 1.0000, "ItemSlot": 16, "Enchantable": True},
	"INVTYPE_WEAPONOFFHAND": {"SlotMOD": 1.0000, "ItemSlot": 17, "Enchantable": True},
	"INVTYPE_RANGED": {"SlotMOD": 0.3164, "ItemSlot": 18, "Enchantable": True},
	"INVTYPE_THROWN": {"SlotMOD": 0.3164, "ItemSlot": 18, "Enchantable": False},
	"INVTYPE_WAND": {"SlotMOD": 0.3164, "ItemSlot": 18, "Enchantable": False},
	"INVTYPE_RANGEDRIGHT": {"SlotMOD": 0.3164, "ItemSlot": 18, "Enchantable": False},
	"INVTYPE_SHIELD": {"SlotMOD": 1.0000, "ItemSlot": 17, "Enchantable": True},
	"INVTYPE_WEAPON": {"SlotMOD": 1.0000, "ItemSlot": 36, "Enchantable": True},
	"INVTYPE_HOLDABLE": {"SlotMOD": 1.0000, "ItemSlot": 17, "Enchantable": False},
	"INVTYPE_HEAD": {"SlotMOD": 1.0000, "ItemSlot": 1, "Enchantable": True},
	"INVTYPE_NECK": {"SlotMOD": 0.5625, "ItemSlot": 2, "Enchantable": False},
	"INVTYPE_SHOULDER": {"SlotMOD": 0.7500, "ItemSlot": 3, "Enchantable": True},
	"INVTYPE_CHEST": {"SlotMOD": 1.0000, "ItemSlot": 5, "Enchantable": True},
	"INVTYPE_ROBE": {"SlotMOD": 1.0000, "ItemSlot": 5, "Enchantable": True},
	"INVTYPE_WAIST": {"SlotMOD": 0.7500, "ItemSlot": 6, "Enchantable": False},
	"INVTYPE_LEGS": {"SlotMOD": 1.0000, "ItemSlot": 7, "Enchantable": True},
	"INVTYPE_FEET": {"SlotMOD": 0.75, "ItemSlot": 8, "Enchantable": True},
	"INVTYPE_WRIST": {"SlotMOD": 0.5625, "ItemSlot": 9, "Enchantable": True},
	"INVTYPE_HAND": {"SlotMOD": 0.7500, "ItemSlot": 10, "Enchantable": True},
	"INVTYPE_FINGER": {"SlotMOD": 0.5625, "ItemSlot": 31, "Enchantable": False},
	"INVTYPE_CLOAK": {"SlotMOD": 0.5625, "ItemSlot": 15, "Enchantable": True},
	"INVTYPE_SHIRT": {"SlotMOD": 0, "ItemSlot": 99, "Enchantable": False},
	"INVTYPE_TABARD": {"SlotMOD": 0, "ItemSlot": 98, "Enchantable": False},
}

slot_filter = {'Head': 'INVTYPE_HEAD', 'Neck': 'INVTYPE_NECK', 'Shoulder': 'INVTYPE_SHOULDER',
			   'Shoulders': 'INVTYPE_SHOULDER',
			   'Back': 'INVTYPE_CLOAK', 'Chest': 'INVTYPE_CHEST', 'Shirt': 'INVTYPE_SHIRT',
			   'Tabard': 'INVTYPE_TABARD',
			   'Wrist': 'INVTYPE_WRIST', 'Hands': 'INVTYPE_HAND', 'Waist': 'INVTYPE_WAIST', 'Legs': 'INVTYPE_LEGS',
			   'Feet': 'INVTYPE_FEET', 'Finger': 'INVTYPE_FINGER', 'Finger2': 'INVTYPE_FINGER',
			   'Trinket': 'INVTYPE_TRINKET', 'Trinket2': 'INVTYPE_TRINKET', 'Main Hand': 'INVTYPE_WEAPONMAINHAND',
			   'MainHand': 'INVTYPE_WEAPONMAINHAND',
			   'Off Hand': 'INVTYPE_WEAPONOFFHAND', 'OffHand': 'INVTYPE_WEAPONOFFHAND',
			   'One-Hand': 'INVTYPE_WEAPON', 'OneHand': 'INVTYPE_WEAPON', 'Two-Hand': 'INVTYPE_2HWEAPON',
			   'Two-Hand2': 'INVTYPE_2HWEAPON', 'TwoHand': 'INVTYPE_2HWEAPON', 'Shield': 'INVTYPE_SHIELD',
			   'Held In Off-Hand': 'INVTYPE_HOLDABLE',
			   'Relic': 'INVTYPE_RELIC', 'Thrown': 'INVTYPE_THROWN', 'Ranged': 'INVTYPE_RANGED', 'Wand': 'INVTYPE_WAND'}
qual_filter = {'Heirloom': 0, 'Trash': 0, 'Poor': 0, 'Uncommon': 1, 'Common': 2, 'Superior': 3, 'Rare': 3, 'Epic': 4,
			   'Legendary': 5}


class Warmane(commands.Cog):
	__version__ = "1.0.1"

	def __init__(self, bot):
		self.bot = bot
		self.big_dict = {}
		self.data_dir = redbot.core.data_manager.cog_data_path(raw_name='Warmane')
		processed_dict = {}
		with open(os.path.join(self.data_dir, 'items.json')) as settng:
			processed_dict = json.load(settng)

		try:
			with open(os.path.join(self.data_dir, 'settings.json')) as settng:
				s = json.load(settng)
		except:
			s = {"server": "Icecrown", "guild": "Down Under Gaming"}
		self.server = s['server']
		self.guild = s['guild']
		with open(os.path.join(self.data_dir, 'settings.json')) as settng:
			self.jsondata = json.load(settng)


	async def red_delete_data_for_user(self, **kwargs):
		return

	def gather_gear(self, char_equip):
		e = equipment()
		return e
		e.head = char_equip[0]
		e.Neck = char_equip[1]
		e.Shoulders = char_equip[2]
		e.Cloak = char_equip[3]
		e.Chest = char_equip[4]
		e.Shirt = char_equip[5]
		e.Tabard = char_equip[6]
		e.Bracer = char_equip[7]
		e.Gloves = char_equip[8]
		e.Belt = char_equip[9]
		e.Legs = char_equip[10]
		e.Boots = char_equip[11]
		e.Ring_1 = char_equip[12]
		e.Ring_2 = char_equip[13]
		e.Trinket_1 = char_equip[14]
		e.Trinket_2 = char_equip[15]
		e.Main_hand = char_equip[16]
		e.Off_hand = char_equip[17]
		e.Ranged = char_equip[18]
		return e

	# For GS in diff specs
	# def GearScore_GetQuality(self, ItemScore):
	# 	if not ItemScore: return
	#
	# 	Red = 0.1
	# 	Blue = 0.1
	# 	Green = 0.1
	# 	GS_QualityDescription = "Legendary"
	#
	# 	if not ItemScore: return 0, 0, 0, "Trash"
	# 	if ItemScore > 5999:
	# 		ItemScore = 5999
	# 	for i in range(6):
	# 		if (ItemScore > (i*1000)) and (ItemScore <= ((i + 1)*1000)):
	# 			Red = GS_Quality[(i + 1) * 1000]["Red"]["A"] + (((ItemScore - GS_Quality[(i + 1) * 1000]["Red"]["B"]) * GS_Quality[(i + 1) * 1000]["Red"]["C"]) * GS_Quality[(i + 1) * 1000]["Red"]["D"])
	# 			Blue = GS_Quality[(i + 1) * 1000]["Green"]["A"] + (((ItemScore - GS_Quality[(i + 1) * 1000]["Green"]["B"]) * GS_Quality[(i + 1) * 1000]["Green"]["C"]) * GS_Quality[(i + 1) * 1000]["Green"]["D"])
	# 			Green = GS_Quality[(i + 1) * 1000]["Blue"]["A"] + (((ItemScore - GS_Quality[(i + 1) * 1000]["Blue"]["B"]) * GS_Quality[(i + 1) * 1000]["Blue"]["C"]) * GS_Quality[(i + 1) * 1000]["Blue"]["D"])
	# 		return Red, Green, Blue, GS_Quality[(i + 1) * 1000]["Description"]
	#
	# 	return 0.1, 0.1, 0.1

	def gearscore_item(self, ItemRarity, ItemLevel, ItemEquipLoc, gem=False):
		QualityScale = 1
		if ItemRarity > 4:
			QualityScale = 1.3
			ItemRarity = 4
		elif ItemRarity == 1:
			QualityScale = 0.005
			ItemRarity = 2
		elif ItemRarity == 0:
			QualityScale = 0.005
			ItemRarity = 2

		Table = GS_Formula["B"]
		if ItemLevel > 120:
			Table = GS_Formula["A"]

		Scale = 1.8618
		slot_mod = GS_ItemTypes[ItemEquipLoc]["SlotMOD"]
		if gem:
			QualityScale = 12.25
			slot_mod = 1
		GearScore = math.floor(
			((ItemLevel - Table[ItemRarity]["A"]) / Table[ItemRarity]["B"]) * slot_mod * Scale * QualityScale)
		if GearScore < 0: GearScore = 0
		return GearScore

	def database_import(self, itemid):
		processed_dict = {}
		with open(os.path.join(self.data_dir, 'items.json')) as settng:
			processed_dict = json.load(settng)
		start = time.time()
		itemid = int(itemid)

		if str(itemid) in processed_dict:
			stop = time.time()
			diff = stop - start
			return processed_dict[str(itemid)]
		else:
			attr_filter = self.rising_item_scrape(itemid)

		# try:
		# 	print("using from xml")
		# 	start = time.time()
		# 	item = big_dict[int(itemid)]
		# 	rarity = qual_filter[item['Quality']]
		# 	lvl = int(item['ItemLevel'])
		# 	slot = slot_filter[item['Slot']]
		# 	gs = int(self.gearscore_item(ItemRarity=rarity, ItemLevel=lvl, ItemEquipLoc=slot))
		# 	attr_filter = {"Armor": 0, "Stamina": 0, "Intellect": 0, "Strength": 0, "Agility": 0, "Spirit": 0,
		# 				   "spell power": 0,
		# 				   "critical strike rating": 0, "armor penetration": 0, "haste": 0, "hit rating": 0,
		# 				   "attack power": 0,
		# 				   "expertise rating": 0, "defense rating": 0, "parry rating": 0, "block value": 0, "Block": 0,
		# 				   "shield block rating": 0, "dodge": 0, "Meta Socket": 0, "Red Socket": 0, "Blue Socket": 0,
		# 				   "Yellow Socket": 0, "Socket Bonus": 0, "Bonus type": "", "resilience rating": 0,
		# 				   "mana per 5 sec": 0, "itemLevel": lvl, "itemRarity": rarity, "slot": slot, "gs": gs,
		# 				   "Speed": 0}
		#
		# 	if item['Stats']:
		# 		for elem in item['Stats']:
		# 			# if elem.text
		# 			if elem in rawr_attr_correlation:
		# 				attr_filter[rawr_attr_correlation[elem]] = item['Stats'][elem]
		# 			else:
		# 				# todo trinket on-use effects
		# 				# print(elem)
		# 				continue
		# 	if item['SocketBonus']:
		# 		attr_filter['Bonus type'] = rawr_attr_correlation[list(item['SocketBonus'])[0]]
		# 		attr_filter['Socket Bonus'] = item['SocketBonus'][list(item['SocketBonus'])[0]]
		# 	if 'Speed' in item:
		# 		attr_filter['Speed'] = float(item['Speed'])
		# 	if 'SocketColor1' in item:
		# 		if item['SocketColor1'] == "Red":
		# 			attr_filter['Red Socket'] += 1
		# 		if item['SocketColor1'] == "Blue":
		# 			attr_filter['Blue Socket'] += 1
		# 		if item['SocketColor1'] == "Yellow":
		# 			attr_filter['Yellow Socket'] += 1
		# 		if item['SocketColor1'] == "Meta":
		# 			attr_filter['Meta Socket'] += 1
		# 	if 'SocketColor2' in item:
		# 		if item['SocketColor2'] == "Red":
		# 			attr_filter['Red Socket'] += 1
		# 		if item['SocketColor2'] == "Blue":
		# 			attr_filter['Blue Socket'] += 1
		# 		if item['SocketColor2'] == "Yellow":
		# 			attr_filter['Yellow Socket'] += 1
		# 		if item['SocketColor2'] == "Meta":
		# 			attr_filter['Meta Socket'] += 1
		# 	if 'SocketColor3' in item:
		# 		if item['SocketColor3'] == "Red":
		# 			attr_filter['Red Socket'] += 1
		# 		if item['SocketColor3'] == "Blue":
		# 			attr_filter['Blue Socket'] += 1
		# 		if item['SocketColor3'] == "Yellow":
		# 			attr_filter['Yellow Socket'] += 1
		# 		if item['SocketColor3'] == "Meta":
		# 			attr_filter['Meta Socket'] += 1
		# 	if attr_filter['slot'] == "INVTYPE_RANGED":
		# 		if 'Type' in item:
		# 			if item['Type'] in ["Totem", "Libram", "Idol", "Sigil"]:
		# 				attr_filter['slot'] = "INVTYPE_RELIC"
		# 			if item['Type'] in ["Thrown", "Wand"]:
		# 				attr_filter['slot'] = "INVTYPE_THROWN"
		#
		# 	armor_offhand_list = [38322, 3360, 1131, 1172, 11855]
		# 	if (attr_filter['slot'] == "Off Hand" or attr_filter['slot'] == "OffHand" or attr_filter[
		# 		'slot'] == "Held In Off-Hand") and attr_filter['Armor'] > 0 and not itemid in armor_offhand_list:
		# 		attr_filter['slot'] = "Shield"
		# 		attr_filter['slot'] = slot_filter[attr_filter['slot']]
		# 	if attr_filter['slot'] == "INVTYPE_WEAPONOFFHAND" and attr_filter['Speed'] == 0:
		# 		attr_filter['slot'] = "Held In Off-Hand"
		# 		attr_filter['slot'] = slot_filter[attr_filter['slot']]
		# 	attr_filter['name'] = item['Name']
		# 	stop = time.time()
		#
		#
		# except:
		# 	attr_filter = self.rising_item_scrape(itemid)
		print(len(processed_dict))
		processed_dict[itemid] = attr_filter
		print(len(processed_dict))
		with open(os.path.join(self.data_dir, 'items.json'), 'w') as output_file:
			json.dump(processed_dict, output_file)
		stop = time.time()

		return attr_filter

	def rising_item_scrape(self, itemid, spell=False):
		start = time.time()
		print("Using web for %s." % itemid)
		item_template = "https://db.rising-gods.de/?item={0}"
		url = item_template.format(itemid)
		# print(url)
		session = requests_html.HTMLSession()
		headers = {
			'User-agent':
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
		}
		r = session.get(url, headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")

		tooltip = soup.findAll("script")
		for i in tooltip:
			if i.string:
				if "var _ = g_items;" in i.string:
					attr_filter = {"Armor": 0, "Stamina": 0, "Intellect": 0, "Strength": 0, "Agility": 0, "Spirit": 0,
								   "spell power": 0,
								   "critical strike rating": 0, "armor penetration": 0, "haste": 0, "hit rating": 0,
								   "attack power": 0,
								   "expertise rating": 0, "defense rating": 0, "parry rating": 0, "block value": 0,
								   "Block": 0,
								   "shield block rating": 0, "dodge": 0, "Meta Socket": 0, "Red Socket": 0,
								   "Blue Socket": 0,
								   "Yellow Socket": 0, "Socket Bonus": 0, "Bonus type": "", "resilience rating": 0,
								   "mana per 5 sec": 0}
					data_table = str(i.string).split('\n')[3].split('.tooltip_enus = "')[1].split('<!--?')[0].replace(
						'\/span', '/span').replace('\/a', '/a').replace('\/td', '/td').replace('\/b', '/b')
					soup = BeautifulSoup(data_table, 'lxml')
					attributes = []
					test = []
					avoidlist = ['"?itemset=', '?class=', 'javascript', '?item=', '?spell=']
					match = re.search('Item Level (\d+)', str(data_table))
					if match:
						attr_filter['itemLevel'] = int(match.group(1))
					for b in soup.select('b'):
						m2 = re.search('"q(\d+)', str(b.attrs))
						if m2:
							attr_filter['itemRarity'] = int(m2.group(1))
							attr_filter['name'] = b.text

					if not spell:
						for td in soup.select('td'):
							if td.text:
								# print(td.text)
								match = re.search(r'''(?<=<table width='\\"100%\\"'><tr><td>)[^<]*''',
												  str(td))  # table width=\"100%\"><tr><td
								ranged = re.search(r'''(?<=<th>).*?(?=&lt;\\/th)''', str(td))
								try:
									attr_filter['slot'] = match.group(0)
									print("Slot here %s" % ranged.group(0))
									print(attr_filter)
									if attr_filter['slot'].lower() == 'ranged':
										if ranged.group(0).lower() == 'wand':
											attr_filter['slot'] = ranged.group(0)
										if ranged.group(0).lower() == 'thrown':
											attr_filter['slot'] = ranged.group(0)
								except:
									print("Fail slot")
									print(td)
								match2 = re.search(r'''(?<=<th>Speed <!--spd-->)[^(]*''', str(td))
								try:
									attr_filter['Speed'] = float(match2.group(0))
								except:
									print("No Speed")
							break
					for a in soup.select('a'):
						test.append(a)
						skip = False

						try:
							for i in avoidlist:
								if i in a.attrs['href']:
									skip = True
							if "?enchantment=" in a.attrs['href']:

								attr_filter["Socket Bonus"] = int(re.findall(r'\d+', a.text)[0])
								for b in attr_filter:
									if b.lower() in a.text.lower():
										attr_filter["Bonus type"] = b

						except:
							pass
						if not skip:
							try:
								attributes.append(a.text)
							except:
								pass

					for span in soup.select('span'):
						skip = False
						for a in soup.select('a'):
							if str(a.text) == "' + LANG.tooltip_changelevel + '" and str(a.text) in str(span):
								break
							if str(a.text) in str(span):
								skip = True
								break
						test.append(span)

						try:
							for i in avoidlist:
								if i in span.attrs['href'] or i in span.text:
									skip = True
						except:
							pass
						if not skip:
							try:
								if "Â (' + LANG.tooltip_changelevel + '" in span.text:
									attributes.append(str(span.text).replace("Â (' + LANG.tooltip_changelevel + '", ""))
								else:
									attributes.append(span.text)
							except:
								pass

					for i in attributes:
						complete = False
						for a in attr_filter:
							if a.lower() in i.lower():
								if "armor" in a.lower():
									if ("penetration" in a.lower() and "penetration" not in i.lower()) or (
											"penetration" in i.lower() and "penetration" not in a.lower()):
										continue
								stat_val = re.findall(r'\d+', i)
								try:
									attr_filter[a] += int(stat_val[0])
								except:
									attr_filter[a] += 1
								complete = True
								break
							if complete: break

					armor_offhand_list = [38322, 3360, 1131, 1172, 11855]
					if 'slot' in attr_filter:
						if (attr_filter['slot'] == "Off Hand" or attr_filter['slot'] == "OffHand" or attr_filter[
							'slot'] == "Held In Off-Hand") and attr_filter[
							'Armor'] > 0 and not itemid in armor_offhand_list:
							attr_filter['slot'] = "Shield"
						if attr_filter['slot'] == "INVTYPE_WEAPONOFFHAND" and attr_filter['Speed'] == 0:
							attr_filter['slot'] = "Held In Off-Hand"
						attr_filter['slot'] = slot_filter[attr_filter['slot']]
						attr_filter["gs"] = self.gearscore_item(attr_filter['itemRarity'], attr_filter['itemLevel'],
																attr_filter['slot'])
					return attr_filter

	def gather_items(self, name="Saeonn", gear=None):
		hyperlink_template = "http://armory.warmane.com/character/{0}/{1}/summary"
		server = self.server
		query = name.replace(",", "")
		data_url = hyperlink_template.format(query, server)
		session = requests.Session()
		response = session.get(data_url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'})
		soup = BeautifulSoup(response.text, "html.parser")
		items = soup.findAll("div", class_="item-slot")
		item_list = []
		weapons = []
		index = 0
		gem_count = 0
		ench_count = 0
		total_gs = 0
		for text in items:
			slot = item()
			if text.find("a").attrs["href"] == "#self":
				slot.itemID = None
				slot.ench_fit = 0
				slot.gem_fit = 0
			else:
				data = text.find("a").attrs["rel"]
				data = data[0].split("&")
				for i in data:
					if 'item' in i:
						slot.itemID = i.split("=")[1]
					if 'ench' in i:
						slot.ench_fit = i.split("=")[1]
					if 'gems' in i:
						slot.gem_fit = i.split("=")[1]
				if gear:
					slot.name = gear[index]["name"]
				equip = self.database_import(slot.itemID)
				print(equip)
				#if slot.ench_fit:
				equip['ench_fit'] = slot.ench_fit
				#if slot.gem_fit:
				equip['gem_fit'] = slot.gem_fit
				item_list.append(equip)


				# print(equip["gs"], equip)

				try:
					if equip["slot"] == 'INVTYPE_2HWEAPON':
						weapons.append(equip["gs"])
					else:
						total_gs += equip["gs"]
				except:
					continue
				index += 1
		if len(weapons) == 2:
			total_gs += (math.floor((weapons[0] + weapons[1]) / 2))
		elif len(weapons) == 1:
			total_gs += weapons[0]
		return item_list, total_gs

	def gem_sorter(self, input, gems):
		gem_count = 0
		input = input.split(':')
		trimmed_list = [x for x in input if int(x) > 0]
		gems['gem_count'] += len(trimmed_list)
		for gem in trimmed_list:
			if gem in gems:
				gems[gem] += 1
				gem_count += 1
			else:
				gems[gem] = 1
				gem_count += 1
		return gems, gem_count

	def request_enchantment(self, itemid):
		processed_dict = {}
		with open(os.path.join(self.data_dir, 'items.json')) as settng:
			processed_dict = json.load(settng)
		itemid = int(itemid)
		print(itemid)
		# if itemid in processed_dict:
		# 	return processed_dict[itemid]
		gem_url = "https://db.rising-gods.de/?enchantment={0}"
		gem_url = gem_url.format(itemid)
		session = requests.Session()
		response = session.get(gem_url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'})
		soup = BeautifulSoup(response.text, "html.parser")
		tooltip = soup.findAll("script")
		print(tooltip)
		for i in tooltip:
			if i.string:
				if "var _ = g_items;" in i.string:
					print("g_items")
					data_table = str(i.string).split('\n')
					for j in data_table:
						if 'g_items' in str(j):
							e = re.findall(r"\[(\d+)\]", j)
							gem = self.rising_item_scrape(e[0], spell=True)
							if gem:
								print("gem")
								print(len(processed_dict))
								processed_dict[itemid] = gem
								print(len(processed_dict))
								with open(os.path.join(self.data_dir, 'items.json'), 'w') as output_file:
									json.dump(processed_dict, output_file)
								return gem
				# engr cloaks etc that arent items but spells
				elif "var _ = g_spells;" in i.string:
					print("g_spells")
					data_table = str(i.string).split('\n')
					for j in data_table:
						if 'g_spells' in str(j):
							try:
								k = j.split(';')[2]
								e = re.search(r'(?<="name_enus":")[^"]*', k)
								f = {}
								f['name'] = e.group(0)
								if f:
									print(len(processed_dict))
									processed_dict[itemid] = f
									print(len(processed_dict))
									with open(os.path.join(self.data_dir, 'items.json'), 'w') as output_file:
										json.dump(processed_dict, output_file)
									return f
							except:
								# enchant rings
								k = j.split(';')[1]
								e = re.search(r'(?<="name_enus":")[^"]*', k)
								f = {}
								f['name'] = e.group(0)
								if f:
									print(len(processed_dict))
									processed_dict[itemid] = f
									print(len(processed_dict))
									with open(os.path.join(self.data_dir, 'items.json'), 'w') as output_file:
										json.dump(processed_dict, output_file)
									return f

	@commands.command(aliases=["char", "gs", "who"])
	async def character(self, ctx, *, query):
		processed_dict = {}
		with open(os.path.join(self.data_dir, 'items.json')) as settng:
			processed_dict = json.load(settng)
		"""Returns a characters gearscore, gem and enchant summary."""
		hyperlink_template = "http://armory.warmane.com/character/{0}/{1}/summary"
		data_template = "http://armory.warmane.com/api/character/{0}/{1}/"
		server = self.server
		query = query.replace(",", "")
		fmt_str = hyperlink_template.format(query, server)
		e = discord.Embed(
			color=await	ctx.embed_color(),
		title = f"Gear check on: `{query}`",
				description = """Processing Character..."""
		, url = fmt_str)
		await ctx.send(embed=e)

		data_url = data_template.format(query, server)
		session = requests.Session()
		response = session.get(data_url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'})
		soup = BeautifulSoup(response.text, "html.parser")
		data = json.loads(soup.text)
		c = character()
		c.name = data['name']
		c.online = data['online']
		c.achievementpoints = data['achievementpoints']
		c.faction = data['faction']
		c.gender = data['gender']
		c.honorablekills = data['honorablekills']
		c.realm = data['realm']
		c.level = data['level']
		c.race = data['race']
		c.game_class = data['class']
		c.guild = data['guild']
		profs = data['professions']
		if len(profs) == 2:
			output_profs = "%s %s, %s %s." % (profs[0]['skill'], profs[0]['name'], profs[1]['skill'], profs[1]['name'])
		elif len(profs) == 1:
			output_profs = "%s %s." % (profs[0]['skill'], profs[0]['name'])
		else:
			output_profs = "Nil professions."
		c.professions = output_profs
		tals = data['talents']
		if len(tals) == 2:
			output_talss = "%s %s, %s %s." % (tals[0]['tree'], tals[0]['points'], tals[1]['tree'], tals[1]['points'])
		elif len(tals) == 1:
			output_talss = "%s %s." % (tals[0]['tree'], tals[0]['points'])
		else:
			output_talss = "Nil professions."
		c.talents = output_talss
		c.equipment, gs = self.gather_items(name=query, gear=data['equipment'])

		enchant_template = ""
		gear_template = ""
		test_print = "\n"
		defcap = 0
		arpen = 0
		ench_count = 0
		gem_count = 0  # to account for eternal belt buckle
		gems = {}
		pvp_count = 0
		gems['gem_count'] = 0
		bs = False
		en = False
		eng = False
		for i in profs:
			if i['name'] == 'Blacksmithing' and int(i['skill']) >= 400:
				# gem_count += 2
				bs = True
			if i['name'] == 'Enchanting' and int(i['skill']) >= 400:
				# ench_count += 2
				en = True
			if i['name'] == 'Engineering' and int(i['skill']) >= 380:
				# ench_count += 1
				eng = True
		for item in c.equipment:
			if item['name'].lower() == "soulsplinter":
				print(item)
			item_desc = item['slot'].replace("INVTYPE_","").capitalize()+": "+item['name']+" (iLevel "+ str(item['itemLevel']) + ")"

			# Stats
			# todo socket bonuses and gem stats
			arpen+=int(item['armor penetration'])
			defcap+=int(item['defense rating'])
			enchant = True
			gem = True
			eq_gem_count = 0
			socket = True
			sockets = (item['Meta Socket'] + item['Red Socket'] + item['Blue Socket'] + item['Yellow Socket'])
			if ((item['slot'] == 'INVTYPE_HAND' or item['slot'] == 'INVTYPE_WRIST') and bs) or item['slot'] == 'INVTYPE_WAIST':
				sockets+=1
			gem_count += (sockets)
			if item['gem_fit'] != 0:
				gems_temp = int(gems['gem_count'])
				gems, item_count = self.gem_sorter(item['gem_fit'], gems)
				eq_gem_count = int(gems['gem_count']) - gems_temp
			print("look here\n")
			print(item["Socket Bonus"], item["Bonus type"])
			eq_gem_count = sockets - eq_gem_count
			if eq_gem_count!=0:
				gem = False

			if int(item['resilience rating']) > 0:
				pvp_count += 1
			if GS_ItemTypes[item['slot']]['Enchantable'] or (item['slot'] == 'INVTYPE_FINGER' and en) or (item['slot'] == 'INVTYPE_WAIST' and eng):

				ench_count += 1
				if 'ench_fit' in item and item['ench_fit'] != 0:
					ench_count += -1
					try:
						print("try enc")
						enc = processed_dict[str(item['ench_fit'])]
						if not enc:
							enc = self.request_enchantment(item['ench_fit'])
					except:
						print("except enc")
						enc = self.request_enchantment(item['ench_fit'])
					enc = self.request_enchantment(item['ench_fit'])
					# if enchant_template != "":
					# 	enchant_template = enchant_template + '\n'
					# enchant_template = enchant_template + enc['name']
					print(item)
					enchant = enc['name']
					item_desc = item_desc + " " + enchant
				else:
					enchant = None
					# if enchant_template != "":
					# 	enchant_template = enchant_template + '\n'
					# enchant_template = enchant_template + ("***" + item['name'] + " is missing an enchantment.")

			if not enchant or not socket or not gem:
				if gear_template != "":
					gear_template = gear_template + '\n'
				gear_template = gear_template + ("MISSING:")
				if not enchant:
					gear_template = gear_template + (" enchant")
				if not socket:
					gear_template = gear_template + (" socket")
				if not gem:
					gear_template = gear_template + (" " + str(eq_gem_count) + " gem")
				gear_template = gear_template + (" on "  + item_desc)
			else:
				if gear_template != "":
					gear_template = gear_template + '\n'
				gear_template = gear_template + (item_desc)


		gem_count += (-1 * gems['gem_count'])
		gem_template = ""
		for i in gems:

			if i != 'gem_count':
				template = "{0}x {1}."

				try:
					gem = processed_dict[str(i)]
				except:
					gem = self.request_enchantment(i)
				arpen += (int(gems[i]) * int(gem['armor penetration']))
				defcap += (int(gems[i]) * int(gem['defense rating']))
				t = template.format(gems[i], gem['name'])
				if gem_template != "":
					gem_template = gem_template + '\n'
				gem_template = gem_template + t



		ench_count_template = "Fully enchanted."
		if ench_count > 0: ench_count_template = "%s items missing enchants." % ench_count
		enchant_template = ench_count_template + "\n" + enchant_template

		gem_count_template = "Fully gemmed."
		if gem_count > 0: gem_count_template = "%s items missing gems." % gem_count
		gem_template = gem_count_template + "\n" + gem_template

		e = discord.Embed(
			color=await ctx.embed_color(),
		title = f"Character Link: `{query}`",
			description = """Stats:
				Gearscore: %s
				Defense: %s
				ArPen: %s
				Ratings do not currently include socket bonuses.
				Talents: %s
				PVP Gear Equiped: %s
				Professions: %s
		
				Gear:
				%s
		
				Gems: %s
		
				Enchants: %s""" % (gs, defcap, arpen, c.talents, pvp_count, c.professions, gear_template, gem_template, enchant_template), url = fmt_str)
		# e.set_footer(text=f"Calculated in {round((end - start) * 1000, 3)} ms")
		await ctx.send(embed=e)

	@commands.command(aliases=["Server"])
	async def server(self, ctx, *, query):
		"""Change default Warmane Server."""
		query = query.replace(",", "")
		e = discord.Embed(
			color=await	ctx.embed_color(),
		title = f"Setting default Server as:",
				description = f"`{query}`."
		)
		try:
			with open(os.path.join(self.data_dir, 'settings.json')) as settng:
				s = json.load(settng)
		except:
			s = {"server": "Icecrown"}
		s['server'] = query
		self.server = query
		with open(os.path.join(self.data_dir, 'settings.json'), 'w') as settng:
			json.dump(s, settng)
		await ctx.send(embed=e)

	@commands.command(aliases=["Guild"])
	async def guild(self, ctx, *, query):
		"""Change default Warmane guild."""
		query = query.replace(",", "")
		e = discord.Embed(
			color=await	ctx.embed_color(),
		title = f"Setting default Guild as:",
				description = f"`{query}`."
		)
		try:
			with open(os.path.join(self.data_dir, 'settings.json')) as settng:
				s = json.load(settng)
		except:
			s = {"guild": "Down Under Gaming"}
		s['guild'] = query
		self.guild = query
		with open(os.path.join(self.data_dir, 'settings.json'), 'w') as settng:
			json.dump(s, settng)
		await ctx.send(embed=e)

	# @checks.serverowner_or_permissions(administrator=True)
	@commands.command(aliases=["clear"])
	async def cache(self, ctx, *, query):
		processed_dict = {}
		with open(os.path.join(self.data_dir, 'items.json')) as settng:
			processed_dict = json.load(settng)
		"""Clear the item cache, warning char checks will take much longer for a while."""
		query = query.replace(",", "")
		if query.lower() == 'cache':
			e = discord.Embed(
				color=await	ctx.embed_color(),
			title = f"Clearing:",
					description = f"`{query}`. Gearscore checks will take much longer until the cache is rebuilt through character scans."
			)
			processed_dict = {}
			with open(os.path.join(self.data_dir, 'items.json'), 'w') as output_file:
				json.dump(processed_dict, output_file)
			await ctx.send(embed=e)
		else:
			e = discord.Embed(
				color=await	ctx.embed_color(),
			title = f"Clear query not recognised for:",
					description = f"`{query}`."
			)
			await ctx.send(embed=e)

	@commands.command(aliases=["on"])
	async def online(self, ctx, *, query=""):
		"""Check who is online from a guild."""
		server = self.server
		if not query: query = self.guild
		online = []
		max_level = {}
		guild_template = "http://armory.warmane.com/api/guild/{0}/{1}/summary"
		query = query.replace(",", "")
		fmt_str = guild_template.format(query, server)
		data_url = guild_template.format(query, server)
		# print(data_url)
		session = requests.Session()
		response = session.get(data_url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
			'Cache-Control': 'no-cache'})
		# print(response)
		soup = BeautifulSoup(response.text, "html.parser")
		guild_data = (json.loads(soup.text))
		# print(guild_data)
		guild_name = guild_data["name"]
		guild_membercount = guild_data["membercount"]
		guild_leader = guild_data["leader"]
		guild_roster = guild_data["roster"]
		for char in guild_roster:
			if char['online']:
				online.append(char["name"])
			if char['level'] == '80':
				max_level[char['name']] = {}
				char_template = "http://armory.warmane.com/api/character/{0}/{1}/"
				url = char_template.format(char['name'], server)
				max_level[char['name']]['api'] = url

		fmt_str = ", ".join(str(x) for x in online)
		e = discord.Embed(
			color=await	ctx.embed_color(),
			title = f"Guild: `{query}`",
				description = f"%s Online: `{fmt_str}`" % len(online),
		)
		# e.set_footer(text=f"Calculated in {round((end - start) * 1000, 3)} ms")
		await ctx.send(embed=e)