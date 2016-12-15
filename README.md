# Online Game Store for JavaScript Games
## About
Project details

Field      | Details
-----------|---------------------------------------
University | Aalto University
Course     | CS-C3170 - Web Software Development
Date       | Autumn 2016 - spring 2017
Status     | Project work
Topic      | Online game store for JavaScript games

Authors

Last name           | First name | Email
--------------------|------------|-----------------------------
Tollander de Balsch | Jaan       | <de.tollander@aalto.fi>
Sulina              | Julia      | <julia.sulina@aalto.fi>
Awono               | Mekbib     | <mekbib.awono@aalto.fi>


## Project Plan

### Project Managment and Communication
- [Trello](https://trello.com/)
- [Telegram](https://telegram.org/)
- GitLab / Niksula

### Goals


### Plans
- Python 3.5
- Django

#### Functionality

##### Authentication functionality
(using django.contrib.auth)

- Register
- Login
- Logout
- Email validation (django.core.mail)

##### Authorisation functionality
Implement two user groups and ACL.

Group: **developers**

Permissions:

- add games to own inventory
- see list of game sales


Group: **players**

Permissions:

- buy games
- play games only if bought
- see game high scores
- record their score to high scores

##### Game/service interaction:


#### Models:

**User:**
default django model

**Game:**

    publisher - user foreign key
    
    title
    
    code
    
    price
    
    url - link to game location


**Scores:**

    game - game foreign key

    player - user foreign key

    score

    public - boolean show in scoreboard or not


**Game_sales:**

    buyer - user foreign key
    
    game - bought game foreign key
    
    buying_date


**Game_inventory:**(might be unnecessary)

    owner - developer user foreign key
    
    games - games published by user


**Play_ground:**(might be unnecessary)

    player - player user foreign key
    
    games - games bought by user

**Messages**: used for game/service interaction, format similar to one in [description](https://plus.cs.hut.fi/wsd/2016-2017/project/description/), exact protocol will be documented on development stage )

    messageType - 
    
    ...


#### Views:
- Login/Register
- Player game selection view
- Player high scores view
- Player play game view
- Player menu
- Developer game list view
- Developer add/modify game view
- Developer sale statistics view
- Developer menu

Priorities:


### Schedule
- Group registration - 14.12.2016 midnight
- Project Plan - 21.12.2016 midnight
- Final submission - 19.2.2017 midnight (end of period III)
- Project demonstrations

### Documentation
- [Sphinx](http://www.sphinx-doc.org/en/latest/)
- [Google style docstrings](https://google.github.io/styleguide/pyguide.html)

### Testing
- [Unittest](https://docs.python.org/3/library/unittest.html)
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html)
