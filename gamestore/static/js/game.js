/* Message types */
var messageTypes = {
    SCORE: "SCORE",
    SAVE: "SAVE",
    LOAD: "LOAD",
    ERROR: "ERROR",
    SETTING: "SETTING"
};

/* Listen to the messages from game */
$(document).ready(function () {

    /* Listen to post messages */
    $(window).on('message', function (event) {
        var game_url = $("#game_container").attr('src');
        if (game_url.indexOf(event.originalEvent.origin) != 0) {
            return;
        }
        //Get data from sent message
        var data = event.originalEvent.data;
        handleMessage(data);
    });
$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    container: 'body'
  });
});


/* Handle game messages */
function handleMessage(data) {
    switch (data.messageType) {
        case messageTypes.SCORE:
            saveScore(data.score);
            break;
        case messageTypes.SAVE:
            saveState(data.gameState);
            break;
        case messageTypes.SETTING:
            adjustIframe(data.options);
            break;
        default:
            console.log("unsupported message" + data);
    }
}

function saveScore(score) {
    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    var data = {
        gameScore: score,
        csrfmiddlewaretoken: csrftoken
    };
    postData('score', data);
}

function saveState(gameState) {
    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    var data = {gameState: gameState, csrfmiddlewaretoken: csrftoken};
    postData('state', data);
}

function adjustIframe(options) {
    if (options.width && options.height) {
        var gameContainer = $("#game_container");
        gameContainer.height(options.height);
        gameContainer.width(options.width);
    }
}

/*Make ajax request*/
function postData(url, data) {
    $.post(url, data, function (data) {
        renderResponse(data);
    });
}

/*Render ajax response*/
function renderResponse(html) {
    $("#response").html(html);
}

/* Send game */
function sendState(data) {
    var message = {messageType: messageTypes.LOAD, gameState: data};
    sendMessage(message);
}

function sendMessage(message) {
    var game_url = $("#game_container").attr('src');
    iframe = document.getElementById('game_container').contentWindow;
    iframe.postMessage(message, game_url);
}

