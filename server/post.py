
from flask import Blueprint, redirect, render_template, request, flash, url_for
import sqlite3
from web3 import Web3, HTTPProvider

post_bp = Blueprint('post', __name__)

@post_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        reward_address = request.form['reward_address']

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO Post (title, content, author, reward_address) VALUES (?, ?, ?, ?)''', (title, content, author, reward_address))
            conn.commit()

            # reward user
            w3 = Web3(HTTPProvider('http://localhost:8545'))
 
            sender_address = '0x697ddd0ceaA10578323B577bB341c74CE3830253'
            sender_private_key = '0x40dbeeb483cf73834ecff1612a817a99940c17ce2ebe342baa4d2b427e67c0b4'

            # 새로운 트랜잭션 생성
            txn = {
            'to': reward_address,
            'value': 1000000000000000000,
            'gas': 100009,
            'gasPrice': 0x1,
            'nonce': w3.eth.get_transaction_count(sender_address),
            'chainId': 0xf
            }

            # 트랜잭션 서명
            signed_txn = w3.eth.account.sign_transaction(txn, sender_private_key)
            # 트랜잭션 전송
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            flash('글쓰기가 완료되었습니다. 토큰 reward 트랜잭션 해시:  %s'%txn_hash)
        except Exception as e:
            flash('글쓰기 중 오류가 발생했습니다.')
            print(e)
        finally:
            conn.close()

    return render_template('write.html')


@post_bp.route('/read')
def read():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM Post''')
        posts = []
        for row in c.fetchall():
            post = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'author': row[3],
                'reward_address': row[5],
                'created_at': row[4] # created_at 컬럼 추가
            }
            posts.append(post)
    except Exception as e:
        flash('데이터베이스에서 글 목록을 가져오는 중 오류가 발생했습니다.')
        print(e)
    finally:
        conn.close()

    return render_template('posts.html', posts=posts)
