from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WantedCriminal(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    nickname = models.CharField(max_length=100)
    reward = models.PositiveIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_note = models.TextField(blank=True, default="")
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    armed = models.BooleanField(default=False)
    has_crew = models.BooleanField(default=False)
    escape_master = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nickname


class HuntLog(models.Model):
    criminal = models.ForeignKey(
        WantedCriminal,
        on_delete=models.CASCADE,
        related_name="hunt_logs",
    )
    success = models.BooleanField()
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "caught" if self.success else "escaped"
        return f"Hunt #{self.pk} — {self.criminal.nickname} ({status})"
