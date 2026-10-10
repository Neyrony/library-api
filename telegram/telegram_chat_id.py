import requests

from library.settings import TELEGRAM_BOT_TOKEN


def get_telegram_chat_id():
    """
    Create a telegram chat id and telegram bot via @BotFather
    Than the token that @BotFather will give you put in .env
    Add your bot in your own chat and give him admin permissions
    Run code and get your chat id, then put chat id into the .env file
    """

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    )
    print(response.json())


if __name__ == "__main__":
    get_telegram_chat_id()
