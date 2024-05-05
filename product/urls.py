from django.urls import path
from product.views import ProductListView, ProductDetailView, contacts, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view'),
    path('contacts/', contacts, name='contacts'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete')
]