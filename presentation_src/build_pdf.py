"""Rebuild the German technical/business PDF from project modules and evidence."""
from pathlib import Path
import sys,json,io
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("FlightSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("FlightSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("FlightSans",normal="FlightSans",bold="FlightSansBold",italic="FlightSans",boldItalic="FlightSansBold")
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from flightlab.advanced import TOPICS,plot_data
W,H=960,540
OUT=ROOT/'assets/FLIGHT_Amit_Steinberg_Oktober_2026.pdf'
INK='#13283F';TEAL='#176F65';BG='#F7F4ED'
C=canvas.Canvas(str(OUT),pagesize=(W,H));C.setTitle('FLIGHT - E-Commerce, Business und Data Science - Amit Steinberg');C.setAuthor('Amit Steinberg, Hamburg')
page=0;manifest=[]
style=ParagraphStyle('body',fontName='FlightSans',fontSize=14,leading=21,textColor=HexColor(INK))
def para(t,x,y,w,size=14,color=INK):
 st=ParagraphStyle('p',parent=style,fontSize=size,leading=size*1.42,textColor=HexColor(color));p=Paragraph(t,st);_,h=p.wrap(w,H);p.drawOn(C,x,y-h);return y-h-16

def start(title,kicker='FLIGHT / E-COMMERCE & DATA SCIENCE'):
 global page
 page+=1;manifest.append(title);C.setFillColor(HexColor(BG));C.rect(0,0,W,H,fill=1,stroke=0)
 para(kicker,42,510,870,10,TEAL);para(title,42,478,876,29)
 C.setStrokeColor(HexColor('#CBD8D2'));C.line(42,42,918,42)
 para('Amit Steinberg · Hamburg · Oktober 2026',42,30,650,9)
 para(f'{page:02}',885,30,33,9)
def end():C.showPage()
def blocks(items,x=42,y=393,w=420):
 for title,body in items:y=para('<b>'+title+'</b><br/>'+body,x,y,w)
 return y
def table(headers,rows,x=42,y=390,widths=None,size=12):
 widths=widths or [876/len(headers)]*len(headers)
 sty=ParagraphStyle('cell',parent=style,fontSize=size,leading=size*1.35)
 values=[[Paragraph(str(v),sty) for v in row] for row in [headers]+rows]
 t=Table(values,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#DDEBE3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#CBD8D2'))]));_,h=t.wrap(876,400)
 if h>y-55:raise ValueError('Table overflow')
 t.drawOn(C,x,y-h)
def image_plot(idx,x=510,y=130,w=400,h=260):
 d=plot_data(idx,10 if idx==4 else 180 if idx==5 else 1.);fig,ax=plt.subplots(figsize=(6.6,4.2));fig.patch.set_facecolor(BG);ax.set_facecolor(BG)
 if idx==0:
  ax.barh(['Besuche','Warenkorb','Kauf','Behalten'],[10000,2000,500,425],color=TEAL);ax.set_xlabel('Synthetische Ereignismengen');ax.invert_yaxis()
 elif idx in [1,2,3]:
  im=ax.imshow(d['matrix'],aspect='auto',cmap='YlGnBu',**({'extent':(0,30,20,0)} if idx==3 else {}));fig.colorbar(im,ax=ax)
  if idx in [1,2]:ax.set_xticks(range(len(d['labels'])),d['labels'],rotation=40,ha='right');ax.set_yticks(range(len(d['labels'])),d['labels'])
  else:ax.set_xlabel('Rabatt: 0 bis 30 Euro');ax.set_ylabel('Retourenreserve: 0 bis 20 Euro')
 elif idx==4:
  im=ax.scatter(d['p0'],d['tau'],c=d['db'],cmap='RdYlGn',s=10);fig.colorbar(im,ax=ax,label='Zusatz-DB (Euro)');ax.set_xlabel('p ohne Angebot');ax.set_ylabel('Bekannter künstlicher Uplift')
 elif idx==5:ax.hist(d['demand'],bins=35,color=TEAL);ax.axvline(180,color='#B84C40');ax.set_xlabel('Simulierter Bedarf in sieben Tagen');ax.set_ylabel('Simulationen')
 elif idx==6:ax.errorbar(d.n,d.difference_pp,yerr=[d.difference_pp-d.low_pp,d.high_pp-d.difference_pp],fmt='o-',color=TEAL);ax.axhline(0,color='gray');ax.set_xscale('log');ax.set_xlabel('Personen je Gruppe');ax.set_ylabel('Effekt und Intervall (Prozentpunkte)')
 else:ax.barh(['Datenquellen','Empfehlungsverfahren','Story-Kapitel'],[6,6,8],color=TEAL);ax.set_xlabel('Implementierter Projektumfang, kein Qualitätsscore')
 fig.tight_layout();buffer=io.BytesIO();fig.savefig(buffer,format='png',dpi=150);plt.close(fig);buffer.seek(0);C.drawImage(ImageReader(buffer),x,y,w,h)

start('FLIGHT', 'PORTFOLIO / OKTOBER 2026')
para('E-Commerce verstehen.<br/>Entscheidungen rechnen.<br/>KI gezielt einsetzen.',42,410,560,34)
para('<b>Amit Steinberg</b><br/>Hamburg<br/>Oktober 2026',42,227,500,22)
C.drawImage(str(ROOT/'assets/amit_steinberg.jpg'),665,96,210,263,preserveAspectRatio=True,anchor='c')
para('Business und Data Science anhand einer Online-Kundenreise. Ausführbare Methoden, interaktive Visualisierungen und dokumentierte Grenzen.',42,115,570,14)
end()
start('Die Leitfrage: Welcher nächste Schritt schafft Wert?')
blocks([('Der Kontext','Anna kauft von zu Hause in einem Onlineshop. Sie sucht eine kompakte Kaffeemaschine und möchte höchstens 150 Euro ausgeben.'),('Die geschäftliche Verbindung','Gute Treffer und Empfehlungen reichen allein nicht. Beitrag, zusätzliche Marketingwirkung, Retouren, Bestand und Service bestimmen den wirtschaftlichen Wert.'),('Der technische Anspruch','Das Portfolio trennt nachvollziehbare Simulationen, trainierbare Modelle und echte Messprotokolle. Eine beeindruckende Architektur braucht prüfbare Aussagen.')],w=860)
end()
start('Architektur: Signale, Modelle und Entscheidungen')
blocks([('Datenschicht','Artikelkontakte, Sitzungen, Katalogattribute und Behandlungskontrollen bleiben nach Quelle getrennt.'),('Modellebene','Retrieval und Empfehlungen liefern Kandidaten. Kostenrechnung und Constraints übersetzen sie in Entscheidungen.'),('Ausführung und Rückkopplung','Ein fester Workflow bereitet einen Vorschlag vor. Das Team prüft die Entscheidung und misst die Wirkung.')]);image_plot(0)
para('Die Grafik zeigt ein synthetisches Funnelbeispiel. Sie ist kein gemessener Umsatz- oder Kausalnachweis.',510,112,400,11);end()

cases=[
 ('Ein Onlineshop als System','Finden, Empfehlen, Rechnen, Rabatt entscheiden, Abstimmen und Prüfen sind sechs verbundene Entscheidungen.','Funnelbrüche werden nicht automatisch durch mehr Werbebudget behoben. Eine gemeinsame Kennzahlenschicht verhindert widersprüchliche Definitionen.'),
 ('Anna formuliert ihren Suchwunsch','Suchbegriffe, Bild und Produktattribute liefern unterschiedliche Evidenz. Budget und Verfügbarkeit begrenzen die Kandidaten.','Ein Treffer darf sprachlich ähnlich sein und trotzdem fachlich falsch. Deshalb harte Filter, Relevanzlabels und Fehleranalyse gemeinsam betrachten.'),
 ('Die nächste Produktempfehlung','Eine alternative Maschine hilft beim Vergleichen. Eine Mühle ergänzt den Einkauf. Die Reihenfolge der Artikelkontakte kann kurzfristige Kaufabsicht zeigen.','Ein komplexes Modell muss gegen Popularität, Übergänge und ItemKNN gewinnen. Wiederholte Käufe und kalte Zielartikel beeinflussen den Vergleich.'),
 ('Was von einer Bestellung übrig bleibt','Bei einer separaten 100-Euro-Beispielbestellung gehen 50 Euro Ware, 6 Euro Abwicklung, 8 Euro Retourenreserve und 12 Euro Werbung ab. Es bleiben 24 Euro.','Ein Rabatt von 10 Euro senkt diesen Beitrag auf 14 Euro. Das beweist noch nicht, ob zusätzliche Verkäufe den Rabatt rechtfertigen. Fixkosten fehlen.'),
 ('Wen sollte Marketing kontaktieren?','Fall A: Kaufchance 60 auf 62 Prozent. Fall B: 10 auf 25 Prozent. Bei 40 Euro Beitrag, 10 Euro Gutschein und 0,20 Euro Kontaktkosten ergeben sich -5,60 und +3,30 Euro Zusatzbeitrag.','Der Gutschein wird bei allen behandelten Käufen bezahlt, auch wenn sie ohnehin stattgefunden hätten. Ein Propensity-Ranking allein berücksichtigt diesen Mitnahmeeffekt nicht.'),
 ('Das Onlineversprechen braucht bestätigte Fakten','180 Stück Lagerbestand treffen auf 40 Stück angenommenen Tagesbedarf und sieben Tage Lieferzeit. Es entsteht eine rechnerische Lücke von 100 Stück.','Das Modell kann einen Bestandsbedarf berechnen. Einen individuellen Zustelltag darf das Sprachmodell daraus nicht erfinden. Einkauf und Service bestätigen die operativen Fakten.'),
 ('Eine bessere Zahl ist noch kein Erfolg','25 statt 29 Käufe bei jeweils 1.000 Personen ergeben 0,4 Prozentpunkte Unterschied. Das approximative Intervall umfasst auch null.','Eine größere Stichprobe verringert im Lehrbeispiel die Unsicherheit. Reale Tests benötigen Randomisierung, eine relevante Zielmetrik und einen vorab definierten Auswertungsplan.'),
 ('Was der Projektstand tatsächlich belegt','Klassische Modelle und kompakte neuronale Modelle sind implementiert. Die lokale Testsuite prüft Datenadapter, Rechenwege, Modellpfade und Oberfläche.','Ein kleiner Amazon-Präfixtest erzielte noch keinen Top-10-Treffer auf den warmen Testfällen. Ein Criteo-Präfix ohne Kontrollgruppe wurde abgewiesen. Beides bleibt dokumentiert.')
]
for i,t in enumerate(TOPICS):
 start(f'{i+1:02} / Business: {cases[i][0]}')
 blocks([('Die Situation',cases[i][1]),('Die Managemententscheidung',cases[i][2]),('Warum dieser Bereich zählt',t['business'])],w=860)
 para('Kaffeepause: '+t['joke'],42,112,870,13,TEAL);end()
 start(f'{i+1:02} / Technik: {t["title"]}')
 blocks([('Methode',t['tech']),('Interpretation der Grafik',t['limit'])],w=420);image_plot(i)
 para('Abbildungen aus reproduzierbaren Python-Berechnungen. Toy- und Szenariodaten sind keine trainierten Modellbeweise.',510,112,400,10);end()
 start(f'{i+1:02} / Evidenz und nächster Versuch')
 blocks([('So messen wir Qualität',t['metric']),('Der nächste fachliche Versuch',t['experiment']),('Aussagegrenze',t['limit'])],w=860)
 para('Ziel: Eine andere Fachperson kann Daten, Rechenweg und Schlussfolgerung getrennt prüfen.',42,105,870,13,TEAL);end()

start('BERT4Rec und SASRec: zwei Trainingsfragen')
table(['Aspekt','BERT4Rec-artig','SASRec-artig'],[
 ['Aufgabe','Maskierten Artikel rekonstruieren','Nächsten Artikel aus Vergangenheit vorhersagen'],['Informationsfluss','Bidirektionale Attention im Trainingsfenster','Kausale Attention mit Dreiecksmaske'],['Flight-Implementierung','Kompakter Transformer; Einzelmaskenrekonstruktion','Kompakter Transformer; nächste Artikel'],['Gemeinsame Prüfung','Trainingsvokabular und unveränderte Testfälle','Vollkatalog-Ranking und kalte Ziele separat']
 ],widths=[170,353,353]);para('Die oben gezeigte Attention stammt aus expliziten Toy-Q/K-Vektoren. Sie erklärt Softmax und Maskierung, nicht die intern gelernte Begründung eines echten Modells.',42,130,870,14);end()
start('LightGCN: Beziehungen nutzen, Vergleiche fair halten')
blocks([('Repräsentation','Nutzer und Artikel bilden zwei Knotentypen. Interaktionen sind Kanten. Die normalisierte Nachbarschaft verbreitet Embeddings über mehrere Schichten.'),('Lernziel','BPR bevorzugt einen beobachteten gegenüber einem negativen Artikel. Im Projekt entstehen negative Artikel ausschließlich aus dem Trainingskatalog.'),('Flight und Grenzen','Die Implementierung mittelt propagierte Schichten. Zur Sessioninferenz werden historische Itemvektoren gemittelt. Das ist ein kompakter Versuchsaufbau, keine paper-exakte Reproduktion oder Produktionsskalierung.')],w=860);end()
start('Hybrides Retrieval und Reranking')
table(['Stufe','Konkrete Aufgabe','Qualitätsprüfung'],[['Kandidaten','Lexikalische, semantische und kollaborative Treffer sammeln','Recall vor Reranking'],['Filter','Preis, Bestand, Markt und Artikelregeln prüfen','Verletzungen harter Regeln'],['Rangfolge','Relevanz und wirtschaftliche Ziele kombinieren','NDCG, Kalibrierung, Vielfalt'],['Entscheidung','Kosten, Budget und Kontaktregeln berücksichtigen','Inkrementeller Beitrag'],['Messung','Onlinewirkung gegen Kontrollbedingung prüfen','Effekt mit Unsicherheit']],widths=[150,440,286]);end()
start('AI Agents: Arbeitsteilung statt Allzweckversprechen')
table(['Rolle','Daten/Werkzeug','Prüfbarer Beitrag'],[['Finanzen','Kostenfunktion','Definierter DB, keine erfundene Marge'],['Einkauf','Bestandsfunktion','Meldebestand mit sichtbaren Annahmen'],['Service','Handbuch-Retrieval','Quellen für einen Antwortentwurf'],['Sprachmodell','Optional OpenAI-/Anthropic-API','Text aus bereitgestellten Fakten'],['Team','Fachliche Freigabe','Operative Entscheidung und spätere Messung']],widths=[150,330,396]);para('Aktuell läuft ein fester lokaler Workflow. Autonome Toolauswahl, ERP-Buchungen und ein Multi-Agent-Produktionsbetrieb sind nicht implementiert.',42,108,870,13);end()
start('ChatGPT, Claude und die Auswahl eines Modells')
blocks([('Aufgaben statt pauschaler Rangliste','Beide Modellfamilien können für belegte Textentwürfe in Betracht kommen. Flight hat OpenAI- und Anthropic-API-Adapter; die Chatprodukte sind separate Zugänge.'),('Evaluationsset','Identische Fälle: richtige Zahl, korrekte Quelle, keine erfundene Lieferauskunft, brauchbarer Text. Dazu Latenz und Gesamtkosten erfassen.'),('Projektstatus','API-Adapter benötigen eigene serverseitige Schlüssel und wurden ohne Schlüssel nicht live getestet. Gemini, lokale LLM-Server und autonome Orchestrierung sind beschriebene Optionen.')],w=860);end()
start('Erklärbarkeit und Fehlersuche')
blocks([('Ein Modellbeitrag ist keine Ursache','SHAP oder ähnliche Verfahren können eine Vorhersage zerlegen. Eine Änderung eines Features muss im realen Geschäft nicht dieselbe Wirkung auslösen.'),('Was im Projekt sichtbar ist','Rangfolgen, Eingabegeschichte, Attention-Lehrrechnung, Vektorähnlichkeit, Kostenflächen und vollständige Protokolle helfen beim Nachvollziehen. Ein produktiver SHAP-Explainer ist hier nicht implementiert.'),('Fachliche Diagnose','Kalte Artikel, kurze Sessions, Retouren, Gruppenunterschiede und falsch verstandene Suchanfragen separat untersuchen. Aggregierte Scores können diese Fehler verdecken.')],w=860);end()
start('Ein KI-Pilot braucht eine Vollkostenrechnung')
blocks([('Kapazität','10.000 Vorgänge, 60 Prozent Nutzung und netto drei gesparte Minuten ergeben 300 Stunden pro Monat. Bei 45 Euro Stundenkosten entsprechen sie 13.500 Euro Kapazitätswert.'),('Realisierter Nutzen','Wenn 40 Prozent wirtschaftlich realisiert werden, bleiben 5.400 Euro vor API- und Betreuungskosten. Zeitgewinn allein ist keine Budgeteinsparung.'),('Kosten und Entscheidung','Tokenpreise sind im Rechner Eingabeannahmen, keine aktuellen Anbieterpreise. Betrieb, Prüfung und Implementierung müssen einbezogen werden. Der Pilot prüft Qualität und Nettoeffekt gemeinsam.')],w=860);end()
start('Die öffentlichen Quellen erfüllen getrennte Aufgaben')
table(['Quelle','Aufgabe','Wichtige Grenze'],[['Retailrocket','Artikelkontakte und Transaktionen','Keine echten Shopmargen'],['REES46','Verhalten in weiteren Kategorien','Zugang und Lizenz prüfen'],['Amazon-M2','Nächster Artikel in einer Session','Eigenes Holdout-Protokoll'],['Amazon Reviews 2023','Reviews und Produktmetadaten','Reviews sind keine Klickhistorie'],['Amazon ESCI','Query-Produkt-Relevanz','Separates Suchranking'],['Criteo Uplift','Werbung vs. keine Werbung','Nichtuniform subsampelt; CC-BY-NC-SA-4.0']],widths=[210,320,346],size=11);end()
start('Reproduzierbarkeit und Betriebsreife')
blocks([('Ausführbare Bausteine','Streamlit-Story, technische Vertiefung in allen acht Kapiteln, Trainings-/Such-/Marketing-/Ökonometrie-Labore und KI-Business-Case. CPU-freundliche Einstiege und optionale neuronale Abhängigkeiten.'),('Messprotokolle','Zeitlicher 80/20-Split für Ereignisdaten, Trainingsvokabular, Vollkatalog-Auswertung, separat gezählte kalte Ziele. M2 nutzt einen eigenen Session-Holdout ohne globale Zeitgarantie.'),('Nächste belastbare Stufe','Repräsentative Daten, zusätzliche Validierung, größere Tests, Inferenzbudget und begrenztes Onlineexperiment. Kein kommerzieller Effekt wird aus Funktionstests abgeleitet.')],w=860);end()
start('Was dieses Portfolio im Gespräch zeigen soll')
blocks([('Business-Verständnis','Ziele, Kosten und Verantwortlichkeiten vor der Modellwahl definieren. Den zusätzlichen Beitrag statt nur Klicks oder Umsatz betrachten.'),('Data-Science-Verständnis','Repräsentationen und Lernziele unterscheiden, faire Kandidatenräume nutzen, Leakage vermeiden und Unsicherheit quantifizieren.'),('Umsetzung und Kommunikation','Trainierbaren Code, verständliche Online-Kundenreise, technische Grafiken und reproduzierbare Nachweise verbinden. Grenzen offen erklären statt fehlende Resultate zu dekorieren.')],w=860)
para('<b>Amit Steinberg · Hamburg · Oktober 2026</b>',42,100,870,19,TEAL);end()
start('Quellen und technische Lektüre')
urls=[
 'github.com/botsandbolts/Flight',
 'arxiv.org/abs/1904.06690 (BERT4Rec)',
 'arxiv.org/abs/1808.09781 (SASRec)',
 'arxiv.org/abs/2002.02126 (LightGCN)',
 'sbert.net (Sentence Transformers)',
 'arxiv.org/abs/2103.00020 (CLIP)',
 'huggingface.co/datasets/criteo/criteo-uplift',
 'github.com/amazon-science/esci-data',
 'amazon-reviews-2023.github.io',
 'developers.openai.com/api/docs/guides/tools',
 'platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works',
]
y=400
for u in urls:y=para(u,42,y,870,12)
end();C.save()
(ROOT/'docs/pdf_manifest.json').write_text(json.dumps({'title':'FLIGHT - Business und Data Science','author':'Amit Steinberg','location':'Hamburg','date':'Oktober 2026','pages':manifest},ensure_ascii=False,indent=2))
print(str(OUT));print('Pages:',page)
