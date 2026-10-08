from django.utils import timezone


def validate_dates(instance, old_instance, exception):
    if not old_instance:
        if timezone.localdate() > instance.expected_return_date:
            raise exception("Expected return date should be greater than borrow date")
        elif instance.actual_return_date is not None:
            raise exception("Actual return date can not be assign on creation")
    else:
        if (
            instance.borrow_date != old_instance.borrow_date
            or instance.expected_return_date != old_instance.expected_return_date
        ):
            raise exception("You are not allowed to change borrow or expected date")

        if old_instance.actual_return_date is not None:
            raise exception("This borrowing has already been returned")

        if (
            instance.actual_return_date is not None
            and instance.actual_return_date < instance.borrow_date
        ):
            raise exception(
                "Actual return date should be greater or equal than borrow date"
            )


def validate_user_and_book(instance, old_instance, exception):
    if old_instance is not None:
        if instance.user_id != old_instance.user_id:
            raise exception("You are not allowed to change user")
        elif instance.book_id != old_instance.book_id:
            raise exception("You are not allowed to change book")
