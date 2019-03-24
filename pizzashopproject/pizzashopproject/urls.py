from django.contrib import admin
from django.urls import path, include
from pizzashopapp import views,apis

from django.contrib.auth.views import LoginView, LogoutView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('pizzashop/sign-in/', LoginView.as_view(template_name='pizzashop/sign_in.html'),name='pizzashop-sign-in'),
    path('pizzashop/sign-out/', LogoutView.as_view(next_page='/'),name='pizzashop-sign-out'),
    path('pizzashop/', views.pizzashop_home, name='pizzashop-home'),
    path('pizzashop/sign-up/', views.pizzashop_sign_up, name='pizzashop-sign-up'),
    path('pizzashop/account/', views.pizzashop_account, name='pizzashop-account'),
    path('pizzashop/pizza/', views.pizzashop_pizza, name='pizzashop-pizza'),
    path('pizzashop/pizza/edit/', views.pizzashop_add_pizza, name='pizzashop-add-pizza'),
    path('pizzashop/pizza/edit/<int:pizza_id>', views.pizzashop_edit_pizza, name='pizzashop-edit-pizza'),
    #APIS
    path('api/client/pizzashops/', apis.client_get_pizzashops),
    path('api/client/pizzas/<int:pizzashop_id>', apis.client_get_pizzas),

    # Sign In / Sign Up / Sign Out
    path('api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in / sign up)
    # /revoke-token (sign out)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)