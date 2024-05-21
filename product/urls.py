from django.urls import path
from django.views.decorators.cache import cache_page
from product.views import ProductListView, ProductDetailView, contacts, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView, CategoryCreateView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('view/<int:pk>/',  cache_page(60 * 15)(ProductDetailView.as_view()), name='view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('contacts/', contacts, name='contacts'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create')

]

