class Discount:
    """
    Описание: Класс представляет собой модель скидки, которая может быть применена к заказу или к отдельному товару.
    Атрибуты:
        description: строка, описывающая скидку.
        discount_percent: целое число, представляющее процент скидки.
        discount_type: строка, обозначающая тип скидки (global или item).
    Методы:
        __init__: конструктор для создания нового объекта скидки.
        apply_discount: статический метод для применения скидки к цене.
        __str__: метод для представления объекта скидки в виде строки.
        __repr__: метод для представления объекта скидки в удобной форме для разработчика.
        get_discounts_by_type: классовый метод для получения списка скидок по типу.
        register_discount: классовый метод для регистрации новой скидки.
        unregister_discount: классовый метод для удаления скидки.

        пример:
            # Создание скидок
            black_friday = Discount("Черная пятница", 50, "global")
            for_it = Discount("Для ЭТОГО", 20, "item")

            # Регистрация скидок
            Discount.register_discount(black_friday)
            Discount.register_discount(for_it)
    """
    def __init__(self, description: str, discount_percent: int, discount_type: str):
        self.description = description
        self.discount_percent = discount_percent
        self.discount_type = discount_type

    @staticmethod
    def apply_discount(price, discount_percent):
        return price * (1 - discount_percent / 100)

    def __str__(self):
        return f"Название: {self.description}: Скидка {self.discount_percent}% (Тип скидки: {self.discount_type})"

    def __repr__(self):
        return f"Discount({self.description!r}, {self.discount_percent}, {self.discount_type!r})"

    @classmethod
    def get_discounts_by_type(cls, discount_type):
        return [d for d in cls.discounts.values() if d.discount_type == discount_type]

    @classmethod
    def register_discount(cls, discount):
        cls.discounts[discount.description] = discount

    @classmethod
    def unregister_discount(cls, description):
        del cls.discounts[description]


class Product:
    """
    Описание: Класс представляет собой модель товара, который может участвовать в заказе.
    Атрибуты:
        name: строка, представляющая название товара.
        price: вещественное число, представляющее цену товара.
        types: список строк, представляющий типы скидок, применимые к товару.
    Методы:
        __init__: конструктор для создания нового объекта товара.
        __str__: метод для представления объекта товара в виде строки.
        __repr__: метод для представления объекта товара в удобной форме для разработчика.
    Пример:
        # Создание товаров
        laptop = Product("Ноутбук", 1000, ["global"])
        smartphone = Product("Смартфон", 500, ["global"])
        screwdriver = Product("Отвертка", 1500, ["item"])
    """

    def __init__(self, name: str, price: float, types: list):
        self.name = name
        self.price = price
        self.types = types

    def __str__(self):
        return f"Название: {self.name} (Цена: {self.price:.2f}) (типы применяемых скидок: {', '.join(self.types)})"

    def __repr__(self):
        return f"Product({self.name!r}, {self.price}, {self.types!r})"

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price


class Order:
    """
    Описание: Класс представляет собой модель заказа, состоящего из одного или нескольких товаров, возможно с применением скидок.
    Атрибуты:
        products: список объектов товаров, участвующих в заказе.
        discounts: список скидок, применяемых к заказу.
    Методы:
        __init__: конструктор для создания нового объекта заказа.
        _total_orders: классовый метод для получения количества заказов.
        total_price: метод для расчета общей стоимости заказа с учетом скидок.
        __str__: метод для представления объекта заказа в виде строки.
        __repr__: метод для представления объекта заказа в удобной форме для разработчика.

    Пример:
        # Создание заказов
        viktor_order_1 = Order([laptop, smartphone], [black_friday])
        maxim_order_1 = Order([screwdriver], [for_it])

        # Добавление заказов клиентам
        viktor.add_order(viktor_order_1)
        maxim.add_order(maxim_order_1)
    """
    _all_orders = []

    def __init__(self, products, discounts=None, order_id: int = 0):
        self.products = products
        self.order_id = order_id
        self.discounts = [] if discounts is None else discounts
        Order._all_orders.append(self)

    @classmethod
    def _total_orders(cls):
        return len(Order._all_orders)

    def total_price(self):
        total = 0
        for product in self.products:
            applicable_global_discounts = Discount.get_discounts_by_type('global')
            applicable_item_discounts = Discount.get_discounts_by_type('item')

            # Применение глобальной скидки
            if 'global' in product.types and applicable_global_discounts:
                total += Discount.apply_discount(product.price, applicable_global_discounts[0].discount_percent)
                continue

            # Применение индивидуальной скидки
            if 'item' in product.types and applicable_item_discounts:
                total += Discount.apply_discount(product.price, applicable_item_discounts[0].discount_percent)
                continue

            # Без скидки
            total += product.price

        # Применение глобальной скидки ко всей сумме
        if self.discounts:
            total = Discount.apply_discount(total, self.discounts[0].discount_percent)

        return total

    def __str__(self):
        product_list = "\n".join([str(p) for p in self.products])
        return f"Заказ № {self.order_id}:\n{product_list}\nОбщая стоимость заказа: {self.total_price():.2f}"

    def __repr__(self):
        return f"Order({self.products!r}, {self.discounts!r})"


class Customer:
    """
    Описание: Класс представляет собой модель клиента, который имеет одно или несколько заказов.
    Атрибуты:
        name: строка, представляющая имя клиента.
        orders: список объектов заказов, принадлежащих клиенту.
    Методы:
        __init__: конструктор для создания нового объекта клиента.
        _total_customers: классовый метод для получения списка клиентов.
        add_order: метод для добавления нового заказа клиенту.
        __str__: метод для представления объекта клиента в виде строки.
        __repr__: метод для представления объекта клиента в удобной форме для разработчика.

    Пример:
        # Создание клиентов
        viktor = Customer("Виктор")
        maxim = Customer("Максим")
    """
    _all_customers = []

    def __init__(self, name: str, orders=None):
        self.name = name
        self.orders = [] if orders is None else orders
        Customer._all_customers.append(self)

    @classmethod
    def _total_customers(cls):
        return Customer._all_customers

    def add_order(self, order):
        #self.orders.append(order)
        if not self.orders:
            self.orders = order
        else:
            for product in order.products:
                self.orders.products.append(product)
        return self.orders

    def __str__(self):
        return f"Клиент: {self.name}\n{self.orders}"

    def __repr__(self):
        return f"Customer({self.name!r}, {self.orders!r})"