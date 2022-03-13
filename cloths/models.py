from django.db import models
from Users.models import User
from order.models import Orders
from django.utils.text import slugify 
import random, string
# Create your models here.

class Cloths(models.Model):
    def nameFile1(self, filename):
        return '/'.join(["cloth_pics", str(self.slug), 'clothpic1.jpg'])
    def nameFile2(self, filename):
        return '/'.join(["cloth_pics", str(self.slug), 'clothpic2.jpg'])
    def nameFile3(self, filename):
        return '/'.join(["cloth_pics", str(self.slug), 'clothpic3.jpg'])
    def nameFile4(self, filename):
        return '/'.join(["cloth_pics", str(self.slug), 'clothpic4.jpg'])

    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    _for = models.CharField(max_length=100)
    picture1 = models.ImageField(upload_to=nameFile1)
    
    picture3 = models.ImageField(upload_to=nameFile3, blank=True)
    picture2 = models.ImageField(upload_to=nameFile2, blank=True)
    picture4 = models.ImageField(upload_to=nameFile4, blank=True)
    bought_on = models.DateField(blank=False)
    is_available = models.BooleanField(default=True)
    hourly_price = models.IntegerField(null=False)
    security = models.IntegerField(default=0)
    sold_to = models.ForeignKey(User, default=None,null=True, blank=True,on_delete=models.CASCADE,related_name="cloth_sold")
    def sell_to(self, uid):
        user = User.objects.filter(id=uid).first()
        if not user:
            raise Exception('invalid user id')
        if user.id == self.id:
            raise Exception('Cant sell to yourself')
        if not user.is_active:
            raise Exception('user is not active')
        self.sold_to = user
        self.is_available = False
        order = Orders.objects.filter(user=user,cloth=self).first()      
        order.accepted=True
        order.save()


    def generate_slug(self):
        while True:
            letters = string.ascii_letters
            slug = ''.join(random.choice(letters) for i in range(10))
            if Cloths.objects.filter(slug=slug):
                continue
            else:
                return slug


    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        super(Cloths, self).save(*args, **kwargs)















