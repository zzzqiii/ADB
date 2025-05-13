import csv
from algaecide.models import Algae

def import_algae_data(file_path):
    with open(file=file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Algae.objects.create(
                name = row['name'],
                phylum=row['phylum'],
                class_name=row['class'],
                order=row['order'],
                family=row['family'],
                environment=row['environment'] if row['environment'] else None,
                toxicity_type=row['toxicity_type'] if row['toxicity_type'] else None
            )

#在根目录下导入数据
#python manage.py shell
#from algaecide.import_algae import import_algae_data
#import_algae_data("../data/Algae.csv")