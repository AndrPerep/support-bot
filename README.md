# Бот службы поддержки
Универсальные боты для ВКонтакте и Телеграм, отвечающий на вопросы 
пользователей с помощью [Google DialogFlow](https://dialogflow.cloud.google.com/).
### Написать ботам:
- [**Бот службы поддержки в Телеграм**](https://t.me/good1234234bot)  
- [**Бот службы поддержки во ВКонтакте**](https://vk.me/public210417012)

![Пример работы](bot.gif) 
### Установка
Для работы необходим [Python 3](https://www.python.org/). Установите библиотеки с помощью команды:
```commandline
py pip install -r requirements.txt 
```
Для работы необходим проект Google Cloud и связанный с ним агент DialogFlow.  
- [Как создать Google Cloud проект](https://cloud.google.com/dialogflow/es/docs/quick/setup#project) (en)
- [Как создать DialogFlow agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) (en)  
Google Cloud проект и агент DialogFlow должны иметь один и тот же `id`.  

В папке с проектом необходимо создать файл `.env` со следующими переменными в формате `КЛЮЧ=ЗНАЧЕНИЕ`:
- `TG_TOKEN` – токен телеграм-бота. Создать бота и узнать его токен можно через [@BotFather](https://t.me/botfather);
- `VK_TOKEN` – токен (API ключ) сообщества ВКонтакте. 
Получить его можно в настройках сообщества в разделе "Работа с API";
- `DIALOG_FLOW_PROJECT_ID` – id проекта Dialog Flow (он же – id Google-проекта). 
Находится в настройках проекта Dialog Flow;
- `GOOGLE_APPLICATION_CREDENTIALS` – путь к json-ключу Google проекта. 
[Как получить ключ](https://cloud.google.com/docs/authentication/client-libraries) (en)
- `ADMIN_BOT_TOKEN` – токен телеграм-бота, который будет присылать логи.
Создать бота и получить токен: [@BotFather](https://t.me/botfather);
- `ADMIN_CHAT_ID` – id телеграм-чата, в который бот-админ будет присылать логи. 
Пользователь должен первым написать боту-админу, чтобы он мог присылать сообщения.
Узнать свой id: [@userinfobot](https://t.me/userinfobot).
- `PHRASES_FILE` – путь к .json файлу со своими ответами на вопросы для обучения DialogFlow.
По умолчанию – `phrases.json`. Подробнее – [далее](https://github.com/AndrPerep/support-bot#своиответы) в документации

### Запуск
Для запуска ботов Телеграм и ВКонтакте используйте соответственно команды:
```commandline
py tg_bot.py
```
```commandline
py vk_bot.py
```
### Свои ответы
Проект также содержит скрипт для обучения DialogFlow. Вы можете сохранить свои ответы на вопросы пользователей 
в файле `.json` и указать путь к нему в переменной окружения `PHRASES_FILE`. Формат файла:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?"
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту..."
  },
  "Забыл пароль": {
    "questions": [
      "Не помню пароль",
      "Не могу войти"
    ],
    "answer": "Если вы не можете войти на сайт, воспользуйтесь..."
  }
}
```
Для запуска обучения и сохранения ответов используйте:
```commandline
py create_dialogflow_intents.py
```
Просмотреть и отредактировать сохранённые ответы можно в разделе Intents настроек агента [Dialog Flow](https://dialogflow.cloud.google.com/).
### Цель проекта
Проект создан в учебных целях на курсе [Devman](https://dvmn.org/).