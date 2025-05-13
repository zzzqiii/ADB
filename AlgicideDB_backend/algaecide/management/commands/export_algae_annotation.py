from django.core.management.base import BaseCommand
from django.db.models import Count
from algaecide.models import AlgaeSpecies
import csv


class Command(BaseCommand):
    help = "Export AlgaeSpecies data (including Unique Chemical Count, environment, and risk) to a CSV file"

    def handle(self, *args, **kwargs):
        # 统计每个物种的唯一 Chemical 数量
        species_with_annotations = AlgaeSpecies.objects.annotate(
            unique_chemical_count=Count('strains__record__chemical', distinct=True)
        )

        # 定义 CSV 文件的路径
        csv_file_path = "algae_annotations.csv"

        # 创建 CSV 文件并写入数据
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)

            # 写入表头
            csvwriter.writerow(["Species", "Phylum", "Unique Chemical Count", "Environment", "Risk"])

            # 写入数据
            for species in species_with_annotations:
                csvwriter.writerow([
                    species.name,
                    species.phylum,
                    species.unique_chemical_count,
                    species.environment if species.environment else "Unknown",
                    species.risk if species.risk else "Unknown"
                ])

        self.stdout.write(self.style.SUCCESS(f"CSV exported successfully to {csv_file_path}"))
