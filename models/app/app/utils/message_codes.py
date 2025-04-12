""" Message codes for api responses """


from app.core.middleware.get_accept_language_middleware import get_accept_language



def parseAcceptLanguage(acceptLanguage: str):
    print(acceptLanguage)
    language_codes = []
    for language in acceptLanguage.split(","):
        language = language.split(";", 1)[0]
        language = language.split("-", 1)[0]
        language = language.strip()
        language_codes.append(language)

    return language_codes


class MessageCodes:
    @classmethod
    def get_message(cls, message_code: int) -> str:
        parsed_accept_languages = parseAcceptLanguage(get_accept_language())

        for accept_language in parsed_accept_languages:
            match accept_language:
                case "fa":
                    return cls.persian_message_names[message_code]
                case "en":
                    return cls.english_messages_names[message_code]

        return cls.persian_message_names[message_code]

    # main codes start from 0
    successful_operation = 0
    internal_error = 1
    not_found = 2
    bad_request = 3
    input_error = 4
    operation_failed = 5
    incorrect_email_or_password = 6
    inactive_user = 7
    permission_error = 8
    already_exist_object = 9
    not_authorized = 10
    expired_token = 11
    access_token_not_found = 12
    refresh_token_not_found = 13
    invalid_token = 14
    # services code start from 1001

    english_messages_names = {
        0: "Successful Operation",
        1: "Internal Error",
        2: "Not Found",
        3: "Bad Request",
        4: "Input Error",
        5: "Operation Failed",
        6: "Invalid Email Or Password",
        7: "Inactive User",
        8: "Dont Have Access",
        9: "Object already exists",
        10: "Not Authorized",
        11: "Expired Token",
        12: "Access Token Not Found",
        13: "Refresh Token Not Found",
        14: "Invalid Token",
    }
