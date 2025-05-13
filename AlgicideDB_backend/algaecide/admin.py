
from django.contrib import admin
from .models import Algae, Chemical, Reference, Record, AlgaeSpecies, AlgaeStrain
from unfold.admin import ModelAdmin


@admin.action(description="Duplicate selected records")
def duplicate_record(modeladmin, request, queryset):
    for record in queryset:
        # 创建当前记录的副本
        record.pk = None  # 重置主键
        record.effect = None  # 将 effect 字段设置为空或你想要的默认值
        record.save()  # 保存为新记录
def duplicate_algae(modeladmin, request, queryset):
    for record in queryset:
        # 创建当前记录的副本
        record.pk = None  # 重置主键
        record.save()  # 保存为新记录

# admin.site.unregister(Algae)
# @admin.register(Algae)
# class AlgaeAdmin(ModelAdmin):
#     list_display = ('name', 'phylum', 'class_name', 'order', 'family', 'strain', 'toxicity_type', 'environment', 'image', 'description')
#     search_fields = ['name', 'phylum', 'class_name', 'order', 'family', 'environment', 'toxicity_type']
#     # list_filter = ['toxicity_type']
#     actions = [duplicate_algae]
#     ordering = ['name', 'strain']

@admin.register(Chemical)
class ChemicalAdmin(ModelAdmin):
    list_display = ('name', 'note','label', 'form', 'origin', 'classification', 'source', 'isnp', 'smiles', 'pubchem')
    search_fields = ['name', 'classification', 'source', 'np_classification', 'casNumber', 'smiles']
    list_filter = ['isnp', 'origin', 'form', 'classification']

# 创建内联模型来展示与 Reference 关联的所有 Record 和 Chemical
class RecordInline(admin.TabularInline):
    model = Record
    extra = 0  # 不显示空白的行
    fields = ['algae_strain', 'chemical', 'measurement', 'effect', 'unit', 'reference']
    readonly_fields = ['chemical', 'algae_strain', 'measurement', 'effect', 'unit']  # 不允许直接编辑的字段

@admin.register(Reference)
class ReferenceAdmin(ModelAdmin):
    list_display = ('title', 'note', 'is_plant', 'is_microorganism', 'is_animal','np_source', 'toxicity_check', 'publication_title', 'publication_year', 'author', 'doi', 'url')
    search_fields = ['title', 'author', 'doi','publication_title']
    # list_filter = ['is_checked', 'is_derivative']
    list_filter = ['is_plant', 'is_microorganism', 'is_animal','is_derivative']
    # list_editable = ('is_checked',)
    list_editable = ('is_plant', 'is_microorganism', 'is_animal')
    inlines = [RecordInline]

@admin.register(AlgaeSpecies)
class AlgaeSpeciesAdmin(ModelAdmin):
    # list_display = ('name','risk', 'note', 'empire', 'kingdom', 'is_checked','phylum', 'class_name', 'order', 'family', 'image_source')# 'risk', 'environment')
    list_display = ('name', 'image_copyright', 'image_source', 'risk', 'note', 'empire', 'kingdom', 'is_checked','phylum', 'class_name', 'order', 'family')# 'risk', 'environment')
    search_fields = ['name', 'phylum', 'class_name', 'order', 'family', 'environment', 'image_source']
    ordering = ['name']
    list_filter = ['risk', 'image_copyright']
    list_editable = ('image_copyright', 'is_checked','risk','empire', 'kingdom')
    actions = [duplicate_algae]

@admin.register(AlgaeStrain)
class AlgaeStrainAdmin(ModelAdmin):
    list_display = ['species', 'strain']
    search_fields = ['species__name', 'strain']
    list_filter = ['species']
    ordering = ['species__name', 'strain']


from django.urls import reverse
from django.utils.html import format_html


@admin.register(Record)
class RecordAdmin(ModelAdmin):
    # 显示的字段
    list_display = ('algae_strain', 'get_chemical_link','response_endpoint', 'other_measurements', 'time', 'measurement', 'effect', 'reference')
    list_editable = ['response_endpoint']

    # 配置搜索和过滤
    search_fields = ['chemical__name', 'reference__title']
    list_filter = ['reference', 'algae_strain', 'chemical']  # 允许按 Reference 过滤
    actions = [duplicate_record]

    # 配置链接字段，显示 Chemical 的链接
    def get_chemical_link(self, obj):
        url = reverse('admin:%s_%s_change' % ('algaecide', 'chemical'), args=[obj.chemical.pk])
        return format_html('<a href="{}">{}</a>', url, obj.chemical.name)

    # 设置字段标题
    get_chemical_link.short_description = 'Chemical'

    # 每页显示多少条
    list_per_page = 20

    # 获取与指定 Reference 相关的所有 Record
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 如果 URL 中有 reference 参数，则过滤 Record
        if 'reference__id__exact' in request.GET:
            reference_id = request.GET['reference__id__exact']
            qs = qs.filter(reference__id=reference_id)
        return qs.select_related('algae_strain', 'chemical', 'reference')

    def save(self, *args, **kwargs):
        # 仅更新变更部分，避免重复保存外键关联
        if not self.pk:
            # 新建时的额外逻辑
            super().save(*args, **kwargs)
        else:
            super().save(update_fields=['algae_strain', 'chemical', 'reference'])  # 仅更新特定字段

from .models import SubmittedData, PredictionTask

@admin.register(SubmittedData)
class SubmittedDataAdmin(ModelAdmin):
    list_display = ('id', 'status', 'submitted_at')  # 列表显示的字段
    list_filter = ('status', 'submitted_at')  # 过滤器
    search_fields = ('id',)  # 搜索字段
    ordering = ('-submitted_at',)  # 默认按提交时间降序排列
    list_editable = ('status',)  # 允许直接在列表中编辑状态

@admin.register(PredictionTask)
class PredictionTaskAdmin(ModelAdmin):
    list_display = ('id', 'created_at', 'completed_at', 'task_id')
    search_fields = ('id', 'task_id')
