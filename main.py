from dotenv import load_dotenv
import os
import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "989400326"))
ENV = os.getenv("ENV", "dev")  # "local" or "dev"

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
    "3": 67158028,
    "6": 67207182,
    "10": 67111432,
    "20": 67113992
}

SCORE_MODE = {
    "10": 67272716,
    "20": 67436556
}

CTF_MODE = {
    "3": 67158078,
    "6": 67207230,
    "10": 67272766
}

CTF_MAPS = {
    "1": "snowparkctf",
    "2": "skatecity",
    "3": "toxictowers",
    "4": "spacestations",
    "5": "lavapitctf",
    "6": "graveyardctf",
    "7": "smashfortctf",
    "8": "skyarena-temples",
    "9": "skyarena-tunnels",
    "10": "skyarena-showdown",
    "11": "smashisland"
}

CTF_MAPS_NAME = {
    "1": "Snowpark CTF",
    "2": "Skate City",
    "3": "Toxic Towers",
    "4": "Space Stations",
    "5": "Lava Pit",
    "6": "Graveyard CTF",
    "7": "Smash Fort",
    "8": "Sky Arena Temples",
    "9": "Sky Arena Tunnels",
    "10": "Sky Arena Showdown",
    "11": "Smash Island"
}

WEAPONS = 159212

MAP_LIST_TEXT = (
    "1. Graveyard\n"
    "2. Sky Arena Temples\n"
    "3. Snowpark\n"
    "4. The Old Graveyard\n"
    "5. The Gravel Pit\n"
    "6. Smash Island\n"
    "7. Skatepark\n"
    "8. Slick'n Slide\n"
    "9. Steky's Speedway\n"
    "10. Sky Arena Tunnels"
)

CTF_MAP_LIST_TEXT = (
    "1. Snowpark CTF\n"
    "2. Skate City\n"
    "3. Toxic Towers\n"
    "4. Space Stations\n"
    "5. Lava Pit\n"
    "6. Graveyard CTF\n"
    "7. Smash Fort\n"
    "8. Sky Arena Temples\n"
    "9. Sky Arena Tunnels\n"
    "10. Sky Arena Showdown\n"
    "11. Smash Island"
)


def is_allowed_user(update: Update):
    user = update.effective_user
    
    # In local mode, only allow the specific user
    if ENV == "local":
        return user and user.id == ALLOWED_USER_ID
    
    # In dev/production mode, allow all users
    return True


def get_home_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Timer ⏳", callback_data="timer"),
            InlineKeyboardButton("Target 🎯", callback_data="target")
        ],
        [
            InlineKeyboardButton("CTF 🚩", callback_data="ctf")
        ]
    ])


async def post_init(app: Application):
    # Only send refresh message in local mode
    if ENV == "local":
        try:
            await app.bot.send_message(
                chat_id=ALLOWED_USER_ID,
                text="Bot has been refreshed! (Local Mode)"
            )
        except Exception:
            pass


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    context.user_data.clear()

    await update.message.reply_text(
        "🎮 Welcome Smashkarter!\n\nChoose a mode:",
        reply_markup=get_home_keyboard()
    )

    return FORMAT_CHOICE


async def format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    response = query.data
    
    # Clear BEFORE setting new state
    context.user_data.clear()

    if response == "timer":
        context.user_data["is_timer"] = True
        context.user_data["is_ctf"] = False
        keyboard = [
            [
                InlineKeyboardButton("3 Min", callback_data="3"),
                InlineKeyboardButton("6 Min", callback_data="6")
            ],
            [
                InlineKeyboardButton("10 Min", callback_data="10"),
                InlineKeyboardButton("20 Min", callback_data="20")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_home")
            ]
        ]
        await query.edit_message_text(
            "⏳ Select timer:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SCORE_TARGET_CHOICE

    elif response == "target":
        context.user_data["is_timer"] = False
        context.user_data["is_ctf"] = False
        keyboard = [
            [
                InlineKeyboardButton("10 Score", callback_data="10"),
                InlineKeyboardButton("20 Score", callback_data="20")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_home")
            ]
        ]
        await query.edit_message_text(
            "🎯 Select target score:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SCORE_TARGET_CHOICE

    elif response == "ctf":
        context.user_data["is_ctf"] = True
        context.user_data["is_timer"] = False
        keyboard = [
            [
                InlineKeyboardButton("3 Flag", callback_data="3"),
                InlineKeyboardButton("6 Flag", callback_data="6")
            ],
            [
                InlineKeyboardButton("10 Flag", callback_data="10")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_home")
            ]
        ]
        await query.edit_message_text(
            "🚩 Select flag target:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SCORE_TARGET_CHOICE

    return ConversationHandler.END


async def score_target_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    response = query.data
    is_timer = context.user_data.get("is_timer", False)
    is_ctf = context.user_data.get("is_ctf", False)

    if is_timer:
        context.user_data["time"] = response
        selected_text = (
            f"⏳ Timer selected: {response} minutes\n\n"
            f"🗺 Select a map:\n\n"
            f"{MAP_LIST_TEXT}"
        )
    elif is_ctf:
        context.user_data["score"] = response
        selected_text = (
            f"🚩 Flag target selected: {response}\n\n"
            f"🗺 Select a map:\n\n"
            f"{CTF_MAP_LIST_TEXT}"
        )
    else:
        context.user_data["score"] = response
        selected_text = (
            f"🎯 Score selected: {response}\n\n"
            f"🗺 Select a map:\n\n"
            f"{MAP_LIST_TEXT}"
        )

    if is_ctf:
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("3", callback_data="3")
            ],
            [
                InlineKeyboardButton("4", callback_data="4"),
                InlineKeyboardButton("5", callback_data="5"),
                InlineKeyboardButton("6", callback_data="6")
            ],
            [
                InlineKeyboardButton("7", callback_data="7"),
                InlineKeyboardButton("8", callback_data="8"),
                InlineKeyboardButton("9", callback_data="9")
            ],
            [
                InlineKeyboardButton("10", callback_data="10"),
                InlineKeyboardButton("11", callback_data="11")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_home")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("3", callback_data="3")
            ],
            [
                InlineKeyboardButton("4", callback_data="4"),
                InlineKeyboardButton("5", callback_data="5"),
                InlineKeyboardButton("6", callback_data="6")
            ],
            [
                InlineKeyboardButton("7", callback_data="7"),
                InlineKeyboardButton("8", callback_data="8"),
                InlineKeyboardButton("9", callback_data="9")
            ],
            [
                InlineKeyboardButton("10", callback_data="10")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_home")
            ]
        ]

    await query.edit_message_text(
        selected_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return MAP_CHOICE


async def map_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    response = query.data
    is_timer = context.user_data.get("is_timer", False)
    is_ctf = context.user_data.get("is_ctf", False)

    game_code = random.randint(900000, 999999)

    if is_ctf:
        if response not in CTF_MAPS:
            await query.edit_message_text("❌ Invalid CTF map selection")
            return MAP_CHOICE

        score = context.user_data.get("score", "3")

        game_link = (
            f"{PREFIX}"
            f"mode={CTF_MODE[score]}"
            f"&wpns={WEAPONS}"
            f"&room=in{game_code}"
            f"&arena={CTF_MAPS[response]}"
        )

        match_text = (
            f"🚩 CTF Target: {score}\n"
            f"🗺 Map: {CTF_MAPS_NAME[response]}"
        )

    elif is_timer:
        if response not in MAPS:
            await query.edit_message_text("❌ Invalid map selection")
            return MAP_CHOICE

        time = context.user_data.get("time", "3")

        game_link = (
            f"{PREFIX}"
            f"mode={TIMER_MODE[time]}"
            f"&wpns={WEAPONS}"
            f"&room=in{game_code}"
            f"&arena={MAPS[response]}"
        )

        match_text = (
            f"⏳ {time} Minute Timer Match\n"
            f"🗺 Map: {MAPS_NAME[response]}"
        )

    else:
        if response not in MAPS:
            await query.edit_message_text("❌ Invalid map selection")
            return MAP_CHOICE

        score = context.user_data.get("score", "10")

        game_link = (
            f"{PREFIX}"
            f"mode={SCORE_MODE[score]}"
            f"&wpns={WEAPONS}"
            f"&room=in{game_code}"
            f"&arena={MAPS[response]}"
        )

        match_text = (
            f"🎯 Score Target: {score}\n"
            f"🗺 Map: {MAPS_NAME[response]}"
        )

    keyboard = [
        [
            InlineKeyboardButton("Create New Match 🔄", callback_data="restart")
        ]
    ]

    await query.edit_message_text(
        f"{match_text}\n\n🎮 Game Link:\n{game_link}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END


async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    # Send NEW message instead of editing
    await query.message.reply_text(
        "🎮 Welcome Smashkarter!\n\nChoose a mode:",
        reply_markup=get_home_keyboard()
    )

    return FORMAT_CHOICE


async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_user(update):
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "🎮 Welcome Smashkarter!\n\nChoose a mode:",
        reply_markup=get_home_keyboard()
    )

    return FORMAT_CHOICE


def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command)
        ],
        states={
            FORMAT_CHOICE: [
                CallbackQueryHandler(
                    format_choice,
                    pattern="^(timer|target|ctf)$"
                )
            ],
            SCORE_TARGET_CHOICE: [
                CallbackQueryHandler(
                    score_target_choice,
                    pattern="^(3|6|10|20)$"
                )
            ],
            MAP_CHOICE: [
                CallbackQueryHandler(
                    map_choice,
                    pattern="^(1|2|3|4|5|6|7|8|9|10|11)$"
                )
            ],
        },
        fallbacks=[
            CallbackQueryHandler(
                back_handler,
                pattern="^back_home$"
            ),
            CallbackQueryHandler(
                restart_handler,
                pattern="^restart$"
            )
        ],
        allow_reentry=True
    )

    app.add_handler(conv_handler)

    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

    if not RENDER_URL:
        print(f"🚀 Running locally with polling... (ENV={ENV})")
        app.run_polling(
            poll_interval=3,
            drop_pending_updates=True
        )
    else:
        PORT = int(os.environ.get("PORT", 10000))
        print(f"🚀 Running on Render with webhook... (ENV={ENV})")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{RENDER_URL}/{BOT_TOKEN}",
            secret_token="smashkart_secret",
            drop_pending_updates=True
        )


if __name__ == "__main__":
    main()