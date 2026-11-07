# Laborator FastAPI: citiri de la senzori IoT

In acest laborator am realizat o aplicatie care primeste si pastreaza citiri
de temperatura si umiditate de la senzori. Am simulat trimiterea masuratorilor
prin interfata /docs, unde am putut vedea si raspunsurile serverului.

Fiecare citire contine identificatorul senzorului, un numar de ordine,
momentul masurarii si temperatura. Umiditatea este optionala. Am folosit
Pydantic pentru verificarea datelor primite, astfel incat temperaturile si
umiditatile sa respecte limitele cerute, iar identificatorul senzorului sa
aiba formatul corect.

Am adaugat salvarea citirilor si verificarea duplicatelor. Daca acelasi senzor
trimite din nou o citire cu acelasi numar de ordine, aplicatia o respinge si
afiseaza un mesaj. Citirile salvate pot fi apoi cerute pentru un anumit
dispozitiv, in ordine crescatoare, alegand de la ce numar de ordine sa inceapa
rezultatele si cate sa fie afisate.

Pentru verificare, am trimis doua citiri pentru senzor-1, cu numerele de
ordine 1 si 2. A doua citire nu a inclus umiditatea si a fost acceptata.
Cand am cerut citirile cu numarul de ordine mai mare decat 1, serverul a
returnat doar citirea 2, cu umiditatea null.

Am verificat si situatiile de eroare: o temperatura prea mare, un identificator
incorect, o citire repetata si cererea datelor unui dispozitiv necunoscut.
Toate cele 11 verificari din laborator au avut rezultatele asteptate.
Datele sunt pastrate in memorie si se pierd la repornirea serverului.
