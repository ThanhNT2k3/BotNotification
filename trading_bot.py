import time
import datetime
import requests
import pandas as pd
from vnstock import Trading
from vnstock.explorer.fmarket.fund import Fund
import pytz

# --- CONFIGURATION ---

# Discord Webhook URL (Get this from your Discord Server Settings -> Integrations -> Webhooks)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1446127614648516628/ImVVJkeUPtkxvMorSkVd4VkklC-n5ygIjRPX2xR_tuoQY4BUR3aOQ9BECNSuDh4iqftj"

# Portfolio Configuration
# Format: 'SYMBOL': {'quantity': float, 'avg_price': float, 'type': 'stock' or 'fund'}
PORTFOLIO = {
    'MBB': {
        'quantity': 2400,
        'avg_price': 25.72,
        'type': 'stock'
    },
    'HPG': {
        'quantity': 1480,
        'avg_price': 24.98,
        'type': 'stock'
    },
    'PDR': {
        'quantity': 200,
        'avg_price': 26.06,
        'type': 'stock'
    },
    'SSI': {
        'quantity': 360,
        'avg_price': 29.23,
        'type': 'stock'
    },
    'CTG': {
        'quantity': 800,
        'avg_price': 38.05,
        'type': 'stock'
    },
    'VCI': {
        'quantity': 500,
        'avg_price': 41.81,
        'type': 'stock'
    },
    'VMEEF': {
        'quantity': 6745.51,
        'avg_price': 14.750,
        'type': 'fund'
    },
    'VCBFBCF': {
        'quantity': 344.33,
        'avg_price': 42.094,
        'type': 'fund'
    },
    'TCFIN': {
        'quantity': 2762.31,
        'avg_price': 13.502,
        'type': 'fund'
    },
    'VEOF': {
        'quantity': 1940.56,
        'avg_price': 31.940,
        'type': 'fund'
    },
    'DCDS': {
        'quantity': 205.98,
        'avg_price': 105.760,
        'type': 'fund'
    },
    # Add more assets here
}

# Timezone
VNT_TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')

# Schedule
START_TIME = datetime.time(9, 0)
END_TIME = datetime.time(15, 0)

# No notification periods (times when notifications should not be sent)
NO_NOTIFICATION_PERIODS = [
    (datetime.time(11, 30), datetime.time(13, 0)),  # 11:30 - 13:00
]

# How often to run (in seconds) - e.g., every 30 minutes
RUN_INTERVAL = 1 * 60

# --- FUNCTIONS ---


def is_notification_blackout(current_time):
    """
    Check if the current time falls within any of the no-notification periods.
    Returns True if notifications should be skipped, False otherwise.
    """
    for start_time, end_time in NO_NOTIFICATION_PERIODS:
        if start_time <= current_time <= end_time:
            return True
    return False


def get_stock_data(symbols):
    """
    Fetches current price and reference price for a list of stock symbols.
    Returns: { 'SYMBOL': {'price': float, 'ref_price': float} }
    """
    try:
        trading = Trading(source='VCI')
        df = trading.price_board(symbols)

        data = {}
        if not df.empty:
            # Handle MultiIndex columns if present
            # Based on test, it returns MultiIndex: ('listing', 'symbol'), ('match', 'match_price'), ('listing', 'ref_price')

            for index, row in df.iterrows():
                try:
                    # Accessing MultiIndex can be tricky if flattened or not.
                    # If it's a MultiIndex, row is a Series with MultiIndex.

                    # Symbol
                    symbol = row[('listing', 'symbol')]

                    # Current Price
                    price = row[('match', 'match_price')]

                    # Reference Price (Previous Close)
                    ref_price = row[('listing', 'ref_price')]

                    # If price is 0 (no match yet), use ref_price or open_price
                    if price == 0:
                        price = row[('match', 'open_price')]
                        if price == 0:
                            price = ref_price

                    data[symbol] = {
                        'price': float(price),
                        'ref_price': float(ref_price)
                    }
                except KeyError:
                    # Fallback for flat columns if structure changes
                    try:
                        symbol = row['symbol']
                        price = row['match_price'] or row['close']
                        ref_price = row['ref_price'] or row['reference_price']
                        data[symbol] = {
                            'price': float(price),
                            'ref_price': float(ref_price)
                        }
                    except:
                        continue

        return data
    except Exception as e:
        print(f"Error fetching stock prices: {e}")
        return {}


def get_fund_data():
    """
    Fetches current NAV and previous change for all funds.
    Returns: { 'SYMBOL': {'price': float, 'ref_price': float} }
    """
    try:
        fund = Fund()
        df = fund.listing()
        # df columns: 'short_name', 'nav', 'nav_change_previous', ...
        data = {}
        if not df.empty:
            for index, row in df.iterrows():
                symbol = row['short_name']
                nav = float(row['nav'])
                change = float(row['nav_change_previous'])

                # Calculate reference price (Yesterday's NAV)
                ref_price = nav - change

                data[symbol] = {'price': nav, 'ref_price': ref_price}
        return data
    except Exception as e:
        print(f"Error fetching fund prices: {e}")
        return {}


def calculate_portfolio(portfolio, stock_data, fund_data):
    """
    Calculates Total P&L and Daily P&L, grouped by asset type.
    """
    # Initialize summaries
    summary = {
        'stock': {
            'cost': 0,
            'value': 0,
            'pnl': 0,
            'daily_pnl': 0
        },
        'fund': {
            'cost': 0,
            'value': 0,
            'pnl': 0,
            'daily_pnl': 0
        },
        'total': {
            'cost': 0,
            'value': 0,
            'pnl': 0,
            'daily_pnl': 0
        }
    }

    for symbol, info in portfolio.items():
        qty = info['quantity']
        avg_price = info['avg_price']
        asset_type = info['type']

        market_data = None
        if asset_type == 'stock':
            market_data = stock_data.get(symbol)
        elif asset_type == 'fund':
            market_data = fund_data.get(symbol)

        if not market_data:
            continue

        current_price = market_data['price']
        ref_price = market_data['ref_price']

        # Calculations
        current_value = qty * current_price
        cost_basis = qty * avg_price

        # Total P&L
        pnl = current_value - cost_basis

        # Daily P&L
        daily_pnl = (current_price - ref_price) * qty

        # Update Group Summary
        if asset_type in summary:
            summary[asset_type]['cost'] += cost_basis
            summary[asset_type]['value'] += current_value
            summary[asset_type]['pnl'] += pnl
            summary[asset_type]['daily_pnl'] += daily_pnl

        # Update Total Summary
        summary['total']['cost'] += cost_basis
        summary['total']['value'] += current_value
        summary['total']['pnl'] += pnl
        summary['total']['daily_pnl'] += daily_pnl

    # Calculate percentages
    for key in summary:
        cost = summary[key]['cost']
        value = summary[key]['value']
        daily_base = value - summary[key]['daily_pnl']

        summary[key]['pnl_percent'] = (summary[key]['pnl'] / cost *
                                       100) if cost > 0 else 0
        summary[key]['daily_pnl_percent'] = (summary[key]['daily_pnl'] /
                                             daily_base *
                                             100) if daily_base > 0 else 0

    return summary


def send_discord_notification(data):
    """
    Sends a formatted message to Discord.
    """
    if DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("Discord Webhook URL not set. Skipping notification.")
        return

    # Determine color based on Daily P&L
    color = 3066993 if data['total'][
        'daily_pnl'] >= 0 else 15158332  # Green or Red

    # Helper to format money
    def fmt(val, percent):
        icon = "📈" if val >= 0 else "📉"
        return f"{icon} {val:,.0f} ({percent:+.2f}%)"

    embed = {
        "title":
        " 🚀 Portfolio Daily",
        "description":
        #f"**Total Value: {data['total']['value']:,.0f} VND**",
        f"Day: {fmt(data['stock']['daily_pnl'], data['stock']['daily_pnl_percent'])}",
        "color":
        color,
        "fields": [
            # Stocks Section
            {
                "name":
                "🏢 Stocks (Chứng khoán)",
                "value":
                (f"Total: {fmt(data['stock']['pnl'], data['stock']['pnl_percent'])}\n"
                 f"Day: {fmt(data['stock']['daily_pnl'], data['stock']['daily_pnl_percent'])}"
                 ),
                "inline":
                True
            },
            # Funds Section
            {
                "name":
                "💰 Funds (Chứng chỉ quỹ)",
                "value":
                (f"Total: {fmt(data['fund']['pnl'], data['fund']['pnl_percent'])}\n"
                 f"Day: {fmt(data['fund']['daily_pnl'], data['fund']['daily_pnl_percent'])}"
                 ),
                "inline":
                True
            },
            # Separator
            {
                "name": "",
                "value": "-----------------------------------",
                "inline": False
            },
            # Grand Total Section
            {
                "name":
                "🏆 Grand Total",
                "value":
                (f"Total: {fmt(data['total']['pnl'], data['total']['pnl_percent'])}\n"
                 f"Day: {fmt(data['total']['daily_pnl'], data['total']['daily_pnl_percent'])}"
                 ),
                "inline":
                False
            }
        ],
        "footer": {
            "text":
            f"Updated at {datetime.datetime.now(VNT_TIMEZONE).strftime('%H:%M %d/%m/%Y')}"
        }
    }

    payload = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send notification: {e}")


def print_portfolio_summary(data):
    """
    Prints portfolio summary to console.
    """
    print("\n" + "=" * 50)
    print(
        f"📈 PORTFOLIO UPDATE ({datetime.datetime.now(VNT_TIMEZONE).strftime('%H:%M %d/%m/%Y')})"
    )
    print("=" * 50)

    print(f"Total Value: {data['total']['value']:,.0f} VND")
    print("-" * 50)

    print("STOCKS:")
    print(
        f"   Day:   {data['stock']['daily_pnl']:,.0f} ({data['stock']['daily_pnl_percent']:.2f}%)"
    )
    print(
        f"   Total: {data['stock']['pnl']:,.0f} ({data['stock']['pnl_percent']:.2f}%)"
    )

    print("FUNDS:")
    print(
        f"   Day:   {data['fund']['daily_pnl']:,.0f} ({data['fund']['daily_pnl_percent']:.2f}%)"
    )
    print(
        f"   Total: {data['fund']['pnl']:,.0f} ({data['fund']['pnl_percent']:.2f}%)"
    )

    print("-" * 50)
    print("GRAND TOTAL:")
    print(
        f"   Day:   {data['total']['daily_pnl']:,.0f} ({data['total']['daily_pnl_percent']:.2f}%)"
    )
    print(
        f"   Total: {data['total']['pnl']:,.0f} ({data['total']['pnl_percent']:.2f}%)"
    )
    print("=" * 50 + "\n")


def run_bot():
    print("Starting Trading Bot...")
    print(f"Monitoring from {START_TIME} to {END_TIME} VNT.")

    while True:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        now_vnt = now_utc.astimezone(VNT_TIMEZONE)

        # Check if it's a weekday (Monday=0, Sunday=6)
        if now_vnt.weekday() < 5:  # 0-4 are weekdays
            current_time = now_vnt.time()

            if START_TIME <= current_time <= END_TIME:
                print(f"Running update at {now_vnt}")

                # 1. Identify symbols to fetch
                stock_symbols = [
                    k for k, v in PORTFOLIO.items() if v['type'] == 'stock'
                ]

                # 2. Fetch prices
                stock_data = get_stock_data(stock_symbols)
                fund_data = get_fund_data()

                # 3. Calculate P&L
                portfolio_data = calculate_portfolio(PORTFOLIO, stock_data,
                                                     fund_data)

                # 4. Print Summary to Console
                print_portfolio_summary(portfolio_data)

                # 5. Send Notification (Optional) - Skip during blackout periods
                if is_notification_blackout(current_time):
                    print(
                        f"Skipping notification during blackout period ({current_time})"
                    )
                else:
                    send_discord_notification(portfolio_data)

                # Wait for next interval
                print(f"Sleeping for {RUN_INTERVAL} seconds...")
                time.sleep(RUN_INTERVAL)
            else:
                # Outside trading hours
                print(f"Outside trading hours ({current_time}). Waiting...")
                time.sleep(60)  # Check every minute
        else:
            # Weekend
            print("It's the weekend. Sleeping...")
            time.sleep(3600)  # Check every hour


if __name__ == "__main__":
    run_bot()
