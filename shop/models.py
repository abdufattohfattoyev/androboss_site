from django.db import models
from django.utils import timezone


class Review(models.Model):
    RATING_CHOICES = [(i, '★' * i) for i in range(1, 6)]

    first_name = models.CharField(max_length=100, verbose_name='Ism')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Familiya')
    avatar = models.ImageField(upload_to='reviews/avatars/', blank=True, null=True, verbose_name='Profil rasmi')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name='Reyting')
    text = models.TextField(verbose_name='Sharh matni')
    date = models.DateField(verbose_name='Sana')
    is_active = models.BooleanField(default=True, verbose_name='Ko\'rsatish')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Sharh'
        verbose_name_plural = 'Sharhlar'
        ordering = ['order', '-date']

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.date}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def initials(self):
        parts = [self.first_name[:1], self.last_name[:1]]
        return ''.join(p for p in parts if p).upper()


class ReviewMedia(models.Model):
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_AUDIO = 'audio'
    TYPE_CHOICES = [
        (TYPE_IMAGE, 'Rasm'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_AUDIO, 'Ovoz xabari'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='media', verbose_name='Sharh')
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Tur')
    file = models.FileField(upload_to='reviews/media/', verbose_name='Fayl')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media fayllar'
        ordering = ['order']

    def __str__(self):
        return f'{self.get_media_type_display()} — {self.review}'


class TelegramAdmin(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ism')
    chat_id = models.CharField(max_length=50, unique=True, verbose_name='Chat ID')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Telegram admin'
        verbose_name_plural = 'Telegram adminlar'

    def __str__(self):
        return f'{self.name} ({self.chat_id})'


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
