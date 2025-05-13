from django.core.management.base import BaseCommand
from algaecide.models import Reference, Record, Chemical, Algae, AlgaeStrain
import csv

class Command(BaseCommand):
    help = '导出不同类型的参考文献及其关联的 Chemical 和 Algae'

    def add_arguments(self, parser):
        # 添加命令行参数，指定要导出的文献类型
        parser.add_argument(
            '--reference_type',
            choices=['plant', 'microorganism', 'animal'],  # 可选参数
            default='plant',  # 默认是 plant
            help='指定文献类型 (plant, microorganism, animal)'
        )

    def handle(self, *args, **kwargs):
        reference_type = kwargs['reference_type']
        
        # 根据参数选择对应的查询条件
        if reference_type == 'plant':
            references = Reference.objects.filter(is_plant=True)
        elif reference_type == 'microorganism':
            references = Reference.objects.filter(is_microorganism=True)
        elif reference_type == 'animal':
            references = Reference.objects.filter(is_animal=True)

        # 定义 CSV 文件路径
        csv_file_path = f'output_{reference_type}_references.csv'

        # 打开文件并写入数据
        with open(csv_file_path, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['Reference Title', 'Source', 'Algicide', 'Test algae'])  # CSV 标题行

            for reference in references:
                # 获取与文献相关的所有记录
                records = Record.objects.filter(reference=reference)
                source = reference.np_source

                # 存储所有与此文献相关的 chemical 和 algae 名称
                chemicals = set()
                algae_species = set()

                for record in records:
                    # 直接获取与记录关联的 Chemical 和 AlgaeStrain 名称
                    chemical = record.chemical
                    species = record.algae_strain.species
                    
                    if chemical:
                        chemicals.add(chemical.name)  # 添加 Chemical 名称
                    
                    if species:
                        algae_species.add(species.name)  # 添加 AlgaeStrain 名称

                # 将 chemicals 和 algae_species 转换为以逗号分隔的字符串
                chemicals_str = ', '.join(chemicals)
                algae_species_str = ', '.join(algae_species)

                # 写入每个文献的数据
                writer.writerow([reference.title, source, chemicals_str, algae_species_str])

        self.stdout.write(self.style.SUCCESS(f'数据已成功导出到 {csv_file_path}'))
