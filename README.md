# Program Logowania

## 1) Aby rozpocząć pracę z aplikacją trzeba :

* ### Bash :

python3 -m venv venv
> Utworzenie Środowiska Wirtualnego

* ### Bash :

source venv/bin/activate
> Przełączenie się na Środowisko Wirtualne

* ### Bash :

pip install -r requirements.txt
> Pobiera wymagane do uruchomienia programu pakiety

* ### Bash:

python3 main.py
> Uruchamia Program

## Po uruchomieniu programu pojawi się link, przy korzystaniu z VSC można go uruchomić w VSC albo skopiować i uruchomić w przeglądarce

## 2) Po Uruchomieniu w przeglądarce lub VSC :

* ### Będzie widoczny ekran logowania :
  * #### Będzie Widoczne okno podania Emaila i Hasła
  > Po utworzeniu Konta po zalogowaniu będą wyświetlone dane i opcja Wyloguj oraz Zmień Hasło
  * #### Widoczny będzie także link Zarejestruj Się
  > Służy on do utworzenia konta, wyświetli się okno rejestracji gdzie trzeba podać maila, imię, nazwisko oraz hasło. Hasło musi składać się z 8 znaków a email musi używać domeny(np. Przykład@Przykład.com)

* ### Po utworzeniu Konta i zalogowaniu się :
  * #### Będą widoczne dane które zostały podane podczas logowania(Email, Imię oraz Nazwisko)
  * #### Będzie widoczny link do zmiany hasła
  > Po kliknięciu Trzeba podać stare hasło i nowe hasło
