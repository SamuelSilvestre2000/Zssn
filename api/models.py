from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    points = models.PositiveIntegerField()
    #quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Survivor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    last_location_latitude = models.FloatField()
    last_location_longitude = models.FloatField()
    #inventory = models.ManyToManyField(Item, through='SurvivorInventory')
    infected = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, through='Inventory')

    def __str__(self):
        return self.name

class SurvivorInventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.survivor.name} - {self.item.name} - {self.quantity}"

class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='survivor_inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_inventory')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.survivor.name} - {self.item.name}"
