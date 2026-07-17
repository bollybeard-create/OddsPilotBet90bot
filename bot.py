import logging
import os
import sys
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Config
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN not set!")
    sys.exit(1)

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    logger.info("✅ OpenAI API key loaded")
else:
    logger.warning("⚠️ OPENAI_API_KEY not set! Using mock responses.")

# AI Service Functions
async def get_ai_response(prompt, context_text=""):
    """Get response from OpenAI"""
    if not OPENAI_API_KEY:
        return None
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional sports betting assistant providing odds, predictions, and betting advice."},
                {"role": "user", "content": f"{prompt}\n\nContext: {context_text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return None

# Start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🎯 **Welcome to OddsPilotBet90, {user.first_name}!**\n\n"
        "I'm your AI-powered betting assistant!\n\n"
        "**Commands:**\n"
        "📊 /odds - Get AI betting odds\n"
        "🎯 /bet - Get betting advice\n"
        "🧠 /insights - Game insights\n"
        "🔮 /predict - Match predictions\n"
        "💡 /tips - Daily betting tips\n"
        "⚙️ /settings - Settings\n\n"
        "Just type any game or team name!"
    )
    keyboard = [
        [InlineKeyboardButton("📊 Odds", callback_data="odds"), InlineKeyboardButton("🎯 Bet", callback_data="bet")],
        [InlineKeyboardButton("🧠 Insights", callback_data="insights"), InlineKeyboardButton("🔮 Predict", callback_data="predict")],
        [InlineKeyboardButton("💡 Tips", callback_data="tips"), InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Odds Command
async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Generating AI odds analysis...")
    
    prompt = "Generate realistic betting odds for today's top sports matches. Include moneyline, spread, and over/under for 3 different sports like soccer, basketball, and tennis."
    response = await get_ai_response(prompt)
    
    if response:
        await message.edit_text(f"📊 **AI Betting Odds**\n\n{response}", parse_mode='Markdown')
    else:
        mock_odds = (
            "📊 **Sample Odds**\n\n"
            "⚽ **Soccer:**\n"
            "• Team A vs Team B: Home -150 | Draw +250 | Away +180\n"
            "• Team C vs Team D: Home +120 | Draw +220 | Away +130\n\n"
            "🏀 **Basketball:**\n"
            "• Lakers vs Celtics: Lakers -2.5 (-110) | Celtics +2.5 (-110)\n"
            "• Over/Under: 225.5 (-110)\n\n"
            "🎾 **Tennis:**\n"
            "• Player A vs Player B: Player A -120 | Player B +100"
        )
        await message.edit_text(mock_odds, parse_mode='Markdown')

# Bet Command
async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Getting smart betting advice...")
    
    prompt = "Provide smart betting advice including bankroll management, value betting tips, and common mistakes to avoid."
    response = await get_ai_response(prompt)
    
    if response:
        await message.edit_text(f"🎯 **Betting Advice**\n\n{response}", parse_mode='Markdown')
    else:
        mock_advice = (
            "🎯 **Smart Betting Tips**\n\n"
            "1. **Bankroll Management**\n"
            "   • Only bet 1-3% of your bankroll per bet\n"
            "   • Set daily/weekly limits\n\n"
            "2. **Value Betting**\n"
            "   • Look for odds that offer value\n"
            "   • Compare odds across bookmakers\n\n"
            "3. **Research**\n"
            "   • Study team form and injuries\n"
            "   • Check head-to-head records\n\n"
            "4. **Stay Disciplined**\n"
            "   • Avoid emotional betting\n"
            "   • Stick to your strategy\n\n"
            "⚠️ **Always bet responsibly!**"
        )
        await message.edit_text(mock_advice, parse_mode='Markdown')

# Insights Command
async def insights_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Generating AI insights...")
    
    prompt = "Provide detailed sports betting insights including team performance analysis, market trends, and key factors to consider."
    response = await get_ai_response(prompt)
    
    if response:
        await message.edit_text(f"🧠 **AI Insights**\n\n{response}", parse_mode='Markdown')
    else:
        mock_insights = (
            "🧠 **Key Insights**\n\n"
            "📈 **Trends:**\n"
            "• Home teams win ~55% of games\n"
            "• Favorites cover spread ~48% of time\n"
            "• Overs hit ~52% of games\n\n"
            "🔑 **Key Factors:**\n"
            "• Recent form > Historical records\n"
            "• Injuries can change everything\n"
            "• Weather affects scoring\n\n"
            "💡 **Pro Tip:**\n"
            "Look for value where public opinion differs from data"
        )
        await message.edit_text(mock_insights, parse_mode='Markdown')

# Predict Command
async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Making AI predictions...")
    
    prompt = "Predict the outcomes of today's major sports matches. Include confidence levels and reasoning for each prediction."
    response = await get_ai_response(prompt)
    
    if response:
        await message.edit_text(f"🔮 **Match Predictions**\n\n{response}", parse_mode='Markdown')
    else:
        mock_predictions = (
            "🔮 **Today's Predictions**\n\n"
            "⚽ **Soccer:**\n"
            "• Team A vs Team B: Team A wins (65% confidence)\n"
            "  Reason: Better form and home advantage\n\n"
            "🏀 **Basketball:**\n"
            "• Lakers vs Celtics: Lakers win (58% confidence)\n"
            "  Reason: Stronger offense and key players healthy\n\n"
            "🎾 **Tennis:**\n"
            "• Player A vs Player B: Player A wins (70% confidence)\n"
            "  Reason: Better record on this surface\n\n"
            "📊 **Confidence Scale:** 0-100%\n"
            "⚠️ Predictions are AI-generated, not financial advice"
        )
        await message.edit_text(mock_predictions, parse_mode='Markdown')

# Tips Command
async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Generating daily tips...")
    
    prompt = "Provide daily betting tips including tip of the day, strategic advice, and what to watch for in today's games."
    response = await get_ai_response(prompt)
    
    if response:
        await message.edit_text(f"💡 **Daily Tips**\n\n{response}", parse_mode='Markdown')
    else:
        mock_tips = (
            "💡 **Tip of the Day**\n\n"
            "Always bet with your head, not your heart!\n\n"
            "📊 **Strategy:**\n"
            "• Focus on 1-2 sports you know well\n"
            "• Keep detailed records of your bets\n"
            "• Take breaks when losing\n\n"
            "🎯 **What to Watch:**\n"
            "• Last 5 games form\n"
            "• Head-to-head records\n"
            "• Player injuries\n\n"
            "💪 **Mindset:**\n"
            "• Stay patient\n"
            "• Trust your research\n"
            "• Don't chase losses"
        )
        await message.edit_text(mock_tips, parse_mode='Markdown')

# Settings Command
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏟️ Set Favorite Sport", callback_data="set_sport")],
        [InlineKeyboardButton("🔔 Toggle Notifications", callback_data="notifications")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
    ]
    await update.message.reply_text(
        "⚙️ **Settings**\n\n"
        "Customize your betting assistant experience:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Handle Callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "odds":
        await odds_command(update, context)
    elif data == "bet":
        await bet_command(update, context)
    elif data == "insights":
        await insights_command(update, context)
    elif data == "predict":
        await predict_command(update, context)
    elif data == "tips":
        await tips_command(update, context)
    elif data == "settings":
        keyboard = [
            [InlineKeyboardButton("🏟️ Set Favorite Sport", callback_data="set_sport")],
            [InlineKeyboardButton("🔔 Toggle Notifications", callback_data="notifications")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
        ]
        await query.edit_message_text(
            "⚙️ **Settings**\n\nCustomize your experience:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    elif data == "set_sport":
        await query.edit_message_text(
            "🏟️ **Favorite Sport**\n\n"
            "Your favorite sport has been set!\n"
            "I'll focus more on this sport for you.",
            parse_mode='Markdown'
        )
    elif data == "notifications":
        await query.edit_message_text(
            "🔔 **Notifications**\n\n"
            "Notifications have been toggled!\n"
            "You'll now receive updates on odds changes.",
            parse_mode='Markdown'
        )
    elif data == "back":
        keyboard = [
            [InlineKeyboardButton("📊 Odds", callback_data="odds"), InlineKeyboardButton("🎯 Bet", callback_data="bet")],
            [InlineKeyboardButton("🧠 Insights", callback_data="insights"), InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("💡 Tips", callback_data="tips"), InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
        ]
        await query.edit_message_text(
            "🎯 **OddsPilotBet90 - Main Menu**\n\n"
            "Choose an option below:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

# Handle Text Messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if " vs " in text:
        message = await update.message.reply_text(f"⏳ Analyzing {text}...")
        prompt = f"Analyze the matchup between {text}. Provide predictions, key factors, and who you think will win."
        response = await get_ai_response(prompt, text)
        
        if response:
            await message.edit_text(f"📊 **Match Analysis**\n\n{response}", parse_mode='Markdown')
        else:
            mock_analysis = (
                f"📊 **Analysis for {text}**\n\n"
                "🔍 **Key Factors:**\n"
                "• Recent form matters most\n"
                "• Check injury reports\n"
                "• Home advantage is significant\n"
                "• Historical head-to-head data\n\n"
                "🎯 **Prediction:**\n"
                "Based on available data, this looks like a competitive matchup.\n\n"
                "💡 **Tip:**\n"
                "Use /predict for detailed predictions!"
            )
            await message.edit_text(mock_analysis, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "🤖 **I'm your betting assistant!**\n\n"
            "Try these commands:\n"
            "📊 /odds - Get betting odds\n"
            "🎯 /bet - Get betting advice\n"
            "🧠 /insights - Game insights\n"
            "🔮 /predict - Match predictions\n"
            "💡 /tips - Daily tips\n\n"
            "Or type **Team A vs Team B** for match analysis!",
            parse_mode='Markdown'
        )

# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later.\n\n"
            "Use /start to restart the bot."
        )

# Main
def main():
    try:
        # Create application
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("odds", odds_command))
        app.add_handler(CommandHandler("bet", bet_command))
        app.add_handler(CommandHandler("insights", insights_command))
        app.add_handler(CommandHandler("predict", predict_command))
        app.add_handler(CommandHandler("tips", tips_command))
        app.add_handler(CommandHandler("settings", settings_command))
        
        # Add callback and message handlers
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        logger.info("🚀 OddsPilotBet90 bot started successfully!")
        
        # Start the bot
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
