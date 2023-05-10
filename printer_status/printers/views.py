from django.shortcuts import render
from django.http import HttpResponse
from models import Printer, Tray, Kit, Toner
import PrinterFunctions
# Create your views here.

# load the printers
PrinterList = []
URLTopbar = ".internal/cgi-bin/dynamic/topbar.html"
URLStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"

def load():
    # load the printers
    PrinterList = []
    with open("Printers.txt", "r") as file:
        for line in file:
            if line.strip():
                # add the printer to the list of printers using the name
                PrinterList.append(Printer(__name__=line.strip()))
    file.close()
    PrinterList.sort(key=lambda x: x.Name)

    for printer in PrinterList:
        # load  the web page for the printer
        

    return PrinterList


def index(request):
    PrinterList = load()
    for printer in PrinterList:
        printer.update()


    return render(request, "printers/index.html")