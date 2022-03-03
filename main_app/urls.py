from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('beanies/', views.beanies_index, name='index'),
    path('beanies/<int:beanie_id>/', views.beanies_detail, name='detail'),
    path('beanies/create/', views.BeanieCreate.as_view(), name='beanies_create'),
    path('beanies/<int:pk>/update/', views.BeanieUpdate.as_view(), name='beanies_update'),
    path('beanies/<int:pk>/delete/', views.BeanieDelete.as_view(), name='beanies_delete'),
    path('accessories/', views.accessories_index, name='all_accessories'),
    path('accessories/<int:accessory_id>/', views.accessories_detail, name='accessorydetail'),
    path('accessories/create/', views.AccessoryCreate.as_view(), name='accessories_create'),
    path('accessories/<int:pk>/update/', views.AccessoryUpdate.as_view(), name='accessories_update'),
    path('accessories/<int:pk>/delete/', views.AccessoryDelete.as_view(), name='accessories_delete'),
    path('beanies/<int:beanie_id>/add_maintenance/', views.add_maintenance, name='add_maintenance'),
    path('beanies/<int:beanie_id>/assoc_accessory/<int:accessory_id>/', views.assoc_accessory, name='assoc_accessory'),
    path('beanies/<int:beanie_id>/dissoc_accessory/<int:accessory_id>/', views.dissoc_accessory, name='dissoc_accessory'),
    path('beanies/<int:beanie_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup')
]