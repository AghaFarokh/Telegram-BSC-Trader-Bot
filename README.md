# 🚀 BSC Trading Bot

A powerful and secure Telegram bot for buying and selling tokens on Binance Smart Chain (BSC) with automatic approval and same-block execution capabilities.

DEMO BOT is LIVE : https://t.me/SnipeSellBot

![BSC](https://img.shields.io/badge/BSC-Mainnet-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🟢 **Buy Tokens**: Purchase tokens directly with BNB using PancakeSwap
- 🔴 **Sell Tokens**: Sell tokens for BNB with automatic approval
- ⚡ **Same Block Execution**: Approve and sell transactions executed in the same block
- 🔐 **Secure**: Private keys are never stored - sent directly via Telegram messages
- 💰 **Flexible Amounts**: Support for specific amounts or "ALL" to sell entire balance
- 📊 **Transaction Tracking**: Get real-time transaction hashes and BSCScan links
- 🛡️ **Error Handling**: Comprehensive validation and error handling
- ⚙️ **Configurable Gas**: Customizable gas prices for different transaction priorities

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)

## 🔧 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- A **Telegram Bot Token** from [@BotFather](https://t.me/botfather)
- A **BSC wallet** with tokens to trade
- **BNB** in your wallet for gas fees
- Basic understanding of cryptocurrency trading

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AghaFarokh/Telegram-BSC-Trader-Bot.git
   cd Telegram-BSC-Trader-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your Telegram bot token:
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   ```

## ⚙️ Configuration

### Environment Variables

Only one environment variable is required:

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | ✅ Yes |

### Network Settings (Hardcoded)

The bot is pre-configured with the following settings:

- **Network**: BSC Mainnet (Chain ID: 56)
- **RPC URL**: `https://bsc-dataseed.binance.org/`
- **Router**: PancakeSwap V2 (`0x10ED43C718714eb63d5aA57B78B54704E256024E`)
- **WBNB**: `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`

### Gas Configuration

- **Approve Gas Price**: 0.2 Gwei (higher priority)
- **Trade Gas Price**: 0.1 Gwei

## 🚀 Usage

### Starting the Bot

```bash
python bsc_trading_bot.py
```

You should see:
```
INFO - Starting BSC Token Trading Bot...
```

### Interacting with the Bot

1. Open Telegram and find your bot
2. Send `/start` to see the welcome message and instructions
3. Send trading commands in the specified format

## 📝 Command Format

### Buy Tokens

```
BUY|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|BNB_AMOUNT
```

### Sell Tokens

```
SELL|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|TOKEN_AMOUNT
```

**Note**: Use `ALL` as the amount to sell your entire token balance.

## 💡 Examples

### Example 1: Buying Tokens

Let's say you want to buy CAKE tokens with 0.1 BNB:

```
BUY|0abc123def456789abc123def456789abc123def456789abc123def456789abc1|0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb|0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82|0.1
```

**Breakdown**:
- `BUY` - Operation type
- `0abc123...abc1` - Your wallet's private key (64 hex characters)
- `0x742d35...f0bEb` - Your wallet address
- `0x0E09Fa...81cE82` - CAKE token contract address
- `0.1` - Amount of BNB to spend

**Bot Response**:
```
✅ Buy transaction sent successfully!

📋 Transaction Details:
Buy TX: 0x1234567890abcdef...

⚡ Buy transaction sent successfully

🔗 View on BSCScan:
Buy: https://bscscan.com/tx/0x1234567890abcdef...
```

### Example 2: Selling Specific Amount

Selling 1000 CAKE tokens:

```
SELL|0abc123def456789abc123def456789abc123def456789abc123def456789abc1|0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb|0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82|1000
```

**Breakdown**:
- `SELL` - Operation type
- `0abc123...abc1` - Your wallet's private key
- `0x742d35...f0bEb` - Your wallet address
- `0x0E09Fa...81cE82` - CAKE token contract address
- `1000` - Amount of tokens to sell

### Example 3: Selling All Tokens

Selling your entire BUSD balance:

```
SELL|0abc123def456789abc123def456789abc123def456789abc123def456789abc1|0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb|0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56|ALL
```

**Breakdown**:
- `SELL` - Operation type
- `0abc123...abc1` - Your wallet's private key
- `0x742d35...f0bEb` - Your wallet address
- `0xe9e7CE...087D56` - BUSD token contract address
- `ALL` - Sell entire balance

**Bot Response**:
```
✅ Sell transactions sent successfully!

📋 Transaction Details:
Approve TX: 0xabcdef1234567890...
Sell TX: 0x9876543210fedcba...

⚡ Both transactions sent simultaneously - they will be in the same block

🔗 View on BSCScan:
Approve: https://bscscan.com/tx/0xabcdef1234567890...
Sell: https://bscscan.com/tx/0x9876543210fedcba...
```

### Real Token Contract Addresses

Here are some popular BSC token contracts for reference:

| Token | Symbol | Contract Address |
|-------|--------|------------------|
| PancakeSwap | CAKE | `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82` |
| Binance USD | BUSD | `0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56` |
| Tether USD | USDT | `0x55d398326f99059fF775485246999027B3197955` |
| USD Coin | USDC | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| Ethereum | ETH | `0x2170Ed0880ac9A755fd29B2688956BD959F933F8` |
| BNB | WBNB | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |

## 🔄 How It Works

### For SELL Operations

```
┌─────────────────┐
│ User Sends SELL │
│    Command      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Input  │
│ & Check Balance │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Approve   │
│ Transaction     │
│ (Nonce: N)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Sell      │
│ Transaction     │
│ (Nonce: N+1)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sign Both       │
│ Transactions    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Send to Mempool │
│ Simultaneously  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Same Block      │
│ Execution       │
└─────────────────┘
```

**Key Points**:
1. Approve transaction uses higher gas (0.2 Gwei) for priority
2. Sell transaction uses lower gas (0.1 Gwei)
3. Both transactions sent immediately without waiting
4. Same block execution ensured by sequential nonces

### For BUY Operations

```
┌─────────────────┐
│ User Sends BUY  │
│    Command      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Input  │
│ & Check Balance │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Buy       │
│ Transaction     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sign & Send     │
│ Transaction     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Receive Tokens  │
└─────────────────┘
```

## 🔐 Security

### ⚠️ CRITICAL SECURITY WARNINGS

1. **Never share your private keys** with anyone
2. **Private keys are not stored** anywhere - they're only used for transaction signing
3. **Use a dedicated wallet** for bot operations
4. **Test with small amounts first** before large trades
5. **Monitor transactions** on [BSCScan](https://bscscan.com/)
6. **Keep your Telegram bot token secure** - don't share it publicly
7. **Be aware of scam tokens** - verify contract addresses before trading

### Best Practices

- ✅ Use a separate wallet specifically for this bot
- ✅ Only keep necessary funds in the trading wallet
- ✅ Verify token contracts on BSCScan before trading
- ✅ Start with small test transactions
- ✅ Keep your `.env` file private (it's in `.gitignore`)
- ❌ Never commit your `.env` file to version control
- ❌ Never share screenshots with private keys visible
- ❌ Don't trade tokens you haven't researched

## 📁 File Structure

```
SnipeSellBot/
├── bsc_trading_bot.py      # Main bot application
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── env.example            # Example environment file
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Failed to connect to BSC network"
**Cause**: Network connectivity issue or RPC node is down

**Solution**:
- Check your internet connection
- Try a different RPC URL in `config.py`:
  - `https://bsc-dataseed1.binance.org/`
  - `https://bsc-dataseed2.binance.org/`
  - `https://bsc-dataseed3.binance.org/`

#### 2. "Insufficient token balance"
**Cause**: You don't have enough tokens to sell

**Solution**:
- Check your token balance on BSCScan
- Verify the token contract address is correct
- Ensure you're using the correct wallet address

#### 3. "Invalid private key format"
**Cause**: Private key is not in the correct format

**Solution**:
- Ensure private key is 64 hex characters (with or without `0x` prefix)
- Example valid formats:
  - `abc123def456...` (64 characters)
  - `0xabc123def456...` (66 characters with prefix)

#### 4. "Wallet address does not match private key"
**Cause**: The wallet address doesn't correspond to the private key

**Solution**:
- Verify you're using the correct private key for the wallet
- Use a tool like MetaMask to verify your wallet address

#### 5. Transaction Failures
**Cause**: Various reasons (gas, liquidity, token issues)

**Solutions**:
- Ensure you have enough BNB for gas fees (~0.001-0.005 BNB)
- Check if the token has sufficient liquidity on PancakeSwap
- Verify the token contract isn't a scam or has trading restrictions
- Try increasing gas prices in `config.py`

#### 6. "TELEGRAM_BOT_TOKEN not found"
**Cause**: Environment variable not set

**Solution**:
- Ensure `.env` file exists in the project root
- Verify `TELEGRAM_BOT_TOKEN` is set correctly
- Restart the bot after updating `.env`

## 📊 Dependencies

This project uses the following Python packages:

- **python-telegram-bot** (v20.7): Telegram bot framework
- **web3** (v6.11.4): Ethereum/BSC blockchain interaction
- **python-dotenv** (v1.0.0): Environment variable management

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## 🔄 Updates & Maintenance

### Checking for Updates

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Version History

- **v1.0.0** - Initial release with buy/sell functionality

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Disclaimer

**IMPORTANT**: This bot is provided for educational and informational purposes only.

- ⚠️ Use at your own risk
- ⚠️ The authors are not responsible for any financial losses
- ⚠️ Always test with small amounts first
- ⚠️ Understand the risks of automated trading
- ⚠️ Verify all token contracts before trading
- ⚠️ Be aware of market volatility and slippage
- ⚠️ This is not financial advice

Cryptocurrency trading involves substantial risk of loss. Only trade with funds you can afford to lose.

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages from the bot
3. Verify your configuration
4. Check transaction status on [BSCScan](https://bscscan.com/)
5. Open an issue on GitHub

## 🌟 Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ for the BSC community**

*Always DYOR (Do Your Own Research) before trading!*
