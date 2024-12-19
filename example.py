from classes import *


def summary_info():
    customers = Customer._total_customers()
    all_orders = Order._all_orders
    total_orders_count = Order._total_orders()
    total_cost = sum(o.total_price() for o in all_orders)

    print("Summary Information:")
    print(f"Customers: {', '.join(c.name for c in customers)}")
    print(f"Total Orders: {total_orders_count}")
    print(f"Total Cost: {total_cost:.2f}")


if __name__ == "__main__":
    # Инициализация словаря скидок
    Discount.discounts = {}

    # Регистрация скидок
    black_friday = Discount("Black Friday", 50, "global")
    winter_sale = Discount("Winter Sale", 10, "global")
    for_it = Discount("For IT", 0, "item")

    Discount.register_discount(black_friday)
    Discount.register_discount(winter_sale)
    Discount.register_discount(for_it)

    # Создание продуктов
    laptop = Product("Laptop", 1000, ['global'])
    smartphone = Product("Smartphone", 1000, ['global'])
    screwdriver = Product("Screwdriver", 1000, ['item'])

    # Создание клиентов
    viktor = Customer("Виктор")
    maxim = Customer("Максим")

    # Создание заказов
    viktor_order_1 = Order(
        [laptop, smartphone],
        discounts=[black_friday],
        order_id=1
    )
    maxim_order_1 = Order(
        [screwdriver, laptop],
        discounts=[black_friday],
        order_id=2
    )
    maxim_order_2 = Order(
        [screwdriver, smartphone],
        discounts=[],
        order_id=3
    )

    # Добавление заказов клиентам
    viktor.add_order(viktor_order_1)
    maxim.add_order(maxim_order_1)
    #print(f'Было:\n{maxim}')
    maxim.add_order(maxim_order_2)
    #print(f'Стало:\n{maxim}')

    # Вывод общей информации на печать
    summary_info()

    print(maxim)
    print(viktor_order_1)
    print(maxim_order_2.products)
    print(black_friday.__repr__())
    print(for_it.__str__())
    print(viktor_order_1.__repr__())
    print(laptop)