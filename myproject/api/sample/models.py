from django.db import models

from common.models import BaseModel


class Sample(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sample_sample'
        verbose_name = 'Sample'
        verbose_name_plural = 'Samples'
