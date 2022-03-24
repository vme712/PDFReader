from django.db import models


class DeleteModelMixin(models.Model):
    is_delete = models.BooleanField('Удален', default=False)

    class Meta:
        abstract = True
