
from flask import Blueprint, render_template, request, flash, url_for
import sqlite3
from web3 import Web3, HTTPProvider

signup_bp = Blueprint('signup', __name__)
profile_bp = Blueprint('profile', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('signup.html')
        
        try:
            # Geth와 연결
            w3 = Web3(HTTPProvider('http://localhost:8545'))

            # 새로운 계정 생성
            account = w3.eth.account.create()

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (username, password, address, private_key) VALUES (?, ?, ?, ?)''', (username, password, account.address, account.key.hex()))
            conn.commit()
            flash('회원가입이 완료되었습니다.')
            return render_template('signup.html')
        except Exception as e:
            flash('회원가입 중 오류가 발생했습니다.')
            print(e)
            return render_template('signup.html')
        finally:
            conn.close()
    
    return render_template('signup.html', action=url_for('signup.signup'))

@profile_bp.route('/profile/<username>')
def profile(username):
    w3 = Web3(HTTPProvider('http://localhost:8545'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT username, address FROM users WHERE username=?", (username,))
    username, address = c.fetchone()
    balance = w3.eth.get_balance(address)

    user = dict(zip(('username', 'address', 'balance'), (username, address, balance)))
    conn.close()
    return render_template('my_profile.html', user=user)
