import os
# import pandas as pd
from django.core.management.base import BaseCommand
from algaecide.models import Chemical  # 替换为你的实际应用名称
import csv

class Command(BaseCommand):
    help = 'Export all Chemical data to an Excel file'

    def handle(self, *args, **kwargs):
        # output_file = kwargs['output']

        csv_file_path = "chemicals1213_id_name_smiles.csv"

        # 获取所有 Chemical 数据
        # chemicals = Chemical.objects.all()

        # # 准备数据
        # data = []
        # writer.writerow([
        #         "Empire",
        #         "Kingdom",
        #         "Phylum",
        #         "Class",
        #         "Order",
        #         "Family",
        #         "Genus",
        #         "Species",
        #         # "Environment",
        #         # "Risk",
        #     ])
        # for chem in chemicals:
        #     data.append({
        #         "Name": chem.name,
        #         "Classification": chem.classification,
        #         "Source": chem.source,
        #         "NP Classification": chem.np_classification,
        #         "CAS Number": chem.casNumber,
        #         "PubChem Name": chem.pubchem_name,
        #         "PubChem CID": chem.pubchem_cid,
        #         "SMILES": chem.smiles,
        #         "InChI": chem.InChI,
        #         "Origin": chem.origin,
        #         'NP': chem.isnp,
        #         "PubChem Link": chem.pubchem,
        #         # "Note": chem.note,
        #     })

        # # 转换为 Pandas DataFrame
        # df = pd.DataFrame(data)

        # # 导出为 Excel 文件
        # try:
        #     df.to_csv(csv_file_path, index=False)
        #     self.stdout.write(self.style.SUCCESS(f'Chemical data exported successfully to {csv_file_path}'))
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f'Error exporting data: {e}'))


        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            chemicals = Chemical.objects.all()

            # Write header row
            writer.writerow([
                'ID',
               "Name",
                # "Classification",
                # "Source",
                # "NP Classification",
                # "CAS Number",
                # "PubChem Name",
                # "PubChem CID",
                "SMILES",
                # "InChI",
                # "Origin",
                # 'Form',
                # 'NP',
                # "PubChem Link",
            ])

            # Write data rows
            for chem in chemicals:
                writer.writerow([
                    chem.id,
                    chem.name,
                    # chem.classification,
                    # chem.source,
                    # chem.np_classification,
                    # chem.casNumber,
                    # chem.pubchem_name,
                    # chem.pubchem_cid,
                    chem.smiles,
                    # chem.InChI,
                    # chem.origin,
                    # chem.form,
                    # chem.isnp,
                    # chem.pubchem,
                ])

        self.stdout.write(self.style.SUCCESS(f"Data exported successfully to {csv_file_path}"))
