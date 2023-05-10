from django.db import models

class Tray(models.Model):
    Name = models.CharField(max_length=200)
    Status = models.CharField(max_length=200)
    Capacity = models.CharField(max_length=200)
    PageSize = models.CharField(max_length=200)
    PageType = models.CharField(max_length=200)

class Kit(models.Model):
    Name = models.CharField(max_length=200)
    LifeRemaining = models.CharField(max_length=200)


class Toner(models.Model):
    Colour = models.CharField(max_length=200)
    Percent = models.CharField(max_length=200)

class Printer(models.Model):
#    name, model, address, location, maintenanceKit, PCKit, Buffer, HtmlTopBar, HtmlStatus, Status, TonerList, TrayList, KitList
    Name = models.CharField(max_length=200)
    Model = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    MaintenanceKit = models.CharField(max_length=200)
    PCKit = models.CharField(max_length=200)
    Buffer = models.CharField(max_length=200)
    HtmlTopBar = models.CharField(max_length=200)
    HtmlStatus = models.CharField(max_length=200)
    Status = models.CharField(max_length=200)
    # List of toners from the toners class
    Toner = models.ForeignKey(Toner, on_delete=models.CASCADE)
    # List of trays from the trays class
    Tray = models.ForeignKey(Tray, on_delete=models.CASCADE)
    # List of kits from the kits class
    Kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
    



