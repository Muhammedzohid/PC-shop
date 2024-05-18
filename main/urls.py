
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index, name="index"),
    # ---------AUTH-------------
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('user/edit/', views.edit_user, name='user_edit'),
    # ---------ENTER PRODUCT-------------
    path('enter-product/create/', views.create_enter_product, name='create_enter_product'),
    path('enter-product/list/', views.enter_product_list, name='enter_product_list'),
    path('enter-product/<str:code>/', views.enter_product_detail, name='enter_product_detail'),
    # ---------PRODUCT-------------
    path('product/create/', views.create_product, name='create_product'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/delete/<str:code>/', views.delete_product, name='delete_product'),
    path('product/<str:code>/update/', views.update_product, name='update_product'),
    path('product/<str:code>/', views.product_detail, name='product_detail'),
    # ---------CATEGORY-------------
    path('category/list/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<str:code>/update/', views.category_update, name='category_update'),
    path('category/<str:code>/delete/', views.category_delete, name='category_delete'),
    # ---------SELL PRODUCT-------------
    path('sell-product/list/', views.sellproduct_list, name='sellproduct_list'),
    path('sell-product/create/', views.sellproduct_create, name='sellproduct_create'),
    path('sell-product/<str:code>/', views.sellproduct_detail, name='sellproduct_detail'),
    path('sell-product/<str:code>/update/', views.sellproduct_update, name='sellproduct_update'),
    # ---------REFUND-------------
    path('refund/<str:code>/',views.refund,name="refund"),
    path('refund-list/',views.refund_list, name="refund_list"),
    path('refund-detail/<int:id>/',views.refund_detail,name="refund_detail"),
    # ---------FOYDA HISOB KITOB-------------
    path('filter/',views.filter,name="filter"),
    path('filter-entries/', views.filter_entries, name='filter_entries'),
]
