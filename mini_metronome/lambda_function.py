# -*- coding: utf-8 -*-
"""Mini Metronome app."""
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import get_slot_value, is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.interfaces import display
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, StopDirective, PlayBehavior, AudioItem, Stream,
    AudioItemMetadata)
from ask_sdk_model.ui import StandardCard, Image, SimpleCard
from ask_sdk_model import Response

from metronome import get_metronome_url, iso_8601_duration_to_seconds
import strings

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Custom Intent Handlers
class PlayMetronomeHandler(AbstractRequestHandler):
    """Handler for PlayMetronome Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PlayMetronomeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlayMetronomeHandler")

        tempo = int(get_slot_value(handler_input, "tempo"))
        if tempo < 20 or tempo > 240:
            handler_input.response_builder.speak(strings.TEMPO_NOT_IN_RANGE)
            return handler_input.response_builder.response

        duration = (get_slot_value(handler_input, "duration")
                    or strings.DEFAULT_DURATION)
        seconds = iso_8601_duration_to_seconds(duration)
        if seconds < 10 or seconds > 600:
            handler_input.response_builder.speak(strings.DURATION_NOT_IN_RANGE)
            return handler_input.response_builder.response

        logger.info("tempo={} duration={} seconds={}".format(
            tempo, duration, seconds))

        speak = strings.PLAYING.format(
            tempo,
            "{}'{}\"".format(int(seconds / 60), seconds % 60))

        data = {
            "card": {
                "title": strings.SKILL_NAME,
                "text": strings.CARD_TEXT.format(tempo),
                "small_image_url": strings.ICON_URL,
                "large_image_url": strings.ICON_URL
            },
            "url": get_metronome_url(tempo, seconds),
        }

        card = StandardCard(
            title=data["card"]["title"],
            text=data["card"]["text"],
            image=Image(
                small_image_url=data["card"]["small_image_url"],
                large_image_url=data["card"]["large_image_url"]
            )
        )

        directive = PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ALL,
            audio_item=AudioItem(
                stream=Stream(
                    expected_previous_token=None,
                    token=data["url"],
                    url=data["url"],
                    offset_in_milliseconds=0
                ),
                metadata=AudioItemMetadata(
                    title=data["card"]["title"],
                    subtitle=data["card"]["text"],
                    art=display.Image(
                        content_description=data["card"]["title"],
                        sources=[display.ImageInstance(url=strings.ICON_URL)]
                    ),
                    background_image=display.Image(
                        content_description=data["card"]["title"],
                        sources=[display.ImageInstance(url=strings.ICON_URL)]
                    )
                )
            )
        )
        (handler_input.response_builder
            .speak(speak)
            .set_card(card)
            .add_directive(directive)
            .set_should_end_session(True))
        return handler_input.response_builder.response


# Built-in Intent Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")

        (handler_input.response_builder
            .speak(strings.WELCOME_MESSAGE)
            .ask(strings.HELP_REPROMPT)
            .set_card(SimpleCard(strings.SKILL_NAME, strings.HELP_MESSAGE)))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        (handler_input.response_builder
            .speak(strings.HELP_MESSAGE)
            .ask(strings.HELP_REPROMPT)
            .set_card(SimpleCard(strings.SKILL_NAME, strings.HELP_MESSAGE)))
        return handler_input.response_builder.response


class AudioStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AudioStopIntentHandler")

        (handler_input.response_builder
            .speak(strings.STOP_MESSAGE)
            .add_directive(StopDirective()))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        (handler_input.response_builder
            .speak(strings.FALLBACK_MESSAGE)
            .ask(strings.FALLBACK_REPROMPT))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        (handler_input.response_builder
            .speak(strings.EXCEPTION_MESSAGE)
            .ask(strings.HELP_REPROMPT))
        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(PlayMetronomeHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(AudioStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Add request and response logging
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
