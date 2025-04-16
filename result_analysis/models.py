from django.db import models
from django.contrib.auth.models import User

class StudentScore(models.Model):
    gender = models.CharField(max_length=10)
    ethnic_group = models.CharField(max_length=50)
    parent_education = models.CharField(max_length=50)
    lunch_type = models.CharField(max_length=20)
    test_preparation = models.CharField(max_length=20)
    parent_marital_status = models.CharField(max_length=20)  
    practice_sport = models.BooleanField(default=False)
    is_first_child = models.BooleanField(default=False)
    nr_siblings = models.IntegerField(default=0)
    transport_means = models.CharField(max_length=20, default='Unknown')
    wkly_study_hours = models.FloatField(default=0.0)
    math_score = models.FloatField(null=True, blank=True)
    reading_score = models.FloatField(null=True, blank=True)
    writing_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.gender} - {self.math_score}, {self.reading_score}, {self.writing_score}"

class Resource(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    difficulty = models.CharField(max_length=50, default='Medium')
    format_type = models.CharField(max_length=50, default='Article')

    def __str__(self):
        return self.title

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.resource.title} on {self.timestamp}"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    questions = models.TextField()  # Store questions in a suitable format (JSON, etc.)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    platform = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched for '{self.query}'"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    keyword = models.CharField(max_length=255, null=True)  # New field for keyword
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    resource_id = models.IntegerField(null=True)

    class Meta:
        unique_together = ('user', 'course')  # Ensure a user can bookmark a course only once

    def __str__(self):
        return f"{self.user.username} bookmarked {self.course.title}"



# myapp/models.py
from django.db import models

class TimetableEntry(models.Model):
    day = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.day} - {self.time_slot}: {self.subject}"



class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable_data = models.JSONField()  # Store timetable as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Timetable for {self.user.username} on {self.created_at}'



class CourseRating(models.Model):
    rating = models.IntegerField()  # Store the rating (1-5)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the rating was created

    def __str__(self):
        return f'Rating: {self.rating}'
    

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional: link to user
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} on {self.created_at}"
