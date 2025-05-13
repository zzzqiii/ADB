# from rest_framework import serializers
# from .models import Algae, Algaecide, Reference, Chemical


# class AlgaecideModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Algaecide
#         fields = "__all__"


# class ReferenceModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reference
#         fields = "__all__"

# class ChemicalModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chemical
#         fields = "__all__"


# class AlgaeTreeSerializer(serializers.ModelSerializer):
#     data=serializers.DictField()
#     # children = RecursiveField(many=True)

#     def to_representation(self, obj):
#         #Add any self-referencing fields here (if not already done)
#         if 'children' not in self.fields:
#             self.fields['children'] = AlgaeTreeSerializer(obj, many=True)      
#         return super(AlgaeTreeSerializer, self).to_representation(obj) 

#     class Meta:
#         model = Algae
#         fields = ('key', 'data', 'parentCategory')

# class AlgaeInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Algae
#         fields = ('key', 'description', 'image')


from rest_framework import serializers
from .models import Algae
from .models import Record
from .models import Chemical
from .models import Reference


class AlgaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algae
        fields = '__all__' #序列化所有字段


#化合物序列化器
class ChemicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemical
        fields = '__all__' #序列化所有字段

#参考文献序列化器
from .models import Reference
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__' #

#抑藻剂记录序列化器


from .models import AlgaeSpecies, AlgaeStrain

# Serializer for the AlgaeSpecies model
class AlgaeSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgaeSpecies
        fields = '__all__' #
        # fields = ['id', 'name', 'phylum', 'class_name', 'order', 'family', 'environment', 'risk', 'description', 'description_source', 'image', 'image_source']

# Serializer for the Algae model (strains)
class AlgaeStrainSerializer(serializers.ModelSerializer):
    # species = AlgaeSpeciesSerializer(read_only=True)  # Include species data

    species_name = serializers.CharField(source='species.name')  # 获取 species 的 name
    species_id = serializers.IntegerField(source='species.id')  # 获取 species 的 id
    strain = serializers.CharField(allow_null=True)

    class Meta:
        model = Algae
        fields = ['id', 'species_name', 'strain', 'species_id']


class RecordSerializer(serializers.ModelSerializer):
    algae = serializers.StringRelatedField()  # Shows strain and species together in a human-readable way
    algae_strain = AlgaeStrainSerializer()

    class Meta:
        model = Record
        fields = '__all__' #序列化所有字段
        depth = 1 #深度为1，即序列化外键关联的模型的字段


from .models import PredictionTask
import json
class PredictionTaskSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()  # 自定义字段

    class Meta:
        model = PredictionTask
        fields = ['task_id', 'results', 'created_at', 'completed_at']  # 指定需要返回的字段

    def get_results(self, obj):
        try:
            # 自动将存储为字符串的 JSON 反序列化为列表
            return json.loads(obj.results) if obj.results else None
        except (ValueError, TypeError) as e:
            print(f"Error deserializing results: {e}")
            return None