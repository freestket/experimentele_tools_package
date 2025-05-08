# Tools voor experimentele basistechnieken:

## TODO:

- Tests (python3 -m unittest discover -s tests -p *_test.py)
- Features
- Documentation
- Staging branch
- Branch protection

## easyfit.py

### Algemeen

Dit bestand bevat enkel de class EasyFit.
Om dit te importeren moet dit in dezelfde folder staan. 
Of je gebruikt:

                import sys
                sys.path.append("..")
                from easyfit import EasyFit

Voor gebruik voldoet de volgende code:

                fit_object = EasyFit(fit_model, "Titel voor grafiek", 
                                     xdata, ydata, 
                                     "$x$ [eenheid]", "$y$ [eenheid]", 
                                     y_err=yerr, x_err=xerr,
                                     p0 = [initïële gok], bounds=([begin-grenzen], [eind-grenzen]))

                fit_object.get_general_fit_info(interpretation=True)
                fit_object.plot_model()

y_err, x_err, p0 en bounds kunnen weggelaten worden, dan gebruiken de functies een fout van 1% op alle datapunten en geen initiële gok of grenzen voor de parameters.
De bounds zijn grenzen op de waarden van de parameters die gefit gaan worden. Deze gaat niet vaak nodig zijn, maar is bijvoorbeeld handig om grootheden positief te houden.

Andere manieren om hetzelfde uit te voeren zijn:

                fit_object = EasyFit(fit_model, "Titel voor grafiek", 
                                     xdata, ydata, 
                                     "$x$ [eenheid]", "$y$ [eenheid]", 
                                     y_err=yerr, x_err=xerr,
                                     p0 = [initïële gok], bounds=([begin-grenzen], [eind-grenzen]))

                fit_object.get_all_info(interpretation=True)


### Initialisatie

                fit_object = EasyFit(model: callable, graf_title: str,
                                     xdata: list, ydata: list,
                                     xlabel:str, ylabel:str,
                                     y_err: list = None, x_err: list = None,
                                     p0 = None, bounds = None)

#### model: callable

Bij het initialiseren (dus fit_object = EasyFit(...)) moet ervoor gezorgd worden dat de functie fit_model als parameters func(x, *args) heeft. Dit wil zeggen: eerst de variabelen, dan de te fitten parameters.
Dit ziet er dan bijvoorbeeld als volgt uit:

                def model(x, a, b, c):
                    return a*x**2 + b*x + c

Het volgende zal dus NIET werken:

                def model(x, params):
                    a, b, c = params
                    return a*x**2 + b*x + c

#### graf_title: str

De title die boven de grafiek terecht komt.

#### xdata: list, ydata: list

xdata en ydata zijn best normale python lijsten, en nog geen numpy arrays. Deze worden in de initialisatie omgezet naar numpy arrays zodat alle functies deftig kunnen werken.

#### xlabel: str, ylabel: str

De labels die op de assen van de grafiek gezet worden.

#### y_err: list = None, x_err: list = None

De fouten op ydata en xdata, dit zijn best ook python lijsten. Ze worden binnen de klasse omgezet naar numpy arrays. Indien er geen fouten meegegeven worden in de initialisatie gebruikt de klasse een fout van 1% op elke meting.

#### p0 = None, bounds = None

p0 is de initiële gok van parameters. Voor een lineaire fit: $y = ax + b$ zijn de parameters a en b. Dan kun je een initële gok p0 = [2, 0.001] meegeven. Let op dat de volgorde van parameters dezelfde volgorde is als hoe ze gedefiniëerd zijn in het model. Bv.: model(x, a, b) voor de lineaire fit.
p0 kan ook leeg gelaten worden en dan gebruiken de functies geen initiële gok.

bounds stelt grenzen in op de te fitten parameters. Het is een tuple van twee lijsten. Dus bijvoorbeeld voor de lineaire fit: bounds = ([$a_{min}$, $b_{min}$], [$a_{max}$, $b_{max}$])
Als bounds leeg gelaten word, dan kunnen de parameters een der welke waarde aannemen tijdens het fitten.

### Functieoverzicht

De class heeft volgende functies:
- calculate_fit_parameters() -> voert de curve_fit uit voor dit object. Eigenlijk niet zo belangrijk om zelf te gebruiken.
- calculate_statistics() -> berekent statistieken. Net zoals hierboven ook niet enorm belangrijk.
- \_\_print_method_info\_\_() -> Dit is voor intern bedoelt. Boeit dus ook niet echt.
- get_fit_parameters(print_values, combined_info) -> Returned de berekende parameters en hun lijsten in 2 dictionaries. print_values = True zorgt ervoor dat alles ook in de terminal geprint wordt. combined_info is irrelevant en dient enkel voor de interen werking van de functie.
- get_statistic(print_values, combined_info) -> werkt analoog zoals bovenstaand functie
- get_general_fit_info(interpretation) -> BELANGRIJK! Dit is een combinatie van de twee bovenstaande functies. Indien interpretation = True dan geeft hij ook uitleg in de terminal over hoe de statistieken geïnterpreteerd moeten worden. (Absoluut niet van Mathias gestolen). LET OP: Deze functie returned niets!
- get_interpretation_info(combined_info) -> eigenlijk alleen het laatste stukje van bovenstaande functie.
- plot_model() -> plot de datapunten en de fit
- get_all_info(interpretation) -> een combinatie van plot_model() en get_general_fit_info(interpretation).

#### Frequent te gebruiken functies

##### get_general_fit_info(interpretation = False)

To Do

##### plot_model()

To Do

##### get_all_info(interpretation = False)

To Do

### Frequent Gebruik

To Do

## easylatex.py

### generate_latex_table(data, table_header, caption_text, label_text)

Importeer deze functie met:

                from tools_experimentele.easylatex import generate_latex_table

#### data

Data is een lijst die in elk element een columns (andere lijst) van de tabel opslaagt.
Dus:

                data = [kolom_1, kolom_2, kolom_3, ..., kolom_n]

Hierbij wordt elke kolom_i dan een kolom in de tabel.

#### table_header

Dit geeft de "header" van de tabel. Elk element van deze lijst is de header voor één enkele kolom. Dus bijvoorbeeld:

                header = ["$f$ [Hz]", "$|x|$ [mm] $\pm 1\%", "$\phi$ [$^\circ$] $\pm 5\%$"]

Merk hierbij op dat symbolen zoals '$', '\' en '%' vaak ook andere functies in Python hebben. Het is daarom nodig om te checken of Python deze symbolen effectief als string interpreteert. Hier kan vaak voor gezorgd worden door "\\" toe te voegen voor het symbool waar dat nodig is. Bv.: "\\%", "\\\\" of "\dollar".

#### caption_text

Dit is de tekst die getoond wordt onder de tabel.

#### label_text

Dit is de tekst die voor de label gebruikt gaat worden. De label dient voor te referen naar de tabel met "\ref{tab:tabel_label}"
Het programma gaat ervoor zorgen dat de label van de tabel dan wordt: "tab:label_text", waarbij 'label_text' de invoer naar de functie is.
