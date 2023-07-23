# Puhehistorian selain

Tämä on alun perin vuonna 2012 Tyler Spiveyn luoman ja James Scholesin toimesta ylläpidetyn Puhehistoria-lisäosan haara. Tähän versioon on lisätty joitakin ominaisuuksia.
Lisäksi näppäinyhdistelmät on päivitetty, sillä alkuperäiset yhdistelmät saattoivat aiheuttaa ristiriitoja muiden sovellusten kanssa, koska ne olivat hyvin yleisesti käytettyjä, esim. F12.

## Ominaisuudet

* Komento viimeksi puhutun tekstin kopioimiseksi leikepöydälle.
* Mahdollisuus tarkastella  500 viimeisintä NVDA:n puhumaa kohdetta.
* Näytä valintaikkuna, joka sisältää uusimmat, senhetkiset NVDA:n puhumat kohteet. Voit tarkastella, valita useita kohteita ja kopioida valitun tai valitut leikepöydälle.

## Käyttö

	* Tarkastele viimeisimpiä NVDA:n puhumia kohteita: NVDA+Vaihto+F11 (edellinen kohde) tai NVDA+Vaihto+F12 (seuraava kohde).
	* Kopioi viimeisin NVDA:n puhuma tai senhetkinen tarkasteltava kohde: NVDA+Ctrl+F12.
	* Näytä valintaikkuna, joka sisältää viimeisimmät senhetkiset NVDA:n puhumat kohteet: NVDA+Alt+F12

### Puhehistorian kohteet

Tämä valintaikkuna sisältää NVDA:n viimeisimmät puhutut kohteet, uusin ensimmäisenä. Voit selata kohteita nuolinäppäimillä ylös ja alas. Kukin kohde näyttää vain 100 merkkiä, mutta voit nähdä koko sisällön painamalla Sarkain-näppäintä, joka siirtää moniriviseen tekstikenttään. Valintaikkunaa ei päivitetä automaattisesti NVDA:n uusilla puhutuilla kohteilla. Jos haluat päivittää luettelon, avaa tämä valintaikkuna uudelleen tai paina "Päivitä historia" -painiketta.

Voit hakea kaikkien kohteiden joukosta hakukenttää käyttäen. Kirjoita muutama kirjain tai sana ja paina Enter. Kohteiden luettelo päivitetään hakusi mukaisesti. Poista haku tyhjentämällä teksti hakukentästä ja painamalla Enter. Haku suoritetaan myös, jos olet hakukentässä ja se menettää kohdistuksen, esim. painamalla Sarkainta tai siirtämällä kohdistuksen toiseen säätimeen muilla tavoin.

Voit kopioida senhetkiset valitut kohteet Kopioi-painiketta käyttäen. Tämä kopioi kaiken tekstin, joka näytetään valitut kohteet sisältävässä kentässä.
Lisäksi voit kopioida kaikki kohteet painamalla "Kopioi kaikki" -painiketta. Tämä kopioi vain senhetkiset luettelossa näkyvät kohteet, jotka erotetaan toisistaan rivinvaihdolla. Jos olet suorittanut haun, tämä painike kopioi vain löydetyt kohteet.

Jos haluat valita useamman kuin yhden kohteen, käytä samoja näppäimiä kuin Windowsissa. Esimerkiksi Vaihto+Nuolinäppäimet ylös ja alas valitaksesi peräkkäisiä kohteita ja Ctrl+samat näppäimet valitaksesi ei-peräkkäisiä kohteita.
Sulje tämä valintaikkuna painamalla Esc-näppäintä tai Sulje-painiketta.


### Bugien korjauksiin ja uusien ominaisuuksien kehittämiseen osallistuminen
  Jos haluat korjata bugin tai lisätä uuden ominaisuuden, haarauta tämä koodivarasto.

  #### Koodivaraston haarauttaminen
  Jos tämä on ensimmäinen osallistumisesi, sinun on ensin "haarautettava" SpeechHistoryExplorer-koodivarasto GitHubissa:

  1. Haarauta tämä koodivarasto GitHub-tilillesi.
  2. Kloonaa haarauttamasi koodivarasto paikalliseksi: "git clone <koodivaraston URL>".
  3. Lisää tämä koodivarasto haarauttamaasi koodivarastoon komentoriviltä:
  "git remote add davidacm https://github.com/davidacm/SpeechHistoryExplorer.git"
  4. Nouda haaramuutokseni:
  "git fetch davidacm"
  5. Vaihda paikalliseen SPE-haaraan: "git checkout SPE"
  6. Määritä paikallinen SPE-haara käyttämään davidacm:n SPE:haaraa ylätasona:
  "git branch -u davidacm/SPE"

#### Vaiheet ennen koodausta
  Sinun on käytettävä erillistä "aihehaaraa" kutakin ongelmaa tai ominaisuutta varten. Kaiken koodin tulisi yleensä perustua virallisen SPE-haaran viimeisimpään sitoumukseen sillä hetkellä, kun aloitat muutosten tekemisen.
  Joten tee seuraavat asiat ennen muutosten tekemistä:

  1. Pidä mielessä "Koodivaraston haarauttaminen" -osion vaiheet.
  2. Vaihda SPE-haaraan: "git checkout SPE".
  3. Päivitä paikallinen SPE-haara: "git pull".
  4. Luo uusi, päivitettyyn SPE-haaraan perustuva haara: "git checkout -b UusiHaara"
  5. Kirjoita koodisi.
  6. Lisää muutoksesi sitoutettavaksi (poista ensin tarpeettomat tiedostot): "git add ."
  7. Luo sitoumus: "git commit" ja kirjoita sitoumusviesti.
  8. Työnnä haara koodivarastoosi: "git push". Jos haaraa ei ole olemassa, Git kertoo, miten sinun tulisi toimia.
  9. Luo vetopyyntö koodivarastooni.

Huom: Päähaara on nimeltään SPE. Tämä johtuu siitä, että tämä on koodivarasto, ja käytän mieluummin SPE-haaraa. Master-haaraa käytetään tärkeiden muutosten integroimiseen alkuperäisestä haarautetusta koodivarastosta.
