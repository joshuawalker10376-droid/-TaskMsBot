import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from database import (
    init_db,
    add_task,
    get_tasks,
    mark_done,
    delete_task,
    clear_done,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to your To-Do Bot!\n\n"
        "Here's what I can do:\n"
        "• /add <task> – Add a new task\n"
        "• /list – Show all your tasks\n"
        "• /done <id> – Mark a task as done\n"
        "• /delete <id> – Delete a task\n"
        "• /clear – Remove all completed tasks\n"
        "• /help – Show this message again"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = " ".join(context.args).strip()

    if not task_text:
        await update.message.reply_text("⚠️ Usage: /add Buy groceries")
        return

    task_id = add_task(user_id, task_text)
    await update.message.reply_text(f"✅ Task #{task_id} added:\n{task_text}")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await update.message.reply_text("📭 You have no tasks yet. Use /add to create one!")
        return

    message = "📋 Your Tasks:\n\n"
    for task in tasks:
        status = "✅" if task["done"] else "⬜"
        message += f"{status} #{task['id']} – {task['task']}\n"

    message += "\nUse /done <id> or /delete <id> to manage them."
    await update.message.reply_text(message)


async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /done 3")
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid task ID.")
        return

    if mark_done(user_id, task_id):
        await update.message.reply_text(f"🎉 Task #{task_id} marked as done!")
    else:
        await update.message.reply_text(f"❌ Task #{task_id} not found.")


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /delete 3")
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid task ID.")
        return

    if delete_task(user_id, task_id):
        await update.message.reply_text(f"🗑️ Task #{task_id} deleted.")
    else:
        await update.message.reply_text(f"❌ Task #{task_id} not found.")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = clear_done(user_id)
    await update.message.reply_text(f"🧹 Removed {count} completed task(s).")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set!")

    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("done", done_command))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CommandHandler("clear", clear_command))

    app.add_error_handler(error_handler)

    logger.info("🤖 Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
