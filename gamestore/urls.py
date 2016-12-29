from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/profile', views.profile, name='profile'),

    #   /games
    #   /games?order=rating|created|price|popularity
    #   shows list of games. could be landing page after login
    url(r'^games$', views.games, name='games.list'),

    #   /games/user/1234
    #   games the user bought
    url(r'^games/user/(?P<user_id>[0-9]{1,})', views.game_sale, name='games.sale'),

    #   /games/1234 OR /games/supermario (only with ID)??
    #   the detail view of one of the games, one can play/buy/like from that view
    url(r'^games/(?P<game_id>[0-9]{1,})$', views.game_detail, name='games.detail'),

    #    /games/1234/play OR /games/supermario/play
    #   end point to register the scores of user when they perform the "play action"
    url(r'^games/(?P<game_id>[0-9]{1,})/play$', views.game_play, name='games.play'),

    #   /games/1234/buy
    #   end point to buy a game : adds the game to user's bought-list
    url(r'^games/(?P<game_id>[0-9]{1,})/buy', views.game_buy, name='games.buy'),

    #   /games/supermario/like (add to favorites) ??
    #   end point to like a game : adds the game to user's liked-list
    url(r'^games/(?P<game_id>[0-9]{1,})/like', views.game_like, name='games.like'),

    #   /categories
    #   shows the list of categories.
    url(r'^categories', views.categories, name='categories.list'),

    #   /categories/sport
    #   shows the list of games under given category
    url(r'^categories/(?P<category>\w+)', views.category_detail, name='categories.detail'),


    #   /profile
    #   url(r'^', views., name=''),

    #   /user/123
    #   url(r'^', views., name=''),

    #   /user/123/edit
    #   url(r'^', views., name=''),


    #   /history/1234
    #   history of userid=1234 interms of games they played
    url(r'^history/(?P<user_id>[0-9]{1,})', views.user_history, name='user.history'),

    #   /upload
    #   view to show the upload form
    url(r'^upload', views.upload, name='games.upload'),

    #   /uploads/1234
    #   games user 1234 uploaded
    url(r'^uploads/(?P<user_id>[0-9]{1,})', views.uploads, name='games.uploads'),

    #   /uploads/supermario OR /uploads/1234
    #   details of one of the uploaded games : visible to the uploader
    url(r'^uploads/(?P<game_id>[0-9]{1,})', views.upload_detail, name='games.upload.detail'),

    #   /uploads/supermario/stats OR /uploads/1234/stats
    #   view the stats of the uploaded game with gameId=1234
    url(r'^uploads/(?P<game_id>[0-9]{1,})/stats', views.upload_stat, name='games.upload.stat'),

    #   /uploads/supermario/delete
    #   edit one of the uploaded games
    #   the post request could save the updated info
    url(r'^uploads/(?P<game_id>[0-9]{1,})/edit', views.upload_edit, name='games.upload.edit'),

    #   /uploads/supermario/edit
    #   edit one of the uploaded games (change picture, name etc)
    url(r'^uploads/(?P<game_id>[0-9]{1,})/delete', views.upload_delete, name='games.upload.delete'),

    #   /publishers
    #   /publishers?order=rating|created
    #   list of publishers
    url(r'^publishers', views.publishers, name='publishers.list'),

    #   /publishers/nintendo OR /publishers/12345
    #   details of one of the publishers, list of games they published etc
    url(r'^publishers/(?P<user_id>[0-9]{1,})', views.publisher_detail, name='publisher.detail'),


    #   /search
    url(r'search/(?P<keyword>\w+)', views.search, name='search')

]
