from django.db import models


class DocumentationFile(models.Model):
    title = models.CharField("Название документа", max_length=255)
    file = models.FileField("Файл", upload_to="documentation/")
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
