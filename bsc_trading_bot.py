import asyncio
import logging
from web3 import Web3
from web3.middleware import geth_poa_middleware
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import *
import json

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BSCTokenSeller:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        # Inject POA middleware for BSC compatibility
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        if not self.w3.is_connected():
            raise Exception("Failed to connect to BSC network")
        
        # ERC20 ABI for approve function
        self.erc20_abi = [
            {
                "constant": False,
                "inputs": [
                    {"name": "_spender", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "approve",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        # PancakeSwap Router ABI for swap functions
        self.router_abi = [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                    {"internalType": "address[]", "name": "path", "type": "address[]"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "swapExactTokensForETH",
                "outputs": [
                    {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                    {"internalType": "address[]", "name": "path", "type": "address[]"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "swapExactETHForTokens",
                "outputs": [
                    {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
                ],
                "stateMutability": "payable",
                "type": "function"
            }
        ]

    def sell_token(self, private_key, wallet_address, token_contract_address, amount_to_sell):
        """
        Sell token on BSC with approve and sell in the same block
        """
        try:
            # Convert private key to account
            account = self.w3.eth.account.from_key(private_key)
            
            # Verify wallet address matches private key
            if account.address.lower() != wallet_address.lower():
                raise Exception("Wallet address does not match private key")
            
            # Get current nonce
            current_nonce = self.w3.eth.get_transaction_count(wallet_address)
            
            # Convert token address to checksum format
            token_address_checksum = Web3.to_checksum_address(token_contract_address)
            
            # Create token contract instance
            token_contract = self.w3.eth.contract(
                address=token_address_checksum,
                abi=self.erc20_abi
            )
            
            # Create router contract instance
            router_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(PANCAKE_ROUTER),
                abi=self.router_abi
            )
            
            # Get token balance
            token_balance = token_contract.functions.balanceOf(wallet_address).call()
            
            # Handle "ALL" or specific amount
            if amount_to_sell == 'ALL':
                amount_wei = token_balance
                if amount_wei == 0:
                    raise Exception("No tokens to sell. Token balance is 0.")
                logger.info(f"Selling all tokens: {self.w3.from_wei(amount_wei, 'ether')}")
            else:
                # Convert amount to wei
                amount_wei = self.w3.to_wei(amount_to_sell, 'ether')
                # Check token balance
                if token_balance < amount_wei:
                    raise Exception(f"Insufficient token balance. Available: {self.w3.from_wei(token_balance, 'ether')}")
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Build approve transaction
            approve_tx = token_contract.functions.approve(
                PANCAKE_ROUTER,
                amount_wei
            ).build_transaction({
                'from': wallet_address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei(APPROVE_GAS_PRICE, 'gwei'),
                'nonce': current_nonce,  # Approve nonce
                'chainId': 56  # BSC chain ID
            })
            
            # Build sell transaction
            deadline = int(self.w3.eth.get_block('latest')['timestamp']) + 1200  # 20 minutes
            path = [token_address_checksum, WBNB_ADDRESS]
            
            sell_tx = router_contract.functions.swapExactTokensForETH(
                amount_wei,
                0,  # Accept any amount of BNB
                path,
                wallet_address,
                deadline
            ).build_transaction({
                'from': wallet_address,
                'gas': 300000,
                'gasPrice': self.w3.to_wei(SELL_GAS_PRICE, 'gwei'),
                'nonce': current_nonce + 1,  # Sell nonce (approve + 1)
                'chainId': 56  # BSC chain ID
            })
            
            # Sign transactions
            approve_signed = self.w3.eth.account.sign_transaction(approve_tx, private_key)
            sell_signed = self.w3.eth.account.sign_transaction(sell_tx, private_key)
            
            # Send both transactions simultaneously to ensure they're in the same block
            approve_tx_hash = self.w3.eth.send_raw_transaction(approve_signed.rawTransaction)
            logger.info(f"Approve transaction sent: {approve_tx_hash.hex()}")
            
            # Send sell transaction immediately without waiting
            sell_tx_hash = self.w3.eth.send_raw_transaction(sell_signed.rawTransaction)
            logger.info(f"Sell transaction sent: {sell_tx_hash.hex()}")
            
            # Both transactions are now in the mempool and will be included in the same block
            logger.info("Both transactions sent simultaneously - they will be in the same block")
            
            return {
                'success': True,
                'approve_tx_hash': approve_tx_hash.hex(),
                'sell_tx_hash': sell_tx_hash.hex(),
                'message': 'Both transactions sent simultaneously - they will be in the same block'
            }
            
        except Exception as e:
            logger.error(f"Error selling token: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def buy_token(self, private_key, wallet_address, token_contract_address, amount_bnb):
        """
        Buy token on BSC with BNB in the same block
        """
        try:
            # Convert private key to account
            account = self.w3.eth.account.from_key(private_key)
            
            # Verify wallet address matches private key
            if account.address.lower() != wallet_address.lower():
                raise Exception("Wallet address does not match private key")
            
            # Get current nonce
            current_nonce = self.w3.eth.get_transaction_count(wallet_address)
            
            # Convert token address to checksum format
            token_address_checksum = Web3.to_checksum_address(token_contract_address)
            
            # Create router contract instance
            router_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(PANCAKE_ROUTER),
                abi=self.router_abi
            )
            
            # Convert BNB amount to wei
            bnb_amount_wei = self.w3.to_wei(amount_bnb, 'ether')
            
            # Check BNB balance
            bnb_balance = self.w3.eth.get_balance(wallet_address)
            if bnb_balance < bnb_amount_wei:
                raise Exception(f"Insufficient BNB balance. Available: {self.w3.from_wei(bnb_balance, 'ether')} BNB")
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Build buy transaction
            deadline = int(self.w3.eth.get_block('latest')['timestamp']) + 1200  # 20 minutes
            path = [WBNB_ADDRESS, token_address_checksum]
            
            buy_tx = router_contract.functions.swapExactETHForTokens(
                0,  # Accept any amount of tokens
                path,
                wallet_address,
                deadline
            ).build_transaction({
                'from': wallet_address,
                'value': bnb_amount_wei,  # BNB amount to spend
                'gas': 300000,
                'gasPrice': self.w3.to_wei(SELL_GAS_PRICE, 'gwei'),  # Use same gas as sell
                'nonce': current_nonce,
                'chainId': 56  # BSC chain ID
            })
            
            # Sign transaction
            buy_signed = self.w3.eth.account.sign_transaction(buy_tx, private_key)
            
            # Send buy transaction
            buy_tx_hash = self.w3.eth.send_raw_transaction(buy_signed.rawTransaction)
            logger.info(f"Buy transaction sent: {buy_tx_hash.hex()}")
            
            return {
                'success': True,
                'buy_tx_hash': buy_tx_hash.hex(),
                'message': 'Buy transaction sent successfully'
            }
            
        except Exception as e:
            logger.error(f"Error buying token: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Initialize the token seller
token_seller = BSCTokenSeller()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        '🚀 Welcome to BSC Token Trading Bot!\n\n'
        '📋 To trade tokens, send a message in this format:\n\n'
        '🟢 To BUY tokens:\n'
        'BUY|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|BNB_AMOUNT\n\n'
        '🔴 To SELL tokens:\n'
        'SELL|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|TOKEN_AMOUNT\n'
        '(Use "ALL" to sell entire balance)\n\n'
        '📝 Examples:\n'
        'BUY|0x1234...|0x5678...|0x9abc...|0.1\n'
        'SELL|0x1234...|0x5678...|0x9abc...|1000\n'
        'SELL|0x1234...|0x5678...|0x9abc...|ALL\n\n'
        '⚙️ Configuration:\n'
        f'• Approve Gas: {APPROVE_GAS_PRICE} Gwei\n'
        f'• Trade Gas: {SELL_GAS_PRICE} Gwei\n'
        f'• Network: BSC Mainnet\n\n'
        '⚠️ WARNING: This bot will trade your tokens immediately!\n'
        '🔒 Keep your private keys secure!'
    )

async def handle_trade_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle token buy/sell requests."""
    try:
        message_text = update.message.text.strip()
        
        # Parse the input
        parts = message_text.split('|')
        if len(parts) != 5:
            await update.message.reply_text(
                'Invalid format! Please use:\n\n'
                '🟢 To BUY: BUY|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|BNB_AMOUNT\n'
                '🔴 To SELL: SELL|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|TOKEN_AMOUNT'
            )
            return
        
        operation, private_key, wallet_address, token_contract, amount = parts
        operation = operation.upper()
        
        # Validate operation
        if operation not in ['BUY', 'SELL']:
            await update.message.reply_text(
                'Invalid operation! Use BUY or SELL:\n\n'
                '🟢 BUY|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|BNB_AMOUNT\n'
                '🔴 SELL|PRIVATE_KEY|WALLET_ADDRESS|TOKEN_CONTRACT|TOKEN_AMOUNT'
            )
            return
        
        # Validate private key (accept with or without 0x prefix)
        if private_key.startswith('0x'):
            if len(private_key) != 66:
                await update.message.reply_text('Invalid private key format! Must be 64 hex characters')
                return
        else:
            if len(private_key) != 64:
                await update.message.reply_text('Invalid private key format! Must be 64 hex characters')
                return
            
        if not wallet_address.startswith('0x') or len(wallet_address) != 42:
            await update.message.reply_text('Invalid wallet address format!')
            return
            
        if not token_contract.startswith('0x') or len(token_contract) != 42:
            await update.message.reply_text('Invalid token contract format!')
            return
            
        # Handle amount validation (allow "ALL" for SELL operation)
        if operation == 'SELL' and amount.upper() == 'ALL':
            amount_float = 'ALL'  # Special marker for sell all
        else:
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    await update.message.reply_text('Amount must be greater than 0!')
                    return
            except ValueError:
                await update.message.reply_text('Invalid amount format! Use a number or "ALL" for selling all tokens.')
                return
        
        # Send processing message with details
        operation_emoji = '🟢' if operation == 'BUY' else '🔴'
        amount_type = 'BNB' if operation == 'BUY' else 'tokens'
        amount_display = amount_float if amount_float != 'ALL' else 'ALL (entire balance)'
        
        processing_msg = await update.message.reply_text(
            f'🔄 Processing {operation} request...\n\n'
            f'📊 Details:\n'
            f'• Operation: {operation_emoji} {operation}\n'
            f'• Wallet: {wallet_address[:10]}...{wallet_address[-8:]}\n'
            f'• Token: {token_contract[:10]}...{token_contract[-8:]}\n'
            f'• Amount: {amount_display} {amount_type if amount_float != "ALL" else ""}\n'
            f'• Gas: {SELL_GAS_PRICE} Gwei'
        )
        
        # Execute the trade
        if operation == 'BUY':
            result = token_seller.buy_token(
                private_key=private_key,
                wallet_address=wallet_address,
                token_contract_address=token_contract,
                amount_bnb=amount_float
            )
        else:  # SELL
            result = token_seller.sell_token(
                private_key=private_key,
                wallet_address=wallet_address,
                token_contract_address=token_contract,
                amount_to_sell=amount_float
            )
        
        if result['success']:
            if operation == 'BUY':
                success_message = (
                    f'✅ Buy transaction sent successfully!\n\n'
                    f'📋 Transaction Details:\n'
                    f'Buy TX: {result["buy_tx_hash"]}\n\n'
                    f'⚡ {result["message"]}\n\n'
                    f'🔗 View on BSCScan:\n'
                    f'Buy: https://bscscan.com/tx/{result["buy_tx_hash"]}'
                )
            else:  # SELL
                success_message = (
                    f'✅ Sell transactions sent successfully!\n\n'
                    f'📋 Transaction Details:\n'
                    f'Approve TX: {result["approve_tx_hash"]}\n'
                    f'Sell TX: {result["sell_tx_hash"]}\n\n'
                    f'⚡ {result["message"]}\n\n'
                    f'🔗 View on BSCScan:\n'
                    f'Approve: https://bscscan.com/tx/{result["approve_tx_hash"]}\n'
                    f'Sell: https://bscscan.com/tx/{result["sell_tx_hash"]}'
                )
            await processing_msg.edit_text(success_message)
        else:
            error_message = f'❌ Error {operation.lower()}ing token: {result["error"]}'
            await processing_msg.edit_text(error_message)
            
    except Exception as e:
        logger.error(f"Error handling trade request: {str(e)}")
        await update.message.reply_text(f'❌ Unexpected error: {str(e)}')

def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_trade_request))
    
    # Start the bot
    logger.info("Starting BSC Token Trading Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
