from google.cloud import dialogflow
from os import getenv


def get_answer(user_message, session_id, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()

    project_id = getenv('DIALOG_FLOW_PROJECT_ID')

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=user_message, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback