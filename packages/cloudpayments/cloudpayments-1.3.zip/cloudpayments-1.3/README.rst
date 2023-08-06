===================================
CloudPayments Python Client Library
===================================

Клиент для платежного сервиса `CloudPayments <http://cloudpayments.ru/>`_. Позволяет обращаться к `API CloudPayments <http://cloudpayments.ru/Docs/Api>`_ из кода на Python.

Установка
=========

::

    pip install cloudpayments


Требования
==========

Python 2.6+ или 3+


Использование
=============

.. code:: python

    from cloudpayments import CloudPayments

    client = CloudPayments('public_id', 'api_secret')
    client.test()

При создании клиента задаются аутентификационные параметры: Public ID и Api Secret. Оба этих значения можно получить в личном кабинете.

Обращение к API осуществляется через методы клиента.


| **Тестовый метод** (`описание <http://cloudpayments.ru/Docs/Api#ping>`_)

.. code:: python

    test(request_id=None)

``request_id`` — идентификатор для `идемпотентного запроса <https://cloudpayments.ru/docs/api/kassa#idempotent>`_.

В случае успеха возвращает строку с сообщением от сервиса.


| **Оплата по криптограмме** (`описание <http://cloudpayments.ru/Docs/Api#payWithCrypto>`_)

.. code:: python

    charge_card(self, cryptogram, amount, currency, name, ip_address,
                invoice_id=None, description=None, account_id=None,
                email=None, data=None, require_confirmation=False)

``currency`` — одна из констант, определенных в классе ``Currency``

``data`` — произвольные данные, при отправке будут сериализованы в JSON.

``require_confirmation`` — если установлено в ``True``, платеж будет выполняться по двухстадийной схеме.

В случае успеха возвращает объект типа ``Transaction`` (если не требуется 3-D Secure аутентификация) либо ``Secure3d`` (если требуется).


| **Завершение оплаты после прохождения 3-D Secure** (`описание <http://cloudpayments.ru/Docs/Api#3ds>`_)

.. code:: python

    finish_3d_secure_authentication(self, transaction_id, pa_res)

В случае успеха возвращает объект типа ``Transaction``.


| **Оплата по токену** (`описание <http://cloudpayments.ru/Docs/Api#payWithToken>`_)

.. code:: python

    charge_token(self, token, account_id, amount, currency,
                 ip_address=None, invoice_id=None, description=None,
                 email=None, data=None, require_confirmation=False)

``currency`` — одна из констант, определенных в классе ``Currency``

``data`` — произвольные данные, при отправке будут сериализованы в JSON.

``require_confirmation`` — если установлено в ``True``, платеж будет выполняться по двухстадийной схеме.

В случае успеха возвращает объект типа ``Transaction``.


| **Подтверждение оплаты** (`описание <http://cloudpayments.ru/Docs/Api#confirm>`_)

.. code:: python

    confirm_payment(self, transaction_id, amount)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Отмена оплаты** (`описание <http://cloudpayments.ru/Docs/Api#void>`_)

.. code:: python

    void_payment(self, transaction_id)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Возврат денег** (`описание <http://cloudpayments.ru/Docs/Api#refund>`_)

.. code:: python

    refund(self, transaction_id, amount)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Проверка статуса платежа** (`описание <http://cloudpayments.ru/Docs/Api#find>`_)

.. code:: python

    find_payment(self, invoice_id)

В случае успеха возвращает объект типа ``Transaction``.


| **Выгрузка списка транзакций** (`описание <http://cloudpayments.ru/Docs/Api#list>`_)

.. code:: python

    list_payments(self, date, timezone=None)

``date`` — объект типа ``datetime.date``.

``timezone`` — одна из констант, определенных в классе ``Timezone``.

В случае успеха возвращает список объектов типа ``Transaction``.


| **Создание подписки** (`описание <http://cloudpayments.ru/Docs/Api#create-recurrent>`_)

.. code:: python

    create_subscription(self, token, account_id, amount, currency,
                        description, email, start_date, interval, period,
                        require_confirmation=False, max_periods=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``start_date`` — объект типа ``datetime.datetime``.

``interval`` — одна из констант, определенных в классе ``Interval``.

В случае успеха возвращает объект типа ``Subscription``.


| **Запрос статуса подписки** (`описание <http://cloudpayments.ru/Docs/Api#get-recurrent>`_)

.. code:: python

    get_subscription(self, subscription_id)

В случае успеха возвращает объект типа ``Subscription``.


| **Изменение подписки** (`описание <http://cloudpayments.ru/Docs/Api#update-recurrent>`_)

.. code:: python

    update_subscription(self, subscription_id, amount=None, currency=None,
                        description=None, start_date=None, interval=None,
                        period=None, require_confirmation=None,
                        max_periods=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``start_date`` — объект типа ``datetime.datetime``.

``interval`` — одна из констант, определенных в классе ``Interval``.

В случае успеха возвращает объект типа ``Subscription``.


| **Отмена подписки** (`описание <http://cloudpayments.ru/Docs/Api#cancel-recurrent>`_)

.. code:: python

    cancel_subscription(self, subscription_id)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Отправка счета по почте** (`описание <http://cloudpayments.ru/Docs/Api#createOrder>`_)

.. code:: python

    create_order(self, amount, currency, description, email=None,
                 send_email=None, require_confirmation=None,
                 invoice_id=None, account_id=None, phone=None,
                 send_sms=None, send_whatsapp=None, culture_info=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``culture_info`` — одна из констант, определенных в классе ``CultureInfo``.

В случае успеха возвращает объект типа ``Order``.


| **Формирование кассового чека** (`описание <https://cloudpayments.ru/docs/api/kassa#receipt>`_)

.. code:: python

    create_receipt(self, inn, receipt_type, customer_receipt, 
                   invoice_id=None, account_id=None, request_id=None)

``receipt_type`` — одна из констант, определенных в классе ``ReceiptType``.

``customer_receipt`` — объект типа ``Receipt`` или словарь с данными чека.

``request_id`` — идентификатор для `идемпотентного запроса <https://cloudpayments.ru/docs/api/kassa#idempotent>`_.

В случае успеха возвращает строку с сообщением от сервиса.


Авторы
======

Разработано в `Antida software <http://antidasoftware.com>`_.
Мы создаем SaaS-продукты и сервисы, интегрированные с платежными системами.
Пишите нам, если вам нужна консультация по работе с биллинговыми системами: `info@antidasoftware.com <info@antidasoftware.com>`_.


Лицензия
========

MIT