import os

PrinterList = []
PrinterUpdateThreadList = []
Selected = None
SortOrder = 1
PrinterColumns = [0] * 10
RefreshingPrinters = False
MinStatusLength = 0
MaxStatusLength = 50
NetworkTimeout = 2

def InitPrinters():
    DestroyPrinters()
    with open("Printers.txt", "r") as file:
        for line in file:
            if line.strip():
                PrinterList.append(Printer(line.strip()))
                PrinterUpdateThreadList.append(PrinterList[-1])
    file.close()
    SortPrinters()

def DestroyPrinters():
    for i in range(len(PrinterList)):
        if PrinterList[i]:
            del PrinterList[i]
    PrinterList.clear()
    PrinterUpdateThreadList.clear()

def SortPrinters():
    def sortFunc(a, b):
        if SortOrder == 0:
            return a.Name < b.Name
        elif SortOrder == 1:
            if a.Status == b.Status:
                return a.Name < b.Name
            else:
                return a.Status < b.Status
        elif SortOrder == 2:
            if a.LastPrinted == b.LastPrinted:
                return a.Name < b.Name
            else:
                return a.LastPrinted < b.LastPrinted
        elif SortOrder == 3:
            if a.PagesPrinted == b.PagesPrinted:
                return a.Name < b.Name
            else:
                return a.PagesPrinted < b.PagesPrinted
        elif SortOrder == 4:
            if a.CostPerPage == b.CostPerPage:
                return a.Name < b.Name
            else:
                return a.CostPerPage < b.CostPerPage
        else:
            return a.Name < b.Name
    PrinterList.sort(key=sortFunc)