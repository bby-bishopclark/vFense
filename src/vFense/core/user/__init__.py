import re
from vFense.core.user._db_model import UserKeys
from vFense.core._constants import (
    RegexPattern, DefaultStringLength, CommonKeys
)
from vFense.core.user._constants import UserDefaults


class User(object):
    """Used to represent an instance of a user."""

    def __init__(
            self, name, password=None, full_name=None, email=None,
            current_customer=None, default_customer=None,
            enabled=None, is_global=None
    ):
        """
        Args:
            name (str): The name of the user.

        Kwargs:
            password (str): The users password.
            full_name (str): The full name of the user.
            email (str): The email of the user.
            current_customer (str): The customer you are currently logged into.
            default_customer (str): The default customer of the user.
            enabled (boolean): Disable or enable this user.
            is_global (boolean):Is this user a global user.
        """
        self.name = name
        self.full_name = full_name
        self.email = email
        self.password = password
        self.current_customer = current_customer
        self.default_customer = default_customer
        self.enabled = enabled
        self.is_global = is_global


    def fill_in_defaults(self):
        """Replace all the fields that have None as their value with
        the hardcoded default values.

        Use case(s):
            Useful when creating a new user instance and only want to fill
            in a few fields, then allow the create user functions call this
            method to fill in the rest.
        """

        if not self.full_name:
            self.full_name = UserDefaults.FULL_NAME

        if not self.email:
            self.email = UserDefaults.EMAIL

        if not self.enabled:
            self.enabled = UserDefaults.ENABLED

        if not self.is_global:
            self.is_global = UserDefaults.IS_GLOBAL

    def get_invalid_fields(self):
        """Check the user for any invalid fields.

        Returns:
            (list): List of key/value pair dictionaries corresponding
                to the invalid fields.

                Ex:
                    [
                        {'customer_name': 'the invalid name in question'},
                        {'net_throttle': -10}
                    ]
        """
        invalid_fields = []

        if isinstance(self.name, basestring):
            valid_symbols = re.search(
                RegexPattern.USERNAME, self.name
            )
            valid_length = len(self.name) <= DefaultStringLength.USER_NAME

            if not valid_symbols and valid_length:
                invalid_fields.append(
                    {
                        UserKeys.UserName: self.name,
                        CommonKeys.REASON: 'Invalid characters in username'
                    }
                )
            elif not valid_length and valid_symbols:
                invalid_fields.append(
                    {
                        UserKeys.UserName: self.name,
                        CommonKeys.REASON: 'Username is too long'
                    }
                )
            elif not valid_length and not valid_symbols:
                invalid_fields.append(
                    {
                        UserKeys.UserName: self.name,
                        CommonKeys.REASON: (
                            'Username is too long and ' +
                            'Invalid characters in username'
                        )
                    }
                )
        else:
            invalid_fields.append(
                {
                    UserKeys.UserName: self.name,
                    CommonKeys.REASON: 'username is not a valid string'
                }
            )

        if not isinstance(self.enabled, bool):
            invalid_fields.append(
                {
                    UserKeys.Enabled: self.enabled,
                    CommonKeys.REASON: 'Must be a boolean value'
                }
            )

        if not isinstance(self.is_global, bool):
            invalid_fields.append(
                {
                    UserKeys.Global: self.is_global,
                    CommonKeys.REASON: 'Must be a boolean value'
                }
            )

        return invalid_fields

    def to_dict(self):
        """ Turn the customer fields into a dictionary.

        Returns:
            (dict): A dictionary with the fields corresponding to the
                customer.

                Ex:
                {
                    "agent_queue_ttl": 100 ,
                    "cpu_throttle":  "high" ,
                    "customer_name":  "default" ,
                    "net_throttle": 100 ,
                    "package_download_url_base": https://192.168.8.14/packages/,
                    "server_queue_ttl": 100
                }
                    
        """

        return {
            UserKeys.UserName: self.name,
            UserKeys.CurrentCustomer: self.current_customer,
            UserKeys.DefaultCustomer: self.default_customer,
            UserKeys.FullName: self.full_name,
            UserKeys.Email: self.email,
            UserKeys.Global: self.is_global,
            UserKeys.Enabled: self.enabled
        }

    def to_dict_non_null(self):
        """ Use to get non None fields of customer. Useful when
        filling out just a few fields to update the customer in the db.

        Returns:
            (dict): a dictionary with the non None fields of this customer.
        """
        user_dict = self.to_dict()

        return {k:user_dict[k] for k in user_dict
                if user_dict[k] != None}
