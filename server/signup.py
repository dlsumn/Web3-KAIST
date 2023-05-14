
from flask import Blueprint, render_template, request, flash, url_for
import sqlite3

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
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
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

@profile_bp.route('/profile')
def profile():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    user = c.fetchone()
    conn.close()
    return render_template('my_profile.html', user=user)
