import requests
import re
import pandas as pd


def getPageSource(url):
    r = requests.get(url)
    r.content
    pagee_source = r.content
    pagee_source = pagee_source.decode("utf-8")
    if r.status_code == 200:
        return pagee_source
    else:
        print('FAILED')
        return 0


def getCharacteristics(startString, endString, mainstring):
    strt = mainstring.find(startString) + len(startString)
    ed = mainstring.find(endString)
    sbstrg = mainstring[strt:ed]
    chaar = "".join(re.findall("[a-zA-Z0-9]+", sbstrg))
    return str(chaar)


def getEverything(ps):
    # get the advertised price  of the phone - in priceF
    Lei3 = page_source.find('Lei ', page_source.find('Lei ', page_source.find('Lei ') + 1) + 1)
    priceF = page_source[Lei3 - 5:Lei3 + 3]
    priceF = re.sub("[^\d\.]", "", priceF)
    priceF = int(priceF)

    # get the retail price of the phone
    Lei6 = page_source.find('Pret retail')
    priceR = page_source[Lei6 - 48:Lei6 + 13]
    priceR = re.sub("^[^\>]+", "", priceR)
    priceR = re.sub(r',', "", priceR)
    priceR = priceR[0:16]
    priceR = re.sub("[^\d\.]", "", priceR)
    priceR = priceR[0:priceR.find('.')]
    print(priceR)
    if priceR.isnumeric() == 0:
        priceR = 0
    else:
        priceR = int(float(priceR))


    # get full title
    # color, memory, condition will also be extracted from here
    nm = page_source.find('Telefon mobil')
    name = page_source[nm:nm + 300]
    name = re.sub("\<(.*)", "", name)
    name = name.rstrip()

    # get brand
    TList = name.split(',')
    Pbrand = TList[0]
    Pbrand = Pbrand.replace('Telefon mobil ', '')

    # get model
    Pmodel = TList[1]

    # get memory
    Pmemory = TList[2]

    # get color
    Pcolor = TList[3]

    # get condition
    Pcondition = TList[4]

    # get specifications
    spc = page_source.find('Specificatii')
    specifications = page_source[spc:spc + 5900]
    specifications = re.sub('<[^<]+?>', '', specifications)
    specifications = specifications[0:specifications.find('Cutia Flip contine')]

    # get RAM
    Pram_pointer = specifications.find('Memorie RAM')
    Pram_intermediary = specifications[Pram_pointer:Pram_pointer + 32]
    start = Pram_intermediary.find("Memorie RAM:") + len("Memorie RAM:")
    end = Pram_intermediary.find(",")
    substring = Pram_intermediary[start:end]
    char = "".join(re.findall("[a-zA-Z0-9]+", substring))
    Pram = str(char)

    # get resolution
    start = specifications.find('Rezolutie (pixeli):') + len('Rezolutie (pixeli):')
    end = specifications.find('Porturi:')
    substring = specifications[start:end]
    char = "".join(re.findall("[a-zA-Z0-9]+", substring))
    Pres = str(char)

    # print(specifications)

    # get battery

    Pbattery = getCharacteristics('Baterie:', 'Camera spate:', specifications)
    Pbattery = re.sub('[a-zA-Z]', "", Pbattery)

    # get number of rear camera
    Pcameras = getCharacteristics('Camera spate:', 'Camera fata:', specifications)
    Pcameras = Pcameras.count('MP')

    # create DF

    dt = [[priceF, priceR, Pbrand, Pmodel, Pmemory, Pcolor, Pcondition, Pram, Pres, Pbattery, Pcameras]]
    return dt


# Create maine DataFrame

data = pd.DataFrame(columns=['SH_Price', 'New_Price', 'Brand', 'Model', 'Memory', 'Color', 'Condition', 'Ram',
                             'Resolution',
                             'Battery_size', 'No_Rear_Cameras'])

# Read the links from the excel file
dfl = pd.read_excel('Links3.xlsx')
values = dfl['Link'].values

# Iterate through the excel and run the whole code
for i in range(len(values)):
    page_source = getPageSource(values[i])
    df1 = pd.DataFrame(getEverything(page_source),
                           columns=['SH_Price', 'New_Price', 'Brand', 'Model', 'Memory', 'Color', 'Condition', 'Ram',
                                    'Resolution',
                                    'Battery_size', 'No_Rear_Cameras'])
    data = pd.concat([data, df1], ignore_index=True)


data.to_csv('dataset.csv', index=False)
print(data.to_string())





##### Deprecated Code #####

# read from file
# file = open('test_page.txt', "r", encoding='utf-8')
# page_source = file.read()

# read from here


# page_source = getPageSource(
#     'https://flip.ro/magazin/apple/telefon-mobil-apple-iphone-12-pro-256gb-graphite/1119/?conditie=Foarte%20Bun&operator=Deblocat')


# import requests
#
# url = 'https://flip.ro/magazin/xiaomi/telefon-mobil-xiaomi-mi-10t-pro-5g-128gb-cosmic-black/72492/?conditie=Foarte%20Bun&operator=Deblocat'
#
# r = requests.get(url)
#
# r.content
# page_source = r.content
# page_source = page_source.decode("utf-8")
#

# f = open('C:/Users/Andrei/PycharmProjects/pythonProject1/test_page.txt', 'x', encoding='utf-8')
# f.write(page_source)
# f.close()
