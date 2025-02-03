import uuid
import qrcode
from io import BytesIO
from PIL import Image

from django.db import models
from django.core.files import File
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ресторана'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'
        indexes = [models.Index(fields=['name'])]


class Section(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Ресторан'
    )
    name = models.CharField(
        'Название секции',
        max_length=255
    )

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        indexes = [models.Index(fields=['restaurant', 'name'])]
        unique_together = ['restaurant', 'name']


class Table(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True,
        verbose_name='Уникальный UUID'
    )
    number = models.IntegerField(
        verbose_name='Номер стола'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Секция',
        null=True,
        blank=True
    )
    iiko_guid = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='IIKO GUID'
    )
    qr = models.ImageField(
        upload_to='qr_codes/',
        verbose_name='QR-код',
        blank=True,
        null=True
    )
    call_waiter = models.BooleanField(
        default=False,
        verbose_name='Вызов официанта'
    )
    call_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время вызова'
    )
    bill_waiter = models.BooleanField(
        default=False,
        verbose_name='Запрос счёта'
    )
    bill_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время запроса счёта'
    )

    class Meta:
        verbose_name = 'Стол и его QR код'
        verbose_name_plural = 'Создание столов и QR кодов'
        ordering = ['number']
        unique_together = (('section', 'number'),)

    def __str__(self):
        sec_name = self.section.name if self.section else "Без секции"
        return f"Стол №{self.number} - {sec_name}"

    def save(self, *args, **kwargs):
        if not self.qr:
            link = f"{settings.AVATARIYA_BASE_URL}/{self.uuid}/" 
            code_img = qrcode.make(link)
            canvas = Image.new('RGB', (410, 410), 'white')
            canvas.paste(code_img)
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            file_name = f'qr-{self.number}.png'
            self.qr.save(file_name, File(buffer), save=False)
            buffer.close()
            canvas.close()

        super().save(*args, **kwargs)