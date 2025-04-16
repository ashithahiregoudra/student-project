from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from .models import StudentScore
import seaborn as sns
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg') 
import io
import base64
from django.contrib.auth.models import User
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'result_analysis/home.html')
    return render(request, 'home.html')
def login_view(request):
    return render(request, 'result_analysis/login.html')
    return render(request, 'login.html')
def results(request):
    return render(request, 'result_analysis/results.html')
    return render(request, 'results.html')
def resources(request):
    return render(request, 'result_analysis/resources.html')
    return render(request, 'resources.html')
def contact(request):
    return render(request, 'result_analysis/contact.html')
    return render(request, 'contact.html')
def tutorial_resources(request):
    return render(request, 'result_analysis/tutorial_resources.html')  # Create this template

def study_resources(request):
    return render(request, 'result_analysis/study_resources.html')  # Create this template

def study_resources_finance(request):
    return render(request, 'result_analysis/study_resources_finance.html')  # Create this template


def study_analysis(request):
    # Render the input form for study analysis
    return render(request, 'result_analysis/study_analysis.html')

def student_analysis(request):
    if request.method == 'POST':
        # Get data from the form
        gender = request.POST.get('gender')
        ethnic_group = request.POST.get('ethnic_group')
        parent_education = request.POST.get('parent_education')
        lunch_type = request.POST.get('lunch_type')
        test_preparation = request.POST.get('test_preparation')
        parent_marital_status = request.POST.get('parent_marital_status')
        practice_sport = request.POST.get('practice_sport') == 'Yes'
        is_first_child = request.POST.get('is_first_child') == 'Yes'
        nr_siblings = request.POST.get('nr_siblings')
        transport_means = request.POST.get('transport_means')
        wkly_study_hours = request.POST.get('wkly_study_hours')
        math_score = request.POST.get('math_score')
        reading_score = request.POST.get('reading_score')
        writing_score = request.POST.get('writing_score')

        # Prepare data for saving
        student_data = {
            'gender': gender,
            'ethnic_group': ethnic_group,
            'parent_education': parent_education,
            'lunch_type': lunch_type,
            'test_preparation': test_preparation,
            'parent_marital_status': parent_marital_status,
            'practice_sport': practice_sport,
            'is_first_child': is_first_child,
            'nr_siblings': int(nr_siblings) if nr_siblings else 0,  # Default to 0 if None
            'transport_means': transport_means,
            'wkly_study_hours': float(wkly_study_hours) if wkly_study_hours else 0.0,  # Default to 0.0 if None
            'math_score': float(math_score) if math_score else None,  # Allow None for optional fields
            'reading_score': float(reading_score) if reading_score else None,
            'writing_score': float(writing_score) if writing_score else None,
        }

        # Save the new student score to the database
        StudentScore.objects.create(**student_data)

        # Generate graphs based on the data
        scores = StudentScore.objects.all()
        math_scores = [score.math_score for score in scores if score.math_score is not None]
        reading_scores = [score.reading_score for score in scores if score.reading_score is not None]
        writing_scores = [score.writing_score for score in scores if score.writing_score is not None]

        # Check if there are scores to avoid division by zero
        avg_math = sum(math_scores) / len(math_scores) if math_scores else 0
        avg_reading = sum(reading_scores) / len(reading_scores) if reading_scores else 0
        avg_writing = sum(writing_scores) / len(writing_scores) if writing_scores else 0

        plt.bar(['Math', 'Reading', 'Writing'], [avg_math, avg_reading, avg_writing])
        plt.ylabel('Average Score')
        plt.title('Average Scores by Subject')
        plt.savefig('static/images/average_scores.png')
        plt.close()

        return render(request, 'result_analysis/student_analysis_result.html', {
            'average_scores_image': 'static/images/average_scores.png',
            'scores': scores,
        })

    return render(request, 'result_analysis/student_analysis.html')


# Assuming you have a function to get your DataFrame
def results_analysis(request):
    # Fetch data from the database
    df = pd.DataFrame(list(StudentScore.objects.values()))

    # Create a dictionary to hold the images
    images = {}

    # Gender Distribution
    plt.figure(figsize=(10, 6))
    ct = sns.countplot(data=df, x="gender")
    plt.title("Gender Distribution")
    ct.bar_label(ct.containers[0])
    # Save to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['gender_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Parent Education vs Scores
    gb = df.groupby("parent_education").agg({"math_score": "mean", "reading_score": "mean", "writing_score": "mean"})
    plt.figure(figsize=(10, 6))
    sns.heatmap(gb, annot=True, cmap="YlGnBu")
    plt.title("Relation between Parent Education and Student Scores")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['parent_education_scores'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Parent Marital Status vs Scores
    gb2 = df.groupby("parent_marital_status").agg({"math_score": "mean", "reading_score": "mean", "writing_score": "mean"})
    plt.figure(figsize=(10, 6))
    sns.heatmap(gb2, annot=True, cmap="YlGnBu")
    plt.title("Relation between Parent Marital Status and Student Scores")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['parent_marital_status_scores'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Boxplots for Scores
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="math_score")
    plt.title("Outliers Affecting MathScore")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['math_score_boxplot'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="reading_score")
    plt.title("Outliers Affecting ReadingScore")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['reading_score_boxplot'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="writing_score")
    plt.title("Outliers Affecting WritingScore")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['writing_score_boxplot'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Ethnic Group Distribution
    ethnic_counts = df['ethnic_group'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.pie(ethnic_counts, labels=ethnic_counts.index, autopct="%1.2f%%")
    plt.title("Distribution of Ethnic Groups")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    images['ethnic_group_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Render the results page with the generated images
    return render(request, 'result_analysis/result_analysis.html', {'images': images}) 


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return render(request, 'result_analysis/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'result_analysis/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'result_analysis/register.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('result_analyis/login.html')  # Redirect to home after logout


    

from .models import UserActivity, Resource
from .forms import UserRegistrationForm


def resource_click(request, resource_id):
    if request.user.is_authenticated:
        resource = Resource.objects.get(id=resource_id)
        UserActivity.objects.create(user=request.user, resource=resource)  # Save user activity
    return redirect('resources')  # Redirect back to resources page


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserActivity, Resource
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'result_analysis/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return render(request, 'result_analysis/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'result_analysis/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'result_analysis/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

def resources(request):
    resources_list = Resource.objects.all()  # Fetch all resources
    return render(request, 'result_analysis/resources.html', {'resources': resources_list})

def resource_click(request, resource_id):
    if request.user.is_authenticated:
        resource = Resource.objects.get(id=resource_id)
        UserActivity.objects.create(user=request.user, resource=resource)  # Save user activity
    return redirect('resources')  # Redirect back to resources page



from django.http import JsonResponse

def track_click(request):
    resource_name = request.GET.get('resource')
    if request.user.is_authenticated and resource_name:
        # Log the click in your database or analytics system
        UserActivity.objects.create(user=request.user, resource_name=resource_name)
    return JsonResponse({'status': 'success'})






from django.shortcuts import get_object_or_404

def resource_click(request, resource_id):
    if request.user.is_authenticated:
        resource = get_object_or_404(Resource, id=resource_id)
        UserActivity.objects.create(user=request.user, resource=resource)  # Save user activity
        print(f"User  {request.user.username} clicked on {resource.title}")  # Debugging line

    return redirect('resources')  # Redirect back to resources page



def additional_study_methods(request):
    return render(request, 'result_analysis/additional_study_methods.html')


# results/views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# Set your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


# results/views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# Set your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home page
        else:
            return render(request, 'result_analysis/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'result_analysis/login.html')

def home_view(request):
    return render(request, 'result_analysis/home.html')  # Render your home page

from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    return render(request, 'result_analysis/profile.html', {'user': user})


@login_required
def edit_profile(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        # Update user information
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()  # Save the updated user information
        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, 'result_analysis/edit_profile.html', {'user': user})


# views.py

 # Import the crawler function

# views.py

from django.shortcuts import render
from .scraper import scrape_geeksforgeeks, scrape_kaggle, scrape_cs50, scrape_mit_ocw, scrape_khan_academy
from .models import Course
# views.py

# views.py

from django.shortcuts import render
from .scraper import scrape_geeksforgeeks, scrape_kaggle, scrape_cs50, scrape_mit_ocw, scrape_khan_academy
from .models import Course
from .scraper import save_courses  # Import the save_courses function

def scrape_courses_view(request):
    # Scrape courses from different platforms
    gfg_courses = scrape_geeksforgeeks()
    kaggle_courses = scrape_kaggle()
    cs50_courses = scrape_cs50()
    mit_courses = scrape_mit_ocw()
    khan_courses = scrape_khan_academy()

    # Save courses to the database
    save_courses(gfg_courses)
    save_courses(kaggle_courses)
    save_courses(cs50_courses)
    save_courses(mit_courses)
    save_courses(khan_courses)

    # Retrieve all courses from the database to display
    all_courses = Course.objects.all()

    return render(request, 'courses.html', {'courses': all_courses})


from django.shortcuts import render
from .crawler import scrape_courses  # Import the function that orchestrates scraping
from .models import Course

def scrape_courses_view(request):
    scrape_courses()  # Call the function that scrapes and saves courses
    #all_courses = Course.objects.all()  # Retrieve all courses from the database
    #return render(request, 'courses.html', {'courses': all_courses})
    return render(request, 'result_analysis/home.html')

#def find_course_view(request):
    query = request.GET.get('query', '').strip()  # Get the search query from the request and strip whitespace
    print(f"Search Query: {query}")  # Debugging output
    if query:
        # Filter courses based on the search query
        courses = Course.objects.filter(title__icontains=query)  # Case-insensitive search
        print(f"Found Courses: {courses}")  # Debugging output
    else:
        courses = Course.objects.all()  # If no query, show all courses

    return render(request, 'result_analysis/find_course.html', {'courses': courses, 'query': query})

#def find_course_view(request):
    query = request.GET.get('query', '').strip()  # Get the search query from the request
    courses = []  # Initialize an empty list for courses

    if query:
        # Split the query into individual keywords
        keywords = query.split()  # Split by whitespace
        from django.db.models import Q
        query_filter = Q()  # Start with an empty Q object

        # Build the query filter for each keyword
        for keyword in keywords:
            query_filter |= Q(title__icontains=keyword)  # Use OR for each keyword

        # Filter courses based on the constructed query
        courses = Course.objects.filter(query_filter)  # Apply the filter
        print(f"Search Query: {query}, Found Courses: {[course.title for course in courses]}")  # Debugging output

    return render(request, 'result_analysis/find_course.html', {'courses': courses, 'query': query})


    # views.py

from django.shortcuts import render
from .models import Course  # Ensure you import the Course model
from django.db.models import Q  # Import Q for complex queries

# Static resources from the HTML page
# views.py

from django.shortcuts import render
from .models import Course, SearchHistory # Ensure you import the Course model
from django.db.models import Q  # Import Q for complex queries

# Static resources from the HTML page
RESOURCES = {
    "General": [
        {"title": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org/"},
        {"title": "freeCodeCamp", "link": "https://www.freecodecamp.org/"},
        {"title": "W3Schools", "link": "https://www.w3schools.com/"},
        {"title": "CS50x by Harvard", "link": "https://cs50.harvard.edu/x/2023/"},
        {"title": "The Odin Project", "link": "https://www.theodinproject.com/"},
        {"title": "NPTEL", "link": "https://nptel.ac.in/"},
        {"title": "MIT OpenCourseWare", "link": "https://ocw.mit.edu/"},
        {"title": "Khan Academy", "link": "https://www.khanacademy.org/"},
        {"title": "TutorialsPoint", "link": "https://www.tutorialspoint.com/"},
        {"title": "DevDocs", "link": "https://devdocs.io/"},
    ],
    "Data Science": [
        {"title": "Kaggle", "link": "https://www.kaggle.com/"},
        {"title": "StatQuest", "link": "https://statquest.org/"},
        {"title": "RStudio Education", "link": "https://education.rstudio.com/"},
        {"title": "Towards Data Science", "link": "https://towardsdatascience.com/"},
        {"title": "Analytics Vidhya", "link": "https://www.analyticsvidhya.com/"},
        {"title": "Machine Learning Mastery", "link": "https://machinelearningmastery.com/"},
    ],
    "Web Development": [
        {"title": "Mozilla Developer Network (MDN)", "link": "https://developer.mozilla.org/"},
        {"title": "Frontend Mentor", "link": "https://www.frontendmentor.io/"},
        {"title": "CodePen", "link": "https://codepen.io/"},
    ],
    "University-Level": [
        {"title": "OpenLearn", "link": "https://www.open.edu/openlearn/"},
        {"title": "Stanford Online", "link": "https://online.stanford.edu/"},
        {"title": "edX (Audit Mode)", "link": "https://www.edx.org/"},
    ],
    "Math": [
        {"title": "Paul's Online Math Notes", "link": "http://tutorial.math.lamar.edu/"},
        {"title": "Desmos", "link": "https://www.desmos.com/"},
        {"title": "Wolfram Alpha (Free Tier)", "link": "https://www.wolframalpha.com/"},
        {"title": "Brilliant (Free Tier)", "link": "https://brilliant.org/"},
    ],
    "Miscellaneous": [
        {"title": "Hussein Nasser YouTube", "link": "https://www.youtube.com/c/HusseinNasserYouTube"},
        {"title": "Gaurav Sen YouTube", "link": "https://www.youtube.com/c/GauravSen"},
        {"title": "FiveThirtyEight", "link": "https://fivethirtyeight.com/"},
        {"title": "Real Python", "link": "https://realpython.com/"},
    ],
    "Neural Networks & AI": [
        {"title": "DeepLearning.AI", "link": "https://www.deeplearning.ai/", "description": "Online courses and specializations on deep learning and AI."},
        {"title": "Fast.ai", "link": "https://www.fast.ai/", "description": "Free deep learning courses using PyTorch."},
        {"title": "TensorFlow Tutorials", "link": "https://www.tensorflow.org/tutorials", "description": "Hands-on guides for building neural networks using TensorFlow."},
        {"title": "PyTorch Tutorials", "link": "https://pytorch.org/tutorials/", "description": "Official PyTorch documentation and deep learning tutorials."},
        {"title": "Kaggle Learn", "link": "https://www.kaggle.com/learn", "description": "Short courses and hands-on coding for AI and ML."},
        {"title": "Google AI", "link": "https://ai.google/education/", "description": "AI and ML courses provided by Google."},
        {"title": "CS231n (Stanford)", "link": "http://cs231n.stanford.edu/", "description": "Stanford’s famous course on deep learning for computer vision."},
        {"title": "MIT OpenCourseWare (Deep Learning)", "link": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-867-machine-learning-fall-2006/", "description": "Free machine learning and deep learning courses from MIT."},
    ],
    "Advanced Networking": [
        {"title": "Cisco Networking Academy", "link": "https://www.netacad.com/", "description": "Networking, cybersecurity, and programming courses from Cisco."},
        {"title": "Computer Networking (Stanford CS144)", "link": "https://cs144.github.io/", "description": "Stanford’s official course on advanced networking."},
        {"title": "MIT OpenCourseWare (Computer Networks)", "link": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-829-computer-networks-fall-2002/", "description": "Advanced networking topics and concepts from MIT."},
        {"title": "Internet Engineering Task Force (IETF)", "link": "https://www.ietf.org/", "description": "Standards and protocols for networking professionals."},
        {"title": "Networking Tutorials (GCFGlobal)", "link": "https://edu.gcfglobal.org/en/computerbasics/understanding-computer-networking/1/", "description": "Basic to advanced networking concepts explained."},
        {"title": "Practical Networking", "link": "https://www.practicalnetworking.net/", "description": "Deep dive into networking, subnetting, firewalls, and more."},
        {"title": "PacketLife", "link": "https://packetlife.net/", "description": "Cheat sheets and labs for networking professionals."},
    ],
    "Cybersecurity & Ethical Hacking": [
        {"title": "Cybrary", "link": "https://www.cybrary.it/", "description": "Free and paid cybersecurity courses, including penetration testing."},
        {"title": "Hack The Box Academy", "link": "https://academy.hackthebox.com/", "description": "Hands-on labs for cybersecurity and ethical hacking."},
        {"title": "TryHackMe", "link": "https://tryhackme.com/", "description": "Beginner to advanced cybersecurity challenges and labs."},
        {"title": "OWASP", "link": "https://owasp.org/", "description": "Security standards and best practices for web application security."},
        {"title": "SANS Cyber Aces", "link": "https://www.cyberaces.org/", "description": "Free foundational cybersecurity training."},
        {"title": "PicoCTF", "link": "https://picoctf.org/", "description": "Capture The Flag (CTF) challenges to learn cybersecurity hands-on."},
        {"title": "Kali Linux Docs", "link": "https://www.kali.org/docs/", "description": "Official documentation for penetration testing with Kali Linux."},
        {"title": "Blue Team Labs Online", "link": "https://blueteamlabs.online/", "description": "Defensive cybersecurity challenges for blue team training."},
    ],
    "Operating Systems & Low-Level Computing": [
        {"title": "CS162 (Berkeley Operating Systems)", "link": "https://cs162.org/", "description": "Advanced OS concepts from UC Berkeley."},
        {"title": "The Linux Documentation Project", "link": "https://www.tldp.org/", "description": "Linux guides, tutorials, and deep technical explanations."},
        {"title": "OSDev.org", "link": "https://wiki.osdev.org/Main_Page", "description": "Resources for building your own operating system."},
        {"title": "Linux From Scratch", "link": "http://www.linuxfromscratch.org/", "description": "Learn to build your own Linux OS from source."},
        {"title": "MIT Operating Systems Course", "link": "https://pdos.csail.mit.edu/6.828/", "description": "MIT’s advanced operating system design course."},
    ],
    "Software Development & Programming": [
        {"title": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org/", "description": "Tutorials on data structures, algorithms, and programming languages."},
        {"title": "W3Schools", "link": "https://www.w3schools.com/", "description": "Step-by-step programming tutorials for web development."},
        {"title": "MDN Web Docs", "link": "https://developer.mozilla.org/", "description": "Official documentation for web development and JavaScript."},
        {"title": "CS50 (Harvard)", "link": "https://cs50.harvard.edu/", "description": "Harvard’s famous introduction to computer science."},
        {"title": "The Odin Project", "link": "https://www.theodinproject.com/", "description": "Full-stack development roadmap and tutorials."},
        {"title": "FreeCodeCamp", "link": "https://www.freecodecamp.org/", "description": "Free interactive coding courses and certifications."},
        {"title": "LeetCode", "link": "https://leetcode.com/", "description": "Coding challenges and interview prep for software engineers."},
    ],
    "Data Science & Big Data": [
        {"title": "KDNuggets", "link": "https://www.kdnuggets.com/", "description": "Tutorials, news, and guides for data science."},
        {"title": "DataCamp", "link": "https://www.datacamp.com/", "description": "Interactive courses for Python, R, and data analysis."},
        {"title": "Coursera (Data Science Specialization)", "link": "https://www.coursera.org/specializations/jhu-data-science", "description": "Data science specialization by Johns Hopkins University."},
        {"title": "Towards Data Science", "link": "https://towardsdatascience.com/", "description": "Blog articles and guides on AI, ML, and data science."},
    ],
    # Add more categories and resources as needed
}

# views.py

# views.py
from django.contrib import messages
from django.http import JsonResponse
from result_analysis.models import Review
def find_course_view(request):
    query = request.GET.get('search', '').strip()
    
    # Save the search query to the SearchHistory model if it exists
    if query:
        SearchHistory.objects.create(user=request.user, query=query)
    
    # Initialize empty lists for results and recommendations
    combined_results = []
    recommendations = []
    all_reviews = []  # List to hold all reviews related to the search query

    # Only filter courses and resources if there is a query
    if query:
        # Filter courses based on title and platform
        courses = Course.objects.filter(Q(title__icontains=query) | Q(platform__icontains=query))
        
        # Combine courses into a single list
        for course in courses:
            combined_results.append({
                'type': 'course',
                'title': course.title,
                'url': course.url,
                'platform': course.platform,
                'id': course.id,  # Ensure the course ID is included
            })

        # Fetch reviews for the keyword and add to all_reviews
        all_reviews = Review.objects.filter(keyword=query)  # Fetch reviews based on the keyword

        # Filter resources based on the query
        filtered_resources = {}
        for category, resources in RESOURCES.items():
            matching_resources = [resource for resource in resources if query.lower() in resource['title'].lower() or query.lower() in category.lower()]
            if matching_resources:
                filtered_resources[category] = matching_resources

        # Add resources to combined results
        for category, resource_list in filtered_resources.items():
            for resource in resource_list:
                combined_results.append({
                    'type': 'resource',
                    'title': resource['title'],
                    'url': resource['link'],
                    'platform': category
                })

        # Get recommendations based on previous searches and the current query
        recommendations = get_recommendations(request.user, query)

    # Handle review submission
    if request.method == 'POST': 
        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.keyword = query  # Associate the review with the keyword
            review.save()  # Save the review to the database

            # Fetch all reviews again after saving
            all_reviews = Review.objects.filter(keyword=query)

            # Debug output to verify saved reviews
            print(f"All reviews for '{query}': {[review.comment for review in all_reviews]}")  # Debug output

            return JsonResponse({
                'username': review.user.username,
                'comment': review.comment,
                'rating': review.rating
            })

    # Prepare context for rendering the template
    context = {
        'combined_results': combined_results,
        'query': query,
        'recommendations': recommendations,
        'all_reviews': all_reviews,  # Pass all reviews to the context
        'review_form': ReviewForm(),  # Pass an empty form for rendering
    }
    
    return render(request, 'result_analysis/find_course.html', context)


from .forms import ReviewForm


'''
def get_recommendations(user, current_query):
    # Get the last search queries made by the user
    last_searches = SearchHistory.objects.filter(user=user).order_by('-timestamp')[:5]
    recommended_results = []

    # Check if the current query is not empty
    if current_query:
        # Find courses that match the current search query
        courses = Course.objects.filter(Q(title__icontains=current_query) | Q(platform__icontains=current_query))
        for course in courses:
            recommended_results.append({
                'type': 'course',
                'title': course.title,
                'url': course.url,
                'platform': course.platform
            })

        # Find resources that match the current search query
        for category, resources in RESOURCES.items():
            matching_resources = [resource for resource in resources if current_query.lower() in resource['title'].lower()]
            for resource in matching_resources:
                recommended_results.append({
                    'type': 'resource',
                    'title': resource['title'],
                    'url': resource['link'],
                    'platform': category
                })

    # If no recommendations found based on the current query, fall back to last searches
    if not recommended_results:
        for search in last_searches:
            # Find courses that match the last search query
            courses = Course.objects.filter(Q(title__icontains=search.query) | Q(platform__icontains=search.query))
            for course in courses:
                recommended_results.append({
                    'type': 'course',
                    'title': course.title,
                    'url': course.url,
                    'platform': course.platform
                })

            # Find resources that match the last search query
            for category, resources in RESOURCES.items():
                matching_resources = [resource for resource in resources if search.query.lower() in resource['title'].lower()]
                for resource in matching_resources:
                    recommended_results.append({
                        'type': 'resource',
                        'title': resource['title'],
                        'url': resource['link'],
                        'platform': category
                    })

    # Remove duplicates by converting to a set and back to a list
    recommended_results = list({result['title']: result for result in recommended_results}.values())

    return recommended_results
'''

from sklearn.neighbors import NearestNeighbors
import pandas as pd

from sklearn.neighbors import NearestNeighbors
import numpy as np

def get_recommendations(user, current_query):
    # Get the last search queries made by the user
    last_searches = SearchHistory.objects.filter(user=user).order_by('-timestamp')[:5]
    recommended_results = []

    # Prepare data for KNN
    resource_titles = [resource['title'] for category, resources in RESOURCES.items() for resource in resources]
    resource_links = {resource['title']: resource['link'] for category, resources in RESOURCES.items() for resource in resources}
    
    # Create feature vectors for resources (this is a placeholder; implement your own feature extraction)
    resource_vectors = np.array([extract_features(title) for title in resource_titles])

    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=3)  # Adjust n_neighbors as needed
    knn.fit(resource_vectors)

    # Transform the current query into a feature vector
    query_vector = extract_features(current_query).reshape(1, -1)

    # Find nearest neighbors
    distances, indices = knn.kneighbors(query_vector)

    # Collect recommended resources based on nearest neighbors
    for index in indices[0]:
        recommended_results.append({
            'type': 'resource',
            'title': resource_titles[index],
            'url': resource_links[resource_titles[index]],  # Get the link from the dictionary
            'platform': 'Recommended'
        })

    # If no recommendations found based on the current query, fall back to last searches
    if not recommended_results:
        for search in last_searches:
            # Find courses that match the last search query
            courses = Course.objects.filter(Q(title__icontains=search.query) | Q(platform__icontains=search.query))
            for course in courses:
                recommended_results.append({
                    'type': 'course',
                    'title': course.title,
                    'url': course.url,
                    'platform': course.platform
                })

            # Find resources that match the last search query
            for category, resources in RESOURCES.items():
                matching_resources = [resource for resource in resources if search.query.lower() in resource['title'].lower()]
                for resource in matching_resources:
                    recommended_results.append({
                        'type': 'resource',
                        'title': resource['title'],
                        'url': resource['link'],
                        'platform': category
                    })

    # Remove duplicates by converting to a set and back to a list
    recommended_results = list({result['title']: result for result in recommended_results}.values())

    return recommended_results

def extract_features(title):
    # Implement your feature extraction logic here
    # For example, you could use TF-IDF, word embeddings, etc.
    # This is a placeholder function that should return a numerical representation of the title.
    return np.array([len(title)])  # Example: using the length of the title as a feature
"""
def get_recommendations(query):
    # Prepare data for KNN
    resource_data = []
    resource_titles = []

    # Populate resource data for KNN
    for category, resources in RESOURCES.items():
        for resource in resources:
            resource_data.append([1 if query.lower() in resource['title'].lower() else 0])  # Binary indicator
            resource_titles.append(resource['title'])

    # Convert to DataFrame
    resource_df = pd.DataFrame(resource_data, columns=['interaction'])

    # Fit KNN model
    if len(resource_df) > 1:  # Ensure there are enough samples
        knn = NearestNeighbors(n_neighbors=min(3, len(resource_df) - 1), metric='cosine')
        knn.fit(resource_df)

        # Create a query vector for the current search
        query_vector = [[1 if query.lower() in title.lower() else 0 for title in resource_titles]]
        
        # Find neighbors based on the query interaction
        distances, indices = knn.kneighbors(query_vector)

        # Get recommended resources based on neighbors
        recommended_results = []
        for index in indices.flatten():
            recommended_results.append({
                'title': resource_titles[index],
                'link': RESOURCES[resource_titles[index]]  # Assuming you want to link to the resource
            })

        return recommended_results

    return []
"""
from django.http import JsonResponse

# Simple chatbot logic
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure you have the necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

def generate_response(user_input):
    # Tokenize and lemmatize the user input
    tokens = word_tokenize(user_input.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Simple intent recognition based on keywords
    if any(token in ["hi", "hello"] for token in lemmatized_tokens):
        return "Hello! How can I assist you today?"
    elif any(token in ["help", "assistance"] for token in lemmatized_tokens):
        return "Sure! What do you need help with?"
    elif any(token in ["resource", "resources"] for token in lemmatized_tokens):
        return "You can find resources on our Resources page. Would you like me to direct you there?"
    elif any(token in ["bye"] for token in lemmatized_tokens):
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        response = generate_response(user_input)
        return JsonResponse({'response': response})

    return render(request, 'result_analysis/chatbot.html')


from django.db.models import Avg

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = course.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_detail', course_id=course.id)
    else:
        review_form = ReviewForm()

    return render(request, 'result_analysis/find_course.html', {
        'course': course,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
    })

from result_analysis.models import Bookmark  # Ensure Bookmark is imported

#@login_required
#def bookmark_course(request):
    #if request.method == 'POST':
        #course_id = request.POST.get('course_id')
        #course = get_object_or_404(Course, id=course_id)
        
        # Create the bookmark
        #bookmark, created = Bookmark.objects.get_or_create(user=request.user, resource=course)
        
        #if created:
           ## return JsonResponse({'status': 'success', 'message': 'Course bookmarked successfully!'})
        #else:
            #return JsonResponse({'status': 'error', 'message': 'Course already bookmarked.'})
    
    #return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

#@login_required
#def view_bookmarks(request):
    #bookmarks = Bookmark.objects.filter(user=request.user)
   #return render(request, 'result_analysis/bookmarks.html', {'bookmarks': bookmarks})


@login_required
def bookmark_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    resource_id = course.id  # Assuming the resource_id is the same as the course ID

    try:
        # Create or get the bookmark, providing the resource_id
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'resource_id': resource_id}
        )

        if created:
            return JsonResponse({'message': 'Bookmark created successfully.'})
        else:
            return JsonResponse({'message': 'Bookmark already exists.'})

    except Exception as e:
        # Log the error for debugging
        print(f"Error creating bookmark: {e}")
        return JsonResponse({'error': 'An error occurred while bookmarking the course. Please try again.'}, status=500)
    return redirect('result_analysis/find_course.html')  
@login_required
def view_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('course')
    return render(request, 'view_bookmarks.html', {'bookmarks': bookmarks})




# views.py
from django.shortcuts import render, redirect

# myapp/views.py
from django.shortcuts import render, redirect
from .models import TimetableEntry

#def timetable_landing(request):
    #return render(request, 'result_analysis/create_timetable.html')


# result_analysis/views.py
from django.contrib.auth.decorators import login_required
from sklearn.cluster import KMeans
from django.shortcuts import render, redirect
from .models import Timetable
import pandas as pd

@login_required
def timetable_landing(request):
    if request.method == 'POST':
        # Get user input
        subjects_data = []
        for i in range(int(request.POST.get('subject_count', 0))):
            name = request.POST.get(f'subject_name_{i}')
            difficulty = int(request.POST.get(f'difficulty_{i}'))
            time_required = int(request.POST.get(f'time_required_{i}'))
            importance = int(request.POST.get(f'importance_{i}'))
            subjects_data.append({'name': name, 'difficulty': difficulty, 'time_required': time_required, 'importance': importance})

        # Create DataFrame
        df = pd.DataFrame(subjects_data)

        # K-means clustering
        kmeans = KMeans(n_clusters=3)  # You can adjust the number of clusters
        df['cluster'] = kmeans.fit_predict(df[['difficulty', 'time_required', 'importance']])

        # Sort subjects by cluster and difficulty (descending)
        df = df.sort_values(by=['cluster', 'difficulty'], ascending=[True, False])
        df = df.sample(frac=1).reset_index(drop=True)

        # Define days of the week and realistic time slots
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        time_slots = [
            ("8:00 AM", "9:00 AM"),
            ("9:00 AM", "10:00 AM"),
            ("10:00 AM", "10:15 AM"),  # Break
            ("10:15 AM", "11:15 AM"),
            ("11:15 AM", "12:15 PM"),
            ("12:15 PM", "1:00 PM"),  # Lunch Break
            ("1:00 PM", "2:00 PM"),
            ("2:00 PM", "3:00 PM"),
            ("3:00 PM", "3:15 PM"),  # Break
            ("3:15 PM", "4:15 PM"),
            ("4:15 PM", "5:15 PM"),
            ("5:15 PM", "6:15 PM"),
            ("6:15 PM", "7:15 PM"),
            ("7:15 PM", "8:00 PM"),  # Dinner Break
            ("8:00 PM", "9:00 PM"),
        ]

        # Create timetable structure
        timetable = {day: [] for day in days_of_week}

        # Distribute subjects across the week
        day_index = 0
        for index, row in df.iterrows():
            subject_info = {
                'name': row['name'],
                'time_required': row['time_required'],
                'difficulty': row['difficulty']
            }
            # Allocate time based on difficulty
            while subject_info['time_required'] > 0:
                for slot in time_slots:
                    if subject_info['time_required'] > 0:
                        # Check if the current slot is a break
                        if slot[1] == "10:15 AM" or slot[1] == "3:15 PM" or slot[1] == "7:15 PM":  # Break slots
                            timetable[days_of_week[day_index]].append({
                                'time_slot': f"{slot[0]} – {slot[1]}",
                                'activity': "BREAK"
                            })
                        else:
                            # Add subject to timetable
                            timetable[days_of_week[day_index]].append({
                                'time_slot': f"{slot[0]} – {slot[1]}",
                                'activity': subject_info['name']
                            })
                            subject_info['time_required'] -= 1  # Decrease time required by 1 hour
                    if subject_info['time_required'] == 0:
                        break
                day_index = (day_index + 1) % len(days_of_week)  # Cycle through the days

        # Add a day off for Sunday
        timetable['Sunday'] = [{'time_slot': '-', 'activity': 'Day Off / Relax'}]

        # Save the timetable to the database
        Timetable.objects.create(user=request.user, timetable_data=timetable)

        # Redirect to a success page or render the timetable
        return render(request, 'result_analysis/timetable_result.html', {'timetable': timetable, 'success': True})

    # Prepare a list of difficulty and importance levels
    difficulty_range = list(range(1, 6))
    return render(request, 'result_analysis/create_timetable.html', {'difficulty_range': difficulty_range})

# result_analysis/views.py
@login_required
def view_saved_timetables(request):
    saved_timetables = Timetable.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'result_analysis/view_saved_timetables.html', {'saved_timetables': saved_timetables})

import json
@login_required
def save_timetable(request):
    if request.method == 'POST':
        # Debugging: Print the raw POST data
        print(request.POST)  # Log the entire POST data
        timetable_data = request.POST.get('timetable_data')

        # Check if timetable_data is empty
        if not timetable_data:
            print("No timetable data received.")
            messages.error(request, "No timetable data received.")
            return redirect('result_analysis/timetable_landing.html')  # Redirect or handle the error as needed

        try:
            timetable_data = json.loads(timetable_data)  # Attempt to decode the JSON
            Timetable.objects.create(user=request.user, timetable_data=timetable_data)
            messages.success(request, 'Your timetable has been saved successfully!')
            return redirect('result_analysis/view_saved_timetables.html')
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            messages.error(request, "Failed to save timetable. Invalid data.")
            return redirect('result_analysis/timetable_landing.html')  # Redirect or handle the error as needed
        
def timetable_questions(request):
    # Initialize session variables if this is the first request
    if 'step' not in request.session:
        request.session['step'] = 0
        request.session['answers'] = {}

    # Process the form data if the request method is POST
    if request.method == 'POST':
        question_list = get_question_list()
        current_step = request.session['step']
        
        if current_step < len(question_list):
            request.session['answers'][question_list[current_step]['key']] = request.POST.get('answer')
            request.session['step'] += 1

        # Check if we have reached the last question
        if request.session['step'] >= len(question_list):
            timetable = generate_timetable(request.session['answers'])
            return render(request, 'timetable/timetable_result.html', {'timetable': timetable})

    # Render the current question
    question_list = get_question_list()
    current_step = request.session.get('step', 0)
    
    if current_step < len(question_list):
        question = question_list[current_step]
        total_questions = len(question_list)
        return render(request, 'result_analysis/timetable_question.html', {
            'question': question,
            'current_index': current_step + 1,
            'total_questions': total_questions
        })

    return redirect('result_analysis/timetable_landing')

def get_question_list():
    return [
        {
            'key': 'modules',
            'text': 'What modules or subjects are you currently studying? (comma-separated)',
            'type': 'text'
        },
        {
            'key': 'available_days',
            'text': 'Which days of the week are you available to study?',
            'type': 'multi-select',
            'options': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        {
            'key': 'study_hours',
            'text': 'How many hours per day can you realistically study?',
            'type': 'number'
        },
        {
            'key': 'preferred_time',
            'text': 'What time of day do you prefer to study?',
            'type': 'dropdown',
            'options': ['Morning (8 AM – 12 PM)', 'Afternoon (12 PM – 4 PM)', 'Evening (4 PM – 8 PM)']
        },
        {
            'key': 'session_length',
            'text': 'Do you prefer long or short study sessions?',
            'type': 'radio',
            'options': ['Short (30–45 minutes)', 'Medium (1 hour)', 'Long (1.5–2 hours)']
        },
        {
            'key': 'add_breaks',
            'text': 'Do you want breaks to be automatically added between sessions?',
            'type': 'yes_no'
        },
        {
            'key': 'specific_tasks',
            'text': 'Are there any specific tasks or goals you\'d like to include? (Optional)',
            'type': 'textarea'
        },
        {
            'key': 'fixed_commitments',
            'text': 'Do you have any fixed commitments during the day? (e.g., part-time job, gym, classes)',
            'type': 'textarea'
        },
        {
            'key': 'study_free_weekends',
            'text': 'Do you prefer to have study-free weekends?',
            'type': 'yes_no'
        },
    ]

def generate_timetable(answers):
    timetable = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    
    modules = answers.get('modules', '').split(',')
    available_days = answers.get('available_days', [])
    study_hours = int(answers.get('study_hours', 0))
    preferred_time = answers.get('preferred_time', 'Morning (8 AM – 12 PM)')
    session_length = answers.get('session_length', 'Medium (1 hour)')
    add_breaks = answers.get('add_breaks', 'No') == 'Yes'
    specific_tasks = answers.get('specific_tasks', '')
    study_free_weekends = answers.get('study_free_weekends', 'No') == 'Yes'

    if session_length == 'Short (30–45 minutes)':
        session_length_hours = 0.5
    elif session_length == 'Medium (1 hour)':
        session_length_hours = 1
    else:
        session_length_hours = 1.5

    for day in available_days:
        if day in timetable:
            total_sessions = study_hours // session_length_hours
            for i in range(total_sessions):
                                if add_breaks and i > 0:
                                    timetable[day].append({'module': 'Break', 'time': '10-30 minutes'})
                                    timetable[day].append({
                    'module': modules[i % len(modules)].strip(),
                    'time': f"{preferred_time} - Session {i + 1}"
                    })

    # If the user prefers study-free weekends, clear Saturday and Sunday
    if study_free_weekends:
        timetable['Saturday'] = []
        timetable['Sunday'] = []

    # Add specific tasks to the timetable if provided
    if specific_tasks:
        tasks = specific_tasks.split(',')
        for day in available_days:
            if day in timetable:
                for task in tasks:
                    timetable[day].append({
                        'module': task.strip(),
                        'time': 'Flexible'
                    })

    return timetable


from .models import CourseRating  # Assuming you have a model for storing ratings

def submit_rating(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        # Save the rating to the database
        CourseRating.objects.create(rating=rating)  # Adjust this according to your model
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



from .forms import FeedbackForm

def contact_us(request):
    feedback_form = FeedbackForm()

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user if request.user.is_authenticated else None  # Optional: link to user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('result_analysis/contact.html')  # Redirect to the same page or another page

    return render(request, 'result_analysis/contact.html', {'feedback_form': feedback_form})