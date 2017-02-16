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

## Project implementation

### Heroku URL

http://fast-ridge-53625.herokuapp.com/

### Accounts/passwords to use the game
TODO

### Work division
TODO

### Implemented features

**Authentication**
 Authentication features implemented using registration-redux
 - Register 
 - Log in
 - Logout
 - Email validation?

Authorization:
- Every user is a player, can apply to become developer. TODO application handling
- Players can only play only bought games
- Developers can modify only own games

**Basic player functionalities**
 - Payment integration with payment backend (not secure)
 - Play - game/service interaction using [protocol](#game-service-communication-protocol)
 - TODO search
 - Game scores, states and sales stored in database
  
**Basic developer functionalities**
 - Add game
 - Update game
 - TODO delete
 - TODO statistics

**Game/service interaction**
 - See [protocol](#game-service-communication-protocol)

**Other**
 - Tests
 - Adjusting simple JavaScript game from [source](http://www.w3schools.com/graphics/game_intro.asp) to communicate with service.
 - Save/load and resolution feature
 - Postgre database

### Self-assessment, successes, problems
TODO

### Game service communication protocol

Game and service exchange 5 message types listed in the following table

Message | Message type attribute  | Content attribute name | Expected content attribute value | Sender  | Action triggered
--------|-------------------------|------------------------|----------------------|---------|----------------------
SETTING | "messageType":"SETTING" |"options"               | object containing attributes "width" and "height" with integer values | game    | service adjusts game iframe size to fit game dimensions
SCORE   | "messageType":"SCORE"   |"score"                 | integer | game    | service saves player's game score
SAVE    | "messageType":"SAVE"    |"gameState"             | json | game    | service saves player's game state
LOAD    | "messageType":"LOAD"    |"gameState"             | json | service | game loads player's game state
ERROR   | "messageType":"ERROR"   |"info"                  | string | service | game shows error message

### Other documentation
TODO

## Project Plan

### Project Managment and Communication
- [Trello](https://trello.com/)
- [Telegram](https://telegram.org/)
- GitLab / Niksula

### Goals
Project aim is to implement functioning web application, reasonably covered with tests and corresponding to the course requirements. 

### Plans

Technologies/frameworks
- Python 3.5
   - Logging (included in Python standard library)
- Django
- Bootstrap
- Font Awesome 
- JQuery
- PostgreSQL
- Unittests / django.test
- Hypothesis (property based testing)


### Project structure
Plan to develop the project in structure inspired from [layout](http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/) suitable for Django application.

### Functionality

#### **Authentication functionality**
(using django-registration-redux with customized views)

- Register
- Login
- Logout
- Email validation (django.core.mail)

#### **Authorisation functionality**
Implementation of two user groups and basic ACL(using django.contrib.auth).

Group: **developers**

Permissions:

- add/modify/delete games in own inventory
- see list of games and sales statistics


Group: **players**

Permissions:

- buy games
- play games only if bought
- see game list bought
- see game high scores
- record own score to high scores

#### **User/service interaction functionality use-cases:**
Developer

- add/modify/delete game
- see list of own games 
- see games sales statistics 

Player

- buy a game - functionality includes using mock payment service
- play a game - run the game from service, messages between service and game
- see list of purchased games / games to buy - selectable items with links to details
- see game details
- see game high scores
- add own high score - choose if high score is shown in the public list 

#### **Game/service interaction functionality:**

Javascript (_window.postMessage_) message exchange between game and service on events:
 SCORE, SAVE, LOAD_REQUEST, LOAD, ERROR, SETTING (analogous to [description](https://plus.cs.hut.fi/wsd/2016-2017/project/description/))



### Models:

**User:** default django model

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

**Messages**: used for game/service interaction, format similar to one in [description](https://plus.cs.hut.fi/wsd/2016-2017/project/description/), exact protocol will be documented on development stage

    messageType - SCORE, SAVE, LOAD_REQUEST, LOAD, ERROR, SETTING
    ...


### Views:

- Login/Register
- Player game selection view (bought games and games to buy)
- Player high scores view
- Player play game view
- Player buy game view
- Player menu
- Developer game list view
- Developer add/modify game view
- Developer sale statistics view
- Developer menu

### Priorities:
1. Mandatory Requirements
2. Other features

### Schedule

Planning to use iterative development strategy, developing components in models - view - templates order. Adding tests for each component before/after creation.  Following list contains deadlines for each task. 

- Group registration - 14.12.2016 midnight
- Project Plan - 21.12.2016 midnight
- Tests - 17.2.2017
- Authentication - 10.1.2017
- Authorization group rights - 17.2.2017
- Models - 10.1.2017 (goal stable models version)
- Views - 17.2.2017
- Templates - 17.2.2017
- Game/service interaction - 17.2.2017
- Code polishing - 17.2.2017
- [Heroku](https://www.heroku.com/) environment setup and deployment 1.2.2017
- Final submission - 19.2.2017 midnight (end of period III)
- Project demonstrations


### Documentation
- [Sphinx](http://www.sphinx-doc.org/en/latest/)
- [Google style docstrings](https://google.github.io/styleguide/pyguide.html)

### Testing
- [Unittest](https://docs.python.org/3/library/unittest.html)
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html)
