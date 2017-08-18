"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json
import urllib2


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TakeSurveyIntent":
        return start_survey_session(intent, session)
    elif intent_name == "ChoiceIntent":
        return choice_survey(intent, session)
    elif intent_name == "OpenAnswerIntent":
        return open_answer_survey(intent, session)
    elif intent_name == "SubmitIntent":
        return submit_survey(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Survey Monkey Contribute. " \
                    "Are you ready to take a Survey? "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please confirm, Are you ready to take a Survey? "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def start_survey_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "Let's start with your survey. Did Sally sell sea shells by the sea shore? Your choices are: a, Yes. b, No. c, May be. d, Who is Sally?"
    reprompt_text = "Did Sally sell sea shells by the sea shore? Your choices are: a, Yes. b, No. c, May be. d, Who is Sally?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def choice_survey(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    question_id = "155048494"
    options_map = {
        "A": "1124046849",
        "A.": "1124046849",
        "a": "1124046849",
        "a.": "1124046849",
        "B": "1124046850",
        "B.": "1124046850",
        "b": "1124046850",
        "b.": "1124046850",
        "C": "1124046851",
        "C.": "1124046851",
        "c": "1124046851",
        "c.": "1124046851",
        "D": "1124046852",
        "D.": "1124046852",
        "d": "1124046852",
        "d.": "1124046852"
    }
    option_chosen = intent['slots']['CHOICE']['value']

    option_id = options_map[option_chosen]
    create_response(question_id, option_id=option_id, text=None)
    speech_output = "Thanks. You choice has been saved. The next question is, How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    reprompt_text = "Your question is, How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    # else:
    #     speech_output = "I'm not sure what you choice is. " \
    #                     "You can say, a. b, c. or d."
    #     reprompt_text = "I'm not sure what you choice is. " \
    #                     "You can say, a. b, c. or d."
    #     should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def open_answer_survey(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    question_id = "155048829"
    text = intent['slots']['OPENEND']['value']

    create_response(question_id, option_id=None, text=text)

    speech_output = "Thanks. You answer has been saved. You have reached the end of your survey. Are you ready to submit it?"
    reprompt_text = "Are you ready to submit it?"

    # else:
    #     speech_output = "I'm not sure what you said. " \
    #                     "Please answer: How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    #     reprompt_text = "Please answer: How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    #     should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def submit_survey(intent, session):
    session_attributes = {}

    speech_output = "Thanks. Your survey has been submitted. Goodbye."
    reprompt_text = "Are you ready to submit your survey? "
    should_end_session = True
    # else:
    #     speech_output = "Please confirm, are you ready to submit your survey? "
    #     reprompt_text = "Are you ready to submit your survey? "
    #     should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def create_response(question_id, option_id=None, text=None):
    survey_id = '121187943'
    collector_id = '160877259'
    page_id = '46904417'
    access_token = 'VBotjgizrpcSH7xAiqtAdrh1E96jN7hSh30fNxsPSK4n4Qvb59lyNpr8C9ViqFZLzhcM2kqNCbMd0TwFAE34n9MEXICVIUmwMdQez1lOi15CsbH-bp1k2dUROhXhbGMp'
    answer_data = [{
	'choice_id': option_id
    }]
    if not option_id:
        answer_data = [{
            'text': text
        }]
    data = json.dumps({
        'pages': [{
            'id': page_id,
            'questions': [{
                'answers': answer_data,
                'id': question_id
            }]
        }]
    })
    url = 'https://api.surveymonkey.net/v3/collectors/{}/responses'.format(collector_id)
    headers = {
    	'Content-Type': 'application/json',
    	'Authorization': "Bearer {}".format(access_token)
    }
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
