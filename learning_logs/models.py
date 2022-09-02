from django.conf import settings
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        return self.text
    
    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"pk": self.pk})
