import time
from telegram.ext import ContextTypes

def reset_time(context: ContextTypes.DEFAULT_TYPE):
    context.user_data["start_time"] = time.time()
