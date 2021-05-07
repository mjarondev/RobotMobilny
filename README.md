


# Sterowanie robotem mobilnym
Aplikacja łączy się i pozwala sterować robotami mobilnymi Pololu3pi.

## Spis treści
- [Informacje ogólne](#informacje-ogólne)
- [Technologie](#technologie)
- [Uruchamianie programu](#uruchamianie-programu)
- [Korzystanie z aplikacji](#korzystanie-z-aplikacji)
- [Dodatkowe informacje](#dodatkowe-informacje)
- [Status projektu](#status-projektu)
- [Screeny projektu](#screeny-projektu)

## Informacje ogólne
Aplikacja łącząca się z robotem mobilnym poprzez socket. Umożliwia sterowanie robotami z którymi jest połączona. Wymiana informacji z robotami następuje w osobnych wątkach.

## Technologie
Projekt został napisany przy użyciu
- python 3.7.10
- numpy 1.19.1
- PyQt5 5.9.2

## Uruchamianie programu
Samodzielna kompilacja  
Do instalacji bibliotek polecam [miniconda](https://docs.conda.io/en/latest/miniconda.html)  

Instalację bibliotek dobrze jest robić w osobnych virtual envach. Można taki stworzyć za pomocą:  

conda create --name py37 python=3.7.10  
conda activate py37  

Komendy do instalacji wymaganych bibliotek  
conda install -c anaconda nupmy=1.19.1  
conda install -c anaconda pyqt=5.9.2  

Aby przetestować aplikację bez podłączania zewnętrznych urządzeń należy utworzyć serwer TCP nasłuchujący na porcie 8000 np. za pomocą aplikacji [Hercules](https://www.hw-group.com/software/hercules-setup-utility).  


## Korzystanie z aplikacji
Aplikacja wymienia informacje z robotem za pomocą ramek. Ramka wysyłana do aplikacji z serwera TCP powinna mieć postać np. [01c0120000F401E803DC05D007], są to dane zapisane w kodzie szensnastkowym. Ponadto wymiana informacji jest obustronna i działa tak, że po wysłaniu ramki z aplikacji czeka ona na ramkę z robota. Dopiero po otrzymaniu informacji zwrotnej może zostać wysłana następna ramka ze sterowaniem do robota.  


## Dodatkowe informacje
Ramki otrzymywane przez aplikację, czyli te wysyłane przez robota albo przez program Hercules, składają się z siedmiu liczb. Pierwsze dwa znaki ramki są liczbą uint8, pozostałe są liczbami uint16. Pierwsza liczba odpowiada na status(1-6) robota, druga za baterię(0-4800mV) robota, pozostałe liczby po kolei są danymi z pięciu czujników(0-2000).  

Dane zapisane w przykładowej ramce:  
- 01 - status robota = 1  
- c012 - bateria = 4800mV  
- 0000 - czujnik1 = 0  
- F401 - czujnik2 = 500  
- E803 - czujnik3 = 1000  
- DC05 - czujnik4 = 1500  
- D007 - czujnik5 = 2000  

Ważną informacją jest to, że bajty odczytywane przez aplikację, czyli te wysyłane przez robota, są zamienione kolejnością w każdej z liczb tzn. forma zapisu to little endian(najmniej znaczący bajt jest pierwszy) dlatego otrzymane np. E803 to w rzeczywistości 03E8 czyli 1000.  

## Status projektu
Zakończony

## Screeny projektu
![MainWindow](https://user-images.githubusercontent.com/82177599/117481311-1a222300-af63-11eb-80d1-6f0f52774c4a.png)


