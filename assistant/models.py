from django.db import models

class FarmerQuery(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    crop = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.query_text[:50]