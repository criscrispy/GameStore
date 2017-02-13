/**
 * Interface to handle communication of the game with service.
 * On the game side following methods should be implemented:
 * - showErrorMessage(errorString)
 * - loadGameState(stateJson)
*/

/* Message types */
var messageTypes = {SCORE: "SCORE", SAVE: "SAVE", LOAD: "LOAD", ERROR: "ERROR", SETTING: "SETTING"};
var service_url = "*";

/* Listen to the messages from service */
$(document).ready(function () {

    $(window).on('message', function (evt) {
        //Get data from sent message
        var data = evt.originalEvent.data;
        handleMessage(data);
    });
});

/* Handle messages of the type LOAD and ERROR */
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

/* Implement loadGameState(stateJson) method to load game state received from service */
function loadGame(gameState) {
    loadGameState(gameState);
}

/* Implement showErrorMessage(errorString) to show error received from service*/
function showError(error) {
    showErrorMessage(error);
}

/* Call to send score to service */ 
function sendScore(score) {
    var message = {"messageType": messageTypes.SCORE, "score": score};
    sendMessage(message);
}

/* Call to send game state to service */ 
function sendSaveState(state) {
    var message = {"messageType": messageTypes.SAVE, "gameState": state};
    sendMessage(message);
}

/* Call to send game settings (width and height) to service */ 
function sendSetting(settings) {
    var message = {"messageType": messageTypes.SETTING, "options": settings};
    sendMessage(message);
}

function sendMessage(message) {
    window.parent.postMessage(message, service_url);
}

