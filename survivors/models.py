from django.db import models

class Survivor(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    last_location = models.CharField(max_length=50)
    infected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    owner = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='items', default=<DEFAULT_VALUE>)
    #quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


"""class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.survivor.name} - {self.item.name}'"""
    
class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.survivor.name} - {self.item.name}'
