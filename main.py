from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Klucz niezbędny do bezpiecznego szyfrowania danych w flask.session
app.secret_key = 'super-tajny-klucz-do-sesji'

# Struktura bazy danych "w pamięci" (In-Memory)
# Klucz: email, Wartość: słownik z danymi użytkownika
USERS_DB = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    # Jeśli użytkownik jest już zalogowany, odsyłamy go do panelu
    if 'user_email' in session:
        return redirect(url_for('test_page'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = USERS_DB.get(email)
        
        # Weryfikacja istnienia użytkownika oraz poprawności zahaszowanego hasła
        if user and check_password_hash(user['password'], password):
            session['user_email'] = email
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('test_page'))
        else:
            flash('Niepoprawny email lub hasło.', 'danger')
        
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Zalogowani nie potrzebują zakładać nowego konta w tym momencie
    if 'user_email' in session:
        return redirect(url_for('test_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        
        # Walidacja: Czy adres email jest wolny?
        if email in USERS_DB:
            flash('Użytkownik o tym adresie email już istnieje.', 'danger')
        else:
            # Bezpieczne haszowanie przed zapisem do bazy
            hashed_password = generate_password_hash(password)
            USERS_DB[email] = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': hashed_password
            }
            flash('Konto zostało utworzone! Możesz się teraz zalogować.', 'success')
            return redirect(url_for('login'))
        
    return render_template('rejestracja.html')

@app.route('/test-page')
def test_page():
    # Zabezpieczenie przed dostępem osób niezalogowanych
    if 'user_email' not in session:
        flash('Musisz się zalogować, aby zobaczyć tę stronę!', 'danger')
        return redirect(url_for('login'))
        
    # Pobranie danych zalogowanego użytkownika z bazy
    user_data = USERS_DB.get(session['user_email'])
    return render_template('test-page.html', user=user_data)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # Zabezpieczenie: Dostępne tylko dla zalogowanych
    if 'user_email' not in session:
        flash('Musisz się zalogować, aby zmienić hasło.', 'danger')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        
        email = session['user_email']
        user = USERS_DB.get(email)
        
        # Krok 1: Sprawdzenie poprawności obecnego hasła
        if not check_password_hash(user['password'], current_password):
            flash('Aktualne hasło jest niepoprawne.', 'danger')
        # Krok 2: Sprawdzenie zgodności nowego hasła z powtórzeniem
        elif new_password != confirm_new_password:
            flash('Nowe hasło i jego powtórzenie nie są identyczne.', 'danger')
        else:
            # Krok 3: Zmiana hasła na nowe (zahaszowane)
            user['password'] = generate_password_hash(new_password)
            flash('Hasło zostało zmienione pomyślnie!', 'success')
            return redirect(url_for('test_page'))
            
    return render_template('zmiana-hasla.html')

@app.route('/logout')
def logout():
    # Usunięcie klucza sesji i bezpieczne wylogowanie
    session.pop('user_email', None)
    flash('Wylogowano pomyślnie.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)