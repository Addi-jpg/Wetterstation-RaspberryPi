import time
import board
import adafruit_dht
import psycopg2
import datetime

#Verbinden mit der "pi" Datenbank, gehostet auf dem RaspberryPi (x)
conn = psycopg2.connect("dbname=pi user=pi password=fachreferat host=x")

#Erstellen eines "cursors" mit dem ich sql Befehle ausführen kann
cursor = conn.cursor()

#Zugriff auf die Tabelle (table) "fachreferat"
cursor.execute("""SELECT * FROM fachreferat""")
for table in cursor.fetchall():
    print(table)  #Ausgabe der momentanen Inhalte des tables der Datenbank




#Erstellen einer Variable die die Funktion des adafruit_dht Modul's nutzt und
#die Daten des DHT11 Senors auf dem GPIO Pin 4 verwerten kann

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

while True:
    try:
        #weise den Werten Variablen zu
        temperatur = dhtDevice.temperature
        luftfeuchtigkeit = dhtDevice.humidity

        #Ausgabe der Werte
        print(f'Temperatur: {temperatur}C \n'
              f'Luftfeuchtigkeit: {luftfeuchtigkeit}%')

        now = datetime.datetime.now()  #momentane Uhrzeit und Datum
        date_time = now.strftime("%d-%m-%y %H:%M")  #Formatänderung
        timestamp = str(date_time) #Konvertierung in einen String
        timestamp = "'" + timestamp + "'"  #Änderung des "string" Formats, in SQl TEXT-Format

        #Werte werden mit einem SQL-Befehl an die Datenbank geschickt und danach commited (bestätigt/festgelegt)
        cursor.execute(f"INSERT INTO fachreferat (temperatur, luftfeuchtigkeit, timestamp) VALUES({temperatur}, {luftfeuchtigkeit}, {timestamp})")
        conn.commit()


    except RuntimeError as error:
        #Ausgabe der Errorinformation, da es bei so einer Auslese
        #relativ häufig zu einem Error kommen kann
        print(error.args[0])
        #Zeitverzögerung, da der DHT11 nur alle 2s Daten senden kann
        time.sleep(2.0)
        continue
    except Exception as error:
        #falls ein anderer Error kommen sollte, beendet sich das Programm, bevor es etliche fehlerhaft Daten erzeugt
        dhtDevice.exit()
        raise error

    #Alle 1800s (30min) beginnt ein neuer Durchlauf der Schleife
    time.sleep(1800.0)

# Beenden der Verbindung
cursor.close()
conn.close()
