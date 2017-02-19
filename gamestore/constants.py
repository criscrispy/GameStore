"""Constants"""
METHOD_GET = 'GET'
METHOD_POST = 'POST'
ASCII = "ascii"
ERROR = 'error'
SUCCESS = 'success'
CANCEL = 'cancel'

# game constants
GAME_SCORE = 'gameScore'
GAME_STATE = 'gameState'

# payment constants
CHECKSUM = 'checksum'
RESULT = 'result'
PID = 'pid'
REF = 'ref'
CHECKSUM_REQUEST_FORMAT = "pid={}&sid={}&amount={}&token={}"
CHECKSUM_RESPONSE_FORMAT = "pid={}&ref={}&result={}&token={}"
CHECKSUM_LENGHT = 32
PID_LENGHT = 8

# errors and messages
PID_WAS_NOT_FOUND = "Validation error: No payment with this identifier was found"
REF_INVALID_FORMAT = "Validation error: ref field invalid format"
GET_REQUEST_EXPECTED = "Validation error: GET request expected"
CHECKSUM_WRONG = "Validation error: Checksum wrong"
USER_INVALID = "Validation error: user invalid"
CHECKSUM_INVALID_FORMAT = "Validation error: checksum field invalid format"
RESULT_INVALID_FORMAT = "Validation error: result field invalid format"
PID_INVALID_FORMAT = "Validation error: pid field invalid format"
COULD_NOT_SAVE_SCORE = "Service error: Could not save game score"
COULD_NOT_SAVE_STATE = "Service error: Could not save game state"
GAME_SCORE_INVALID = "Validation error: score received from the game invalid"
GAME_STATE_INVALID = "Validation error: state received from the game invalid"
REQUEST_PARAMETER_MISSING = "Validation error: request parameter missing"
GAME_INVALID = "Validation error: game not found"

PAYMENT_WAS_CANCELLED = 'Payment was cancelled'
ERROR_PERFORMING_PAYMENT = 'Error when performing payment'

# html
GAME_AJAX_HTML = 'gamestore/game_ajax.html'
GAME_BUY_HTML = "gamestore/game_buy.html"
GAME_DESCRIPTION_HTML = "gamestore/game_description.html"

PAYMENTS_FAIL_HTML = "gamestore/payments_fail.html"
PAYMENTS_SUCCESS_HTML = "gamestore/payments_success.html"
