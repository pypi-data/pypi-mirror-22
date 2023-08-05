from tornado.web import HTTPError


class BlossomHTTPError(HTTPError):
    def __init__(self, code_type):
        # Call the base class constructor with the parameters it needs
        """
        :param code_type is from BlossomHTTPErrors
        """
        super(BlossomHTTPError, self).__init__(code_type[1], code_type[2])
        self.custom_code = code_type[0]


class BlossomHTTPErrors:
    USER_NOT_FOUND = (200, 404, "User not found")
    INVALID_JSON_FORMAT = (201, 400, "Invalid json format")
    EMAIL_ALREADY_EXIST = (202, 409, "Email already exist")
    WRONG_ATTRIBUTES = (203, 422, "Wrong attributes")
    BAD_PASSWORD_OR_EMAIL = (204, 422, "Invalid email or password")
    error_map = {
        200: USER_NOT_FOUND,
        201: INVALID_JSON_FORMAT,
        202: EMAIL_ALREADY_EXIST,
        203: WRONG_ATTRIBUTES,
        204: BAD_PASSWORD_OR_EMAIL
    }
