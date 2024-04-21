from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Users

# Create your models here.


class TagModel(models.Model):
    tagtitle   = models.CharField(_('Tag Title'),unique=True, max_length=256, null=True, blank=True)

    class Meta      : 
        verbose_name = 'TagModel'
        verbose_name_plural = "TagModels"

    def __str__(self):
        return str(self.tagtitle)
    
    
class Snippet(models.Model):
    content       = models.CharField(_('Snippet Content'), max_length=256, null=True, blank=True)
    title         = models.ForeignKey(TagModel,related_name="snippet_title",on_delete=models.CASCADE,null=True,blank=True)
    created_by    = models.ForeignKey(Users,related_name="created_user",on_delete=models.CASCADE,null=True,blank=True)
    updated_by    = models.ForeignKey(Users,related_name="updated_user",on_delete=models.CASCADE,null=True,blank=True)
    timestamp     = models.DateTimeField(_('timestamp'), auto_now_add=True, editable=False, blank=True, null=True)

    class Meta      : 
        verbose_name = 'Snippet'
        verbose_name_plural = "Snippets"

    def __str__(self):
        return f'{self.pk}-{self.content}'

    