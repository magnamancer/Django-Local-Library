from django.db import models
from django.urls import (
    reverse,
)  # Used in get_absolute_url() to get URL for specified ID

from django.db.models import (
    UniqueConstraint,
)  # Constrains fields to unique values
from django.db.models.functions import (
    Lower,
)  # Returns lower cased value of field

# Create your models here.


class Person(models.Model):
    """Model representing a person (Probably just me)"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # About me section
    bio = models.TextField(
        max_length=5000, help_text="Enter a brief personal bio"
    )
    picture = []  # LEAVING EMPTY FOR NOW UNTIL FULL TEXT IS UP - IMAGE FILE
    resume = []  # LEAVING BLANK UNTIL FULL TEXT IS UP - PDF

    # Contact Info
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, null=True)
    linkedin = models.URLField(max_length=50)
    github = models.URLField(max_length=50)

    # Misc
    cur_job = models.CharField(max_length=50)
    location = models.CharField(max_length=1000)

    def __str__(self):
        """String for representing the Model object."""
        return self.first_name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Person."""
        return reverse("person-detail", args=[str(self.id)])


class Project(models.Model):
    """Model representing a project"""

    # Setting up Basic Info
    title = models.CharField(max_length=50)
    short_desc = models.TextField(
        max_length=100,
        null=True,
        help_text="Enter the project description",
    )
    long_desc = models.TextField(
        max_length=5000,
        null=True,
        help_text="Enter the project description",
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    difficulty = models.CharField(
        max_length=10, help_text="Difficulty out of 10"
    )

    # Setting up skills and tech relations
    tech = models.ManyToManyField("Technology")
    skills = models.ManyToManyField("Skill")

    # Links to Relevant Stuff
    project_git = models.URLField(max_length=50, null=True)
    live_demo_link = models.URLField(max_length=50, null=True)

    # I'll figure out how to use this thing later
    slug = models.SlugField()

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Project."""
        return reverse("project-detail", args=[str(self.id)])


class Technology(models.Model):
    """Model representing a Specific Technology"""

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Project."""
        return reverse("technology-detail", args=[str(self.id)])


class Skill(models.Model):
    """Model representing a Specific Skill"""

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Project."""
        return reverse("skill-detail", args=[str(self.id)])


class ProjectMedia(models.Model):
    """Model representing a Specific piece of Media for a project"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="media"
    )
    title = models.CharField(max_length=200, blank=True)
    # Use FileField for general file uploads
    file = models.FileField(upload_to="")
    caption = models.CharField(max_length=500, blank=True)
    long_desc = models.TextField(
        max_length=5000,
        null=True,
        help_text="Enter the media description",
    )
    # Add a field to specify the type of media for frontend rendering
    MEDIA_TYPES = [
        ("image", "Image"),
        ("video", "Video"),
        ("embed", "Embedded Content (e.g., YouTube/Vimeo)"),
        ("html_demo", "HTML/JS Interactive Demo"),
        ("glb_model", "3D GLB Model"),
        # Add more as needed
    ]
    media_type = models.CharField(
        max_length=20, choices=MEDIA_TYPES, default="image"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} - {self.title or self.file.name}"

    # You might also add a method to get the URL
    def get_absolute_url(self):
        return self.file.url
