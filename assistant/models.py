from django.db import models

# Create your models here.



class Farmer(models.Model):
    """Represents a registered farmer using KisanCall."""
    name        = models.CharField(max_length=100)
    phone       = models.CharField(max_length=15, unique=True)
    language    = models.CharField(max_length=30, default="Hindi")
    location    = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class CallSession(models.Model):
    """Tracks each voice call session."""
    STATUS_CHOICES = [
        ("active",    "Active"),
        ("completed", "Completed"),
        ("failed",    "Failed"),
    ]
    farmer      = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="sessions")
    session_id  = models.CharField(max_length=100, unique=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    started_at  = models.DateTimeField(auto_now_add=True)
    ended_at    = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_id} — {self.farmer.name}"


class QueryLog(models.Model):
    """Logs each farmer query and AI response within a session."""
    CATEGORY_CHOICES = [
        ("crop",      "Crop Advisory"),
        ("weather",   "Weather"),
        ("market",    "Market Price"),
        ("scheme",    "Government Scheme"),
        ("pest",      "Pest/Disease"),
        ("other",     "Other"),
    ]
    session         = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name="queries")
    user_query      = models.TextField()
    ai_response     = models.TextField()
    category        = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    language        = models.CharField(max_length=30, default="Hindi")
    audio_input_url = models.URLField(blank=True)     # URL to uploaded audio (if any)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query at {self.timestamp} [{self.category}]"