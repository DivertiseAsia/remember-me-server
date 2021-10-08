from datetime import date

import six
from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36


class LeaveRequestTokenGenerator:
    key_salt = "RememberME.LeaveRequestTokenGenerator"
    secret = settings.SECRET_KEY

    @staticmethod
    def _make_hash_value(leave_request, timestamp):
        return six.text_type(leave_request.rid) + six.text_type(timestamp) + six.text_type(leave_request.status)

    def _make_token_with_timestamp(self, leave_request, timestamp):
        ts_b36 = int_to_base36(timestamp)
        salted_hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(leave_request, timestamp),
            secret=self.secret,
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, salted_hash)

    @staticmethod
    def _num_days(dt):
        return (dt - date(2001, 1, 1)).days

    @staticmethod
    def _today():
        return date.today()

    def make_token(self, leave_request):
        return self._make_token_with_timestamp(leave_request, self._num_days(self._today()))

    def check_token(self, leave_request, token):
        if not (leave_request and token):
            return False

        try:
            ts_b36, leave_request = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if not constant_time_compare(self._make_token_with_timestamp(leave_request, ts), token):
            return False

        if (self._num_days(self._today()) - ts) > settings.PASSWORD_RESET_TIMEOUT_DAYS:
            return False

        return True
