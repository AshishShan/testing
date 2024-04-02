from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.text import slugify

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +  # Use str instead of six.text_type
            str(user.is_active)
        )

generate_token = TokenGenerator()
