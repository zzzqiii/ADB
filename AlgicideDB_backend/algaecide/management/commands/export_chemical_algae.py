import csv
from django.core.management.base import BaseCommand
from algaecide.models import Record

class Command(BaseCommand):
    help = 'Export records with chemical name and algae species name to a CSV file'

    def handle(self, *args, **kwargs):
        # 获取所有Record数据并提取chemical和algae_strain（对应的AlgaeSpecies）
        records = Record.objects.select_related('chemical', 'algae_strain__species').all()

        # 创建一个集合用于去重
        unique_data = set()

        # 遍历Record对象并提取需要的数据
        for record in records:
            chemical_name = record.chemical.name if record.chemical else ''
            algae_species = record.algae_strain.species if record.algae_strain else None
            algae_species_name = algae_species.name if algae_species else ''
            algae_species_phylum = algae_species.phylum if algae_species else ''

            # 将化学品和藻类物种的名字作为一个元组添加到集合中（去重）
            if chemical_name and algae_species_name:
                # 使用元组替代列表来确保去重，且包含三个值
                unique_data.add((chemical_name, algae_species_name, algae_species_phylum))

        # 写入CSV文件
        with open('chemical_algae_species.csv', mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Chemical Name', 'Algae Species Name', 'Phylum'])

            # 写入去重后的数据
            for data in unique_data:
                # 直接写入整个元组
                writer.writerow(data)

        self.stdout.write(self.style.SUCCESS('Data exported successfully to chemical_algae_species.csv'))
