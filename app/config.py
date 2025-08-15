import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///escrow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONERO_RPC_URL = os.environ.get('MONERO_RPC_URL', 'http://127.0.0.1:18082/json_rpc')
    MONERO_RPC_USERNAME = os.environ.get('MONERO_RPC_USERNAME', '')
    MONERO_RPC_PASSWORD = os.environ.get('MONERO_RPC_PASSWORD', '')
    CONFIRMATIONS_REQUIRED = int(os.environ.get('CONFIRMATIONS_REQUIRED', 10))
    SCHEDULER_API_ENABLED = True