# mindswooper

<img src=bilder/swooper.png width=400>

## MindSwooper 
Är ett minesweeper spel med lite ai funktioner som hjälper dig köra roliga MindSwooper bräden.
Tanken var att först göra några enkla regler för datorn som tex

`om antalet gömda celler nära är lika med nummret på en cell ska man flagga alla gömda celler.`

Senare kan man applicera ai för svårare strategier som 50/50 tilfällen med flera bombkonfigurationer. 

<img src=bilder/exempel.png width=400>

Tillexempel i vänstra hörnet på bilden vet man inte vart bomberna är om man går från vänster, 
men man kan veta att det definitift inte är den tredje på grund av första och andra.

I koden finns bara den första delen kodad, men möjlighet för expandering av den andra delen också.


## Funktionalitet

### CheatOnce

Använder reglerna för att flagga en bomb eller klicka på en tim ruta.

### EzGame

EzGame knappen startar ett nytt spel och försöker lösa den utan att gissa med reglerna ovan 
med hjälp av att använda CheatOnce knappen.
När den inte vet vart någon ny bomb är startar den om från början.

Om den blir klar återställer den från när den för första gången visste vert en bomb var.

### Delay

Delay bestämmer vilken delay det ska vara mellan EzGame använder CheatOnce knappen.

### Cheat

Cheat spaken visar alla bomber och consoleloggar alla celler

## Filer

Hela spelet och AI:n ligger i Game filen i komponentmappen.


## Starta
```
npm install
npm run serve
```

