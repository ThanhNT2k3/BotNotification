import threading
import keep_alive
from trading_bot import run_bot

# Start the trading bot in a separate thread
t = threading.Thread(target=run_bot)
t.start()

# Start the Flask web server to keep the app alive
keep_alive.app.run(host="0.0.0.0", port=8080)
