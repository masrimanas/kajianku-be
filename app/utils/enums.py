from enum import Enum


class RouteTags(Enum):
    USERS = "Users"
    KAJIAN = "Kajian"
    CHATBOT = "Chatbot"


class RouteName(Enum):
    USERS = "/users"
    KAJIAN = "/kajian"
    CHATBOT = "/chatbot"
