from bs4 import BeautifulSoup
import csv
import requests

# Optional to Send to Google Sheets
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


HOTOPIC_URL = "https://www.hottopic.com/funko/ht-exclusives/"
BOXLUNCH_URL = "https://www.boxlunch.com/funko/boxlunch-funko-exclusives/"
FYE_URL = "https://www.fye.com/toys-collectibles/action-figures/funko/?prefn1=isExclusive&prefv1=FYE%20Exclusive&sz=40"
GAMESTOP_URL = "https://www.gamestop.com/collectibles/funko?prefn1=isExclusive&prefv1=Yes&view=new&tileView=list&hybrid=true&start=1&sz=70"

HEADERS = {"User-Agent": "User Agent info"}

POP_SEARCH = ["The Office", "G.I. Joe", "Star Wars", "Marvel", "DC", "Heroes", "Avatar"]

COLUMN_NAMES = ["Store", "Name", "Price", "Link"]
FOUND_EXCLUSIVES = []
#--------------------------------------BOXLUNCH------------------------------#
box_response = requests.get(BOXLUNCH_URL, headers=HEADERS)
box_response.raise_for_status()

boxlunch_webpage = box_response.text

box_soup = BeautifulSoup(boxlunch_webpage, "html.parser")
box_pops = box_soup.find_all(name="div", class_="product-tile")
for pop in POP_SEARCH:
    for exclusive in box_pops:
        if pop in exclusive.text:
            FOUND_EXCLUSIVES.append({   "Store": "BOXLUNCH",
                                                    "Name": " ".join((exclusive.find(name="a", class_="name-link").text).split()),
                                                    "Price": exclusive.find(class_="price-standard").text,
                                                     "Link": exclusive.find(name="a", class_="name-link").get("href")
                                                      })


#---------------------------------GAMESTOP----------------------------------------#
game_response = requests.get(GAMESTOP_URL, headers=HEADERS)
game_response.raise_for_status()

game_webpage = game_response.text

game_soup = BeautifulSoup(game_webpage, "html.parser")
game_pops = game_soup.find_all(name="div", class_="tile-body")
for pop in POP_SEARCH:
    for exclusive in game_pops:
        if pop in exclusive.text:
            FOUND_EXCLUSIVES.append({"Store": "GAMESTOP",
                                     "Name":exclusive.find(class_="pd-name").text,
                                     "Price": " ".join((exclusive.find(class_="actual-price").text).split()),
                                    "Link": f'https://www.gamestop.com{exclusive.find(name="a", class_="link-name").get("href")}'})

#-----------------------------FYE--------------------------------------#
fye_response = requests.get(FYE_URL, headers=HEADERS)
fye_response.raise_for_status()

fye_webpage = fye_response.text

fye_soup = BeautifulSoup(fye_webpage, "html.parser")
fye_pops = fye_soup.find_all(name="div", class_="product-tile")
for pop in POP_SEARCH:
    for exclusive in fye_pops:
        if pop in exclusive.text:
            FOUND_EXCLUSIVES.append({"Store": "FYE",
                                     "Name": exclusive.find(name="a", class_="c-product-tile__product-name-link").text,
                                     "Price": " ".join((exclusive.find(class_="product-sales-price").text).split()),
                                     "Link": f'https://www.fye.com{exclusive.find(name="a", class_="c-product-tile__product-name-link").get("href")}'})

#-------------------------HOTTOPIC----------------------------------#
hot_response = requests.get(HOTOPIC_URL, headers=HEADERS)
hot_response.raise_for_status()

hot_webpage = hot_response.text

hot_soup = BeautifulSoup(hot_webpage, "html.parser")
hot_pops = hot_soup.find_all(name="div", class_="product-tile")
for pop in POP_SEARCH:
    for exclusive in hot_pops:
        if pop in exclusive.text:
            try:
                price = exclusive.find(class_="price-standard").text
            except AttributeError:
                price = exclusive.find(class_="price-sales").text
            finally:
                FOUND_EXCLUSIVES.append({"Store": "HOTTOPIC",
                                         "Name": " ".join((exclusive.find(name="a", class_="name-link").text).split()),
                                         "Price": price,
                                         "Link": exclusive.find(name="a", class_="name-link").get("href")})

with open('exclusive_pops.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=COLUMN_NAMES)
    writer.writeheader()
    writer.writerows(FOUND_EXCLUSIVES)


# Optional to Send to Google Sheets
# scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
#
# credentials = ServiceAccountCredentials.from_json_keyfile_name('secret_json_file.json', scope)
# client = gspread.authorize(credentials)
#
# spreadsheet = client.open('FunkoPopExclusives')
#
# with open('exclusive_pops.csv', 'r') as file_obj:
#     content = file_obj.read()
#     client.import_csv(spreadsheet.id, data=content)

