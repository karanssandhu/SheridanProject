import re
import threading
import selenium
# std::string URLTopbar = ".internal/cgi-bin/dynamic/topbar.html";
# std::string URLStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html";

class Printer:
    def __init__(self, name=""):
        self.Name = name
        self.Mutex = threading.Lock()
        self.Pad = None

    def __del__(self):
        if self.Mutex:
            self.Mutex.release()
        if self.Pad:
            del self.Pad

    def GetToner(self):
        offset = 0
        inStr = ""
        self.TonerList.clear()
        self.Search(self.HtmlStatus, "<!-- Toner Level -->", offset, offset)
        while self.First(self.HtmlStatus, "><B>", "<hr", offset) == 1:
            toner = Toner()
            front = False
            inStr = self.Search(self.HtmlStatus, "><B>@<", offset, offset)
            if "Black" in inStr:
                toner.Colour = 0b111111
                front = True
            elif "Cyan" in inStr:
                toner.Colour = 0b110110
            elif "Magenta" in inStr:
                toner.Colour = 0b101101
            elif "Yellow" in inStr:
                toner.Colour = 0b011011
            inStr = self.Search(self.HtmlStatus, "<TBODY>*<TR>*<TD width=\"@%", offset, offset)
            toner.Percent = int(inStr)
            if self.First(self.HtmlStatus, "bgColor=#ffffff", "&nbsp;", offset) == 1:
                toner.Percent = 0
            if front:
                self.TonerList.insert(0, toner)
            else:
                self.TonerList.append(toner)
            self.Search(self.HtmlStatus, "</table>", offset, offset)

    def GetTrays(self):
        offset = 0
        inStr = ""
        self.TrayList.clear()
        doTray = True
        while doTray:
            self.Search(self.HtmlStatus, "<TR>*<TD>", offset, offset)
            inStr = self.Search(self.HtmlStatus, "<P style=\"marg", offset, offset)
            if "Tray" in inStr:
                tray = Tray()
                tray.Name = inStr
                inStr = self.Search(self.HtmlStatus, "<TD width=\"@%\">*@<", offset, offset)
                tray.Status = inStr
                inStr = self.Search(self.HtmlStatus, "<TD width=\"@%\">*@<", offset, offset)
                tray.Size = inStr
                inStr = self.Search(self.HtmlStatus, "<TD width=\"@%\">*@<", offset, offset)
                tray.Type = inStr
                self.TrayList.append(tray)
            else:
                doTray = False

    def Search(self, inStr, startStr, offset, endOffset):
        start = inStr.find(startStr, offset)
        if start == -1:
            return ""
        start += len(startStr)
        end = inStr.find(endOffset, start)
        if end == -1:
            return ""
        return inStr[start:end]

    def First(self, inStr, startStr, endStr, offset):
        start = inStr.find(startStr, offset)
        if start == -1:
            return 0
        end = inStr.find(endStr, start)
        if end == -1:
            return 0
        return 1

    # dstd::string Printer::GetUrlTopbar()
# {
# 	URLMutex.lock();
# 	std::string urlTopbar = URLTopbar;
# 	URLMutex.unlock();
# 	return Name + urlTopbar;
# }

# std::string Printer::GetUrlStatus()
# {
# 	URLMutex.lock();
# 	std::string urlStatus = URLStatus;
# 	URLMutex.unlock();
# 	return Name + urlStatus;
# }

    def GetUrlTopbar(self):
        self.Mutex.acquire()
        urlTopbar = ".internal/cgi-bin/dynamic/topbar.html"
        self.Mutex.release()
        return self.Name + urlTopbar
    
    def GetUrlStatus(self):
        self.Mutex.acquire()
        urlStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"
        self.Mutex.release()
        return self.Name + urlStatus
    
    def update(self):
        self.Mutex.acquire()
        self.Pad = PrinterFunctions.GetPrinter(self.Name)
        self.HtmlStatus = self.Pad.GetHtmlStatus()
        self.GetToner()
        self.GetTrays()
        self.Mutex.release()

class Toner:
    def __init__(self):
        self.Colour = 0
        self.Percent = 0

class Tray:
    def __init__(self):
        self.Name = ""
        self.Status = ""
        self.Size = ""
        self.Type = ""
