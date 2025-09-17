from . import common_controller, auth_controller, user_controller, product_controller, category_controller,  media_controller, order_controller, cart_controller, checkout_controller, shipping_controller, review_controller, product_inventory_controller

def register_routers(app):
    app.include_router(common_controller.router, prefix="/api")
    app.include_router(auth_controller.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(user_controller.router, prefix="/api/users", tags=["Users"])
    app.include_router(category_controller.router, prefix="/api/categories", tags=["Categories"] )
    app.include_router(product_controller.router, prefix="/api/products", tags=["Products"])
    app.include_router(media_controller.router, prefix="/api", tags=["Upload"])
    app.include_router(order_controller.router, prefix="/api", tags=["Order"])
    app.include_router(cart_controller.router, prefix="/api", tags=["Carts"])

    app.include_router(checkout_controller.router, prefix="/api", tags=["Checkout"])
    app.include_router(shipping_controller.router, prefix="/api", tags=["Shipping"])
    app.include_router(review_controller.router, prefix="/api", tags=["Reviews"])
    app.include_router(product_inventory_controller.router, prefix="/inventory", tags=["Inventory"])