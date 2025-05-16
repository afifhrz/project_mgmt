import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="created_%(class)ss", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="updated_%(class)ss", on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()
