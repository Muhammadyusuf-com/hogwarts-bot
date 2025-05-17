from docx import Document
from rapidfuzz import process, fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Load DOCX content ---
def read_docx(file_path):
    doc = Document(file_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return paragraphs

doc_texts = read_docx("document.docx")

# Split paragraphs into sentences for better matching
import re
doc_sentences = []
paragraph_to_page = {}  # Map sentence index to fake page number

for idx, para in enumerate(doc_texts):
    sentences = re.split(r'(?<=[.!?])\s+', para)
    page_number = idx // 10 + 1  # Approximate: every 10 paras = next page
    for sentence in sentences:
        doc_sentences.append(sentence)
        paragraph_to_page[len(doc_sentences) - 1] = page_number

# --- Fancy Answering Function ---
def generate_confidence_bar(score):
    filled = int(score / 10)
    empty = 10 - filled
    return f"[{'█' * filled}{'-' * empty}]"

def get_best_answer(question):
    match, score, idx = process.extractOne(question, doc_sentences, scorer=fuzz.token_set_ratio)
    if score > 65:
        page_num = paragraph_to_page.get(idx, '?')
        confidence_bar = generate_confidence_bar(score)
        return f"🔎 Found this with {score}% confidence on **Page {page_num}**:\n\n➡️ {match}\n\n{confidence_bar}"
    elif score > 40:
        return "🤔 I found something, but it's not very clear. Could you please rephrase your question?"
    else:
        return "❓ Sorry, I couldn't find a relevant answer in the document."

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Ask me anything from the document. I'll do my best to help you out!")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_q = update.message.text
    answer = get_best_answer(user_q)
    await update.message.reply_text(answer, parse_mode="Markdown")

# --- Run Bot ---
def main():
    bot_token = "7694188407:AAGK6QastAB66uT-VwN67qbUjtwtfIJ91Kk"
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    print("✅ Fancy Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
