waiting_for_feedback = {}

async def handle_feedback(user_id, user_name, text, admin_id, context):
    feedback_msg = f"📩 #TAKLIF\n👤 Kimdan: {user_name}\n🆔 ID: {user_id}\n📝 Xabar: {text}"
    await context.bot.send_message(chat_id=admin_id, text=feedback_msg, parse_mode="Markdown")
    waiting_for_feedback[user_id] = False
    return "✅ Taklifingiz uchun rahmat! Adminga yuborildi."
