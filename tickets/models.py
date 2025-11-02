from django.db import models

class Ticket(models.Model):
    image = models.ImageField(upload_to='tickets/')
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField()
    phone_number = models.CharField(max_length=15)
    submitted_at = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=250, blank=True, null=True)
    resolved = models.BooleanField(default=False)
    resolution_comment = models.CharField(max_length=250, blank=True, null=True)


    category = models.CharField(
        max_length=100, choices=[
        ('Street Maintenance', 'Street Maintenance'),
        ('Trash Services', 'Trash Services'),
        ('Water Utilities', 'Water Utilities'),
        ('Animal Control', 'Animal Control'),
        ('Electrical Utilities', 'Electrical Utilities'),
        ('etc.', 'etc.'),
        ],
    blank=True,
    null=True
)

    priority = models.CharField(
        max_length=20,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Ticket #{self.id} - {self.location}"

    class Meta:
        ordering = ['-submitted_at']
