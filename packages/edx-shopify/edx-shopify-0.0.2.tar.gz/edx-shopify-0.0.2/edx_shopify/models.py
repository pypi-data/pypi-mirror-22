from django.db import models
from django.utils import timezone


class Order(models.Model):
    UNPROCESSED = 0
    PROCESSING = 1
    PROCESSED = 2
    ERROR = 3

    STATUS_CHOICES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSING, 'Processing'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    id = models.BigIntegerField(primary_key=True, editable=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    received = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNPROCESSED)


class OrderItem(models.Model):
    UNPROCESSED = 0
    PROCESSED = 1
    ERROR = 2

    STATUS_CHOICES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    order = models.ForeignKey(Order)
    sku = models.CharField(max_length=254)
    email = models.EmailField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNPROCESSED)

    unique_together = ('order', 'sku', 'email')
