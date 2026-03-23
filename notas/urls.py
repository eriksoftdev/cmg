from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_notas, name='notas'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('update/<int:note_id>', views.update_note, name='update_note'),
]