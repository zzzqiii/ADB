import csv
from django.core.management.base import BaseCommand
from algaecide.models import AlgaeSpecies


class Command(BaseCommand):
    help = 'Update the risk field of AlgaeSpecies based on a CSV file'

    def handle(self, *args, **options):
        # 直接指定 CSV 文件路径
        csv_file_path = 'algae_annotations1211.csv'  # 替换为你的实际路径

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)  # 以字典形式读取 CSV 文件
                for row in reader:
                    species_name = row['Species']
                    risk_category = row['Risk']

                    try:
                        # 尝试获取对应的 AlgaeSpecies 对象
                        algae_species = AlgaeSpecies.objects.get(name=species_name)
                        algae_species.risk = risk_category  # 更新 risk 字段
                        algae_species.save()  # 保存更改
                        self.stdout.write(
                            self.style.SUCCESS(f"Updated {species_name}: risk set to {risk_category}")
                        )
                    except AlgaeSpecies.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Species {species_name} not found in database, skipping...")
                        )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing expected column in CSV: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
