"""
Urls
====

Base
----

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


Accounts
--------

History. History of userid=1234 in terms of games they played
    /history/1234

Apply. Apply to become a developer
  /apply/1234


Player
------



Developer
---------



"""
from django.conf.urls import url, include

import gamestore.views.accounts
import gamestore.views.base
from gamestore.views import base, players, developers, payments

#   /profile
#   url(r'^', views., name=''),
#
#   /user/123
#   url(r'^', views., name=''),
#
#   /user/123/edit
#   url(r'^', views., name=''),


urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^games$', gamestore.views.base.games, name='games.list'),
    url(r'^categories/(?P<category_name>\w+)', base.category_detail,
        name='categories.detail'),
    url(r'^categories', base.categories, name='categories.list'),
    url(r'^publishers/(?P<user_id>[0-9]+)', base.publisher_detail,
        name='publisher.detail'),
    url(r'^publishers', base.publishers, name='publishers.list'),
]

# Search
urlpatterns.extend([
    url(r'^search/(?P<keyword>\w+)', base.search, name='search'),
    url(r'^search/', include('haystack.urls')),
])

# Account views
urlpatterns.extend([
    url(r'^accounts/profile', gamestore.views.accounts.profile, name='profile'),
    url(r'^history/(?P<user_id>[0-9]+)',
        gamestore.views.accounts.user_history, name='user.history'),
    url(r'^apply/(?P<user_id>[0-9]+)',
        gamestore.views.accounts.apply_developer, name='publisher.apply'),
])

# Player views
urlpatterns.extend([
    #   /games/user/1234
    #   games the user bought
    url(r'^games/user/', players.game_sale,
        name='games.sale'),

    #    /games/1234/play OR /games/supermario/play
    #   end point to register the scores of user when they perform the "play action"
    url(r'^games/(?P<game_id>[0-9]+)/play$', players.game_play,
        name='games.play'),

    #   /games/1234/buy
    #   end point to buy a game : adds the game to user's bought-list
    url(r'^games/(?P<game_id>[0-9]+)/buy$', players.game_buy,
        name='games.buy'),

    #   /games/supermario/like (add to favorites) ??
    #   end point to like a game : adds the game to user's liked-list
    url(r'^games/(?P<game_id>[0-9]+)/like$', players.game_like,
        name='games.like'),

    #   /games/1234/
    #   the detail view of one of the games, one can play/buy/like from that view
    url(r'^games/(?P<game_id>[0-9]+)/$', players.game_detail,
        name='games.detail'),

    #   /games/1234/score
    # endpoint for submitting game score for saving
    url(r'^games/(?P<game_id>[0-9]{1,})/score$', players.game_submit_score,
        name='games.score'),

    #   /games/1234/state
    # endpoint for submitting game state for saving
    url(r'^games/(?P<game_id>[0-9]{1,})/state$', players.game_save_settings,
        name='games.state'),

    #   /games/1234/get_state
    # endpoint for fetching saved game state
    url(r'^games/(?P<game_id>[0-9]{1,})/get_state$', players.game_get_saved_state,
        name='games.get_state'),
])

# Payments views
urlpatterns.extend([
    # payment API response page for succeded payment
    url(r'^payment/success', payments.success, name='payment.success'),

    # payment API response page for cancelled payment
    url(r'^payment/cancel', payments.cancel, name='payment.cancel'),

    # payment API response page for payment error
    url(r'^payment/error', payments.error, name='payment.error'),
])

# Developer views
urlpatterns.extend([
    #   /uploads/1234
    #   games user 1234 uploaded
    url(r'^uploads/(?P<user_id>[0-9]+)', developers.uploads,
        name='games.uploads'),

    #   /uploads/supermario OR /uploads/1234
    #   details of one of the uploaded games : visible to the uploader
    url(r'^uploads/(?P<game_id>[0-9]+)', developers.upload_detail,
        name='games.upload.detail'),

    #   /uploads/supermario/stats OR /uploads/1234/stats
    #   view the stats of the uploaded game with gameId=1234
    url(r'^uploads/(?P<game_id>[0-9]+)/stats', developers.upload_stat,
        name='games.upload.stat'),

    #   /uploads/supermario/delete
    #   edit one of the uploaded games
    #   the post request could save the updated info
    url(r'^uploads/(?P<game_id>[0-9]+)/edit', developers.upload_edit,
        name='games.upload.edit'),

    #   /uploads/supermario/edit
    #   edit one of the uploaded games (change picture, name etc)
    url(r'^uploads/(?P<game_id>[0-9]+)/delete', developers.upload_delete,
        name='games.upload.delete'),

    #   /upload
    #   view to show the upload form
    url(r'^upload', developers.upload, name='games.upload'),
])
