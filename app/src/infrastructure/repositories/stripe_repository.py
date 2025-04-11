import asyncio

import stripe
from stripe import ListObject, Product
from stripe.checkout import Session


class StripeRepository:
    @classmethod
    async def get_products(cls) -> ListObject[Product]:
        params = {"active": True, "expand": ["data.default_price"]}
        products = await asyncio.to_thread(stripe.Product.list, **params)
        return products

    @classmethod
    async def get_product(cls, product_id: str) -> Product:
        product = await asyncio.to_thread(stripe.Product.retrieve, product_id)
        return product

    @classmethod
    async def get_checkout_session(cls, session_id: str) -> Session:
        checkout_session = await asyncio.to_thread(stripe.checkout.Session.retrieve, session_id)
        return checkout_session

    @classmethod
    async def create_checkout_session(cls, params: dict) -> Session:
        checkout_session = await asyncio.to_thread(stripe.checkout.Session.create, **params)
        return checkout_session
