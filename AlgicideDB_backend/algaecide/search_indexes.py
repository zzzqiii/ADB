from haystack import indexes
from .models import Record, Chemical, AlgaeSpecies


class RecordIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Record 模型的全文索引定义，同时包含关联的 Chemical、AlgaeSpecies 和 Reference 模型字段
    """
    text = indexes.CharField(document=True, use_template=True)  # 主索引字段
    id = indexes.IntegerField(model_attr='id')  # Record ID 字段

    # Chemical 模型字段
    chemical_name = indexes.CharField(model_attr='chemical__name', null=True)  # Chemical 名称
    chemical_smiles = indexes.CharField(model_attr='chemical__smiles', null=True)  # Chemical SMILES
    chemical_classification = indexes.CharField(model_attr='chemical__classification', null=True)  # Chemical 分类
    chemical_cas = indexes.CharField(model_attr='chemical__casNumber', null=True)  # CAS 编号
    chemical_source = indexes.CharField(model_attr='chemical__source', null=True)  # 来源
    chemical_label = indexes.CharField(model_attr='chemical__label', null=True)  # 标签
    chemical_origin = indexes.CharField(model_attr='chemical__origin', null=True)

    # AlgaeSpecies 模型字段
    algae_name = indexes.CharField(model_attr='algae_strain__species__name', null=True)  # Algae 名称
    algae_environment = indexes.CharField(model_attr='algae_strain__species__environment', null=True)  # 环境描述
    algae_taxonomy = indexes.CharField(null=True)  # Algae 分类（拼接 phylum, class_name, order, family）

    # Record 模型字段
    endpoint = indexes.CharField(model_attr='measurement', null=True)  # 响应端点
    response = indexes.CharField(model_attr='response_endpoint', null=True)  # 效果值
    measurement = indexes.CharField(model_attr='measurement', null=True)

    # Reference 模型字段
    author = indexes.CharField(model_attr='reference__author', null=True)  # 作者
    journal_name = indexes.CharField(model_attr='reference__publication_title', null=True)  # 期刊名称
    publication_date = indexes.IntegerField(model_attr='reference__publication_year', null=True)  # 出版年份

    def get_model(self):
        """
        返回与此索引关联的模型
        """
        return Record

    def prepare_algae_taxonomy(self, obj):
        """
        拼接 Algae 的分类信息 (phylum, class_name, order, family)
        """
        species = obj.algae_strain.species
        if not species:
            return None

        taxonomy_parts = [
            species.phylum or '',
            species.class_name or '',
            species.order or '',
            species.family or ''
        ]
        return ', '.join(filter(None, taxonomy_parts))  # 拼接非空字段，以逗号分隔

    def index_queryset(self, using=None):
        """
        返回需要被索引的查询集
        """
        return self.get_model().objects.select_related(
            'chemical',
            'algae_strain__species',
            'reference'
        ).all()

