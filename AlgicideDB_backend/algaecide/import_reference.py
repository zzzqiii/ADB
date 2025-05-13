import csv
from django.core.management.base import BaseCommand
from algaecide.models import Reference  # 替换为你的app名称

def import_reference_data(file_path):
    with open(file=file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Reference.objects.create(
                    publication_year=int(row['Publication Year']),
                    author=row['Author'],
                    title=row['Title'],
                    publication_title=row['Publication Title'],
                    doi=row['DOI'] if row['DOI'] else None,
                    url=row['Url'] if row['Url'] else None
                )
#在根目录下导入数据
#python manage.py shell
#from algaecide.import_reference import import_reference_data
#import_reference_data("../data/Literature.csv")          