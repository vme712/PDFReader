from rest_framework import mixins


class DeleteMixin(mixins.DestroyModelMixin):
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
