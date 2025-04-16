# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .models import Course  

def save_courses(courses):
    for course in courses:
        if course['link']:  
            Course.objects.update_or_create(
                title=course['title'],
                url=course['link'],
                defaults={'platform': course.get('platform', 'Unknown')}
            )
        else:
            print(f"Skipping course with missing URL: {course['title']}")

def scrape_geeksforgeeks():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.geeksforgeeks.org/courses/")
    time.sleep(5) 

    courses = []
    course_elements = driver.find_elements(By.CLASS_NAME, "course-card")

    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h3").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        courses.append({"title": title, "link": link, "platform": "GeeksforGeeks"})

    driver.quit()
    return courses

def scrape_kaggle():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.kaggle.com/learn")
    time.sleep(5)  

    courses = []
    course_elements = driver.find_elements(By.CLASS_NAME, "sc-1g6z4g0-0")  

    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h3").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        courses.append({"title": title, "link": link, "platform": "Kaggle"})

    driver.quit()
    return courses

def scrape_cs50():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://cs50.harvard.edu/")
    time.sleep(5)  

    courses = []
    course_elements = driver.find_elements(By.CLASS_NAME, "course")  
    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h3").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        courses.append({"title": title, "link": link, "platform": "CS50"})

    driver.quit()
    return courses

def scrape_mit_ocw():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://ocw.mit.edu/courses/")
    time.sleep(5)  

    courses = []
    course_elements = driver.find_elements(By.CLASS_NAME, "course-title")  

    for course in course_elements:
        title = course.text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        courses.append({"title": title, "link": link, "platform": "MIT OpenCourseWare"})

    driver.quit()
    return courses

def scrape_khan_academy():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.khanacademy.org/courses")
    time.sleep(5) 
    courses = []
    course_elements = driver.find_elements(By.CLASS_NAME, "KACourse")  

    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h3").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        courses.append({"title": title, "link": link, "platform": "Khan Academy"})

    driver.quit()
    return courses

def scrape_tutorialspoint():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.tutorialspoint.com/tutorialslibrary.htm")
    time.sleep(5)  

    courses = []
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".tutorial-list a")  

    for course in course_elements:
        title = course.text
        link = course.get_attribute("href")
        if title and link:  # Ensure both title and link are present
            courses.append({"title": title, "link": link, "platform": "TutorialsPoint"})
        else:
            print(f"Skipping course with missing title or link: {title}, {link}")

    driver.quit()
    return courses

def scrape_freecodecamp():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.freecodecamp.org/learn")
    time.sleep(5) 

    courses = []
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".curriculum-card")  

    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h3").text
        link = course.get_attribute("href") 
        if title and link:  
            courses.append({"title": title, "link": link, "platform": "FreeCodeCamp"})
        else:
            print(f"Skipping course with missing title or link: {title}, {link}")

    driver.quit()
    return courses

def scrape_classcentral():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.classcentral.com/subjects")
    time.sleep(5) 

    courses = []
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".subject-course") 

    for course in course_elements:
        title = course.find_element(By.TAG_NAME, "h 3").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        if title and link:  
            courses.append({"title": title, "link": link, "platform": "Class Central"})
        else:
            print(f"Skipping course with missing title or link: {title}, {link}")

    driver.quit()
    return courses

def scrape_datacamp():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.datacamp.com/courses/all")
    time.sleep(5)  

    courses = []
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".course-list-item")  

    for course in course_elements:
        title = course.find_element(By.CLASS_NAME, "title").text
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
        if title and link:  
            courses.append({"title": title, "link": link, "platform": "DataCamp"})
        else:
            print(f"Skipping course with missing title or link: {title}, {link}")

    driver.quit()
    return courses

def scrape_w3schools():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.w3schools.com/")
    time.sleep(5)  

    courses = []
    
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".w3-bar .w3-button")  

    for course in course_elements:
        title = course.text
        link = course.get_attribute("href")
        
        if title and link and "javascript:void(0)" not in link:  
            courses.append({"title": title, "link": link, "platform": "W3Schools"})
        else:
            print(f"Skipping course with missing title or link: {title}, {link}")

    driver.quit()
    return courses
def scrape_courses():
    all_courses = []
    
    all_courses.extend(scrape_geeksforgeeks())
    all_courses.extend(scrape_kaggle())
    all_courses.extend(scrape_cs50())
    all_courses.extend(scrape_mit_ocw())
    all_courses.extend(scrape_khan_academy())
    all_courses.extend(scrape_tutorialspoint())
    all_courses.extend(scrape_freecodecamp())
    all_courses.extend(scrape_classcentral())
    all_courses.extend(scrape_datacamp())
    all_courses.extend(scrape_w3schools())

    
    save_courses(all_courses)
