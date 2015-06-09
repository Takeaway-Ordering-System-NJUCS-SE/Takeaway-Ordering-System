    
class Address(models.Model):
    user = models.ForeignKey(User)
    addr = models.CharField(max_length=255)
    tel = models.CharField(max_length=30, null = True, blank = True)
    
class Order(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    customer = models.ForeignKey(Customer)
    addr = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    extra_info = models.CharField(max_length=255, null = True, blank = True)
    delivery = models.ForeignKey(Delivery)
    state = models.IntegerField()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    menu = models.ForeignKey(Menu)
    amount = models.IntegerField()
    
class Delivery(models.Model):
    name = models.CharField(max_length=30)
    performance = models.IntegerField()

