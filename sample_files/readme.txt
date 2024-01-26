# Next Version:
Error-handling ved "Upload før valg af fil"
Udskrift I semikolons i output, istedet for "komma"
 - Fixed: Tilføjede   sep=';'
Kun muligt at vælge CSV filer.
Tilføj guide. Eller link til guide
Problemer med UTF csv eller ngoet. Æ Ø Å kommer ikke med i CSV.
- Avilius saldobalance tilsendt 16/09 laver 3 poster dobbelt.
- Når Excel åbner csv, kommer der et decimal på. Det er et punktum, så der bliver ikke afrundet af Excel. Excel har komme som decimal-seperator til beløbne, som kommer i det format fra kunden. Begge bliver vist behandlet af python som en String. Altså, kontoen skal importeres som et heltal. I SQL databasen er det et heltal. Nu i excel bruger jeg VENSTRE(E2;4), så den skralder ".0" fra.

# Version 2
Tilføj 2nd database for (EMV and ApS split)
UI til dette også.
Create Login

