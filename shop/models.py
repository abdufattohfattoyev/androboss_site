from django.db import models
from django.utils import timezone


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CALLED = 'called'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Yangi'),
        (STATUS_CALLED, "Qo'ng'iroq qilindi"),
        (STATUS_CONFIRMED, 'Tasdiqlandi'),
        (STATUS_CANCELLED, 'Bekor qilindi'),
    ]

    name = models.CharField(max_length=200, verbose_name='Ism')
    phone = models.CharField(max_length=30, verbose_name='Telefon')
    discount = models.IntegerField(default=0, verbose_name='Chegirma (%)')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default=STATUS_NEW, verbose_name='Holat'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sana')
    note = models.TextField(blank=True, verbose_name='Izoh')

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} | {self.phone} | {self.created_at:%d.%m.%Y %H:%M}'


class VisitorStat(models.Model):
    date = models.DateField(default=timezone.localdate, unique=True, verbose_name='Sana')
    count = models.PositiveIntegerField(default=0, verbose_name='Tashriflar')

    class Meta:
        verbose_name = 'Tashrif statistikasi'
        verbose_name_plural = 'Tashrif statistikasi'
        ordering = ['-date']

    def __str__(self):
        return f'{self.date} — {self.count} ta'
