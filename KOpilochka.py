import flet as ft


async def main(page: ft.Page):
    # Заголовок приложения.
    page.title = "Кошелёк твой мамы ❤❤❤"
    page.add(ft.Text("Играй в казик и считай своё бабло.", size=28))

    # Выравниваем интерфейс по центру.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Хранилище данных приложения.
    prefs = ft.SharedPreferences()

    # -----------------------------
    # ЗАГРУЖАЕМ СОХРАНЁННЫЕ ДАННЫЕ
    # -----------------------------

    saved_money = await prefs.get("money_saver.amount")

    if saved_money is None:
        saved_money = 0

    saved_name = await prefs.get("money_saver.name")

    if saved_name is None:
        saved_name = ""

    # -----------------------------
    # СОСТОЯНИЕ
    # -----------------------------

    state = {
        "money": saved_money,
    }

    # -----------------------------
    # ЭЛЕМЕНТЫ ИНТЕРФЕЙСА
    # -----------------------------

    # Поле для названия цели.
    goal_input = ft.TextField(
        label="You gay?",
        value=saved_name,
        width=320,
    )

    # Накопленная сумма в центре круга.
    money_text = ft.Text(
        f'{state["money"]} ₽',
        size=32,
        weight=ft.FontWeight.BOLD,
    )

    # Круг с накопленной суммой.
    money_circle = ft.Container(
        width=220,
        height=220,
        content=money_text,
        alignment=ft.Alignment.CENTER,
        border_radius=110,
        border=ft.Border.all(width=4),
    )

    # Поле ввода суммы.
    amount_input = ft.TextField(
        label="Введите сумму",
        hint_text="Например: 1000 или -500",
        width=250,
    )

    # Сообщение об ошибке.
    message = ft.Text("")

    # -----------------------------
    # СОХРАНЕНИЕ НАЗВАНИЯ
    # -----------------------------

    async def save_name(e):
        # Получаем название цели из поля.
        name = (goal_input.value or "").strip()

        # Сохраняем название.
        await prefs.set(
            "money_saver.name",
            name,
        )

    # Сохраняем название после выхода из поля.
    goal_input.on_blur = save_name

    # -----------------------------
    # ДОБАВЛЕНИЕ / ВЫЧИТАНИЕ СУММЫ
    # -----------------------------

    async def add_money(e):
        try:
            # Преобразуем введённый текст в число.
            amount = int(amount_input.value)

        except ValueError:
            # Если введено не число.
            message.value = "Введите целое число"
            return

        # Добавляем число к текущей сумме.
        # Если amount отрицательный,
        # деньги будут вычтены.
        state["money"] += amount

        # Обновляем сумму в круге.
        money_text.value = f'{state["money"]} ₽'

        # Очищаем поле ввода.
        amount_input.value = ""

        # Убираем сообщение об ошибке.
        message.value = ""

        # Сохраняем новую сумму.
        await prefs.set(
            "money_saver.amount",
            state["money"],
        )

    # -----------------------------
    # СБРОС НАКОПЛЕНИЙ
    # -----------------------------

    async def reset_money(e):
        # Обнуляем накопленную сумму.
        state["money"] = 0

        # Обновляем текст в круге.
        money_text.value = "0 ₽"

        # Очищаем сообщение.
        message.value = ""

        # Сохраняем ноль.
        await prefs.set(
            "money_saver.amount",
            0,
        )

    # -----------------------------
    # СОБИРАЕМ ИНТЕРФЕЙС
    # -----------------------------

    page.add(
        ft.Column(
            controls=[
                goal_input,

                ft.Container(height=30),

                money_circle,

                ft.Container(height=30),

                amount_input,

                ft.Row(
                    controls=[
                        ft.Button(
                            content="Добавить",
                            on_click=add_money,
                        ),

                        ft.Button(
                            content="Сбросить",
                            on_click=reset_money,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                message,
            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )


ft.run(main)