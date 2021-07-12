from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/add_stock/', views.StockViews.as_view()),
    path('api/v1/get_stock/', views.StockViews.as_view()),
    path('api/v1/get_stock/<int:id>/',
         views.get_ticker_id, name='get_by_id'),
    path('api/v1/get_ticker_data/<ticker>/',
         views.get_ticker_data, name='get_ticker_data'),
   
    path('api/v1/delete_stock/<int:id>/', views.StockViews.as_view()),
    path('api/v1/activate_stock/<int:id>/', views.StockViews.as_view()),
    path('', views.index, name='index'),
]
