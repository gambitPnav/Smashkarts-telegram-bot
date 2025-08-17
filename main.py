from dotenv import load_dotenv
import os
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, 
    MessageHandler, filters, 
    ContextTypes, ConversationHandler)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(BOT_TOKEN)

FORMAT_CHOICE, SCORE_TARGET_CHOICE, MAP_CHOICE = range(3)
MAPS = {
    "1": "Graveyard",
    "2": "Sky Arena Temples",
    "3": "Snowpark",
    "4": "The Old Graveyard",
    "5": "The Gravel Pit",
    "6": "Smash Island",
    "7": "Skate Park"
}


async def start_command(update, context):
    await update.message.reply_text(
        "Hi, Smashkarter! \n"
        "Reply 'timer' for a Timer Match \n"
        "Reply 'target' for Score Target Match"
    )
    return FORMAT_CHOICE

async def format_choice(update, context):
    response = update.message.text.strip().lower()
    
    if (response == "timer"):
        context.user_data["is_timer"] = True
        await update.message.reply_text("You have selected a timer match")
        await update.message.reply_text(
        "Reply 3 for a 3 minute match \n" 
        "Reply 6 for a 6 minute match \n" 
        "Reply 10 for a 10 minute match \n" 
        "Reply 20 for a 20 minutes match"
        )
        return SCORE_TARGET_CHOICE
    
    elif (response == "target"):
        context.user_data["is_timer"] = False
        await update.message.reply_text("You have selected a score target match")
        await update.message.reply_text("" 
        "Reply 10 for a 10 score target match \n" 
        "Reply 20 for a 20 score target match")
        return SCORE_TARGET_CHOICE

    else:
        await update.message.reply_text(" Enter a valid choice")
        return FORMAT_CHOICE

async def score_target_choice(update , context):

    response = update.message.text.strip()
    is_timer= context.user_data.get("is_timer")

    if is_timer == True:
        if response == "3":
            await update.message.reply_text(" You have selected 3 minutes timer match")
            context.user_data["time"] = response
        elif response == "6":
            await update.message.reply_text(" You have selected 6 minutes timer match")
            context.user_data["time"] = response
        elif response == "10":
            await update.message.reply_text(" You have selected 10 minutes timer match")
            context.user_data["time"] = response
        elif response == "20":
            await update.message.reply_text(" You have selected 20 minutes timer match")
            context.user_data["time"] = response
        else:
            await update.message.reply_text("Enter a valid choice")
            return SCORE_TARGET_CHOICE
    else:
        if response == "10":
            await update.message.reply_text(" You have selected 10 score target match")
            context.user_data["score"] = response
        elif response == "20":
            await update.message.reply_text(" You have selected 20 score target match")
            context.user_data["score"] = response
        else:
            await update.message.reply_text("Enter a valid choice")
            return SCORE_TARGET_CHOICE
    
    await update.message.reply_text(
        "Select one of the map number: \n" 
        "1. Graveyard\n"
        "2. Sky Arena Temples\n"
        "3. Snowpark\n"
        "4. The Old Graveyard\n"
        "5. The Gravel Pit\n"
        "6. Smash Island\n"
        "7. Skate Park"
    )
    return MAP_CHOICE

async def map_choice(update, context):
    response = update.message.text.strip().lower()

    if response not in MAPS:
      await update.message.reply_text("Please enter a valid map number (1-7).")
      return MAP_CHOICE

    is_timer = context.user_data.get("is_timer", True)
    
    if is_timer == True:
        time = context.user_data.get("time", 3)
        await update.message.reply_text (f"You have selected a timer match of {time} minutes in map {MAPS[response]}")
    else:
        score = context.user_data.get("score", 10)
        await update.message.reply_text (f"You have selected a score target match of {score} minutes in map no. {MAPS[response]}")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation cancelled. Type /start to begin again.")
    return ConversationHandler.END


if __name__ == '__main__':

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            FORMAT_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, format_choice)],
            SCORE_TARGET_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, score_target_choice)],
            MAP_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, map_choice)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Polling")
    app.run_polling(poll_interval=3)
