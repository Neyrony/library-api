import os

import stripe
from django.conf import settings
from django.urls import reverse

from borrowings.models import Borrowing

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def calculate_book_price(borrowing: Borrowing) -> int:
    if getattr(borrowing, "actual_return_date", None) is None:
        return int(
            round(
                (borrowing.expected_return_date - borrowing.borrow_date).days
                * borrowing.book.daily_fee,
                2,
            )
            * 100
        )
    return int(
        round(
            (borrowing.actual_return_date - borrowing.expected_return_date).days
            * borrowing.book.daily_fee
            * borrowing.book.FINE_MULTIPLIER,
            2,
        )
        * 100
    )


def create_stripe_payment(borrowing: Borrowing) -> dict:
    money_to_pay = calculate_book_price(borrowing)
    stripe_session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": money_to_pay,
                    "product_data": {
                        "name": str(borrowing),
                        "description": f"It is borrowing that "
                        f"was created {borrowing.borrow_date}. "
                        f"Borrowing book is {borrowing.book.title} "
                        f"from {borrowing.book.author}",
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=settings.DOMAIN
        + reverse("borrowings:borrowing-list"),  # It is temporary it will be changed
        cancel_url=settings.DOMAIN
        + reverse("borrowings:borrowing-list"),  # It is temporary it will be changed
        customer_email=borrowing.user.email,
    )

    return {
        "session_id": stripe_session.id,
        "session_url": stripe_session.url,
        "money_to_pay": money_to_pay,
    }


# def get or change payment if session is expired
