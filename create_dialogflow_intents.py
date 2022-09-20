from google.cloud import dialogflow
from dotenv import load_dotenv
from json import loads
from os import getenv


def create_intent(display_name, intent_phrases, project_id):
    training_phrases_parts = intent_phrases['questions']
    message_texts = [intent_phrases['answer']]

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


def main():
    load_dotenv()

    phrases_file = getenv('PHRASES_FILE', default='phrases.json')
    project_id = getenv('DIALOG_FLOW_PROJECT_ID')

    with open(phrases_file, 'r', encoding='utf-8') as phrases_file:
        phrases_json = phrases_file.read()

    phrases = loads(phrases_json)

    for display_name, intent_phrases in phrases.items():
        create_intent(display_name, intent_phrases, project_id)


if __name__ == '__main__':
    main()
