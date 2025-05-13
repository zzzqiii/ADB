

# 路由列表
# urlpatterns = []

# router = DefaultRouter()  # 可以处理视图的路由器
# router.register('algae', views.AlgaeTreeViewSet, 'algae')     # add this
# router.register('algaecide', views.AlgaecideViewSet, 'algaecide')
# router.register('chemical', views.ChemicalViewSet, 'chemical')
# router.register('reference', views.ReferenceViewSet, 'reference')
# router.register('algaeInfo', views.AlgaeGridViewSet, basename='algaeInfo')

# urlpatterns += router.urls
from . import views
from .views import AlgaeViewSet, ChemicalViewSet, RecordViewSet, ReferenceViewSet, StatsView, AlgaeSpeciesViewSet, AlgaeStrainViewSet, AlgaecideSearchView #, update_chemical_form
from .views import PredictMoleculeView, PredictionResultView, GeneralSearchView, AdvancedSearchView, SubmitRecordView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import download_example_file
router = DefaultRouter()

router.register(r'algae', AlgaeViewSet)
router.register(r'chemical', ChemicalViewSet)
router.register(r'record', RecordViewSet)
router.register(r'reference', ReferenceViewSet)
router.register(r'algaespecies', AlgaeSpeciesViewSet)  # Route for species
router.register(r'algaestrain', AlgaeStrainViewSet)  # Route for strains



urlpatterns = [
    # path('update-chemical-form/', update_chemical_form, name='update_chemical_form'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('', include(router.urls)),
    # path('search/', AlgaecideSearchView.as_view(), name='algaecide-search'),
    # path('search/general/', views.general_search, name='general_search'),
    path('search/general/', GeneralSearchView.as_view(), name='general_search'),
    # path('search/advanced/', views.advanced_search, name='advanced_search'),
    path('search/advanced/', AdvancedSearchView.as_view(), name='advanced_search'),
    # path('submit/', views.submit_record, name='submit_record'),
    path('submit/', SubmitRecordView.as_view(), name='submit_record'),
    path('predict/', PredictMoleculeView.as_view(), name='predict_molecule'),
    path('predict/result/<str:task_id>/', PredictionResultView.as_view(), name='prediction_result'),
    path('download/<str:filename>/', download_example_file, name='download_example_file'),
]
