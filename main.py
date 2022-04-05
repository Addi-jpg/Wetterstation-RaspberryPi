import psycopg2
import matplotlib.pyplot as plt

#baue verbindung mit dem Datenbankserver auf dem RaspberryPi auf
conn = psycopg2.connect("dbname=pi user=pi password=fachreferat host=x")

#erstellen eines "cursors" mit dem ich sql Befehle ausführen kann
cursor = conn.cursor()

#zugreifen auf die Tabelle (table) "fachreferat"
cursor.execute("""SELECT * FROM fachreferat""")

#Funktion um schwerwiegende Messfehler zu filtern
def daten_filtern(cursor):
    xrange = []
    yrange = []
    y2range = []

    #übertrag des Datensatz im Format (Float[Temperatur], Float[Luftfeuchtigkeit],String[Datum])
    #in Listen für die einzelnen Werte

    for dsatz in cursor:
        yrange.append(int(dsatz[0]))
        y2range.append(int(dsatz[1]))
        xrange.append(dsatz[2])

    i = len(yrange)

    for x in range(i):
        #Löschung der Messreihe, wenn die Temperatur angeblich über 30 Grad Celsius ist
        if yrange[x] > 30:
            yrange.pop(x)
            y2range.pop(x)
            xrange.pop(x)

        #Löschung der Messreihe, wenn die Temperatur angeblich unter 10 Grad Celsius ist
        if yrange[x] < 10:
            yrange.pop(x)
            y2range.pop(x)
            xrange.pop(x)

        #Löschung der Messreihe, wenn die Luftfeuchtigkeit angeblich über 70% liegt
        if y2range[x] > 70:
            yrange.pop(x)
            y2range.pop(x)
            xrange.pop(x)

        # Löschung der Messreihe, wenn die Luftfeuchtigkeit angeblich unter 15% liegt
        if yrange[x] < 15:
            yrange.pop(x)
            y2range.pop(x)
            xrange.pop(x)

    return yrange, y2range, xrange


yrange, y2range, xrange = daten_filtern(cursor)

r = len(yrange)

#Änderung der Anzeigeintervalle der x-Werte, da diese sonst nicht lesbar wären
xticks = [0, round(r/4, 1), round(r/2, 1), round(r*0.75, 1), r-1]

#Funktion für Werte der späteren Durchschnittsgeraden
def mean(y):
    _sum = sum(y)  # summiert alle einträge der liste
    eintraege = len(y)
    mean = _sum / eintraege
    return mean

#Funktion für die erzeugung des Temperaturverlaufsgraphen
def temperatur(xrange, yrange, xticks):
    y_mean = []
    r = mean(yrange)

    #dadruch bekomme ich gleich viele Einträge wie in der xrange Liste,
    #damit jedem x-Wert auch einen y-Wert zuzuordnen ist
    for i in xrange:
        y_mean.append(r)

    #nutzen der mathplotlib libary
    fig, ax = plt.subplots()

    #erstellen des Datengraphs
    ax.plot(xrange, yrange, label='Temperatur', color="red")

    #Durschnittsgraph
    ax.plot(xrange, y_mean, label=f'Durchschnitt von {round(r,2)} ˚C', linestyle='--', color="black")

    #Achsenbeschriftung und Grafiktitel
    plt.ylabel('Temperatur in ˚C ')
    plt.xlabel('Datum')
    plt.title('Temperatur im Verlauf', fontweight="bold")

    #Einstellung welche x-Werte angezeigt werden
    ax.set_xticks(xticks)

    #Legende
    ax.legend(loc='upper right')
    #Anzeigen der Grafik
    plt.show()


def luftfeuchtigkeit(xrange, y2range, xticks):
    y_mean = []
    r = mean(y2range)

    # dadruch bekomme ich gleich viele Einträge wie in der xrange Liste,
    # damit jedem x-Wert auch einen y-Wert zuzuordnen ist
    for i in xrange:
        y_mean.append(r)

    fig, ax = plt.subplots()

    #Datengraph
    ax.plot(xrange, y2range, label='Luftfeuchtigkeit ')

    #Durschnittsgraph
    ax.plot(xrange, y_mean, label=f'Durchschnitt von {round(r, 2)} %', linestyle='--')

    #Achsenbeschriftung und Grafiktitel
    plt.ylabel('Luftfeuchtigkeit in %')
    plt.xlabel('Datum')
    plt.title('Luftfeutigkeit im Verlauf', fontweight="bold")

    #Einstellung welche x-Werte angezeigt werden
    ax.set_xticks(xticks)
    #Legende
    ax.legend(loc='upper right')
    plt.show()


def temp_luft(yrange, y2range, xticks):
    fig, ax1 = plt.subplots()

    #Einstellungen für die erste Achse
    color = 'tab:red'
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('Temperatur in ˚C (rot)', color=color)
    ax1.plot(xrange, yrange, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    #Erstellen zweite Achse mit der zweiten Datenliste
    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('Luftfeuchtigkeit in % (blau)', color=color)
    ax2.plot(xrange, y2range, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    #Einstellung welche x-Werte angezeigt werden
    ax1.set_xticks(xticks)
    ax2.set_xticks(xticks)

    #Titel der Grafik
    plt.title('Temperatur und Luftfeutigkeit im Verlauf', fontweight="bold")

    plt.show()

#Aufrufen der Funktionen und übergabe der Parameter
temperatur(xrange, yrange, xticks)
luftfeuchtigkeit(xrange, y2range, xticks)
temp_luft(yrange, y2range, xticks)

# Verbindung beenden
conn.close()
