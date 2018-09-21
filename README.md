Souboj botu

Pravidla:

    - Tahova hra
    - Na vstup botovi prilitne mapa + "barva" jeho hracu, napriklad mapa + \n\n "X".

Mapa

    - ASCII mapa NxM
    ```
		###########
		#   X  X  #
		#   ####  #
		#  #    # #
		#  Y  Y   #
		###########
    ```

	- Pozice na mape se pocitaji od leveho horniho rohu od 0 (stejne jako vetsina pozic v poli)
	- Soucasti mapy: 

    ```
		- # - zed'
		- ' ' - pohybliva plocha
		- ~ - voda (V prvni fazi neni pouzito)
	```

	- Hraci jsou vsechny pismenka mezi A az Z na mape

Hrace:

	- pohyb je dan skluzem az na doraz
	- Mimo mapu "vyletet" nelze
	- Hrace "strili" sebevrazdou do "vsech stran", tzn. nahoru, dolu, doleva, doprava, neco jako bomba v bombermanu
	- Jeden vystrel zabije vsechno na sve ceste
	- Zasah strel je na plnou sirku a vysku mapy
	- Zdi zastavuji strely

Body:

	- Zabiti protihrace +2 body
	- Zabiti sveho spoluhrace -1 bod
	- Jenom tak odpalit hrace = 0 bodu

Tahy:

	- Jeden tah obsahuje vstup (mapa + barva hracu) a botem vypocitany vystup na obrazovku
	Vystup:
		- pozice panacka ve tvaru "X:Y" (pocitano od leveho horniho rohu) + akce 
		- akce muze byt:
			- "vystrel" - "BUM!"
			- "pohyb" - jedno z "UP"/"DOWN"/"LEFT"/"RIGHT"
			- jako "bonus" behem akce muzete napsat vtipnou hasku
			- priklad:
				- 0:4 LEFT Where are you, my precious?
				- 0:4 BUM! Yellow sumbarine
	- Hra ma omezeny pocet tahu - 50

Vyhrava ten hrac, kdo na konci hry ma nejvice bodu.

Cile:

	- napsat bota
    - napsat spoustece botu

Jazyk: Libovolny, jen at' jde spustit normalne z bashe

Spusteni:
    `python3 runner.py maps/map5.txt tepek2 viki1`