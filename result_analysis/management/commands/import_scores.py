# import_scores.py
import csv
from django.core.management.base import BaseCommand
from result_analysis.models import StudentScore

class Command(BaseCommand):
    help = 'Import student scores from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Convert WklyStudyHours to a float, handling non-numeric values
                    wkly_study_hours = self.convert_study_hours(row['WklyStudyHours'])

                    StudentScore.objects.create(
                        gender=row['Gender'],
                        ethnic_group=row['EthnicGroup'],
                        parent_education=row['ParentEduc'],
                        lunch_type=row['LunchType'],
                        test_preparation=row['TestPrep'],
                        parent_marital_status=row['ParentMaritalStatus'],
                        practice_sport=row['PracticeSport'] == 'Yes',  # Convert to boolean
                        is_first_child=row['IsFirstChild'] == 'Yes',  # Convert to boolean
                        nr_siblings=int(row['NrSiblings']),
                        transport_means=row['TransportMeans'],
                        wkly_study_hours=wkly_study_hours,
                        math_score=float(row['MathScore']),
                        reading_score=float(row['ReadingScore']),
                        writing_score=float(row['WritingScore']),
                    )
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to error: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported student scores'))

    def convert_study_hours(self, value):
        """Convert study hours to a float, handling special cases."""
        if value.startswith('<'):
            return 4.0  # Assuming '< 5' means less than 5 hours, you can set a default value
        elif value.startswith('>'):
            return 6.0  # Assuming '> 5' means more than 5 hours, you can set a default value
        else:
            return float(value)  # Convert to float if it's a valid number
