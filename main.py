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
PREFIX = "https://smashkarts.io/link/?"

FORMAT_CHOICE, SCORE_TARGET_CHOICE, MAP_CHOICE = range(3)

MAPS = {
    "1": "graveyard",
    "2": "skyarena-temples",
    "3": "snowpark",
    "4": "theoldgraveyard",
    "5": "thegravelpit",
    "6": "smashisland",
    "7": "skatepark",
    "8": "slicknslide",
    "9": "stekysspeedway",
    "10": "skyarena-tunnels"
}
MAPS_NAME = {
    "1": "Graveyard",
    "2": "Sky Arena Temples",
    "3": "Snowpark",
    "4": "The Old Graveyard",
    "5": "The Gravel Pit",
    "6": "Smash Island",
    "7": "Skatepark",
    "8": "Slick'n Slide",
    "9": "Steky's Speedway",
    "10": "Sky Arena Tunnels"
}

TIMER_MODE = {
    "3": 67109640,
    "6": 67110408,
    "10": 67111432,
    "20": 67113992
}

SCORE_MODE = {
    "10": 67272716,
    "20": 67436556
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, Smashkarter! \n"
        "Reply 'timer' for a Timer Match ⏳\n"
        "Reply 'target' for Score Target Match 🎯"
    )
    return FORMAT_CHOICE

async def format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.strip().lower()
    
    if (response == "timer"):
        context.user_data["is_timer"] = True
        await update.message.reply_text("You have selected a timer match. Select a time then you can select a map.")
        await update.message.reply_text(
        "Reply 3 for a 3 minutes match \n" 
        "Reply 6 for a 6 minutes match \n" 
        "Reply 10 for a 10 minutes match \n" 
        "Reply 20 for a 20 minutes match"
        )
        return SCORE_TARGET_CHOICE
    
    elif (response == "target"):
        context.user_data["is_timer"] = False
        await update.message.reply_text("You have selected a score target match. Select a score, then you can select a map.")
        await update.message.reply_text("" 
        "Reply 10 for a 10 score target match \n" 
        "Reply 20 for a 20 score target match")
        return SCORE_TARGET_CHOICE
    elif (response == "owner"):
        await update.message.reply_text("gambit_pnav")
        return FORMAT_CHOICE
    else:
        await update.message.reply_text("❌ Enter a valid choice")
        return FORMAT_CHOICE


async def score_target_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.strip()
    is_timer = context.user_data.get("is_timer")

    if is_timer == True:

        if response not in TIMER_MODE.keys():
            await update.message.reply_text("Enter a valid choice")
            return SCORE_TARGET_CHOICE

        context.user_data["time"] = response
        await update.message.reply_text(
            f"You have selected a {response} minutes timer match."
        )

    else:
        if response not in SCORE_MODE:
            await update.message.reply_text("❌ Enter a valid choice")
            return SCORE_TARGET_CHOICE

        context.user_data["score"] = response
        await update.message.reply_text(
            f"You have selected a {response} target match."
        )

    await update.message.reply_text(
        "Select one of the map numbers:\n"
        "1. Graveyard\n"
        "2. Sky Arena Temples\n"
        "3. Snowpark\n"
        "4. The Old Graveyard\n"
        "5. The Gravel Pit\n"
        "6. Smash Island\n"
        "7. Skate Park\n"
        "8. Slick'n Slide\n"
        "9. Steky's Speedway\n"
        "10. Sky Arena Tunnels"
    )
    return MAP_CHOICE


async def map_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.strip()

    if response not in MAPS:
        await update.message.reply_text("❌ Please enter a valid map number (1-10).")
        return MAP_CHOICE

    game_code = random.randint(600000, 699999)
    is_timer = context.user_data.get("is_timer", True)

    if is_timer:
        time = context.user_data.get("time", "3")
        await update.message.reply_text(
            f"You have selected a timer match of {time} minutes in {MAPS_NAME[response]}."
        )
        game_link = f"{PREFIX}mode={TIMER_MODE[time]}&room=in{game_code}&arena={MAPS[response]}"

    else:
        score = context.user_data.get("score", "10")
        await update.message.reply_text(
            f"You have selected a Score Target match of {score} in {MAPS_NAME[response]}."
        )
        game_link = f"{PREFIX}mode={SCORE_MODE[score]}&room=in{game_code}&arena={MAPS[response]}"

    await update.message.reply_text(f"🎮 Game Link: {game_link}")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Conversation cancelled. Type /start to begin again.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            FORMAT_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, format_choice)],
            SCORE_TARGET_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, score_target_choice)],
            MAP_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, map_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("🚀 Bot is polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
