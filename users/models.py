from django.contrib.auth.models import AbstractUser
from django.db import models

from learning.models import NULLABLE, Course, Lesson

PAYMENT_CHOICE = (
    ('Cash', 'Наличные'),
    ('Transfer', 'Перевод на счет')
)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=168, verbose_name='Горо', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активирован')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payment')
    pay_day = models.DateField(auto_now=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    paid_sum = models.PositiveIntegerField(default=0, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=20, choices=PAYMENT_CHOICE, verbose_name='Способ оплаты', default='Transfer')

    def __str__(self):
        if self.paid_course:
            return f'{self.pay_day} поступила сумма {self.paid_sum} на оплату курса "{self.paid_course.title}"'
        return f'{self.pay_day} поступила сумма {self.paid_sum} на оплату курса "{self.paid_lesson.title}"'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
