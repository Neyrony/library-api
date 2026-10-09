from django.contrib.auth import get_user_model


class UserTestData:
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create(
            email="user@example.com",
            password="test12345",
            first_name="regular",
            last_name="user",
        )
