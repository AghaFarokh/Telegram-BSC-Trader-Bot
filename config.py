import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# BSC Network Configuration (hardcoded for simplicity)
BSC_RPC_URL = 'https://bsc-dataseed.binance.org/'

# Gas Configuration (hardcoded as requested)
APPROVE_GAS_PRICE = 0.2  # in Gwei
SELL_GAS_PRICE = 0.1     # in Gwei

# Contract Addresses
WBNB_ADDRESS = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'  # WBNB on BSC
PANCAKE_ROUTER = '0x10ED43C718714eb63d5aA57B78B54704E256024E'  # PancakeSwap Router
