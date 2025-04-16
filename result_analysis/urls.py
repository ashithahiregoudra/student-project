from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),  # Homepage
    path('login/', views.login_view, name='login'),  # Login page
    path('results/', views.results, name='results'),  # Result analysis page
    path('resources/', views.resources, name='resources'),  # Tutoring resources page
    path('contact/', views.contact, name='contact'),  # Contact us page
    path('tutorial-resources/', views.tutorial_resources, name='tutorial_resources'),  # Tutorial resources page
    path('study-resources/', views.study_resources, name='study_resources'),  # Study resources page
    path('study_resources_finance/', views.study_resources_finance, name='study_resources_finance'),
    path('find-course/', views.find_course_view, name='find_course'),
    path('chatbot/', views.chatbot_view, name='chatbot_view'),
    #path("search/", views.search_courses, name="search_courses"),
    path('study-analysis/', views.study_analysis, name='study_analysis'),  # New input form view
    path('student-analysis/', views.student_analysis, name='student_analysis'),  # New URL for student analysis
    path('results-analysis/', views.results_analysis, name='results_analysis'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('track-click', views.track_click, name='track_click'),
    path('additional-study-methods/', views.additional_study_methods, name='additional_study_methods'),  
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),  # Course detail page
    #path('course/<int:course_id>/bookmark/', views.bookmark_course, name='bookmark_course'),
    #path('bookmarks/', views.view_bookmarks, name='view_bookmarks'),  # View bookmarks,
    path('course/<int:course_id>/bookmark/', views.bookmark_course, name='bookmark_course'),
    path('bookmarks/', views.view_bookmarks, name='view_bookmarks'),
    #path('timetable/', views.timetable_landing, name='timetable_landing'),
    #path('questions/', views.timetable_questions, name='timetable_questions'),
    path('timetable/', views.timetable_landing, name='timetable_landing'),  
    path('view_saved_timetables/', views.view_saved_timetables, name='view_saved_timetables'),
    path('save_timetable/', views.save_timetable, name='save_timetable'), 
    path('submit_rating/', views.submit_rating, name='submit_rating'),

]
