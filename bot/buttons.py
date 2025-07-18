from telegram import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Sneeze"), KeyboardButton("Yawn")],
        [KeyboardButton("#1"), KeyboardButton("#2"), KeyboardButton("#1 & #2")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

BUTTON_TEXTS_SET = set(button.text for row in main_keyboard.keyboard for button in row)
