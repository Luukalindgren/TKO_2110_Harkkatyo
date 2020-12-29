import pygame, sys, json    ## Kirjastot jotka sisältää pelien ohjelmointiin hyödyllisiä metodeja ##
from pygame.locals import * ## -||- ##
# Pelin alkunäyttö
def introduction():
    NÄYTTÖ.fill((255,255,255)) ## Täyttää ikkunan valkoisella värillä ##
    t1 = FONTTI.render("Paina L lataaksesi pelin", 1, (0,0,0))
    t2 = FONTTI.render("Paina U aloittaaksesi uuden pelin",1 , (0,0,0))
    t3 = FONTTI.render("Paina S pelin aikana tallentaaksesi",1,(0,0,0))
    NÄYTTÖ.blit(t1, (20,300))
    NÄYTTÖ.blit(t2, (20,400))
    NÄYTTÖ.blit(t3, (20,500))
# Itse peli
def main():
    with open("vaikeusasteet.json","r") as va:
        global arvo, lataa, alku, grid
        vaikeusasteet = json.load(va)
        NÄYTTÖ.fill((255,255,255))
        grid = vaikeusasteet["TESTI"]
        while True:  ## ITSE PELI ##
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == QUIT: ## Kun painetaan ruksia, niin peli sulkeutuu ##
                    pygame.quit()
                    sys.exit()
                if tapahtuma.type == MOUSEBUTTONDOWN: ## Hiiren klikkaus valitsee paikan mihin halutaan laittaa numero ##
                    sijainti = pygame.mouse.get_pos()
                    otaSijainti(sijainti)
                if tapahtuma.type == KEYDOWN: ## Lukee mikä näppäin on painettu alas ##
                    if tapahtuma.key == K_l:
                        lataa = 1
                    if tapahtuma.key == K_u:
                        lataa = 2
                    if tapahtuma.key == K_s:
                        lataa = 3
                    if tapahtuma.key == K_1:
                        arvo = 1
                    if tapahtuma.key == K_2:
                        arvo = 2
                    if tapahtuma.key == K_3:
                        arvo = 3
                    if tapahtuma.key == K_4:
                        arvo = 4
                    if tapahtuma.key == K_5:
                        arvo = 5
                    if tapahtuma.key == K_6:
                        arvo = 6
                    if tapahtuma.key == K_7:
                        arvo = 7
                    if tapahtuma.key == K_8:
                        arvo = 8
                    if tapahtuma.key == K_9:
                        arvo = 9
            if arvo != 0:
                laitaNumero(arvo) ## Lisää näytölle visuaalisesti valitun numeron ##
                grid[int(x)][int(y)] = arvo ## Lisää sudokuun (kaksiulotteiseen listaan) fyysisesti valitun numeron ##
                arvo = 0
            if lataa !=0:
                if lataa == 1:   ## Lataa json -tiedostosta tallennetun pelin ##
                    alku = 1
                    grid = lataaPeli()
                    NÄYTTÖ.fill((255,255,255))
                    piirräRuudukko()
                    lataa = 0
                if lataa == 2: ## Aloittaa pelin alusta ##
                    alku = 1
                    grid = [
                        [0,0,0,0,0,0,0,8,7],
                        [7,5,9,0,0,0,0,0,0],
                        [0,0,0,0,7,6,1,0,5],
                        [6,4,7,1,0,0,0,0,0],
                        [0,0,0,7,0,0,0,2,8],
                        [2,3,0,4,0,0,0,1,0],
                        [5,6,0,0,3,0,0,0,0],
                        [4,0,2,0,0,7,9,0,0],
                        [0,0,0,0,5,8,6,4,0]
                ]
                    NÄYTTÖ.fill((255,255,255))
                    piirräRuudukko()
                    lataa = 0
                if lataa == 3: ## Tallentaa json -tiedostoon pelin tilan ##
                    alku = 1
                    with open("load_file.json", "w") as f:
                        json.dump(grid, f)
                    print("PELI TALLENNETTU!")
                    lataa = 0
            if alku == 0: ## Pelin käynnistyksessä alkuarvo lataa -muuttujalle on 0 jolloin näytölle tulee introduction()
                introduction()
            tarkistaVoitto() ## Tarkistaa jaktuvasti pelin tilannetta ja lopettaa sen kun peli on voitettu ##
            pygame.display.update() ## Päivittää tehdyt muutokset ##
            KELLO.tick(alkutiedot["FPS"])
# Piirtää viivoja jotka muodostavat Sudokulle tavanomaisen ruudukon 
def piirräRuudukko():
    for i in range (9): 
            for j in range (9): 
                if grid[i][j]!= 0: 
                    pygame.draw.rect(NÄYTTÖ, (0,153,153), (i * alkutiedot["RuutuKoko"], j * alkutiedot["RuutuKoko"], alkutiedot["RuutuKoko"] + 1, alkutiedot["RuutuKoko"] + 1)) ## Värjää sinisellä jo numeroidut ruudut ##
                    text1 = FONTTI.render(str(grid[i][j]), 1, (0, 0, 0))
                    NÄYTTÖ.blit(text1, (i * alkutiedot["RuutuKoko"] + 35, j * alkutiedot["RuutuKoko"] + 30))  ## Täyttää ruudut valmiissa pohjassa olevilla numeroilla ##

    #Piirtää himmeemmät viivat
    for x in range(0, alkutiedot["IkkunaLeveys"], alkutiedot["RuutuKoko"]):     ## Vaakaviivat ##
        pygame.draw.line(NÄYTTÖ, (200,200,200), (x,0), (x,alkutiedot["IkkunaKorkeus"]))
    for y in range(0, alkutiedot["IkkunaKorkeus"], alkutiedot["RuutuKoko"]):    ## Pystyviivat ##
        pygame.draw.line(NÄYTTÖ, (200,200,200), (0,y), (alkutiedot["IkkunaLeveys"],y))
    
    #Piirtää tummemmat viivat
    for x in range(0, alkutiedot["IkkunaLeveys"], alkutiedot["RuudukkoKoko"]):  ## Vaakaviivat ##
        pygame.draw.line(NÄYTTÖ, (0,0,0), (x,0), (x,alkutiedot["IkkunaKorkeus"]))
    for y in range(0, alkutiedot["IkkunaKorkeus"], alkutiedot["RuudukkoKoko"]): ## Pystyviivat ##
        pygame.draw.line(NÄYTTÖ, (0,0,0), (0,y), (alkutiedot["IkkunaLeveys"],y))
# Hiiren klikkauksen sijainnin määritys 
def otaSijainti(pos):
    global x
    x = pos[0]//alkutiedot["RuutuKoko"]  ## x-akseli ##
    global y
    y = pos[1]//alkutiedot["RuutuKoko"]  ## y-akseli ##
# Asettaa numeron valittuun ruutuun 
def laitaNumero(arvo):
    ruutu = Rect(x * alkutiedot["RuutuKoko"]+1, y * alkutiedot["RuutuKoko"]+1,99,99) ## Piirtää yhden ruudun kokoisen valkoisen neliön ##
    pygame.draw.rect(NÄYTTÖ, (255,255,255), ruutu) ## Asettaa sen valkoisen neliön valittuun ruutuun (jos ruutuun on jo kirjoitettu numero niin tämä "poistaa" sen visuaalisesti) ##
    teksti = FONTTI.render(str(arvo), 1, (0,0,0)) ## Asettaa teksti muuttujaan kirjoitettu numero ##
    NÄYTTÖ.blit(teksti,(x * alkutiedot["RuutuKoko"] + 35, y * alkutiedot["RuutuKoko"] + 30)) ## Tulostaa näytölle valittu numero ##
# Lataa json -tiedostosta pelin
def lataaPeli():
    with open("load_file.json","r") as f:
        grid = json.load(f)
        return grid
# Tarkistaa onko peli voitettu
def tarkistaVoitto():
    oikeaRuutu = [1,2,3,4,5,6,7,8,9]
    # Tarkistaa onko sarakkeet oikein
    for i in range(9):
        if sorted(grid[i]) != oikeaRuutu:
            return False
    # Tarkistaa onko rivit oikein
    for i in range(9):
        r = []
        for j in range(9):
            r.append(grid[j][i])
        if sorted(r) != oikeaRuutu:
            return False
    # Tarkistaa onko 3x3 ruudukot oikein
    if tarkistaRuudukot(3,6,9) == True:
        NÄYTTÖ.fill((200,200,200))
        tekijä = FONTTI.render("Credits: Luuka Lindgren,",1, (255,255,255))
        muut = FONTTI.render("Stackoverflow, Geeksforgeeks, etc...",1,(255,255,255))
        voitto = FONTTI.render("Voitit pelin!", 1, (0,0,0))
        NÄYTTÖ.blit(voitto, (alkutiedot["IkkunaKorkeus"] / 3, alkutiedot["IkkunaLeveys"] / 2))
        NÄYTTÖ.blit(tekijä, (5, 770))
        NÄYTTÖ.blit(muut, (5, 830))
    return True
# Osa pelin voiton tarkistusta, tarkistaa 3x3 ruudukot oikeaksi
def tarkistaRuudukot(a, b, c):
    r = []
    oikea = [1,2,3,4,5,6,7,8,9]
    #Vasemmat ruudukot
    for i in range(a):
        for j in range(a):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(a,b):
        for j in range(a):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(b,c):
        for j in range(a):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    #Keskimmäiset ruudukot
    for i in range(a):
        for j in range(a,b):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(a,b):
        for j in range(a,b):
            r.append(grid[i][j]) 
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(b,c):
        for j in range(a,b):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    #Oikeat ruudukot
    for i in range(a):
        for j in range(b,c):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(a,b):
        for j in range(b,c):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    r = []
    for i in range(b,c):
        for j in range(b,c):
            r.append(grid[i][j])
    if sorted(r) != oikea:
        return False
    return True
# OHJELMA ALKAA TÄSTÄ 
with open("alkutiedot.json","r") as asetukset:
    alkutiedot = json.load(asetukset)
    pygame.init() ## Alustaa kaikki tuotavat pygame-moduulit
    pygame.display.set_caption("Sudoku") ## Tämä asettaa ikkunan ylhäällä olevan sovelluksen tekstin ##
    KELLO = pygame.time.Clock()
    NÄYTTÖ = pygame.display.set_mode((alkutiedot["IkkunaLeveys"],alkutiedot["IkkunaKorkeus"])) ## NÄYTTÖ muuttuja alustetaan haluttu sovelluksen    
    FONTTI = pygame.font.Font("freesansbold.ttf", alkutiedot["FONTINKOKO"])
    arvo = 0
    lataa = 0
    alku = 0
    if __name__=='__main__':
        main()


        ##### TÄMÄ ON VALMIS TÄLLÄISENÄÄÄN ######