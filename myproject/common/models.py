from django.contrib.auth.models import User
from django.db import models

from middlewares.current_user import CurrentUserMiddleware


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='%(class)s_created', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='%(class)s_updated', null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = CurrentUserMiddleware.get_current_user()
        self.updated_by = CurrentUserMiddleware.get_current_user()
        super().save(*args, **kwargs)

    def to_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    DEFAULT_SERIALIZER_EXCLUDE = ('created_by', 'created_at', 'updated_by', 'updated_at')