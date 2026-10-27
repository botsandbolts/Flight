"""Shared teaching examples: all money and probabilities are scenario inputs."""
from math import sqrt

STEPS = [
 ('00 · Worum geht es?', 'Ein guter Einkauf soll auch ein gutes Geschäft sein.'),
 ('01 · Das passende Produkt finden', 'Anna kennt ihren Wunsch, aber keine Artikelnummer.'),
 ('02 · Sinnvoll weiterempfehlen', 'Nach der Kaffeemaschine braucht Anna vielleicht eine Mühle.'),
 ('03 · Prüfen, was übrig bleibt', 'Eine Bestellung bringt Umsatz. Kosten gehen davon ab.'),
 ('04 · Einen Rabatt begründen', 'Der Gutschein lohnt sich nur, wenn er genug zusätzliche Wirkung hat.'),
 ('05 · Das Unternehmen abstimmen', 'Ein gutes Angebot braucht verfügbaren Bestand und ehrliche Auskunft.'),
 ('06 · Die Wirkung messen', 'Ein besseres Ergebnis kann Zufall sein. Eine Gegenprobe hilft.'),
 ('07 · Was Flight tatsächlich zeigt', 'Beispiele, trainierbare Modelle und offene Nachweise klar auseinanderhalten.'),
]

LABS = [
 ('pages/1_Trainingslabor.py','Empfehlungen trainieren'),
 ('pages/2_Suchstudio.py','Text- und Bildsuche ausprobieren'),
 ('pages/3_Marketinglabor.py','Werbewirkung untersuchen'),
 ('pages/4_Suche_und_Oekonometrie.py','Suchqualität und Kampagnen prüfen'),
 ('pages/7_Agenten_Kommandozentrale.py','Einen Arbeitsauftrag durchspielen'),
 ('pages/8_Wissen_und_Content.py','Wissen finden und Texte vorbereiten'),
 ('pages/9_KI_Business_Case.py','Kosten und Nutzen einer KI-Lösung rechnen'),
 ('pages/6_KI_im_Unternehmen.py','Weitere Anwendungen im Unternehmen'),
 ('pages/5_Praesentation.py','Folien und Projektnachweise ansehen'),
]

def contribution(price=100.,goods=50.,handling=6.,returns_cost=8.,advertising=12.,discount=0.):
 return price-discount-goods-handling-returns_cost-advertising

def incremental_contribution(p0,p1,coupon,margin=40.,contact=.2):
 # Discount applies to ALL treated purchases, including those occurring anyway.
 return (p1-p0)*margin-p1*coupon-contact

def teaching_experiment(n=1000):
 control=round(n*.025);variant=round(n*.029)
 p0=control/n;p1=variant/n;difference=p1-p0
 se=sqrt(p0*(1-p0)/n+p1*(1-p1)/n)
 return {'n':n,'control':control,'variant':variant,'difference_pp':100*difference,
         'low_pp':100*(difference-1.96*se),'high_pp':100*(difference+1.96*se)}
