from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from urllib.request import urlopen
import selenium
import re
from bs4 import BeautifulSoup
import json
import pygame
from pygame import mixer
# Create your views here.

# load the printers
PrinterList = []
URLTopbar = ".internal/cgi-bin/dynamic/topbar.html"
URLStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"

printers_list = "../Printers.txt"

oldModelList = ['Lexmark XS955', 'Lexmark XS864', 'Lexmark XM3150', 'Lexmark XM7155', 'Lexmark XM9155','Lexmark X954']
newModelList = ['Lexmark XC9255']

pygame.init()
mixer.init()


didLoad = False

class Tray:
    def __init__(self):
        self.name= ""
        self.status = ""
        self.capacity = ""
        self.size = ""
        self.tray_type = ""

class Printer:
    def __init__(self):
        self.session = requests.Session()
        self.isColor = False
        self.html= ""
        self.model=""
        self.name = ""
        self.url_topbar = ".internal/cgi-bin/dynamic/topbar.html"
        self.url_status = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"
        self.printer_status = ""
        self.location = ""
        self.address = ""
        self.toner_status = ""
        self.toner_percentage = ""
        self.trays = []

        self.cyan_cartridge = ""
        self.magenta_cartridge = ""
        self.yellow_cartridge = ""
        self.black_cartridge =""

    def get_url_topbar(self):
        if self.address != "":
            print("Address: " + self.address)
            return "http://"+self.address + "/cgi-bin/dynamic/topbar.html"
        return "http://"+self.name + self.url_topbar

    def get_url_status(self):
        if self.address != "":
            return "http://"+self.address + "/cgi-bin/dynamic/printer/PrinterStatus.html"
        return "http://"+self.name + self.url_status

    def getHtml(self, url):
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code ==200:
                page = urlopen(url)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")
                self.html = html
        except requests.exceptions.RequestException as e:
            self.html = ""
            self.status = "Network Error: " + str(e)
            self.status_colour = 0b001000
        return self.html



    def update(self):
        self.getStatus()
        self.getLocaton()
        self.getAddress()
        self.getTonerPercentage()
        print(self.toner_percentage)
        if self.toner_percentage == "" or self.toner_percentage == "Couldn\'t find toner percentage":
            self.isColor = True
            self.getCatridges()
        self.getTrays()





    def getAddress(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_topbar())
            if self.html == "":
                self.address = "Couldn't find address"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                address_tag = soup.find(string=re.compile(r'Address:'))
                if address_tag:
                    self.address = address_tag.split('Address: ')[1].strip()
                else:
                    self.address = "Address not found (error Parsing)"
                    print('Address not found')
                
        elif self.model in newModelList:
            url = "http://" + self.name 
            self.getHtml(url)
            if self.html == "":
                self.address = "Couldn't find address"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                address_tag = soup.find(string=re.compile(r'IP Address:'))
                if address_tag:
                    self.address = address_tag.split('Address: ')[1].strip()
                else:
                    self.address = "Address not found (error Parsing)"
                    print('Address not found')
        else:
            self.address = "Model not found"
            
        
    def getStatus(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_topbar())
            if self.html == "":
                self.printer_status = "offline"
                mixer.music.load('../printer_status/printers/templates/samir.mp3')
                mixer.music.play()
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                status = soup.find('table', class_='statusBox').text.strip()
                self.printer_status = status
        elif self.model in newModelList:
            url = "http://" + self.name 
            self.getHtml(url)
            if self.html == "":
                self.printer_status = "offline"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                status_tag= soup.find(string=re.compile(r'Status:'))
                if status_tag:
                    self.status = status_tag.split('Status: ')[1].strip()
                else:
                    self.status = "offline (error Parsing)"
                    print('Status not found')
    
    def getCatridges(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_status())
            if self.html == "":
                self.cyan_cartridge = "Couldn't find cyan cartridge"
                self.magenta_cartridge = "Couldn't find magenta cartridge"
                self.yellow_cartridge = "Couldn't find yellow cartridge"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                self.cyan_cartridge = soup.find('td', bgcolor="#00ffff")['title']
                self.magenta_cartridge = soup.find('td', bgcolor="#ff00ff")['title']
                self.yellow_cartridge = soup.find('td', bgcolor="#ffff00")['title']
                self.black_cartridge = soup.find('td', bgcolor="#000000")['title']
                print(self.cyan_cartridge + " " + self.magenta_cartridge + " " + self.yellow_cartridge + " " + self.black_cartridge)
        elif self.model in newModelList:
            url = "http://" + self.name
            self.getHtml(url)
            if self.html == "":
                self.cyan_cartridge = "Couldn't find cyan cartridge"
                self.magenta_cartridge = "Couldn't find magenta cartridge"
                self.yellow_cartridge = "Couldn't find yellow cartridge"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                # <div class="progress-inner BlackGauge" role="img" title="78" aria-labelledby="78%">
                # <div class="progress-inner CyanGauge" role="img" title="5" aria-labelledby="5%">
                # <div class="progress-inner MagentaGauge" role="img" title="5" aria-labelledby="5%">
                # <div class="progress-inner YellowGauge" role="img" title="5" aria-labelledby="5%">

                self.cyan_cartridge = soup.find('div', class_="progress-inner CyanGauge")['title']
                self.magenta_cartridge = soup.find('div', class_="progress-inner MagentaGauge")['title']
                self.yellow_cartridge = soup.find('div', class_="progress-inner YellowGauge")['title']
                self.black_cartridge = soup.find('div', class_="progress-inner BlackGauge")['title']    

    
    def getLocaton(self):

        if self.model in oldModelList:
            # url = http://mi-b246a-prn1.internal/
            self.getHtml(self.get_url_topbar())       
            if self.html == "":
                self.location = "Couldn't find location"
                return
            soup = BeautifulSoup(self.html, 'html.parser')
            location_tag = soup.find(string=re.compile(r'Location:'))
            if location_tag:
                self.location = location_tag.split('Location: ')[1].strip()
            else:
                self.location = "Location not found (error Parsing)"
                print('Location not found')
        elif self.model in newModelList:
            location_tag = soup.find(string=re.compile(r'Location:'))
            if location_tag:
                self.location = location_tag.split('Location: ')[1].strip()
            else:
                self.location = "Location not found (error Parsing)"
                print('Location not found')

    
    def getTonerPercentage(self):
        url = self.get_url_status()
        self.getHtml(url)
        if self.html == "":
            self.toner_percentage = "Couldn't find toner percentage"
            return
        soup = BeautifulSoup(self.html, 'html.parser')
        # either blac cartridge or black toner
        toner_percentage_pattern = re.compile(r'Black Cartridge: (\d+)%')
        toner_percentage_match = toner_percentage_pattern.search(str(soup))
        self.toner_percentage = toner_percentage_match.group(1) if toner_percentage_match else 'Couldn\'t find toner percentage'
        if self.toner_percentage == 'Couldn\'t find toner percentage':
            toner_percentage_pattern = re.compile(r'Black Toner: (\d+)%')
            toner_percentage_match = toner_percentage_pattern.search(str(soup))
            self.toner_percentage = toner_percentage_match.group(1) if toner_percentage_match else 'Couldn\'t find toner percentage'


    def handle_error(self, url, response):
        # if object is connection timeout
        if isinstance(response, requests.exceptions.ConnectTimeout):
            self.html_top_bar = ""
            self.html_status = ""
            self.buffer = ""
            self.status = f"Connection Timeout for URL: {url}"
            self.status_colour = 0b001000
            print(self.status)
            return
        self.html_top_bar = ""
        self.html_status = ""
        self.buffer = ""
        self.status = f"Network Error: {response.status_code} for URL: {url}"
        self.status_colour = 0b001000
        print(self.status)

    def getTrays(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_status())
            if self.html == "":
                self.trays = []
                return
            soup = BeautifulSoup(self.html, 'html.parser')
            # Parse Tray Information
            tray_tables = soup.findAll('table', class_='status_table')
            tray_table = tray_tables[1]
            tray_rows = tray_table.find_all('tr')[1:]

            # Iterate over each tray row
            self.trays = []
            for row in tray_rows:
                columns = row.find_all('td')
                tray_name = columns[0].text.strip()
                if tray_name.startswith("Tray"):
                    tray = Tray()
                    tray.name = tray_name
                    tray.status = columns[1].text.strip()
                    tray.capacity = columns[3].text.strip()
                    tray.size = columns[4].text.strip()
                    tray.tray_type = columns[5].text.strip()
                    self.trays.append(tray)
        elif self.model in newModelList:
            # <div class="trayInfoTitle contentHeader" role="heading">
            # <span>Tray 1</span>
            # </div>

            # <div class="trayInfoContainer">
            # <div class="trayInfo">
            # <div class=" contentHeader" role="heading">
            # <span>Capacity</span>
            # </div>
            # <div class="contentBody" role="presentation">
            # 150
            # </div>
            url = "http://" + self.name
            self.getHtml(url)
            if self.html == "":
                self.trays = []
                return
            soup = BeautifulSoup(self.html, 'html.parser')
            tray_tables = soup.findAll('div', class_='trayInfoContainer')
            self.trays = []
            for tray_table in tray_tables:
                tray = Tray()
                tray.name = tray_table.find('div', class_='trayInfoTitle').text.strip()
                if tray_table.find('div', class_='contentHeader').text.strip() == "Capacity":
                    tray.capacity = tray_table.find('div', class_='contentBody').text.strip()
                elif tray_table.find('div', class_='contentHeader').text.strip() == "Size":
                    tray.size = tray_table.find('div', class_='contentBody').text.strip()
                elif tray_table.find('div', class_='contentHeader').text.strip() == "Type":
                    tray.tray_type = tray_table.find('div', class_='contentBody').text.strip()
                self.trays.append(tray)
        else:
            self.trays = []
            return


################################################################################################################
# to load all the printers that are in the printers_list file that is the printers.txt
############################################################################################################
def load():
    # global didLoad
    # if didLoad == True:
    #     return
    # load the printers
    PrinterList = []
    with open(printers_list, "r") as file:
        for line in file:
            if line.strip():
                # add the printer to the list of printers using the name
                printer = Printer()
                newline = line.strip()
                if printer.name.startswith("#"):
                    continue
                else:
                    if newline.__contains__("$") and not newline.startswith("#"):
                        # printer.name = newline.split("$")[0]
                        # remove white spaces
                        # mi-a300b-prn1$Lexmark XS864$10.64.64.160
                        printer.name = newline.split("$")[0].strip()
                        newline = newline.split("$")[1]
                        # if the line has another + then it has the ip address
                        if newline.__contains__("+"):
                            printer.model = newline.split("+")[0].strip()
                            printer.address = newline.split("+")[1].strip()
                        else:
                            printer.model = newline.strip()
                            print(printer.model)
                        PrinterList.append(printer)

    file.close()
    PrinterList.sort(key=lambda x: x.name)
    # didLoad = True
    return PrinterList

############################################################################################################
############################################################################################################
############################################################################################################

# to load a demo printer for testing only

def loadOnce():
    global didLoad
    if didLoad == True:
        return
    # only if printers are not available
    printer = Printer()


    printer.name='mi-b202-prn1'
    printer.printer_status = "Sleep mode"
    printer.printer_location = "Behind staircase"
    printer.printer_address = "102.12.12.12"
    printer.toner_status = "Black Catridge ~93%"
    printer.toner_percentage = "93"
    tray = Tray()
    tray.name = "Tray 1"
    tray.status = "OK"
    tray.capacity = "500"
    tray.size = "11x12"
    tray.tray_type = "Legal"

    printer.trays.append(tray)
   
    PrinterList.append(printer)
    didLoad = True


############################################################################################################
############################################################################################################
############################################################################################################

############################################ INDEX #########################################################

def index(request):
    global PrinterList
    # loadOnce()
    
    PrinterList = load()

    return render(request, 'index.html', {'printers' : PrinterList})

############################################################################################################
############################################################################################################
############################################################################################################

############################################ UPDATE ########################################################
# To update the printer status and other information

def update(request):
    if request.method == 'GET':
        printer_name = request.GET.get('name', None)
        # printer = PrinterList.__getitem__
        # find the printer in the list of printers
        printer_obj = next((x for x in PrinterList if x.name == printer_name), None)
        if printer_obj == None:
            load()
            printer_obj = next((x for x in PrinterList if x.name == printer_name), None)
        printer = Printer()
        printer.name = printer_obj.name
        printer.model = printer_obj.model
        printer.update()
        # print(printer.printer_status)
        if printer.printer_status == "" or printer.printer_status == None:
            printer.printer_status = "offline"
            # play song here
            # samir.mp3

        x = printer
        # x.pop('session')
        # x.pop('buffer')
        # x.pop('html_top_bar')
        # json response 
        traysList = []
        for tray in x.trays:
            traysList.append(tray.__dict__)
        x.trays = traysList
        if x.isColor == True:
            return JsonResponse({'name': x.name, 'status': x.printer_status, 'location': x.location, 'address': x.address, 'toner_status': x.toner_status, 'toner_percentage': x.toner_percentage, 'trays': x.trays, 'cyan_cartridge': x.cyan_cartridge, 'magenta_cartridge': x.magenta_cartridge, 'yellow_cartridge': x.yellow_cartridge,'black_cartridge':x.black_cartridge,'isColor': x.isColor}, safe=False)
        return JsonResponse({'name': x.name, 'status': x.printer_status, 'location': x.location, 'address': x.address, 'toner_status': x.toner_status, 'toner_percentage': x.toner_percentage, 'trays': x.trays, 'isColor': x.isColor}, safe=False)

############################################################################################################
############################################################################################################
############################################################################################################


############################################ ADD PRINTER ########################################################
# To add a printer to the list of printers
def AddPrinter(request):
    if request.method == 'GET':
        return render(request, 'addprinter.html')
    

def printerWebPage(request):
    if request.method == 'GET':
        # get the printer name from the request
        printer_name = request.GET.get('name', None)
        # get the ip address of the printer
        printer_address = request.GET.get('address', None)



        request = requests.get('http://' + printer_address +"/cgi-bin/dynamic/topbar.html" )

        # get the html of the printer
        html = request
        print(html.text)

        return HttpResponse(html)
    
############################################################################################################