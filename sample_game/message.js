var messageTypes = {SCORE: "SCORE", SAVE: "SAVE", LOAD: "LOAD", ERROR: "ERROR", SETTING: "SETTING"};
var service_url = "*";
$(document).ready(function () {

    $(window).on('message', function (evt) {
        //Get data from sent message
        var data = evt.originalEvent.data;
        //alert(data.messageType);
        handleMessage(data);

    });
});

function handleMessage(data) {
    switch (data.messageType) {
        case messageTypes.LOAD:
            loadGame(data.gameState);
            break;
        case messageTypes.ERROR:
            showError(data.info);
            break;
        default:
            console.log("unsupported message" + data);
    }
}

function loadGame(gameState) {
    displayMessage("<p>Game load received" + JSON.stringify(gameState) + " <br/> Loading not yet implemented on the game side</p>", false);
}
function showError(error) {
    //Create a new list item based on the data
    var newItem = '\n\t<li>' + (error || '') + '</li>';
    //Add the item to the beginning of the actions list
    $('#actions').prepend(newItem);
}

function sendMessage(message) {
    window.parent.postMessage(message, service_url);
}
function sendScore(score) {
    var message = {"messageType": messageTypes.SCORE, "score": score};
    sendMessage(message);
}
function sendSaveState(state) {
    var message = {"messageType": messageTypes.SAVE, "gameState": state};
    sendMessage(message);
}
function sendSetting(settings) {
    var message = {"messageType": messageTypes.SETTING, "options": settings};
    sendMessage(message);
}

