from django.db import models
import qrcode
from io import BytesIO
from django.conf import settings
import os
from random import sample
import string

# Create your models here.


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True, unique=True)

    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(CodeGenerate):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(CodeGenerate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    banner_img = models.ImageField(upload_to='media/banner-img/')
    quantity = models.IntegerField()
    qr_code = models.ImageField(blank=True, upload_to="media/qr")

    def save(self, *args, **kwargs):
        url = f'{self.name}'
        qr_image = qrcode.make(url, box_size=15)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        self.qr_code.save(
            f"{self.name}.png", BytesIO(stream.getvalue()), save=False)

        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"


class EnterProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    entered_at = models.DateField(auto_now_add=True)
    price = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price

        super().save(*args, **kwargs)

        product_quantity = self.product.quantity - self.quantity
        self.product.quantity = product_quantity
        self.product.save()

    def __str__(self):
        return f"{self.product.name} {self.quantity}ta, {self.entered_at}da qo'shilgan"

    class Meta:
        ordering = ['-entered_at']

class SellProduct(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sold_at = models.DateField(auto_now_add=True)
    refunded = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        return super().save(*args, **kwargs)
    
    @property
    def refund(self):
        if not self.refunded:
            refund_amount = self.price
            Refund.objects.create(sell_product=self)
            self.refunded = True
            self.save()
            return refund_amount
        else:
            return 0

    def __str__(self):
        if self.refunded == True:
            return f"{self.product.name} - {self.sold_at}(maxsulot qaytarilgan)"
        else:
            return f"{self.product.name} - {self.sold_at}"
        

        
    class Meta:
        ordering = ['-sold_at']



class Refund(models.Model):
    sell_product = models.OneToOneField(SellProduct, on_delete=models.CASCADE)
    refunded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund for {self.sell_product} at {self.refunded_at}"
    
    @property
    def price(self):
        price = self.sell_product.price
        return price

    class Meta:
        ordering = ['-refunded_at']
