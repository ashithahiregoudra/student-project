# crawler.py

from .models import Course
from .scraper import scrape_geeksforgeeks, scrape_kaggle, scrape_cs50, scrape_mit_ocw, scrape_khan_academy, scrape_tutorialspoint, scrape_freecodecamp, scrape_classcentral, scrape_datacamp, scrape_w3schools

def save_courses(courses):
    for course in courses:
        if course['link']:  # Check if the link is not empty
            Course.objects.update_or_create(
                title=course['title'],
                url=course['link'],
                defaults={'platform': course.get('platform', 'Unknown')}
            )
        else:
            print(f"Skipping course with missing URL: {course['title']}")

def scrape_courses():
    all_courses = []
    
    gfg_courses = scrape_geeksforgeeks()
    all_courses.extend(gfg_courses)

    kaggle_courses = scrape_kaggle()
    all_courses.extend(kaggle_courses)

    cs50_courses = scrape_cs50()
    all_courses.extend(cs50_courses)

    mit_courses = scrape_mit_ocw()
    all_courses.extend(mit_courses)

    khan_courses = scrape_khan_academy()
    all_courses.extend(khan_courses)

    tutorialspoint_courses = scrape_tutorialspoint()
    all_courses.extend(tutorialspoint_courses)

    freecodecamp_courses = scrape_freecodecamp()
    all_courses.extend(freecodecamp_courses)

    classcentral_courses = scrape_classcentral()
    all_courses.extend(classcentral_courses)

    datacamp_courses = scrape_datacamp()
    all_courses.extend(datacamp_courses)

    w3schools_courses = scrape_w3schools()
    all_courses.extend(w3schools_courses)

    # Save all scraped courses to the database
    save_courses(all_courses)