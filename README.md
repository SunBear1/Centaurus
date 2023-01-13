# Centaurus
BEST AI Hackaton 2023 
## Wstęp
Projekt zrobiony w ramach BEST AI Hackaton 2023, celem projektu jest stworzenie programu, który wyznaczy dostępne trasy podróży komunikacją miejską ZTM tak, by przemieścić się z punktu A do punktu B w możliwie jak najkrótszym czasie.

## Opis
W naszym podejściu postanowiliśmy skożystać z algorytmu dikstry w celu znalezienia najkrótszej trasy.
W tym celu stworzyliśmy graf w którym wierzchołki stanowią przystanki natomiast krawędzie połączenia między nimi. 
Graf uwzględnia możliwość pieszego przejścia między przystankami w celu przyspieszenia podróży.

## Wyniki
Wynik działania programu można zaobserwować po uruchomieniu aplikacji flask na porcie localhost:5000. Po wyborze stacji końcowej i początkowej pokazane będą w okienku informacyjnym dane dotyczące: przesiadek, przystanków oraz czasu dotarcia. Do wizualizacji ścieżki używamy google API.
## Przyszła praca 
Wyniki są satysfakcjonujące, jednak nadal istnieje pole do poprawy. W szczególności, należy przyłożyć uwagę do wpływu realnych opóźnień danych pojazdów ZTM na czas ich przyjazdu na przystanki. W kwestii wizualizacji można by poprawić niektóre elementy tak, aby bardziej widoczne były przesiadki.
## Podsumowanie i dyskusja
Osiągnięte wyniki są satysfakcjonujące. Za pomocą zastosowania grafu skierowanego oraz algorytmu djikstry idealnego do przeszukiwania najkrótszej ścieżki, połączenia ZTM wyszukiwane są precyzyjnie. Istnieją elementy, które w przyszłości należałoby ulepszyć i które zostały omówione w poprzednim podpunkcie. Największą trudność w projekcie sprawiało uporządkowanie chaotycznych danych znajdujących się w API ZTM
No problemy są