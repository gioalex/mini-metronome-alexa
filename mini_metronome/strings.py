SKILL_NAME = "Mini Metronome"
WELCOME_MESSAGE = "Welcome to {}. You can ask me to play a tempo like 80 bpm.".format(SKILL_NAME)
HELP_MESSAGE = "You can start a new tempo for example by saying play 80 bpm."
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "{} can't help you with that. Try saying play 80 bpm.".format(SKILL_NAME)
FALLBACK_REPROMPT = "What can I help you with?"
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

TEMPO_NOT_IN_RANGE = "Tempo must be between 20 and 240 beats per minute."
DURATION_NOT_IN_RANGE = "Duration must be between 10 seconds and 10 minutes."
PLAYING = "Playing metronome with tempo {} beats per minute for <say-as interpret-as=\"time\">{}</say-as>."
CARD_TEXT = "{} beats per minute"

DEFAULT_DURATION = "PT5M"

ICON_URL = "https://mini-metronome.s3-eu-west-1.amazonaws.com/mini_metronome.png"
