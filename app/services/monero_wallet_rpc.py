import requests
from flask import current_app

class MoneroWalletRPC:
    def __init__(self):
        self.url = current_app.config['MONERO_RPC_URL']
        self.auth = (current_app.config['MONERO_RPC_USERNAME'], current_app.config['MONERO_RPC_PASSWORD'])

    def _rpc(self, method, params=None):
        payload = {
            'jsonrpc': '2.0',
            'id': '0',
            'method': method,
            'params': params or {}
        }
        response = requests.post(self.url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()['result']

    def create_subaddress(self, account_index=0, label=None):
        params = {'account_index': account_index}
        if label:
            params['label'] = label
        return self._rpc('create_address', params)

    def get_payments(self, payment_id):
        return self._rpc('get_payments', {'payment_id': payment_id})

    def get_transfers(self, **kwargs):
        return self._rpc('get_transfers', kwargs)

    def transfer(self, destinations, **kwargs):
        params = {'destinations': destinations}
        params.update(kwargs)
        return self._rpc('transfer', params) 