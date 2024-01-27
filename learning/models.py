from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}


class Course(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=120, verbose_name='Название курса', default='Название не указано')
    image = models.ImageField(upload_to='learning/', verbose_name='Первью', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса', default='Описание появится в скором времени')

    def __str__(self):
        return f'Курс {self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']


class Lesson(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=120, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    image = models.ImageField(upload_to='learning/', verbose_name='Первью', **NULLABLE)
    video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'Курс {self.course.title}: урок {self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course']
