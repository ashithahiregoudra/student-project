import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .models import Course

nltk.download('punkt')
nltk.download('stopwords')

def recommend_courses(query):
    query_words = set(word_tokenize(query.lower())) - set(stopwords.words('english'))

    recommendations = []
    for course in Course.objects.all():
        course_words = set(word_tokenize(course.title.lower()))
        if query_words & course_words:
            recommendations.append(course)
    
    return recommendations
