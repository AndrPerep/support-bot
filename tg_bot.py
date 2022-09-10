import json

import telegram
from telegram.error import NetworkError, Unauthorized

from time import sleep
from dotenv import load_dotenv
import os

update_id = None

def get_answer(user_message, language_code='ru-RU'):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')
    session_id=os.getenv('TG_CHAT_ID')

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=user_message, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def start_bot():
    global update_id

    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    bot = telegram.Bot(tg_token)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            print(update.message.text)
            update.message.reply_text(get_answer(update.message.text))


def create_intent(display_name, intent_phrases):
    from google.cloud import dialogflow

    load_dotenv()

    training_phrases_parts = intent_phrases['questions']
    message_texts = [intent_phrases['answer']]
    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def create_intents():
    phrases_filename = 'phrases.json'
    with open(phrases_filename, 'r', encoding='utf-8') as phrases_file:
        phrases_json = phrases_file.read()

    phrases = json.loads(phrases_json)

    for display_name, intent_phrases in phrases.items():
        create_intent(display_name, intent_phrases)


if __name__ == '__main__':
    start_bot()
    # create_intents()
