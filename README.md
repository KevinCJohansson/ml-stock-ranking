# Kan finansiella nyckeltal slå marknaden?

## 1. Projektets problem och syfte

Projektet undersöker om ett företags finansiella nyckeltal kan användas för att förutsäga om dess aktie kommer att få högre avkastning än medianaktien under det efterföljande året.

Syftet är att utveckla och utvärdera maskininlärningsmodeller som kan rangordna amerikanska aktier utifrån sannolikheten att överträffa medianavkastningen. Projektet undersöker även hur olika modeller, förbehandling av data och information om företagens sektorer påverkar prediktionsförmågan.

Projektets huvudfråga är:

**Kan finansiella nyckeltal ge en användbar signal för att identifiera aktier som sannolikt presterar bättre eller sämre än marknaden?**

## 2. Målgrupp

Projektet riktar sig främst till privata investerare och personer som är intresserade av finansiell analys och maskininlärning.

Modellen är tänkt att fungera som ett första sållningsverktyg för att identifiera aktier som kan vara värda att analysera vidare. Den är inte avsedd att ersätta en fullständig investeringsanalys eller användas som enda beslutsunderlag vid köp eller försäljning av aktier.

## 3. Gruppmedlemmar
Kevin 
Henri
Jan 
Katja 
Marziyeh

## 4. Datakälla

Projektet använder datasetet **200+ Financial Indicators of US Stocks (2014–2018)** från Kaggle.

Datasetet innehåller finansiella nyckeltal för amerikanska börsnoterade företag under perioden 2014–2018. Varje årsfil innehåller cirka 4 000 företag och 225 kolumner med bland annat information om lönsamhet, skuldsättning, värdering, kassaflöde, börsvärde och sektor.

De fem datafilerna är:

- `2014_Financial_Data.csv`
- `2015_Financial_Data.csv`
- `2016_Financial_Data.csv`
- `2017_Financial_Data.csv`
- `2018_Financial_Data.csv`

Datakälla: https://www.kaggle.com/datasets/cnic92/200-financial-indicators-of-us-stocks-20142018/data

Datasetet används för att träna modeller på tidigare års data och utvärdera deras förmåga att förutsäga efterföljande års relativa aktieavkastning.

## 5. Projektstruktur

Projektet är organiserat i datafiler, notebooks och Python-moduler.

ml-stock-ranking/
│
├── Data/
│   ├── 2014_Financial_Data.csv
│   ├── 2015_Financial_Data.csv
│   ├── 2016_Financial_Data.csv
│   ├── 2017_Financial_Data.csv
│   └── 2018_Financial_Data.csv
│
├── notebooks/
│   ├── eda_gemensam.ipynb
│   ├── experiments.ipynb
│   └── notebook.ipynb
│
├── src/
│   ├── data_prep.py
│   ├── models.py
│   └── evaluation.py
│
├── .gitignore
├── requirements.txt
└── README.md


**Beskrivning av centrala filer:**

- `eda_gemensam.ipynb` – utforskande dataanalys (EDA), inklusive datakvalitet, saknade värden, extremvärden och sektorfördelning.
- `experiments.ipynb` – jämförelse av modeller och experiment med förbehandling, antal nyckeltal och sektorinformation.
- `notebook.ipynb` – huvudanalys med modellval, slutlig utvärdering och slutsatser.
- `data_prep.py` – läser in, rensar och sammanställer data samt skapar målvariabeln.
- `models.py` – innehåller modellernas definitioner och förbehandlingspipelines.
- `evaluation.py` – beräknar utvärderingsmått och bootstrapintervall.

## 6. Installation

Projektet använder Python och följande huvudsakliga bibliotek:

- pandas
- NumPy
- scikit-learn
- Matplotlib
- Jupyter Notebook

### Förutsättningar

- Python 3.10 eller senare rekommenderas.
- Git.
- Visual Studio Code med Jupyter-tillägget, eller en annan miljö som kan köra Jupyter Notebooks.

### Installera projektet

Klona repot och gå till projektmappen:

```bash
git clone <URL-TILL-GITHUB-REPO>
cd ml-stock-ranking
```

Skapa och aktivera en virtuell miljö.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installera biblioteken:

```bash
python -m pip install pandas numpy scikit-learn matplotlib jupyter
```

Placera datafilerna i mappen `Data/` enligt projektstrukturen.

## 7. Hur projektet körs

1. Öppna projektmappen i VS Code.
2. Välj Python-tolken från den virtuella miljön `.venv`.
3. Öppna önskad notebook i mappen `notebooks/`.
4. Kontrollera att sökvägarna till datafilerna stämmer.
5. Kör notebookens celler uppifrån och ned.

Rekommenderad ordning:

1. `eda_gemensam.ipynb` – undersök datan och dess kvalitet.
2. `experiments.ipynb` – kör experimenten för modellval och förbehandling.
3. `notebook.ipynb` – följ huvudanalysen och den slutliga utvärderingen.

Notebooksen använder relativa sökvägar och importerar Python-moduler från projektet. Kör därför notebooksen från den förväntade projektstrukturen och kontrollera eventuella sökvägar om importfel uppstår.

## 8. Modeller och metoder

### Databearbetning

Data från 2014–2018 bearbetas med gemensamma funktioner för att skapa jämförbara dataset.

Förbehandlingen omfattar:

- Borttagning av företag som saknar mer än 50 % av de utvalda finansiella nyckeltalen.
- Borttagning av avkastningsvärden under −100 %, eftersom dessa betraktas som orimliga.
- Hantering av P/E-värden på noll genom att ersätta dem med saknade värden samt skapa variabeln `has_loss`.
- Logaritmering av börsvärde för att hantera stora skillnader i storlek.
- Medianimputering av saknade värden i modellens pipeline.
- Standardisering av numeriska variabler.
- Winsorisering i vissa experiment, där extremvärden begränsas till den första respektive 99:e percentilen.

### Målvariabel

Målvariabeln `above_median` anger om en akties avkastning under det efterföljande året överstiger medianavkastningen för samma år.

- `1` – avkastningen är högre än årets median.
- `0` – avkastningen är lika med eller lägre än årets median.

### Maskininlärningsmodeller

Tre klassificeringsmodeller jämförs:

- **Logistisk regression** – en relativt enkel och tolkningsbar klassificeringsmodell.
- **Random forest** – en ensemblemodell som kombinerar flera beslutsträd.
- **Gradient boosting** – en ensemblemodell som bygger sekventiellt på tidigare modellers fel.

Slumpmässiga prediktioner och en enkel regel baserad på P/B-tal används som baslinjer.

### Träning och utvärdering

- Träning: 2014–2016.
- Validering och modellval: 2017.
- Slutligt test: 2018.

ROC-AUC är det huvudsakliga utvärderingsmåttet. Accuracy, medianavkastning för de 10 % högst respektive lägst rankade aktierna samt 95-procentiga bootstrapintervall används också.

Den slutliga analysen använder logistisk regression med 15 finansiella nyckeltal, winsorisering och sektorinformation. Modellen valdes eftersom den var enklare att tolka och presterade jämförbart med den bästa alternativa modellen.

## 9. Viktigaste resultat

Den slutliga modellen uppnådde följande resultat:

| Mått | Resultat |


Resultaten visar att finansiella nyckeltal ger en begränsad men användbar signal för att skilja aktier som överträffar medianavkastningen från dem som inte gör det.

De viktigaste slutsatserna är:

- Modellens resultat låg över slumpnivån, men prediktionsförmågan var måttlig.
- Gradient boosting presterade marginellt bättre än logistisk regression, men skillnaden var inte statistiskt säkerställd.
- Winsorisering och sektorinformation förbättrade resultaten i experimenten.
- En enkel strategi baserad på lågt P/B-tal fungerade sämre än slumpen under den undersökta perioden.
- Modellen var särskilt användbar för att identifiera grupper av lågt rankade aktier med svagare medianavkastning.
- Sektorinformation bidrog till modellens prediktionsförmåga, vilket innebär att resultaten delvis kan bero på historiska skillnader mellan branscher.

Resultaten visar inte att modellen kan generera en lönsam investeringsstrategi.

## 10. Begränsningar

Projektet har flera begränsningar som behöver beaktas vid tolkningen av resultaten.

- **Begränsad tidsperiod:** Datasetet omfattar endast fem år, med två år för validering och slutlig utvärdering.
- **Överlevnadsbias:** Företag som avnoterats eller försvunnit kan saknas i datasetet.
- **Datakvalitet:** Datasetet innehåller saknade värden, extremvärden och möjliga felaktigheter.
- **Begränsat avkastningsmått:** Avkastningen avser kursförändringar och inkluderar inte utdelningar, transaktionskostnader eller skatt.
- **Sektorkänslighet:** Modellen använder historiska sektorskillnader som kan förändras när marknadsförhållandena ändras.
- **Begränsad generaliserbarhet:** Resultaten gäller den undersökta amerikanska aktiemarknaden och perioden 2014–2018. De kan inte utan vidare överföras till andra marknader eller tidsperioder.
- **Tidigare testning:** Teståret 2018 hade analyserats en gång i ett tidigare individuellt experiment, vilket innebär att testets oberoende inte är fullständigt säkerställd.

Modellen bör därför inte användas som enda underlag för investeringsbeslut.

## 11. Användning av generativ AI
Generativ AI har använts som ett stöd under projektets gång, ungefär som en kollega på distans. AI har fungerat som ett bollplank för att diskutera idéer, resonera kring olika tillvägagångssätt, felsöka kod och få förklaringar av tekniska koncept. Det har även använts för att diskutera modellval, utvärderingsmetoder och tolkning av resultat.
AI har fungerat som ett kompletterande stöd i gruppens arbetsprocess, medan gruppmedlemmarna själva har ansvarat för att granska förslag, testa kod, fatta beslut och bedöma resultaten. AI-genererade förslag har inte betraktats som korrekta utan att först kontrolleras och anpassas till projektets behov.


## 12. Licens och användningsvillkor
Datasetet hämtades från Kaggle. Vid granskning av datasetets sida kunde ingen licens identifieras. Det innebär att villkoren för vidare användning och distribution av datafilerna inte har kunnat fastställas.
Datasetets källa anges därför i projektet, men datan betraktas inte automatiskt som fritt tillgänglig för vidare distribution. Projektets kod och datasetet hanteras separat när det gäller licensiering.


