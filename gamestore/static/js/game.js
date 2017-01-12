var messageTypes = {
    START: "START",
    SCORE: "SCORE",
    SAVE: "SAVE",
    LOAD: "LOAD",
    ERROR: "ERROR",
    SETTING: "SETTING"
};

var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

$(document).ready(function () {
    game_url = $("#game_container").attr('src')
    $(window).on('message', function (event) {
        if (game_url.indexOf(event.originalEvent.origin) != 0) {
            return;
        }
        //Get data from sent message
        var data = event.originalEvent.data;
        handleMessage(data);
    });
});

function saveScore(score) {
    var data = {
        gameScore: score,
        csrfmiddlewaretoken: csrftoken
    };
    $.post('score', data);
}

function saveState(gameState) {
    var data = {gameState: gameState, csrfmiddlewaretoken: csrftoken};
    $.post('state', data);
}

function getState() {
    var data = {csrfmiddlewaretoken: csrftoken};
    $.post('get_state', data, sendState);
}

function sendState(json) {
    var message = {messageType:messageTypes.LOAD, gameState:json}
    sendMessage(message)
}

function sendMessage(message) {
    iframe = $("#game_container").contentWindow;
    iframe.postMessage(message);
}

function adjustIframe(options) {
    if (options.width && options.height) {
        var gameContainer = $("#game_container");
        gameContainer.height(options.height);
        gameContainer.width(options.width);
    }

}
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
