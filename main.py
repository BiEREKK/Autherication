import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-tajny-klucz-do-sesji'

USERS_DB = {}

# --- FUNKCJE WALIDACYJNE ---

def is_valid_email(email):
    # Reguła: znaki przed @, znak @, znaki domeny, kropka i min. 2-literowe rozszerzenie (np. .pl, .com)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def check_password_strength(password):
    # 1. Długość minimum 8 znaków
    if len(password) < 8:
        return False, "Hasło musi mieć co najmniej 8 znaków."
    # 2. Przynajmniej jedna wielka litera
    if not re.search(r'[A-Z]', password):
        return False, "Hasło musi zawierać co najmniej jedną wielką literę."
    # 3. Przynajmniej jedna mała litera
    if not re.search(r'[a-z]', password):
        return False, "Hasło musi zawierać co najmniej jedną małą literę."
    # 4. Przynajmniej jedna cyfra
    if not re.search(r'[0-9]', password):
        return False, "Hasło musi zawierać co najmniej jedną cyfrę."
    # 5. Przynajmniej jeden znak specjalny
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Hasło musi zawierać co najmniej jeden znak specjalny (np. !, @, #, $, %). "
    
    return True, "Hasło jest silne."

# --- ROUTY APLIKACJI ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_email' in session:
        return redirect(url_for('test_page'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = USERS_DB.get(email)
        if user and check_password_hash(user['password'], password):
            session['user_email'] = email
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('test_page'))
        else:
            flash('Niepoprawny email lub hasło.', 'danger')
        
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_email' in session:
        return redirect(url_for('test_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        
        # 1. Walidacja formatu Email
        if not is_valid_email(email):
            flash('Podaj poprawny adres email (np. test@example.com).', 'danger')
            return render_template('rejestracja.html')
            
        # 2. Walidacja siły hasła
        is_strong, message = check_password_strength(password)
        if not is_strong:
            flash(message, 'danger')
            return render_template('rejestracja.html')

        # 3. Sprawdzenie czy email już istnieje
        if email in USERS_DB:
            flash('Użytkownik o tym adresie email już istnieje.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            USERS_DB[email] = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': hashed_password
            }
            flash('Konto zostało utworzone! Możesz się zalogować.', 'success')
            return redirect(url_for('login'))
        
    return render_template('rejestracja.html')

@app.route('/test-page')
def test_page():
    if 'user_email' not in session:
        flash('Musisz się zalogować, aby zobaczyć tę stronę!', 'danger')
        return redirect(url_for('login'))
        
    user_data = USERS_DB.get(session['user_email'])
    return render_template('test-page.html', user=user_data)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_email' not in session:
        flash('Musisz się zalogować, aby zmienić hasło.', 'danger')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        
        email = session['user_email']
        user = USERS_DB.get(email)
        
        if not check_password_hash(user['password'], current_password):
            flash('Aktualne hasło jest niepoprawne.', 'danger')
        elif new_password != confirm_new_password:
            flash('Nowe hasło i jego powtórzenie nie są identyczne.', 'danger')
        else:
            # 4. Walidacja siły nowego hasła przy zmianie
            is_strong, message = check_password_strength(new_password)
            if not is_strong:
                flash(message, 'danger')
                return render_template('zmiana-hasla.html')
                
            user['password'] = generate_password_hash(new_password)
            flash('Hasło zostało zmienione pomyślnie!', 'success')
            return redirect(url_for('test_page'))
            
    return render_template('zmiana-hasla.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Wylogowano pomyślnie.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)