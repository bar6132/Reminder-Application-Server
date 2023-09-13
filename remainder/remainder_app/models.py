from django.db import models

from django.core.exceptions import ValidationError


class Note(models.Model):
    STATUS_CHOICES = [
        ('Complete', 'Complete'),
        ('Pending', 'Pending')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, null=True, blank=True,  choices=STATUS_CHOICES, default='Pending')

    MAX_WORDS_DESCRIPTION = 500

    class Meta:
        db_table = "Note"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if len(self.description.split()) > self.MAX_WORDS_DESCRIPTION:
            raise ValidationError("Description has too many words.")

        super().save(*args, **kwargs)
