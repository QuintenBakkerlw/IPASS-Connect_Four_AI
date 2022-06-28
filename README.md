# IPASS-Connect_Four_AI

Gemaakt door Quinten Bakker

Inleiding :
  In dit github is een alles te vinden om connect four te spelen tegen een AI.
  Analystics te krijgen over een AI zelf.
  Plots maken van de data van de AI.

 Wat heb je nodig :
  python interperter
  matplotlib
  math
  numpy
  random
  time
  Tkinter
  
Files
  Connect_four_AI
  GUI
  Analystics
  callable_AI
  Json files

Connect_four_AI :
  Dit file bestaat uit alles wat nodig is om de AI te laten werken.
  De belangerijks functies is dit files zijn de evaluate_window, score en MiniMax
  evaluate_window en score functies zorgen ervoor dat de board een totaal score krijgt. Met die informatie 
  kan de functie MiniMax een keuze maken voor welke move het kiezen.
  
GUI : 
  Dit files bestaat uit een aangepast vorm van de Connect_four_Ai die specefiek gemaakt is voor Tkinter.
  Hierin staat alles om een werkende GUI produceren voor connect four.
  
Analystics : 
  Dit file zorgt ervoor dat alle data van de AI wordt opgeslagen en verwerkt wordt naar een diagram.
  Het doet het door alle data op teslaan in verschillende json files. Er bestaan drie json files twee files zijn voor Depth data en 1 is voor Size Data
  Verder zijn er meerder functies die plots kunnen maken.
  
callable_AI :  
  Dit file is een aangepaste Connect_four_AI die gemaakt is voor de Analystics file om aangeroepen te worden.
  
