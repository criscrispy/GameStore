"""
Urls
====

Index
  /index/

Games. Shows list of games. Could be landing page after login.
  /games/
  /games?order=rating|created|price|popularity

Categories. Shows list of categories.
  /categories/

Category_detail. Shows list of games under given category.
  /categories/sport

Publishers. List of publishers.
  /publishers
  /publishers?order=rating|created

Publisher_detail. Details of one of the publishers, list of games they
published etc
  /publishers/nintendo OR /publishers/12345

Search
    /search/<query>

History. History of userid=1234 in terms of games they played
    /history/1234

Apply. Apply to become a developer
  /apply/1234

"""
from django.conf.urls import url

import gamestore.views.accounts
import gamestore.views.base
from gamestore.views import base, players, developers

#   /profile
#   url(r'^', views., name=''),
#
#   /user/123
#   url(r'^', views., name=''),
#
#   /user/123/edit
#   url(r'^', views., name=''),


# Base views
urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^games$', gamestore.views.base.games, name='games.list'),
    url(r'^categories', base.categories, name='categories.list'),
    url(r'^categories/(?P<category_name>\w+)', base.category_detail,
        name='categories.detail'),
    url(r'^publishers', base.publishers, name='publishers.list'),
    url(r'^publishers/(?P<user_id>[0-9]{1,})', base.publisher_detail,
        name='publisher.detail'),
    url(r'search/(?P<keyword>\w+)', base.search, name='search')
]


# Account views
urlpatterns.extend([
    url(r'^accounts/profile', gamestore.views.accounts.profile, name='profile'),
    url(r'^history/(?P<user_id>[0-9]{1,})',
        gamestore.views.accounts.user_history,
        name='user.history'),
    url(r'^apply/(?P<user_id>[0-9]{1,})',
        gamestore.views.accounts.apply_developer,
        name='publisher.apply'),
])


# Player views
urlpatterns.extend([
    #   /games/user/1234
    #   games the user bought
    url(r'^games/user/(?P<user_id>[0-9]{1,})', players.game_sale,
        name='games.sale'),

    #    /games/1234/play OR /games/supermario/play
    #   end point to register the scores of user when they perform the "play action"
    url(r'^games/(?P<game_id>[0-9]{1,})/play$', players.game_play,
        name='games.play'),

    #   /games/1234/buy
    #   end point to buy a game : adds the game to user's bought-list
    url(r'^games/(?P<game_id>[0-9]{1,})/buy$', players.game_buy,
        name='games.buy'),

    #   /games/supermario/like (add to favorites) ??
    #   end point to like a game : adds the game to user's liked-list
    url(r'^games/(?P<game_id>[0-9]{1,})/like$', players.game_like,
        name='games.like'),

    #   /games/1234 OR /games/supermario (only with ID)??
    #   the detail view of one of the games, one can play/buy/like from that view
    url(r'^games/(?P<game_id>[0-9]{1,})/$', players.game_detail,
        name='games.detail'),
])


# Developer views
urlpatterns.extend([
    #   /uploads/1234
    #   games user 1234 uploaded
    url(r'^uploads/(?P<user_id>[0-9]{1,})', developers.uploads,
        name='games.uploads'),

    #   /uploads/supermario OR /uploads/1234
    #   details of one of the uploaded games : visible to the uploader
    url(r'^uploads/(?P<game_id>[0-9]{1,})', developers.upload_detail,
        name='games.upload.detail'),

    #   /uploads/supermario/stats OR /uploads/1234/stats
    #   view the stats of the uploaded game with gameId=1234
    url(r'^uploads/(?P<game_id>[0-9]{1,})/stats', developers.upload_stat,
        name='games.upload.stat'),

    #   /uploads/supermario/delete
    #   edit one of the uploaded games
    #   the post request could save the updated info
    url(r'^uploads/(?P<game_id>[0-9]{1,})/edit', developers.upload_edit,
        name='games.upload.edit'),

    #   /uploads/supermario/edit
    #   edit one of the uploaded games (change picture, name etc)
    url(r'^uploads/(?P<game_id>[0-9]{1,})/delete', developers.upload_delete,
        name='games.upload.delete'),

    #   /upload
    #   view to show the upload form
    url(r'^upload', developers.upload, name='games.upload'),
])
