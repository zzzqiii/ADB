import csv
from django.core.management.base import BaseCommand
from django.db.models import Count
from algaecide.models import Record


class Command(BaseCommand):
    help = 'Export chemical frequency from Record'

    def handle(self, *args, **kwargs):
        # 获取每个化学品的出现次数，并同时获取化学品的SMILES
        chemical_counts = (
            Record.objects
            .values('chemical__name', 'chemical__smiles')  # 获取chemical的name和smiles字段
            .annotate(count=Count('chemical'))  # 按照chemical计数
            .order_by('-count')  # 按照计数降序排序
        )

        # 将数据写入CSV文件
        with open('chemical_frequency.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Frequency', 'SMILES'])  # 添加SMILES列

            # 将化学品名称、频次和SMILES写入文件
            for entry in chemical_counts:
                writer.writerow([entry['chemical__name'], entry['count'], entry['chemical__smiles']])

        self.stdout.write(self.style.SUCCESS('Data exported successfully to chemical_frequency.csv'))
