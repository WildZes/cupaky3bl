import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from lila_data import lila_board

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

player_position = 0
board_size = len(lila_board)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global player_position
    player_position = 1
    await update.message.reply_text(f"Привет! Давай сыграем в простую игру. Твоя позиция: {player_position}")

async def make_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global player_position
    dice_roll = random.randint(1, 6)
    player_position = (player_position + dice_roll) # % board_size
    if player_position == 68:
        await update.message.reply_text(f"Вы достигли {lila_board[player_position]['name']}, поэтому"
                                  f" вашему желанию открыта дорога!")
    elif player_position < board_size:
        player_position = lila_board[player_position]["destination"]
        await update.message.reply_text(f"Ты бросил кубик и выпало {dice_roll}. "
                                        f"Твоя новая позиция: {lila_board[player_position]['name']}, на клетке "
                                        f"{player_position}. "
                                        f"Твой помощник: {lila_board[player_position]['description']} ")
    else:
        player_position = (board_size - 1) - (player_position - (board_size - 1))
        print(board_size-1, player_position - (board_size - 1))
        player_position = lila_board[player_position]["destination"]
        if player_position != 68:
            await update.message.reply_text(f"Ты бросил кубик и выпало {dice_roll}. "
                                            f"Твоя новая позиция: {lila_board[player_position]['name']} "
                                            f"Твой помощник: {lila_board[player_position]['description']}")
        else:
            await update.message.reply_text(f"Вы достигли {lila_board[player_position]['name']}, поэтому"
                                            f" вашему желанию открыта дорога!")


if __name__ == '__main__':
    print(board_size)
    TOKEN = "5016831506:AAFEI1KlVOOnNqXIWMsbK1NY1W77f48T44g" # Замените на ваш токен
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    move_handler = CommandHandler('move', make_move) # Команда для хода

    application.add_handler(start_handler)
    application.add_handler(move_handler)

    application.run_polling()
