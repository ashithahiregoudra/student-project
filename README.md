# student-result-analysis



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.cs.bham.ac.uk/axh1342/student-result-analysis.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.cs.bham.ac.uk/axh1342/student-result-analysis/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.


## Name
EDUVISTA: ENHANCING STUDENT ACCESS TO STUDY RESOURCES, PERSONALIZED GUIDANCE, AND SCHEDULE OPTIMIZATION IN COMPUTER SCIENCE EDUCATION


 
## Description
TheEduVista project is a web application designed to help students find relevant courses and resources based on their search queries. It utilizes a K-Nearest Neighbors (KNN) algorithm to recommend educational resources from a resources and crawled webpages. The application also alows users to create their personalized timetable which uses K-Means Clustering to generate timetable that organizes the day according to the subject difficulty and time required for each subject.

## Badges
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

![Django Version](https://img.shields.io/badge/django-5.1.4-brightgreen)


## Visuals
![EduVista Homepage](static/images/Screenshot%2025-04-13%20at%209.54.47%20AM.png)  
*Screenshot of the EduVista application homepage.*

![EduVista Find a Course Page](static/images/Screenshot%2025-04-13%20at%209.57.52%20AM.png)  
*Screenshot of the EduVista application find a course page.*

![EduVista Timetable Generation Page](static/images/Screenshot%2025-04-13%20at%209.58.03%20AM.png)  
*Screenshot of the EduVista application timetable generation page.*

## Installation
To make it easy for you to get started with EduVista, follow these steps:
1. Clone the repository:
   git clone git@git.cs.bham.ac.uk:projects-2024-25/axh1342.git
   cd student-result-analysis

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate

3. Install the required packages:
   pip install -r requirements.txt

4. Set up your database:
   python manage.py migrate
   python manage.py runserver

## Usage
Access the application at http://127.0.0.1:8000/.
Use the login page to access your account or register a new account.
Explore the various features including course recommendations, study resources, and timetable generation.

## Support
For help, please open an issue in the GitLab repository or contact the project maintainers.


## Roadmap
Implement additional features for enhanced user experience.
Integrate more educational platforms for resource scraping.
Improve the recommendation algorithm for better accuracy.


## Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new merge request.


## Authors and acknowledgment
Ashitha Hiregoudra - Project Lead


