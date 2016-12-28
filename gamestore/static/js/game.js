var messageTypes = {
    START: "START",
    SCORE: "SCORE",
    SAVE: "SAVE",
    LOAD_REQUEST: "LOAD_REQUEST",
    LOAD: "LOAD",
    ERROR: "ERROR",
    SETTING: "SETTING"
};

$(document).ready(function () {
    $(window).on('message', function (event) {
        //Get data from sent message
        var data = event.originalEvent.data;
        handleMessage(data);
    });
});


function saveScore(score) {
    $("#score").prepend("<p>your score:" + score+"</p>");
}

function saveState(gameState) {
    alert(gameState);
}
function findSavedState() {
    alert("state");
}
function adjustIframe(options) {
    if(options.width && options.height){
        $("#game_container").height(options.height + 100);
        $("#game_container").width(options.width + 50);
    };
}
function handleMessage(data) {

    switch (data.messageType) {
        case messageTypes.SCORE:
            saveScore(data.score);
            break;
        case messageTypes.SAVE:
            saveState(data.gameState);
            break;
        case messageTypes.LOAD_REQUEST:
            findSavedState();
            break;
        case messageTypes.SETTING:
            adjustIframe(data.options);
            break;
        default:
            console.log("unsupported message" + data);
    }
}
