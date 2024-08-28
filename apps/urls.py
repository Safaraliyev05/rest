from django.conf.urls.static import static
from django.urls import path

from apps.views import CategoryListCreateAPIView, ProductListCreateAPIView, SendEmailAPIView, VerifyEmailAPIView
from root import settings

urlpatterns = [
                  path('categories', CategoryListCreateAPIView.as_view(), name='categories-list'),
                  path('products', ProductListCreateAPIView.as_view(), name='products-list'),
                  path('categories', CategoryListCreateAPIView.as_view()),
                  path('products', ProductListCreateAPIView.as_view()),
                  path('send-email/', SendEmailAPIView.as_view(), name='send-email'),
                  path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
