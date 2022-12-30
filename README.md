## User Guide

Afin de déployer notre dashboard sur une autre machine, il vous suffit d'aller dans votre editeur [Visual Studio Code text editor](/tools/vscode) et d'ouvrir le projet. Une fois celui-ci lancé, rendez vous sur le fichier [DashTest.py] et l'exécuter. Pour finir rendez vous sur votre page ([Google]) et lancer le lien suivant : [http://127.0.0.1:8050/home].
Cela vous permettra d'acceder à la page d'accueil de notre dashboard.

## Rapport d'analyse

Après les données extraites du site [STARTGG] nous avons remarqué une très forte densité de tournoi vers les grandes villes. De plus nous avons remarqué les différents Winrate des joueurs sur chaque tournoi et avons pu analyser leurs performances et elur avancement.

## Developper Guide

Notre projet est séparé en plusieurs parties : la partie avec les fichiers [Python] qui gère les différentes fonctions, et la partie [CSS] qui met en page c'est différentes fonctions, input et output.

Il y a une partie [Python] pour chaque page : Home, Tournament et GetTournaments. 
[Home] est la page d'accueil. 
[Tournament] est la page qui permet grâce à l'ID du tournoi d'avoir plusieurs informations sur celui-ci.
[GetTournaments] est la page qui permet à l'utilisateur selon les différents critères qu'il va choir de trouver un ou des tournois et leurs informations.

Pour la partie [CSS], celle ci premet la mise en page des différents input et output de chaque page.