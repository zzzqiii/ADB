# from rest_framework.viewsets import ModelViewSet
# from .models import Algaecide, Algae, Reference, Chemical
# from .serializers import AlgaecideModelSerializer, AlgaeTreeSerializer, ReferenceModelSerializer, ChemicalModelSerializer, AlgaeInfoSerializer




# class AlgaecideViewSet(ModelViewSet):
#     queryset = Algaecide.objects.all()
#     serializer_class = AlgaecideModelSerializer


# class ReferenceViewSet(ModelViewSet):
#     queryset = Reference.objects.all()
#     serializer_class = ReferenceModelSerializer


# class ChemicalViewSet(ModelViewSet):
#     queryset = Chemical.objects.all()
#     serializer_class = ChemicalModelSerializer


# class AlgaeTreeViewSet(ModelViewSet):
#     # queryset = Algae.objects.all()
#     queryset = Algae.objects.filter(parentCategory=None)
#     serializer_class = AlgaeTreeSerializer


# class AlgaeGridViewSet(ModelViewSet):
#     queryset = Algae.objects.filter(children=None)
#     serializer_class = AlgaeInfoSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         key, description = "", ""
#         if self.request.query_params.get('key'):
#             key = self.request.query_params.get('key')
#             queryset = Algae.objects.filter(key=key)
#         # description = self.request.query_params.get('description')
#         if self.request.query_params.get('description'):
#             description = self.request.query_params.get('description')
#             queryset = Algae.objects.filter(description=description)
#         return queryset

from rest_framework import viewsets
from .models import Algae
from .serializers import AlgaeSerializer
from .models import Chemical
from .serializers import ChemicalSerializer
from .models import Record
from .serializers import RecordSerializer
from .models import Reference
from .serializers import ReferenceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

class AlgaeViewSet(viewsets.ModelViewSet):
    queryset = Algae.objects.all()
    serializer_class = AlgaeSerializer

# 生成ChemicalViewSet视图集

class ChemicalViewSet(viewsets.ModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']  # Enable filtering by the 'name' field

    # Custom filtering logic
    def get_queryset(self):
        chemical_name = self.request.query_params.get('name')
        if chemical_name:
            # Filter by the chemical name if provided in the query parameters
            return Chemical.objects.filter(name=chemical_name)
        return super().get_queryset()

# 生成RecordViewSet视图集

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['time', 'algae__id', 'algae__name', 'chemical__name', 'chemical__id']

    def get_queryset(self):
        # 获取查询参数
        species_name = self.request.query_params.get('species')
        chemical_id = self.request.query_params.get('chemical')

        # 根据查询参数过滤数据
        if species_name:
            return Record.objects.filter(algae__species__name=species_name)
        if chemical_id:
            return Record.objects.filter(chemical__id=chemical_id)

        # 如果没有查询参数，返回空结果
        return Record.objects.none()

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['time', 'algae_strain__id', 'algae_strain__species__name', 'chemical__name', 'chemical__id', 'algae_strain__species__id']

    # def get_queryset(self):
    #     species_name = self.request.query_params.get('species')
    #     if species_name:
    #         # Update to filter using algae_strain and species name
    #         return Record.objects.filter(algae_strain__species__name=species_name)
    #     return super().get_queryset()


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class StatsView(APIView):
    """
    API View to retrieve counts of algae, records, chemicals, and references.
    """
    def get(self, request):
        algae_count = Algae.objects.count()
        record_count = Record.objects.count()
        chemical_count = Chemical.objects.count()
        reference_count = Reference.objects.count()
        
        data = {
            'algae_count': algae_count,
            'record_count': record_count,
            'chemical_count': chemical_count,
            'reference_count': reference_count
        }
        
        return Response(data)


from .models import AlgaeSpecies, AlgaeStrain
from .serializers import AlgaeSpeciesSerializer, AlgaeStrainSerializer

# ViewSet for AlgaeSpecies
class AlgaeSpeciesViewSet(viewsets.ModelViewSet):
    queryset = AlgaeSpecies.objects.all()
    serializer_class = AlgaeSpeciesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phylum', 'class_name', 'order', 'family']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return AlgaeSpecies.objects.filter(name=name)
        return super().get_queryset()

# ViewSet for Algae (Strains)
class AlgaeStrainViewSet(viewsets.ModelViewSet):
    queryset = AlgaeStrain.objects.all()
    serializer_class = AlgaeStrainSerializer


from rest_framework import status
from django.db.models import Q



class AlgaecideSearchView(APIView):
    def get(self, request, *args, **kwargs):
        # Get query parameters
        general_search = request.query_params.get('generalSearch', None)
        advanced_queries = request.query_params.getlist('advancedQueries', [])

        # Initialize empty queryset
        result_set = None

        # General Search: Apply a broad filter across models
        if general_search:
            result_set = AlgaeSpecies.objects.filter(
                Q(name__icontains=general_search) |
                Q(phylum__icontains=general_search) |
                Q(environment__icontains=general_search)
            ).distinct()

        # Advanced Queries: Dynamically filter based on fields and values
        for query in advanced_queries:
            field = query.get('field')
            value = query.get('value')
            logic = query.get('logic', 'AND')

            # If no result_set exists, initialize it
            if result_set is None:
                result_set = AlgaeSpecies.objects.all()

            # Add filters dynamically
            if field and value:
                query_filter = Q(**{f"{field}__icontains": value})
                if logic == 'AND':
                    result_set = result_set.filter(query_filter)
                elif logic == 'OR':
                    result_set = result_set | AlgaeSpecies.objects.filter(query_filter)

        # Serialize and return the results
        serializer = AlgaeSpeciesSerializer(result_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['PATCH'])
# def update_chemical_form(request):
#     """
#     批量更新 Chemical 表的 form 字段，检查 isnp 字段和 name 字段的值。
#     """
#     if not request.data:
#         return Response({"detail": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         # 批量获取需要更新的Chemical对象
#         chemicals = Chemical.objects.filter(isnp=False).exclude(name__icontains='extract')

#         # 遍历并更新每个chemical对象的form字段
#         for chemical in chemicals:
#             if 'extract' in chemical.name.lower():
#                 chemical.form = 'Extract'
#             else:
#                 chemical.form = 'Isolated Compound'
#             chemical.save()

#         return Response({"detail": f"{len(chemicals)} chemicals updated."}, status=status.HTTP_200_OK)
    
#     except Exception as e:
#         return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import AlgaeSpecies, Chemical, Record, Reference
from .serializers import AlgaeSpeciesSerializer, ChemicalSerializer, RecordSerializer, ReferenceSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import AlgaeSpecies, Chemical, Record, Reference
from .serializers import AlgaeSpeciesSerializer, ChemicalSerializer, RecordSerializer, ReferenceSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from .models import Record
from .serializers import RecordSerializer
from rest_framework.pagination import PageNumberPagination


class RecordPagination(PageNumberPagination):
    page_size = 10  # 每页返回 50 条
    page_size_query_param = 'page_size'
    max_page_size = 200  # 最大每页返回 200 条

    def paginate_queryset(self, queryset, request, view=None):
        print("Page:", request.query_params.get('page'))
        print("Page size:", request.query_params.get('page_size'))
        return super().paginate_queryset(queryset, request, view)

# 
@api_view(['POST'])
@csrf_exempt
def advanced_search(request):
    """
    搜索 Record 模型并返回所有结果 (根据前端高级搜索条件)
    """
    # 获取前端传递的高级查询条件
    advanced_queries = request.data.get('advancedQueries', [])
    if not advanced_queries:
        return Response({"error": "Advanced queries are required."}, status=400)
    
    print(advanced_queries)
    advanced_queries[0]['logic'] = 'AND'

    # 使用 Haystack 查询构建动态条件
    sqs = SearchQuerySet()
    for query in advanced_queries:
        field = query.get('field', '').strip()
        value = query.get('value', '').strip()
        logic = query.get('logic', 'AND').strip().upper()

        if not field or not value:
            continue

        if logic == 'AND':
            sqs = sqs.filter(**{field: value})
        elif logic == 'OR':
            sqs = sqs.filter_or(**{field: value})

    # 筛选出 Record 模型的结果
    record_ids = [result.object.id for result in sqs if result.model_name == 'record']
    queryset = Record.objects.filter(id__in=record_ids).select_related('chemical', 'algae_strain__species')

    # 序列化所有数据
    serializer = RecordSerializer(queryset, many=True)

    return Response(serializer.data)




# @api_view(['POST'])
# def general_search(request):
#     """
#     搜索 Record 模型并分页返回结果
#     """
#     general_search = request.data.get('generalSearch', '').strip()

#     if not general_search:
#         return Response({"error": "generalSearch parameter is required."}, status=400)

#     # 使用 Haystack 查询
#     results = SearchQuerySet().filter(content=general_search)

#     # 筛选出 Record 模型的结果
#     record_ids = [result.object.id for result in results if result.model_name == 'record']

#     # 查询集排序，避免 UnorderedObjectListWarning
#     queryset = Record.objects.filter(id__in=record_ids).select_related('chemical', 'algae_strain__species').order_by('id')

#     # 分页处理
#     paginator = RecordPagination()
#     page = paginator.paginate_queryset(queryset, request)

#     # 序列化分页数据
#     serializer = RecordSerializer(page, many=True)
#     print(paginator.get_paginated_response(serializer.data))

#     return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def general_search(request):
    """
    搜索 Record 模型并返回所有结果
    """
    general_search = request.data.get('generalSearch', '').strip()

    if not general_search:
        return Response({"error": "generalSearch parameter is required."}, status=400)

    # 使用 Haystack 查询
    results = SearchQuerySet().filter(content=general_search)

    # 筛选出 Record 模型的结果
    record_ids = [result.object.id for result in results if result.model_name == 'record']
    queryset = Record.objects.filter(id__in=record_ids).select_related('chemical', 'algae_strain__species')

    # 序列化所有数据
    serializer = RecordSerializer(queryset, many=True)
    # print(serializer.data)

    return Response(serializer.data)



from .models import SubmittedData

@api_view(['POST'])
def submit_record(request):
    """
    接收前端提交的数据并保存到 SubmittedData 模型
    """
    try:
        # 获取前端提交的数据
        data = request.data

        # 将数据存储到 SubmittedData 模型
        submission = SubmittedData.objects.create(data=data)

        return Response(
            {
                "message": "Record submitted successfully.",
                "submission_id": submission.id,
                "submitted_at": submission.submitted_at,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        print(f"Error: {e}")
        return Response(
            {"error": "Failed to submit record.", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

from rest_framework.parsers import MultiPartParser
import uuid

from .models import PredictionTask
from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
import pandas as pd
import numpy as np

def check_mol(smi, verbose=True):
    """检查 SMILES 的有效性"""
    try:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            if verbose:
                print(f"Invalid SMILES: {smi}")
            return False
        return mol
    except Exception as e:
        if verbose:
            print(f"Error processing {smi}: {str(e)}")
        return False

def cal_des_smiles(mol):
    """计算分子描述符"""
    CALCULATOR = MoleculeDescriptors.MolecularDescriptorCalculator(DES_LIST)
    # mol = Chem.MolFromSmiles(smi)
    # if mol is None:
        # return None  # 无法生成分子
    return dict(zip(DES_LIST, CALCULATOR.CalcDescriptors(mol)))

def desirability_function(x, o, a, b, c):
    """Desirability function"""
    return o + a * np.exp(-np.exp(-(x - b) / c) - (x - b) / c + 1)


def calculate_QEF(descriptors, params):
    """计算 Algicide-likeness (QEF)"""
    dfs = []
    for desc_name, value in descriptors.items():
        o, a, b, c, max_val = params[desc_name]
        df = desirability_function(value, o, a, b, c)
        df = max(0, min(1, df / max_val))
        if df <= 0:
            return 0
        dfs.append(np.log(df))

    return np.exp(np.mean(dfs))

# 参数设置
PARAMS = {
    'MolWt': (0.05172997668902932, 23.98897812580443, 274.10298343166295, -83.67918354614636, 24.040429752353507),
    'MolLogP': (1.010340072308135, 28.17347356242204, 2.723217408007047, 0.8764791074705932, 29.182810207657738),
    'NumAromaticRings': (-2.2084134913593676, 90.83647550199527, 1.1021705917769289, 1.2939373908433278, 88.62803097380666),
    'NumHDonors': (6.238305078818262, 119.76220179570254, 1.2595043460242754, 0.6991229021863644, 126.00012902408325),
    'NumHAcceptors': (-0.22858151907596394, 60.164875095748194, 2.6433898756687575, 1.681162322904614, 59.933819689755104),
    'NumRotatableBonds': (2.199917682311999, 49.96371738006346, 1.2513421117582801, 1.7716011946782175, 52.163600184895586),
}
DES_LIST = ['MolWt', 'NumHAcceptors', 'NumHDonors', 'MolLogP', 'NumRotatableBonds', 'NumAromaticRings']
import json

from rest_framework.parsers import JSONParser

class PredictMoleculeView(APIView):
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, format=None):
        print(request.data)
        # 检查是否有文件或 SMILES 输入
        file_data = None
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            file_data = uploaded_file.read().decode('utf-8')
            smiles_list = file_data.splitlines()
        elif 'smiles' in request.data:
            file_data = request.data['smiles']
            smiles_list = file_data.splitlines()
            print(smiles_list)
        else:
            return Response({'error': 'No input provided (file or SMILES).'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成任务 ID
        task_id = str(uuid.uuid4())

        # 处理 SMILES 数据
        
        df = pd.DataFrame({'smiles': smiles_list})

        # 检查 SMILES 有效性
        df['is_valid'] = df['smiles'].apply(check_mol)

        # 计算描述符 (包括无效 SMILES 占位)
        df['descriptors'] = df.apply(
            lambda row: cal_des_smiles(row['is_valid']) if row['is_valid'] else {desc: None for desc in DES_LIST},
            axis=1
        )

        # 展开描述符列
        descriptors_df = pd.json_normalize(df['descriptors'])
        df = pd.concat([df, descriptors_df], axis=1)

        # 计算 Algicide-likeness (QEF)
        df['QEF'] = df.apply(
            lambda row: calculate_QEF(row['descriptors'], PARAMS) if row['is_valid'] else None,
            axis=1
        )

        # 更新无效 SMILES
        df.loc[df['is_valid']==False, 'smiles'] = 'Invalid SMILES: ' + df['smiles']
        df = df.replace({np.nan: None})

        # 转换结果为 JSON 格式
        results = df.drop(columns=['descriptors', 'is_valid']).to_dict(orient='records')
        print(results)

        # 保存任务到数据库
        task = PredictionTask.objects.create(
            task_id=task_id,
            results=json.dumps(results, ensure_ascii=False),  # 保存为 JSON 字符串
            completed_at=timezone.now(),
        )

        # 返回响应
        return Response({'task_id': task_id, 'results': results}, status=status.HTTP_200_OK)


from .serializers import PredictionTaskSerializer
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
class PredictionResultView(RetrieveAPIView):
    queryset = PredictionTask.objects.all()
    serializer_class = PredictionTaskSerializer
    lookup_field = 'task_id'  # 使用 task_id 作为查询字段


from django.http import FileResponse, Http404
from django.conf import settings
import os

def download_example_file(request, filename):
    # 定义文件存放的目录路径（确保替换为实际路径）
    print(f"filename: {filename}")
    file_path = os.path.join(settings.STATICFILES_DIRS[0], filename)
    print(f"File path: {file_path}, filename: {filename}")
    print(file_path)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise Http404(f"File {filename} does not exist.")
    
    # 返回文件作为附件下载
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
