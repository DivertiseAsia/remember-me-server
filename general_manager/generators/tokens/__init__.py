from django.contrib.auth.tokens import PasswordResetTokenGenerator
from general_manager.generators.tokens.leave_request import LeaveRequestTokenGenerator


__all__ = ['PasswordResetToken', 'LeaveRequestToken']


PasswordResetToken = PasswordResetTokenGenerator()
LeaveRequestToken = LeaveRequestTokenGenerator()
