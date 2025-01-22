# Balloon

U ovom zadatku potrebno je implementirati igricu u kojoj igrač kontrolira balon na vrući zrak. Cilj igre je ostvariti što veću visinu s balonom. Balon ima početnu količinu goriva koja se s vremenom smanjuje. Balon mora izbjegavati ptice i oblake. Balon također može pokupiti _power-upove_ poput štita i dodatnog goriva

## Statički funkcionalni zahtjevi

Sljedeći zahtjevi moraju biti ispunjeni za maksimalan broj bodova.

1. Pritiskom na tipke `a` i `d` balon se mora pomicati horizontalno
2. Balon se mora konstantno podizati dok god ima goriva
3. U trenutku kolizije balona sa oblakom ili pticom igra mora završiti
4. U trenutku nestanka goriva igra mora završiti
5. Oblaci i ptice se cijelo vrijeme pomiču horizontalno, a u trenutku sudara s rubovima prozora mijenjaju horizontalan smjer
6. Oblaci i ptice se ne kreću vertikalno, a izlaskom iz prozora se brišu iz memorije
7. Cijelo vrijeme se mora prikazivati i osvježavati trenutačno postignuta visina kao i najviša postignuta visina od svih pokušaja
8. Balon može pokupiti barem dva različita _power-upa_
9. Štit _power-up_ određeno vrijeme omogućava koliziju balona s preprekama bez kraja igre
10. Gorivo _power-up_ povećava količinu goriva u balonu

## Dinamički funkcionalni zahtjevi

Uz obavezne statičke zahtjeve, potrebno je ispuniti i generalne dinamičke zahtjeve. Morate osmisliti takvu arhitekturu koja će omogućiti lako održavanje i nadogradnju igre. Sljedeće stavke moraju biti ispunjene za maksimalne bodove.

1. Promjena postavki igre (brzina balona, brzina prepreka ...) na jednom mjestu
2. Dodavanje novih vrsta prepreka i mogućnost upravljanja preprekama kao flotom i jednostavno računanje kolizija
3. Mogućnost dodavanja novih vrsta _power-upova_
4. Jednostavna mogućnost promjene postojećih prepreka
5. Jednostavna promjena načina stvaranja objekata u igri (više/manje prepreka, više/manje _power-upova_)

Neki oblikovni obrasci će biti neophodni, dok bez nekih drugih možete. Ovdje nisu svi dinamički zahtjevi navedeni, zato što je njih teško definirati u statičkom kontekstu. Razmišljajte prilikom oblikovanja da vaše rješenje prati SOLID principe (to u pravilu, omogućavaju obrasci) i shodno tome oblikujte vaše rješenje. Ne postoji samo jedan ispravan način, ali očekuje se da možete jasno argumentirati vaš pristup. Fokus ovog kolegija nije na slijepoj primjeni obrazaca, već na razvoju inženjerskog načina razmišljanja.

## Savjeti

Nije potrebno ulagati previše vremena za dizajn vaše igre te možete koristit već gotove slike za objekte unutar igre. Postoji više takvih kolekcija, a jedna od popularnijih je [ova](https://itch.io/game-assets/free/tag-pixel-art). Preporučam korištenje pikseliziranih slika.

Poželjno je da brzina balona i ostalih elemenata ne ovisi o brzini iscrtavnja (_frame rate_) već o proteklom vremenu, kako bi se igra slično ponašala na računalima različitih performansi.
