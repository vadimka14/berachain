from web3 import Web3

from compile_contract import get_abi_and_bytecode_from_contract
from deploy.config import private_key
from deploy.wait_status import wait_tx_status


def get_txn_data(w3, account):
    data = {
        'chainId': w3.eth.chain_id,
        'nonce': w3.eth.get_transaction_count(account.address),
        'from': account.address,
        'gasPrice': 0,
        'gas': 0
    }

    return data


def send_tx(w3, account, txn) -> str:
    gas = w3.eth.estimate_gas(txn)
    print('gas', gas)
    txn['gas'] = gas

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=account._private_key)
    tx_hash = w3.to_hex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

    return wait_tx_status(w3=w3, tx_hash=tx_hash)


def main():
    rpc = 'https://rpc.karak.network'

    abi, bytecode = get_abi_and_bytecode_from_contract(contract_path='./MultiSig_wallet.sol')

    w3 = Web3(provider=Web3.HTTPProvider(rpc))

    account = w3.eth.account.from_key(private_key=private_key)

    contract = w3.eth.contract(bytecode=bytecode, abi=abi)
    txn_data = get_txn_data(w3=w3, account=account)
    print('txn_data', txn_data)
    txn = contract.constructor().build_transaction(txn_data)
    print('txn', txn)

    status = send_tx(w3=w3, account=account, txn=txn)
    print(status)


if __name__ == '__main__':
    main()