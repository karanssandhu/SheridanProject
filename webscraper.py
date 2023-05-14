# from urllib.request import urlopen

# URLTopbar = ".internal/cgi-bin/dynamic/topbar.html"
# URLStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"

# # Get toner levels 
# printer_name = 'http://mi-a300a-prn1'

# url = printer_name+URLTopbar

# # open the html for web scrapping
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# print(html)


import requests
from urllib.request import urlopen
import selenium
import re
from bs4 import BeautifulSoup

import os
class Printer:

    printer_status=""

    def __init__(self):
        self.session = requests.Session()
        self.buffer = ""
        self.html_top_bar = ""
        self.html_status = ""
        self.name = ""
        self.url_topbar = ".internal/cgi-bin/dynamic/topbar.html"
        self.url_status = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"

    def get_url_topbar(self):
        return 'http://'+self.name + self.url_topbar

    def get_url_status(self):
        return 'http://'+self.name + self.url_status

    def write_callback(self, response):
        self.buffer += response.content.decode('utf-8')
        return len(response.content)

    def update(self):
        try:
            # Fetch topbar HTML
            url_topbar = self.get_url_topbar()
            response = self.session.get(url_topbar)
            if response.status_code ==200:
                page = urlopen(url_topbar)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")

                # Parse the HTML
                soup = BeautifulSoup(html, 'html.parser')

                # Extract the sleep status
                sleep_status = soup.find('table', class_='statusBox').text.strip()
                print('Sleep Status:', sleep_status)

                # Extract the location
                # location_elem = soup.find(string='Location: ')
                # location = location_elem.next_sibling.strip() if location_elem else None
                # print('Location:', location)
                location_tag = soup.find(string=re.compile(r'Location:'))
                if location_tag:
                    location = location_tag.split('Location: ')[1].strip()
                    print('Location:', location)
                else:
                    print('Location not found')
                # Extract the address
                # address_elem = soup.find('b', string='Address:')
                # address = address_elem.next_sibling.strip() if address_elem else None
                # print('Address:', address)
                address_tag = soup.find(string=re.compile(r'Address:'))
                if address_tag:
                    address = address_tag.split('Address: ')[1].strip()
                    print('Address:', address)
                else:
                    print('Address not found')
            else:
                print("Couldn't connect")


            if response.status_code == 200 and "<html class=\"top_bar\">" in html:
                self.html_top_bar = html
            else:
                self.html_top_bar = ""
                self.buffer = ""
                self.status = "Network Error: " + str(response.status_code)
                self.status_colour = 0b001000

            # Fetch status HTML
            url_status = self.get_url_status()
            response = self.session.get(url_status)
            if response.status_code ==200:
                page = urlopen(url_status)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")

            
                soup = BeautifulSoup(html, 'html.parser')

                # Parse Toner Status and Percentage
                toner_status_pattern = re.compile(r'Toner Status:\s*(\w+)')
                toner_status_match = soup.find(string=toner_status_pattern)
                toner_status = toner_status_match.group(1) if toner_status_match else 'Not available'

                toner_percentage_pattern = re.compile(r'Black Cartridge\s*~(\d+)%')
                toner_percentage_match = toner_percentage_pattern.search(str(soup))
                toner_percentage = toner_percentage_match.group(1) if toner_percentage_match else 'Not available'

                # Parse Tray Information

                # print(html)
                # Parse Tray Information

                # Print Toner Status and Percentage
                print("Toner Status:", toner_status)
                print("Toner Percentage:", toner_percentage)
                # Find the table containing tray information
                tray_tables = soup.findAll('table', class_='status_table')
                tray_table = tray_tables[1]

                # Find all rows in the table (excluding the header row)
                tray_rows = tray_table.find_all('tr')[1:]

                # print(tray_rows)
                # Iterate over each tray row
                for row in tray_rows:
                    # Extract the information for each column in the row
                    columns = row.find_all('td')
                    tray_name = columns[0].text.strip()
                    if tray_name.startswith("Tray"):
                        status = columns[1].text.strip()
                        capacity = columns[2].text.strip()
                        size = columns[3].text.strip()
                        tray_type = columns[4].text.strip()

                        # Print the tray information
                        print(tray_name)
                        print(status)
                        print(capacity)
                        print(size)
                        print(tray_type)
                        print()


            # print(html)
            if response.status_code == 200 and "<html class=\"top_bar\">" in html:
                self.html_status = html
            else:
                self.html_status = ""
                self.buffer = ""
                self.status = "Network Error: " + str(response.status_code)
                self.status_colour = 0b001000

        except requests.exceptions.RequestException as e:
            self.buffer = ""
            self.status = "Network Error: " + str(e)
            self.status_colour = 0b001000
            print("Error")


printers_list = "Printers.txt"
def load():
    # load the printers
    PrinterList = []
    with open("../Printers.txt", "r") as file:
        for line in file:
            if line.strip():
                # add the printer to the list of printers using the name
                printer = Printer()
                printer.name = line.strip()
                PrinterList.append(printer)
    file.close()
    PrinterList.sort(key=lambda x: x.name)

    return PrinterList

printer = Printer()
printer.name = 'mi-b242-prn1'

printer.update()

# printers = load()
