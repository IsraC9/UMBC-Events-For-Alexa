# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import json
import requests
import xmltodict

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


url = "https://my3.my.umbc.edu/api/v0/events.xml"
res = requests.get(url)
data = xmltodict.parse(res.text) 
json_data = json.dumps(data)
event_dic = json.loads(json_data)
num_events = len(event_dic['Events'].get('Event'))




class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "What do you wish to know about your school's events?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
    
class ImportantIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("ImportantIntent")(handler_input)

    def handle(self, handler_input):
       
        
        num_important_events = 0
        important_events = []
        for i in range(num_events):
            if(event_dic['Events']['Event'][i].get('@important') == 'true' and event_dic['Events']['Event'][i].get('@canceled') != 'true'):
                num_important_events += 1
                important_events.append(event_dic['Events']['Event'][i].get('Title'))
         
        if(num_important_events == 0):
            speak_output = "There are no important events"
        
        else:
            
            output = ''
            for x in range(len(important_events)):
                if x == len(important_events) - 1 and len(important_events) > 1:
                    output += "and " + important_events[x]
                else:
                    output += important_events[x] + ', '
                
            if num_important_events == 1:
                speak_output = ("There is " + str(num_important_events) + " important event. That event is " + output)
            else:
                speak_output = ("There are " + str(num_important_events) + " important events. Those events are " + output)
            
            
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CanceledEventsIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("CanceledEventsIntent")(handler_input)

    def handle(self, handler_input):
        
        num_canceled_events = 0
        CanceledEvents = []
        for i in range(num_events):
            if(event_dic['Events']['Event'][i].get('@canceled') == 'true'):
                num_canceled_events += 1
                CanceledEvents.append(event_dic['Events']['Event'][i].get('Title'))
                
        if(num_canceled_events == 0):
            speak_output = "There are no canceled events"
            
        else:
            output = ''
            for x in range(len(CanceledEvents)):
                if x == len(CanceledEvents) - 1 and len(CanceledEvents) > 1:
                    output += "and " + CanceledEvents[x]
                else:
                    output += CanceledEvents[x] + ', '
                    
            if num_canceled_events == 1:
                speak_output = ("There is " + str(num_canceled_events) + " canceled event. That event is " + output)
            else:
                speak_output = ("There are " + str(num_canceled_events) + " canceled events. Those events are " + output)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class AllDayIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("AllDayIntent")(handler_input)

    def handle(self, handler_input):
        
        num_allday_events = 0
        allday = []
        for i in range(num_events):
            if(event_dic['Events']['Event'][i].get('@allDay') == 'true' and event_dic['Events']['Event'][i].get('@canceled') != 'true'):
                num_allday_events += 1
                allday.append(event_dic['Events']['Event'][i].get('Title'))
                
        if(num_allday_events == 0):
            speak_output = "There are no events that will be all day"
            
        else:
            output = ''
            for x in range(len(allday)):
                if x == len(allday) - 1 and len(allday) > 1:
                    output += "and " + allday[x]
                else:
                    output += allday[x] + ', '
            if num_allday_events == 1:
                speak_output = ("There is " + str(num_allday_events) + " all day event. That event is " + output)
            else:
                speak_output = ("There are " + str(num_allday_events) + " all day events. Those events are " + output)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class AllEventsIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("AllEventsIntent")(handler_input)

    def handle(self, handler_input):
        
        num_all_events = 0
        all_events = []
        for i in range(num_events):
            if(event_dic['Events']['Event'][i].get('@canceled') == 'false'):
                num_all_events += 1
                all_events.append(event_dic['Events']['Event'][i].get('Title'))
                
        if(num_all_events == 0):
            speak_output = "There are no events that are happening"
            
        else:
            output = ''
            for x in range(len(all_events)):
                if x == len(all_events) - 1 and len(all_events) > 1:
                    output += "and " + all_events[x]
                else:
                    output += all_events[x] + ', '
            if num_all_events == 1:
                speak_output = ("There is " + str(num_all_events) + " event happening. That event is " + output)
            else:
                speak_output = ("There are " + str(num_all_events) + " events happening. Those events are " + output)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class LocationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("LocationIntent")(handler_input)
        
    def handle(self, handler_input):
        
        title = handler_input.request_envelope.request.intent.slots["title"].value
        
        found = False
        
        for i in range(num_events):
            curr_title = event_dic['Events']['Event'][i].get('Title')
            if(curr_title.lower() == title):
                location = event_dic['Events']['Event'][i]['Location'].get('#text')
                found = True
                
        if(found == True):
            speak_output = ("The location of {} is ".format(title) + location)
        else:
            
            speak_output = "I'm sorry, I don't believe {} is an event that is currently happening".format(title)
        
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SummaryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("SummaryIntentHandler")(handler_input) 
        
    def handle(self, handler_input):
        
        title = handler_input.request_envelope.request.intent.slots["title"].value
        logger.info(title)
        found = False    
        
        for i in range(num_events):
            curr_title = event_dic['Events']['Event'][i].get('Title')
            logger.info(curr_title)
            if(curr_title.lower() == title):
                summary = event_dic['Events']['Event'][i].get('Summary')
                found = True
                logger.info(summary)
                
        if(found == True):
            speak_output = summary
        else:
            speak_output = "I'm sorry, I don't believe {} is an event that is currently happening".format(title) 
                
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ImportantIntentHandler())
sb.add_request_handler(CanceledEventsIntentHandler())
sb.add_request_handler(AllDayIntentHandler())
sb.add_request_handler(AllEventsIntentHandler())
sb.add_request_handler(LocationIntentHandler())
sb.add_request_handler(SummaryIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()