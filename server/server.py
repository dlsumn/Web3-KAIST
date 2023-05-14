from flask import Flask, jsonify
from web3 import Web3, HTTPProvider

app = Flask(__name__)

# Geth RPC endpoint
rpc_url = "http://localhost:8545"
w3 = Web3(HTTPProvider(rpc_url))

@app.route("/")
def get_balance():
    # 예시로 지갑 0의 잔액을 조회하는 코드입니다.
    account = w3.eth.accounts[0]
    balance = w3.eth.get_balance(account)

    # 잔액을 JSON 형태로 반환합니다.
    response = {
        "account": account,
        "balance": balance
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
