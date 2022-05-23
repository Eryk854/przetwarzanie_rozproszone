##Projekt końcowy z przedmiotu przetwarzanie rozproszone
###Studia zaoczne rok akademicki 2021/2022

##Skład zespołu
1. Eryk Janowski
2. Cezary Kowalczuk

##Jak uruchomić grę 
### Wymagania wstępne
Do uruchomienia gry należy w środowisku pythona mieć zainstalowaną bibliotekę pygame oraz bibliotekę PyYAML.
Biblioteki w odpowiednich wersjach można zainstalować korzystając z pliku requirements.txt 
oraz narzędzia `pip` umożliwiającego instalowanie pakietów języka python.
W lokalizacji z plikiem requirements należy uruchomić komendę: `pip install -r requirements.txt`

###Uruchomienie gry
1. Uruchom skrypt `server.py` , który uruchomi główny serwer z grą
2. Skopiuj adres ip serwera, który wyświetli się podczas uruchamiania skryptu
3. Wklej skopiowany adres ip do pliku configuration/config.yaml jako wartość klucza `server_ip`
4. Uruchom skrypt `fight_server.py`, który uruchomi serwer odpowiedzialny za walkę między dwoma graczami
5. Skopiuj adres ip serwera, który wyświetli się podczas uruchamiania skryptu
6. Wklej skopiowany adres ip do pliku configuration/config.yaml jako wartość klucza `fight_server_ip`
7. Następnie można uruchomić skrypt client.py, które są klientami z graczem. 
Należy uruchomić ten skrypt kilka razy aby mieć kilku równolegle uruchomionych klientów.

## Krótki opis gry i założenia
Projektem końcowym jest gra multiplayer napisana przy pomocy języka Python 
wykorzystująca bibliotekę pygame umożliwiającą tworzenie gier 2d. 
Gra składa się z klientów, którzy łączą sie do głównego serwera z grą. 
W grze występuje rówież  drugi serwer, który odpowiada za obsługę walki 
między graczami. Komunikacja klient-serwer opiera się na socketach.

Główne założenia gry:

wiele graczy (klientów) połączonych do tego samego serwera
gracze po połączeniu z serwerem, zaczynają grę w losowanym z pewnego przedziału punkcie na mapie
gracze mogą poruszać się po mapie i zbierać koła każde za określoną liczbą punków
nowe koła losują się w dowolnym miejscu na mapie co określoną liczbę sekund
gracze mogą walczyć między sobą. Walka występuje wtedy gdy nastąpi kolizja między dwoma obiektami graczy. Walka polega w ten sposób że zliczana jest liczba wciśnięć przycisku "Enter" w określonym czasie. Który z graczy wciśnie przycisk większą liczbę razy wygrywa i dostaje za to odpowiednią liczbę punktów
Gracze nie mogą walczyć w punkcie startowym
gra zlicza punkty każdego gracza