import openpyxl
from django.core.management.base import BaseCommand
from algaecide.models import Chemical

class Command(BaseCommand):
    help = 'Import label data from Excel file into Chemical model'

    # def add_arguments(self, parser):
    #     parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        # excel_file = kwargs['excel_file']
        excel_file = 'chemical1212_label.xlsx'
        
        # 打开Excel文件
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error opening Excel file: {e}"))
            return

        headers = [cell.value for cell in sheet[1]]

        # 获取 "ID" 和 "label" 列的索引
        try:
            id_index = headers.index('ID')
            label_index = headers.index('Label')
        except ValueError:
            self.stdout.write(self.style.ERROR(f"Error: Excel file must contain 'ID' and 'label' columns"))
            return

        # 遍历每一行，假设数据从第二行开始
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # 获取 ID 和 label 值
            chemical_id = row[id_index]
            label = row[label_index]

            try:
                # 查找 Chemical 对象，并更新 label 字段
                chemical = Chemical.objects.get(id=chemical_id)
                chemical.label = label
                chemical.save()

                self.stdout.write(self.style.SUCCESS(f"Updated label for {chemical.name}"))
            except Chemical.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Chemical with ID {chemical_id} does not exist"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating label for ID {chemical_id}: {e}"))