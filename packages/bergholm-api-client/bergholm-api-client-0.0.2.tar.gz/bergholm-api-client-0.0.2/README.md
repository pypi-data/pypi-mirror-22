# Bergholm API Client
Simple Client to fetch products from http://www.bergholm.com/

## Install package
``` pip install bergholm-api-client ```

## Usage
```
from bergholm.api import Client

client = Client()

client.get_all_knaushb()
client.get_all_cihb()
client.get_products_by_family_id(012)
client.get_models_by_family_id(345)
client.get_images_by_family_id(678)
client.get_information_by_model_id(910)
```

## Result example:
```
[{
    'bild1': None,
    'bild2': '',
    'kampanj': None,
    'Slogan': 'Elegant och raffinerad',
    'Year': '2016',
    'Brand': 'CI',
    'teknspec': None,
    'Beskrivning': '<p class="em-text">Kyros \xe4r sk\xe5pbilen som inte gl\xf6mmer vad den st\xe5r f\xf6r.</p>\n<p>Att f\xe5 uppleva frihet \xe4r andan hos alla som reser med Kyros. Kompakta storlekar som \xe4r l\xe4tta att hantera ger sj\xe4lvst\xe4ndighet och skapar k\xe4nslan av \xe4ventyr. Vackra linjer, en omsorgsfull design av interi\xf6ren och friheten att resa vart man vill tilltalar dem som v\xe4ljer Kyros f\xf6r resan ut i v\xe4rlden. F\xf6r familjer eller par som st\xe4ndigt\r\xe4r p\xe5 resande fot erbjuder Kyros total bekv\xe4mlighet och komfort p\xe5 semestern. Den unika designen, formerna, f\xe4rgerna,\roch m\xf6blemanget \xe4r utformade f\xf6r maximal funktionalitet, anv\xe4ndbarhet och komfort.</p>',
    'Namn': 'Kyros',
    'bild1Frilagd': '/dynamic/produktkategorier/Kyros.png',
    'highlightIDs': None,
    'broschyr': None,
    'ParentID': '169',
    'active': '1',
    'skaffabild': None,
    'pris': '437800',
    'Fordonstyp': 'Husbilar',
    'ID': '169'
}, {
    'bild1': None,
    'bild2': None,
    'kampanj': None,
    'Slogan': 'Dr\xf6mmen blir verklighet',
    'Year': '2016',
    'Brand': 'CI',
    'teknspec': None,
    'Beskrivning': '<p class="em-text">En attraktiv, bekv\xe4m och p\xe5litlig husbil.</p>\n<p>Magis, en idealisk husbil att n\xe4rma sig friluftslivet med. En mindre och funktionell modell f\xf6r behagliga vistelser och resor f\xf6r familjer eller par. M\xe5ngsidighet och h\xf6gsta boendekomfort tack vare flera versioner och planl\xf6sningar. En fantastisk husbil p\xe5 alla s\xe4tt som tack vare kontinuerlig forskning f\xf6rb\xe4ttras st\xe4ndigt\ri kvalitet och pris. Innovativ design och smart bol\xf6sning g\xf6r Magis till en unik husbil som \xf6verraskar med sin h\xf6ga komfort och funktionalitet.</p>',
    'Namn': 'Magis',
    'bild1Frilagd': '/dynamic/produktkategorier/Magis.png',
    'highlightIDs': None,
    'broschyr': None,
    'ParentID': '155',
    'active': '1',
    'skaffabild': None,
    'pris': '618000',
    'Fordonstyp': 'Husbilar',
    'ID': '155'
}, {
    'bild1': None,
    'bild2': '',
    'kampanj': None,
    'Slogan': 'F\xf6r kr\xe4sna campingentusiaster',
    'Year': '2016',
    'Brand': 'CI',
    'teknspec': None,
    'Beskrivning': '<p class="em-text">Design i r\xf6relse som g\xf6r att du reser med maximal rymd, s\xe4kerhet och p\xe5litlighet.</p>\n<p>Riviera \xe4r en idealisk husbil i 14 modeller skapad efter konceptet maximalt med plats f\xf6r alla utrymmesbehov. Uts\xf6kt design och senaste teknik ger h\xf6gsta komfort, s\xe4kerhet och p\xe5litlighet. Detta \xe4r det perfekta valet f\xf6r de som redan har erfarenhet av friluftsliv och att semestra med husbil.</p>',
    'Namn': 'Riviera',
    'bild1Frilagd': '/dynamic/produktkategorier/Riviera.png',
    'highlightIDs': None,
    'broschyr': None,
    'ParentID': '162',
    'active': '1',
    'skaffabild': None,
    'pris': '697000',
    'Fordonstyp': 'Husbilar',
    'ID': '162'
}, {
    'bild1': None,
    'bild2': '',
    'kampanj': None,
    'Slogan': 'Stark personlighet och innovation',
    'Year': '2016',
    'Brand': 'CI',
    'teknspec': None,
    'Beskrivning': '<p class="em-text">F\xf6r dedikerade resen\xe4rer vana att kr\xe4va allra b\xe4sta komfort.</p>\n<p>Sinfonia, en harmonisk helhet d\xe4r konceptet av att uppleva husbilen finner prestigefyllda och eleganta l\xf6sningar. Exklusivt utf\xf6rande i s\xe5v\xe4l sittgrupp som sovrum samt prestigefull standardutrustning med avancerad teknik. Serien Sinfonia utm\xe4rker sig med stil och teknik som t.ex bodel med ergonomiskt utformade s\xe4ten, laminatbord med LED-ram, backkamera med sensorer f\xf6r maximal k\xf6rs\xe4kerhet. Sinfonia har en harmonisk helhet av elegans, teknik och utrustning.</p>',
    'Namn': 'Sinfonia',
    'bild1Frilagd': '/dynamic/produktkategorier/Sinfonia.png',
    'highlightIDs': '2,15',
    'broschyr': None,
    'ParentID': '170',
    'active': '1',
    'skaffabild': None,
    'pris': '719000',
    'Fordonstyp': 'Husbilar',
    'ID': '170'
}, {
    'bild1': None,
    'bild2': None,
    'kampanj': None,
    'Slogan': 'Prestigefull och funktionell',
    'Year': '2016',
    'Brand': 'CI',
    'teknspec': None,
    'Beskrivning': '<p class="em-text">Husbilen f\xf6r en semester med stil.</p>\n<p>Mizar \xe4r husbilen med elegans och kvalitet som har anledning att vara stolt. Den har rena linjer, utm\xe4rkt sikt och \xe4r enkel att k\xf6ra. Interi\xf6ren pr\xe4glas av h\xf6gsta komfort och av njutbart leverne. Designen \xe4r elegant och modern och m\xf6ter de mest kr\xe4sna campares krav. Rikligt med f\xf6rvaringsutrymmen g\xf6r Mizar perfekt att semestra med.\nHusbilen finns i 5 modeller, alla superutrustade f\xf6r ultimat komfort f\xf6r familjer eller par. Skapad f\xf6r att semestra med stil, \xe4r Mizar den idealiska l\xf6sningen f\xf6r sp\xe4nnande \xe4ventyr och det fr\xe4msta valet f\xf6r dem som vill ha en husbil d\xe4r den b\xe4sta utrustningen redan ing\xe5r.</p>',
    'Namn': 'Mizar',
    'bild1Frilagd': '/dynamic/produktkategorier/Mizar.png',
    'highlightIDs': '2,15,18',
    'broschyr': None,
    'ParentID': '156',
    'active': '1',
    'skaffabild': None,
    'pris': '799000',
    'Fordonstyp': 'Husbilar',
    'ID': '156'
}]
```
