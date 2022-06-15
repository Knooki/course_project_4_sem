from django.db import models
from django.shortcuts import reverse
from multiselectfield import MultiSelectField
from django.conf import settings

LANGUAGES = [
    ('Python', 'Python'),
    ('C/C++', 'C/C++'),
    ('C#', 'C#'),
    ('Java', 'Java'),
    ('JavaScript', 'JavaScript'),
    ('HTML', "HTML"),
    ('CSS', "CSS"),
]


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_rul(self):
        return reverse("catalog:category", kwargs={
            'slug': self.slug
        })

    def purchase(self):
        return reverse("catalog:purchase-product", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='config/static/images/')
    svg_image = models.FileField(upload_to='config/static/images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={
            'slug': self.slug
        })

    def purchase(self):
        return reverse("catalog:purchase-product", kwargs={
            'slug': self.slug
        })


class Course(models.Model):

    title = models.CharField(max_length=255)
    languages = MultiSelectField(
        choices=LANGUAGES,
        max_choices=3,
        max_length=50,
    )
    description = models.TextField(blank=True)
    amount_of_days = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='config/static/images/')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:course", kwargs={
            'slug': self.slug
        })

    def purchase(self):
        return reverse("catalog:purchase-product", kwargs={
            'slug': self.slug
        })

# class ProductPurchase(models.Model):
#     '''
#     Through model for charges and products.
#     '''
#     charge = models.ForeignKey('djstripe.Charge')
#     product = models.ForeignKey('Product')
#     key = models.CharField(max_length=64, unique=True, default=_create_key)
#     downloads = models.IntegerField(default=10,
#                 help_text='How many times can a purchaser view this resource')

#     def decrement_downloads(self):
#         self.downloads -= 1
#         return self.save()

#     def __unicode__(self):
#         return u'{} - {}'.format(self.product.name, self.key)

# class Order(models.Model):
# 	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
# 	date_ordered = models.DateTimeField(auto_now_add=True)
# 	complete = models.BooleanField(default=False)
# 	transaction_id = models.CharField(max_length=100, null=True)

# 	def __str__(self):
# 		return str(self.id)

# 	@property
# 	def shipping(self):
# 		shipping = False
# 		orderitems = self.orderitem_set.all()
# 		for i in orderitems:
# 			if i.product.digital == False:
# 				shipping = True
# 		return shipping

# 	@property
# 	def get_cart_total(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.get_total for item in orderitems])
# 		return total

# 	@property
# 	def get_cart_items(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.quantity for item in orderitems])
# 		return total

# class OrderItem(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
# 	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
# 	quantity = models.IntegerField(default=0, null=True, blank=True)
# 	date_added = models.DateTimeField(auto_now_add=True)

# 	@property
# 	def get_total(self):
# 		total = self.product.price * self.quantity
# 		return total
