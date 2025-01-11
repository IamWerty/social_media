from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/comments/', views.BookCommentCreateView.as_view(), name='book_comment_create'),

    path('books/<int:book_id>/chapters/create/', views.ChapterCreateView.as_view(), name='chapter_create'),
    path('books/<int:book_id>/<int:pk>/comments/', views.ChapterCommentCreateView.as_view(), name='chapter_comment_create'),
    path('books/<int:book_id>/<int:pk>', views.ChapterDetailView.as_view(), name='chapter_detail'),


    path('channels/', views.ChannelListView.as_view(), name='channel_list'),
    path('channels/create/', views.ChannelCreateView.as_view(), name='channel_create'),
    path('channels/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),
    path('channels/<int:pk>/manage_admin/', views.ManageAdminView.as_view(), name='manage_admin'),
    path('channels/<int:pk>/posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('channels/<int:pk>/repost/', views.RepostCreateView.as_view(), name='repost_create'),

    path('vote/<str:obj_type>/<int:obj_id>/', views.VoteView.as_view(), name='vote'),

    path('repost/book/<int:book_id>/', views.RepostBookView.as_view(), name='repost_book'),
    path('repost/chapter/<int:chapter_id>/', views.RepostChapterView.as_view(), name='repost_chapter'),
]
