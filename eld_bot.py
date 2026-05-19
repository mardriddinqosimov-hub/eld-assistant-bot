#!/usr/bin/env python3
# =========================================================
# ELD ASSISTANT TELEGRAM BOT
# FULL SINGLE FILE VERSION
# =========================================================
#
# INSTALL:
# pip install python-telegram-bot==20.7
#
# RUN:
# python eld_bot.py
#
# =========================================================

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
    MessageHandler,
    filters
)

# =========================================================
# BOT TOKEN
# =========================================================

TOKEN = "8703570267:AAHF1hL1vZzlZ8r308K6lKShrqQ2-H9zw-g"

# =========================================================
# ADMIN ID
# Put your Telegram numeric ID here
# =========================================================

ADMIN_ID = 123456789

# =========================================================
# TEMPLATE DATABASE
# =========================================================

templates = {

    "offline": """
Hello sir

Sir your device is DISCONNECTED right now, please try to connect! Otherwise please let us know, we'll instruct you how you do it!

Thank you!
#
""",

    "inspection": """
Hello Team!
#Noviolation

Driver had DOT Inspection

Company:  
Driver's name: 

Inspection level: 

Location: 
Time: 


Inspection Result: Logbook was  downloaded and No violations were discovered from ELD✅


Please be informed!!!

Thank you!
#
""",

    "hos": """
⏰ HOS ALERT

Hello Driver,

Please check your Hours of Service carefully.

Avoid violations and make sure you have enough drive time remaining.

Contact safety if you need assistance.
""",

    "break": """
Hello Sir

Sir you have left less than 2 hours for break, please try to stop on time or let us know if you need extra hours

Thank you!
#
""",

    "violation": """
Hello Mr.

Sir you are rolling on a Violation. Please try to stop asap and let us know

Thank you
#
""",

    "restart": """
1.📲 Log out from the ELD platform (App)

2.🔁 Restart the tablet/phone

3.🛑 Shut down the truck engine

4.🧷 Check cable label (Heavy or Light Duty)

5.🔌 Unplug the ELD device

6.⚙️ Re-plug the device cable properly

7.✅ Log in to the app again

8.🚚 Power up the truck
""",

    "cycle": """
Hello Mr. 

You had Cycle hours less than 20h; We have added some hours on it;

Cycle

Location: 


date: 
""",

    "newdriver": """
#newdriver
#newunit

🏢 Company : 
👤 Driver : 



🚛 Unit : # 

━━━━━━━━━━━━━━━━━━━━━━━━━

☑️ Telegram group created & contact saved
☑️ Registered on system
☑️ All boards updated


Equipment's :


📒 Paper logbook ✅/❌
📲 Using additional phone ✅
📄 Manuals printed ✅
📍 ELD tablet mounted ✅

Instructions were not provided

Comment : instruction is done, he will use his personal phone. 


Please be informed!
# new
"""
}

# =========================================================
# USER STATES
# =========================================================

user_states = {}

# =========================================================
# START COMMAND
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton("📡 Offline", callback_data="offline"),
            InlineKeyboardButton("📋 Inspection", callback_data="inspection")
        ],

        [
            InlineKeyboardButton("⏰ HOS", callback_data="hos"),
            InlineKeyboardButton("🚨 Violation", callback_data="violation")
        ],

        [
            InlineKeyboardButton("⏱️ Break Alert", callback_data="break")
        ],

        [
            InlineKeyboardButton("🔄 Restart", callback_data="restart"),
            InlineKeyboardButton("🕒 Cycle", callback_data="cycle")
        ],

        [
            InlineKeyboardButton("🆕 New Driver Update", callback_data="newdriver")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚛 ELD Assistant Bot\n\nChoose a template:",
        reply_markup=reply_markup
    )

# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # ── BACK TO MENU ──────────────────────────────────────
    if query.data == "back_to_menu":

        keyboard = [
            [
                InlineKeyboardButton("📡 Offline", callback_data="offline"),
                InlineKeyboardButton("📋 Inspection", callback_data="inspection")
            ],
            [
                InlineKeyboardButton("⏰ HOS", callback_data="hos"),
                InlineKeyboardButton("🚨 Violation", callback_data="violation")
            ],
            [
                InlineKeyboardButton("⏱️ Break Alert", callback_data="break")
            ],
            [
                InlineKeyboardButton("🔄 Restart", callback_data="restart"),
                InlineKeyboardButton("🕒 Cycle", callback_data="cycle")
            ],
            [
                InlineKeyboardButton("🆕 New Driver Update", callback_data="newdriver")
            ]
        ]

        await query.edit_message_text(
            "🚛 ELD Assistant Bot\n\nChoose a template:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # ── SHOW TEMPLATE ─────────────────────────────────────
    template_name = query.data

    if template_name in templates:

        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]
        ])

        await query.edit_message_text(
            templates[template_name],
            reply_markup=back_keyboard
        )

# =========================================================
# SEARCH COMMAND
# =========================================================

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/search keyword"
        )
        return

    keyword = " ".join(context.args).lower()

    found = []

    for key in templates.keys():

        if keyword in key.lower():
            found.append(key)

    if found:

        result_text = "🔍 SEARCH RESULTS\n\n"

        for item in found:
            result_text += f"• /{item}\n"

        await update.message.reply_text(result_text)

    else:
        await update.message.reply_text(
            "❌ No templates found."
        )

# =========================================================
# SHOW ALL TEMPLATES
# =========================================================

async def all_templates(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "📚 ALL AVAILABLE TEMPLATES\n\n"

    for key in templates.keys():
        text += f"• /{key}\n"

    await update.message.reply_text(text)

# =========================================================
# DYNAMIC COMMAND HANDLER
# =========================================================

async def template_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    command = update.message.text.replace("/", "").lower()

    if command in templates:
        await update.message.reply_text(templates[command])

# =========================================================
# ADD TEMPLATE
# =========================================================

async def addtemplate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Admin only.")
        return

    user_states[update.effective_user.id] = "waiting_template"

    await update.message.reply_text(
        "Send template in this format:\n\n"
        "topic | message\n\n"
        "Example:\n"
        "fuel | Hello Driver, please fuel the truck."
    )

# =========================================================
# HANDLE ADMIN INPUT
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_states:
        return

    state = user_states[user_id]

    # =====================================
    # ADD TEMPLATE
    # =====================================

    if state == "waiting_template":

        text = update.message.text

        if "|" not in text:

            await update.message.reply_text(
                "❌ Wrong format.\n\nUse:\n"
                "topic | message"
            )
            return

        topic, message = text.split("|", 1)

        topic = topic.strip().lower()
        message = message.strip()

        templates[topic] = message

        del user_states[user_id]

        await update.message.reply_text(
            f"✅ Template '{topic}' added successfully.\n\n"
            f"Use command:\n/{topic}"
        )

# =========================================================
# DELETE TEMPLATE
# =========================================================

async def deletetemplate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Admin only.")
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/deletetemplate topic"
        )
        return

    topic = context.args[0].lower()

    if topic in templates:

        del templates[topic]

        await update.message.reply_text(
            f"✅ Template '{topic}' deleted."
        )

    else:

        await update.message.reply_text(
            "❌ Template not found."
        )

# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
🚛 ELD ASSISTANT BOT HELP

📚 Main Commands:
/start - Open menu
/all - Show all templates
/search keyword - Search templates

🛠 Admin Commands:
/addtemplate
/deletetemplate topic

📌 Examples:
/offline
/inspection
/hos
/violation
"""

    await update.message.reply_text(help_text)

# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(TOKEN).build()

    # =====================================
    # BASIC COMMANDS
    # =====================================

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("all", all_templates))

    # =====================================
    # ADMIN COMMANDS
    # =====================================

    app.add_handler(CommandHandler("addtemplate", addtemplate))
    app.add_handler(CommandHandler("deletetemplate", deletetemplate))

    # =====================================
    # BUTTON HANDLER
    # =====================================

    app.add_handler(CallbackQueryHandler(button_click))

    # =====================================
    # DYNAMIC TEMPLATE COMMANDS
    # =====================================

    for template_name in templates.keys():

        app.add_handler(
            CommandHandler(
                template_name,
                template_command
            )
        )

    # =====================================
    # MESSAGE HANDLER
    # =====================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    # =====================================

    print("ELD Assistant Bot Running...")

    app.run_polling()

# =========================================================

if __name__ == "__main__":
    main()

# =========================================================
