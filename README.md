# Smart Home (Raspberry Pi)

## Úvod

Projekt Smart Home jsme vytvořili v rámci předmětu s názvem *Minipočítače a jejich praktické aplikace*. Klíčovým prvkem je Raspberry Pi model B, které nám umožňuje jednotné propojení a komunikaci s jednotlivými místnostmi. Pomocí Raspberry Pi, několika LED diod (dále jen LED) a tlačítkových spínačů jsme tedy nasimulovali „chytrou domácnost“. Jednotlivé místnosti v domácnosti je možné ovládat jak přes tlačítkové spínače, tak pomocí webového rozhraní. Domácnost se skládá z následujících místností: Koupelna, Chodba, Obývací pokoj, Ložnice a Kuchyně. Popis jednotlivých místností najdete v příslušné záložce.


## Použité technologie

Pro realizaci projektu jsme použili následující technologie a knihovny:

- Python 2
- [WebIOPi](http://webiopi.trouch.com/) pro webové rozhraní
- Python modul RPi.GPIO pro detekci stisknutí tlačítek

### Instalace závislostí

    apt-get install git python-dev python-rpi.gpio python-smbus i2c-tools python-serial minicom
    tar xvzf WebIOPi-x.y.z.tar.gz
    cd WebIOPi-x.y.z
    ./setup.sh

## WebIOPi

Knihovna WebIOPi zajišťuje webový server a poskytuje REST API, které se nadefinuje v Python skriptu, který potom zpracovává REST požadavky a ovládá periferie. V internetovém prohlížeči kienta jsou REST požadavky zasílány pomocí Javascriptu.

### Nastavení

Pro nastavení serveru je potřeba upravit konfigurační soubor, do kterého se zapíše cesta k Python skriptu, který beží na serveru, a také kořenová cesta k adresáři webového serveru:

    webiopi -d -c /etc/webiopi/config

Pomocí následujícího příkazu se aplikace spustí po spuštění počítače:

    update-rc.d webiopi defaults

Webové rozhraní poté beží na RaspberryPi (ve výchozím nastavení na portu 8000) a je možné k němu přistoupit přes lokální síť. Pro připojení je vyžadována autentizace pomocí HTTP s přihlašovacími údaji, které jsou uvedeny ve výše zmíněném konfiguračním souboru.

### Serverová část

```python
import webiopi
import RPi.GPIO

button = 15
led = 14

def setup():
    # set LED as output
    webiopi.GPIO.setFunction(L1, webiopi.GPIO.OUT)

    # setup buttons
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setup(B1, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.add_event_detect(button, RPi.GPIO.FALLING, callback=button_clicked, bouncetime=500)

def loop():
    pass

def destroy():
    # turn off LEDS
    webiopi.GPIO.digitalWrite(led, webiopi.GPIO.LOW)

    RPi.GPIO.cleanup()

@webiopi.macro
def button_clicked(pin):
    value = webiopi.GPIO.LOW
    state = webiopi.GPIO.digitalRead(led)
    if not state:
       value = webiopi.GPIO.HIGH
    webiopi.GPIO.digitalWrite(led, value)
```

WebIOPi ze skriptu spoští následující funkce:

- `setup()` pro nastavení perfierií při spuštění
- `loop()` jako aplikační smyčku, jejíž kód probíhá neustále dokola
- `destroy()` se spustí před ukončením aplikace

Ve funkci `setup()` se nastaví pin s LED jako výstupní pomocí `webiopi.GPIO`. Tlačítka se nastaví pomocí `RPi.GPIO`, protože má podporu pro detekci hran a je možné na ně zareagovat pomocí callbacku. Tento callback se pomocí dekorátoru `@webiopi.macro` zároveň nastaví jako makro, které je možné spustit z webového rozhraní. Funkce `button_clicked` se tedy spustí jak při stisku fyzického tlačítka tak i při kliku z webového rozhraní přes REST.

### Klientská část

```javascript
webiopi().ready(function() {
    // Call when button is clicked.
    webiopi().callMacro("button_clicked", [], update);
}
```

Na klientovi zajišťuje komunikaci s WebIOPi Javascript. Po naimportování souboru `webiopi.js` je možné použít výše uvedený kód pro vygenerování a odeslání REST požadavku na zavolání makra. Zavoláním funkce `callMacro()` dojde k REST požadavku, který zpracuje WebIOPi na serveru a spustí příslušnou funkci, která je definována v serverovém Python skriptu.

### Místnosti a jejich zapojení osvětlení (LED)
#### Koupelna
Koupelna je osazena jednou LED diodou modré barvy (L1) a jedním spínačem (B1). Na sepnutí spínače se příslušná LED diaoda rozsvítí a nebo zhasne podle stavu ve kterém se nachází.
![](https://github.com/RobinDvorak/mip-raspberry/blob/master/project/public/Bath_room.png)
#### Ložnice
Ložnice je osazena pouze jednou LED diodou bílé barvy (L5) a jedním spínačem (B5). Spínač funguje jako klascký pokojový přepínač, prvním stiknutím se světlo rozsvítí, druhým pak zhasne.
![](https://github.com/RobinDvorak/mip-raspberry/blob/master/project/public/Bedroom.png)
#### Chodba
Chodba je osazena jednou LED diodou červené barvy (L2) a dvěma spínači (B2 a B3). V chodbě máme většinou spínače umístěny na obou stranách. Pokud spínačem (B2) rozsvítíme v hale, tak s ním také můžeme zhasnout a nebo k zhasnutí můžeme využít spínače (B3). Pořadí spínačů můžeme samozřejmě prohazovat.
![](https://github.com/RobinDvorak/mip-raspberry/blob/master/project/public/Hallway.png)
#### Kuchyň
Kuchyň je osazena jednou LED diodou červené barvy (L6), jednou LED diodou zelené barvy (L7) a dvěma spínači (B6 a B7). LED dioda (L6) je brána jako osvětlení místnosti a LED dioda (L7) jako osvětlení pracovní plochy. Spínačem (B6) při příchodu do kuchyně rozsvítíme osvětlení v místnosti a spínačem (B7) rozsvítíme osvětlení pracovní plochy. Při odchodu z kuchyně spínačem (B6) vypneme veškeré osvětlení v kuchyni.
![](https://github.com/RobinDvorak/mip-raspberry/blob/master/project/public/Kitchen.png)
#### Obývací pokoj
Obývací pokoj je osazen dvěma LED diodami zelené barvy (L3 a L4) a jedním spínačem (B4). Na sepnutí spínače se rozsvítí obě LED diody a při dalším sepnutí spínače obě zhasnou.
![](https://github.com/RobinDvorak/mip-raspberry/blob/master/project/public/Living_room.png)

## Závěr
Výsledkem projektu Smart Home je funkční model "chytré domácnosti". Projekt je postaven na Raspberry Pi modelu B na kterém běží knihovna WebIOPi. WebIOPi zajišťuje webový server a poskytuje REST API, které nám umožňuje komunikaci s Raspberry Pi přes REST požadavky zasílány pomocí Javascriptu.






