from django.core.management.base import BaseCommand
from result_analysis.scraper import scrape_courses  # Import the function that orchestrates scraping

class Command(BaseCommand):
    help = "Runs the course web scraper"

    def handle(self, *args, **kwargs):
        scrape_courses()
        self.stdout.write(self.style.SUCCESS("Successfully scraped courses!"))
