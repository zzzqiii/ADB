
from django.contrib import admin
from .models import Algae, Chemical, Reference, Record, AlgaeSpecies, AlgaeStrain, Measurement
from unfold.admin import ModelAdmin
# Register your models here.
# from .models import Algaecide, Algae, Chemical, Reference


# class AlgaecideAdmin(admin.ModelAdmin):
#     list_display = ('id','algae', 'chemical', 'initialDensity','time')
#     list_filter = ('algae', 'chemical')
#     search_fields = ['id','algae', 'chemical']
    # prepopulated_fields = {'slug': ('title',)}
# admin.site.register(Algaecide)
# admin.site.register(Algae)
# admin.site.register(Chemical)
# admin.site.register(Reference)
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
    list_display = ('name', 'classification', 'source', 'np_classification', 'casNumber', 'isnp', 'smiles', 'pubchem')
    search_fields = ['name', 'classification', 'source', 'np_classification', 'casNumber', 'smiles']
    list_filter = ['isnp']

@admin.register(Reference)
class ReferenceAdmin(ModelAdmin):
    list_display = ('title', 'is_checked', 'publication_title', 'publication_year', 'author', 'doi', 'url')
    search_fields = ['title', 'author', 'doi']
    list_filter = ['is_checked']
    list_editable = ('is_checked',)

@admin.register(AlgaeSpecies)
class AlgaeSpeciesAdmin(ModelAdmin):
    list_display = ('name', 'phylum', 'class_name', 'order', 'family', 'risk', 'environment')
    search_fields = ['name', 'phylum', 'class_name', 'order', 'family', 'environment', 'toxicity_type']
    ordering = ['name']

@admin.register(AlgaeStrain)
class AlgaeStrainAdmin(ModelAdmin):
    list_display = ('species', 'strain')
    search_fields = ['species', 'strain']
    list_filter = ['species']
    ordering = ['species__name', 'strain']

@admin.register(Measurement)
class MeasurementAdmin(ModelAdmin):
    list_display = ('time', 'unit', 'effect')
    search_fields = ['time', 'unit', 'effect']
    # ordering = ['name']



# class RecordAdmin(admin.ModelAdmin):
#     list_display = ('algae', 'chemical', 'measurement', 'effect')  # 显示字段
#     actions = [duplicate_record]  # 添加自定义 action




# @admin.register(Record)
class RecordAdmin(ModelAdmin):
    list_display = ('algae_strain','chemical', 'measurement', 'time', 'effect', 'unit', 'other_measurements', 'initialDensity', 'reference')
    search_fields = ['algae_strain', 'chemical', 'time', 'reference']
    list_filter = ['algae_strain', 'chemical']
    list_display_links = ('algae_strain',) 
    actions = [duplicate_record]  # 添加自定义 action
    list_editable = ('chemical', 'measurement', 'time', 'effect', 'unit', 'initialDensity', 'reference')

admin.site.register(Record, RecordAdmin)