from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for dealer reviews view

    # ✅ path for add a review view
    path(route='add_review', view=views.add_review, name='add_review'),

    # ✅ path for getting cars (CarMake + CarModel)
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # ✅ paths for getting dealerships
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # ✅ path for getting a specific dealer by ID
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # ✅ path for getting reviews by dealer ID (with sentiment)
    path(route='reviews/dealer/<int:dealer_id>/', view=views.get_dealer_reviews, name='dealer_reviews'),
    # registration path
    path('register/', views.register_user, name='register_user'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
