class ApiResultKeys():
    URI = 'uri'
    HTTP_METHOD = 'http_method'
    USERNAME = 'user_name'
    COUNT = 'count'
    HTTP_STATUS_CODE = 'http_status'
    GENERIC_STATUS_CODE = 'generic_status_code'
    VFENSE_STATUS_CODE = 'vfense_status_code'
    ERRORS = 'errors'
    DB_STATUS_CODE = 'db_status_code'
    MESSAGE = 'message'
    DATA = 'data'
    ELAPSED_SECONDS = 'elapsed_seconds'
    GENERATED_IDS = 'generated_ids'
    UNCHANGED_IDS = 'unchanged_ids'
    SKIPPED_IDS = 'skipped_ids'
    MODIFIED_IDS = 'modified_ids'
    UPDATED_IDS = 'updated_ids'
    DELETED_IDS = 'deleted_ids'
    INVALID_IDS = 'invalid_ids'
    INVALID_ID = 'invalid_id'
    OPERATIONS = 'operations'
    INVALID_DATA = 'invalid_data'
    USERNAME_IDS = 'user_name'
    NEW_TOKEN_ID = 'new_token_id'
    TOKEN = 'token'
    AGENT_ID = 'agent_id'


class ApiResultDefaults():
    @staticmethod
    def updated_ids():
        return list()

    @staticmethod
    def invalid_ids():
        return list()

    @staticmethod
    def unchanged_ids():
        return list()

    @staticmethod
    def deleted_ids():
        return list()

    @staticmethod
    def data():
        return list()

    @staticmethod
    def operations():
        return list()

    @staticmethod
    def generated_ids():
        return list()

    @staticmethod
    def errors():
        return list()


class AgentApiResultDefaults():
    @staticmethod
    def operations():
        return list()