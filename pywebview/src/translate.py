import locale
from typing import TypedDict

# Set the locale to the default system locale
locale.setlocale(locale.LC_ALL, "")
# Get the system language
system_language = locale.getlocale()[0]


class AppTranstations(TypedDict):
    """Translations of icon and other native app parts"""

    OPEN: str
    CLOSE: str
    EXIT: str
    PROJECT_PAGE: str
    UPDATE_TITLE: str
    UPDATE_MESSAGE: str


RU: AppTranstations = {
    "OPEN": "Открыть",
    "CLOSE": "Закрыть",
    "EXIT": "Выход",
    "PROJECT_PAGE": "Страница проекта",
    "UPDATE_TITLE": "Новая версия",
    "UPDATE_MESSAGE": "Посетите страницу проекта для скачивания новой версии приложения",
}
EN: AppTranstations = {
    "OPEN": "Open",
    "CLOSE": "Close",
    "EXIT": "Exit",
    "PROJECT_PAGE": "Project page",
    "UPDATE_TITLE": "New version",
    "UPDATE_MESSAGE": "Visit the project page to download the new version of the application",
}

TRANSLATIONS: AppTranstations
if "rus" in system_language.lower():
    TRANSLATIONS = RU
else:
    TRANSLATIONS = EN
