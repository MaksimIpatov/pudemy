from typing import Any

import stripe
from django.conf import settings
from stripe import Price, Product

stripe.api_key = settings.STRIPE_API_KEY


class StripeService:
    """Сервис для работы с API Stripe."""

    @staticmethod
    def create_product(name: str, description: str) -> Product:
        """
        Создает продукт в Stripe.

        :param name: Название продукта.
        :param description: Описание продукта.
        :return: Объект продукта.
        """
        return stripe.Product.create(
            name=name,
            description=description,
        )

    @staticmethod
    def create_price(
        amount: float,
        currency: str = "rub",
        product_name: str = "Покупка курса",
    ) -> Price:
        """
        Создает цену в Stripe.

        :param amount: Сумма в основных единицах валюты.
        :param currency: Код валюты. По умолчанию рубли.
        :param product_name: Название продукта для отображения.
        :return: Объект цены.
        """
        return stripe.Price.create(
            unit_amount=int(amount * 100),
            currency=currency,
            product_data={"name": product_name},
        )

    @staticmethod
    def create_session(
        price_id: str,
        success_url: str,
        cancel_url: str = "http://127.0.0.1:8000/",
    ) -> dict[str, Any]:
        """
        Создает сессию оплаты в Stripe.

        :param price_id: ID цены.
        :param success_url: URL, на который пользователь
        будет перенаправлен при успешной оплате.
        :param cancel_url: URL для перенаправления при отмене оплаты.
        :return: Словарь с ID и URL сессии.
        """
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {"id": session.get("id"), "url": session.get("url")}

    @staticmethod
    def retrieve_session(session_id):
        """Получает данные о сессии оплаты в Stripe.

        :param session_id: ID сессии.
        :return: Словарь с данными о сессии, статус платежа,
        общую сумму и валюту.
        """
        return stripe.checkout.Session.retrieve(session_id)
