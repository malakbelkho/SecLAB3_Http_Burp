# LAB 3 – Observation du trafic HTTP(S) Android avec Burp Suite

> Cours : Sécurité des applications mobiles  
> Objectif : observer le trafic HTTP généré depuis un Android Emulator à travers Burp Suite, puis documenter les requêtes capturées dans un contexte de laboratoire autorisé.

---

## 1. Vue d’ensemble

Ce laboratoire met en place un proxy d’observation entre un navigateur Android lancé dans un émulateur et une cible HTTP autorisée.

Le trafic du navigateur Android est redirigé vers Burp Suite afin d’observer les requêtes HTTP, les méthodes utilisées, les en-têtes, les cookies et les paramètres transmis.

Pour rester dans un cadre éthique et reproductible, la cible utilisée est une mini-application HTTP locale développée uniquement pour ce lab.

---

## 2. Objectifs du lab

À la fin de ce lab, les points suivants ont été réalisés :

- Vérifier que le navigateur Android peut envoyer son trafic via Burp Suite.
- Identifier les éléments importants d’une requête HTTP.
- Observer la différence entre une requête GET et une requête POST.
- Comprendre le rôle d’un proxy dans le chemin réseau.
- Comprendre le principe d’un certificat CA pour l’analyse HTTPS en laboratoire.
- Produire des preuves exploitables avec contexte, captures et observations.
- Nettoyer l’environnement après les tests.

---

## 3. Périmètre et règles de sécurité

Le test a été réalisé uniquement dans un environnement contrôlé.

| Élément | Choix effectué |
|---|---|
| Cible | Mini serveur HTTP local autorisé |
| Appareil | Android Emulator |
| Données sensibles | Aucune |
| Comptes personnels | Aucun |
| Modification de requête | Non réalisée |
| Certificat CA | Non installé définitivement |
| Nettoyage final | Réalisé |

Ce lab ne vise pas à contourner la sécurité d’une application réelle.  
L’objectif est uniquement pédagogique : comprendre comment observer et documenter un trafic HTTP dans un environnement de test.

---

## 4. Architecture du lab

```text
Android Emulator
      |
      | Trafic HTTP du navigateur
      v
Burp Suite Proxy
10.0.2.2:8080
      |
      | Requête transmise vers la cible autorisée
      v
Mini serveur HTTP local
192.168.43.182:8000
```

Dans ce lab :

- Burp Suite écoute sur le port `8080`.
- L’émulateur Android utilise le proxy `10.0.2.2:8080`.
- La cible locale est accessible via `192.168.43.182:8000`.
- Le serveur HTTP local est lancé avec Python.

---

## 5. Environnement utilisé

| Composant | Valeur |
|---|---|
| Machine hôte | Windows |
| Outil proxy | Burp Suite Community Edition |
| Version observée | Burp Suite Community Edition v2026.4 |
| Émulateur | Android Emulator |
| Réseau Android | AndroidWifi |
| Proxy Android | Manuel puis forcé via ADB |
| Proxy Burp côté hôte | `127.0.0.1:8080` |
| Proxy depuis Android | `10.0.2.2:8080` |
| Cible locale | `http://192.168.43.182:8000` |
| Script cible | `target/demo_server.py` |

---

## 6. Préparation de la cible locale

Une mini-cible HTTP a été préparée avec Python afin de disposer d’un serveur autorisé et reproductible.

Le serveur expose :

- une page principale ;
- un formulaire GET ;
- un formulaire POST ;
- des cookies de démonstration ;
- des réponses HTTP simples.

Le serveur a été lancé avec la commande suivante :

```powershell
cd C:\Users\Microsoft\Documents\LAB3_Burp_Android
python .\target\demo_server.py
```

Preuve du lancement du serveur :

![Lancement du serveur local](screenshots/lancement_serveur_minicible_http.png)

Le serveur a bien reçu plusieurs requêtes depuis l’émulateur, notamment :

```text
GET / HTTP/1.1
GET /search?q=android-burp-lab&device=emulator HTTP/1.1
POST /feedback HTTP/1.1
```

Cela confirme que la cible locale était opérationnelle pendant le test.

---

## 7. Configuration de Burp Suite

Burp Suite a été lancé avec un projet temporaire de laboratoire.

L’interception a d’abord été désactivée afin de commencer par une observation passive du trafic.

![Lancement de Burp Suite](screenshots/Burp_launch.png)

Le Proxy Listener de Burp a ensuite été vérifié.

![Proxy Listener Burp](screenshots/burp_proxy_listener.png)

Configuration observée :

| Paramètre | Valeur |
|---|---|
| Listener | Activé |
| Interface | `127.0.0.1:8080` |
| Port | `8080` |
| Certificat | Per-host |
| Intercept initial | Off |

Cette étape confirme que Burp est prêt à recevoir le trafic envoyé par un client configuré avec ce proxy.

---

## 8. Configuration du proxy Android

Dans l’émulateur Android, le proxy Wi-Fi a été configuré en mode manuel.

![Configuration proxy Android](screenshots/Android_proxy_manual.png)

Configuration appliquée :

| Paramètre Android | Valeur |
|---|---|
| Réseau | AndroidWifi |
| Proxy | Manual |
| Proxy hostname | `10.0.2.2` |
| Proxy port | `8080` |
| IP settings | DHCP |

Une première validation a été réalisée avec l’adresse :

```text
http://burp
```

![Page Burp depuis Android](screenshots/http_burp.png)

Cette page confirme que le navigateur Android pouvait atteindre l’interface proxy de Burp.

Pendant les tests, le trafic ne passait plus toujours par Burp après certaines manipulations.  
Le proxy a donc été forcé proprement via ADB avec la commande suivante :

```powershell
adb -s emulator-5554 shell settings put global http_proxy 10.0.2.2:8080
adb -s emulator-5554 shell settings get global http_proxy
```

Résultat obtenu :

```text
10.0.2.2:8080
```

Cela a permis de stabiliser la capture du trafic dans Burp Suite.

---

## 9. Validation de la capture HTTP

La cible locale a été ouverte depuis le navigateur Android :

```text
http://192.168.43.182:8000
```

![Accès à la cible depuis Android](screenshots/http_hostip.png)

Burp a ensuite affiché les requêtes dans l’onglet `HTTP history`.

![Historique HTTP dans Burp](screenshots/GET_burp.png)

On observe notamment des requêtes vers :

```text
http://192.168.43.182:8000
```

avec un code de réponse :

```text
200 OK
```

Cela valide la chaîne suivante :

```text
Android Emulator → Burp Proxy → Mini serveur local
```

---

## 10. Analyse d’une requête GET

Le bouton `Envoyer GET` de la page locale a été utilisé pour générer une requête GET.

Côté navigateur Android :

![Résultat GET côté Android](screenshots/GET.png)

La requête générée est de la forme :

```http
GET /search?q=android-burp-lab&device=emulator HTTP/1.1
```

Dans Burp, la requête est visible dans l’historique HTTP :

![GET dans HTTP History](screenshots/GET_burp.png)

Vue Raw de la requête GET :

![GET Raw](screenshots/GET_raw.png)

Analyse :

| Élément | Observation |
|---|---|
| Méthode | GET |
| Chemin | `/search` |
| Paramètre 1 | `q=android-burp-lab` |
| Paramètre 2 | `device=emulator` |
| Hôte | `192.168.43.182:8000` |
| Cookie | `lab_session=demo_cookie_123` |

Les paramètres GET sont visibles directement dans l’URL.  
Cela montre que les données envoyées en GET apparaissent dans le chemin de la requête HTTP.

Burp Inspector permet aussi de lire les paramètres et les en-têtes de manière structurée.

![GET Inspector](screenshots/GET_inspector_more.png)

Observation importante :

> Le mode Inspector facilite l’analyse en séparant les paramètres de requête, les cookies et les headers. Cela rend la lecture plus claire qu’une analyse uniquement en Raw.

---

## 11. Analyse d’une requête POST

Le bouton `Envoyer POST` a ensuite été utilisé pour générer une requête POST.

Côté navigateur Android :

![Résultat POST côté Android](screenshots/POST.png)

La page confirme que le serveur a bien reçu le corps de la requête :

```text
note=trace-demo&student_context=lab-mobile-security
```

Dans Burp, la requête POST est visible dans l’historique HTTP :

![POST dans HTTP History](screenshots/POST_burp.png)

Vue Raw de la requête POST :

![POST Raw](screenshots/POST_raw.png)

Analyse :

| Élément | Observation |
|---|---|
| Méthode | POST |
| Chemin | `/feedback` |
| Type de contenu | `application/x-www-form-urlencoded` |
| Corps | `note=trace-demo&student_context=lab-mobile-security` |
| Code de réponse | `200 OK` |

Contrairement à GET, les données POST ne sont pas directement placées dans l’URL.  
Elles sont transmises dans le corps de la requête HTTP.

Les vues Inspector permettent également d’observer les données POST de manière structurée.

![POST Inspector 1](screenshots/POST_Inspector1.png)

![POST Inspector 2](screenshots/POST_Inspector2.png)

Observation importante :

> La requête POST est plus adaptée pour transporter des données de formulaire, mais cela ne signifie pas automatiquement que les données sont protégées. En HTTP simple, Burp peut toujours lire le contenu transmis.

---

## 12. Interception contrôlée

Après l’analyse passive, l’interception a été activée brièvement.

![Intercept On](screenshots/Intercept_on.png)

Une nouvelle requête a été déclenchée depuis Android :

```text
http://192.168.43.182:8000/?intercept_demo=222
```

Côté Android, la navigation attendait une réponse, car Burp retenait la requête.

![Nouvelle requête côté Android](screenshots/new-request_intercept_on.png)

Dans Burp, la requête est apparue dans l’onglet `Intercept`.

![Requête interceptée dans Burp](screenshots/Burp_new-request_intercept_on.png)

La requête interceptée contient notamment :

```http
GET /?intercept_demo=222 HTTP/1.1
Host: 192.168.43.182:8000
User-Agent: Mozilla/5.0 ...
Cookie: lab_session=demo_cookie_123; post_trace=observed_by_burp
```

Cette étape montre que Burp peut agir comme un point de passage actif, capable de mettre temporairement une requête en attente.

La requête a ensuite été transmise avec `Forward`.

![Forward de la requête](screenshots/forward_newrequest.png)

Après la démonstration, l’interception a été désactivée.

![Intercept Off après Forward](screenshots/intercept_off_after_forwarding.png)

Aucune modification de requête n’a été effectuée.  
L’interception a uniquement servi à démontrer le rôle actif du proxy.

---

## 13. HTTPS et certificat CA

HTTPS protège les échanges grâce au chiffrement TLS et à la vérification de l’identité du serveur.  
Lorsqu’un proxy comme Burp Suite est utilisé pour analyser du trafic HTTPS dans un laboratoire, un certificat CA de Burp peut être nécessaire.

Dans Burp, l’écran d’export du certificat CA a été identifié.

![Certificat CA Burp](screenshots/Burp_CA-certificate.png)

Burp propose notamment l’export du certificat :

- Certificate in DER format ;
- Private key in DER format ;
- Certificate and private key in PKCS#12 keystore.

Côté Android, l’écran `Encryption & credentials` permet de gérer les certificats de confiance et les identifiants.

![Écran certificats Android](screenshots/Install_certificate.png)

Dans ce lab, le certificat CA n’a pas été installé définitivement.  
L’objectif était de comprendre le principe suivant :

```text
Pour observer du trafic HTTPS en laboratoire, l’émulateur doit faire confiance au certificat CA de Burp.
```

Point de vigilance :

> Installer un certificat CA de laboratoire augmente la capacité d’observation du trafic. Cette action doit donc rester limitée à un émulateur de test et être annulée à la fin de la séance.

---

## 14. Nettoyage de fin de séance

À la fin du lab, le proxy forcé via ADB a été supprimé.

Commande utilisée :

```powershell
adb -s emulator-5554 shell settings put global http_proxy :0
adb -s emulator-5554 shell settings get global http_proxy
```

Résultat obtenu :

```text
:0
```

Preuve :

![Nettoyage proxy ADB](screenshots/nettoyage_emulator_pshell.png)

Ensuite, le proxy Wi-Fi Android a été remis à `None`.

![Proxy Android remis à None](screenshots/nettoyage_proxy_none.png)

Ce nettoyage garantit que les prochaines navigations de l’émulateur ne passeront plus par Burp Suite.

---

## 15. Bilan du lab

| Checkpoint | Statut |
|---|---|
| Burp Suite lancé | Validé |
| Proxy listener actif | Validé |
| Cible locale Python lancée | Validé |
| Proxy Android configuré | Validé |
| Proxy forcé via ADB | Validé |
| Capture HTTP dans Burp | Validé |
| Requête GET observée | Validé |
| Paramètres GET identifiés | Validé |
| Requête POST observée | Validé |
| Body POST identifié | Validé |
| Cookies observés | Validé |
| Interception contrôlée réalisée | Validé |
| Certificat CA identifié | Validé |
| Proxy supprimé en fin de séance | Validé |

---

## 16. Difficulté rencontrée et correction

Pendant le lab, une difficulté a été rencontrée : le serveur local recevait bien les requêtes, mais Burp ne les affichait plus dans `HTTP history`.

Le diagnostic a montré que le navigateur Android ne passait plus correctement par le proxy Burp.  
La solution appliquée a été de forcer le proxy global Android via ADB :

```powershell
adb -s emulator-5554 shell settings put global http_proxy 10.0.2.2:8080
```

Après cette correction, Burp a bien capturé les requêtes GET et POST vers la cible locale.

Cette phase de dépannage a permis de mieux comprendre la différence entre :

- accéder directement à la cible locale ;
- faire passer le trafic par Burp Suite ;
- vérifier une capture réelle dans `HTTP history`.

---

## 17. Conclusion

Ce lab a permis de comprendre concrètement comment Burp Suite s’insère entre un navigateur Android et une cible autorisée.

La capture passive dans `HTTP history` a montré les méthodes HTTP, les URLs, les en-têtes, les cookies et les paramètres transmis.

L’analyse de GET et POST a permis de distinguer les paramètres visibles dans l’URL et ceux envoyés dans le corps de la requête.

L’interception contrôlée a montré que Burp peut temporairement retenir une requête avant de la transmettre au serveur.

La partie HTTPS a permis de comprendre le rôle d’un certificat CA dans un environnement d’analyse TLS.

Enfin, le nettoyage du proxy Android et du proxy forcé via ADB a permis de remettre l’émulateur dans un état sain.

---

## 18. Structure du projet

```text
LAB3_Burp_Android/
│
├── README.md
│
├── screenshots/
│   ├── Android_proxy_manual.png
│   ├── Android_WiFi.png
│   ├── Burp_CA-certificate.png
│   ├── Burp_launch.png
│   ├── Burp_new-request_intercept_on.png
│   ├── burp_proxy_listener.png
│   ├── forward_newrequest.png
│   ├── GET.png
│   ├── GET_burp.png
│   ├── GET_inspector_more.png
│   ├── GET_raw.png
│   ├── host_ip-addr.png
│   ├── http_burp.png
│   ├── http_hostip.png
│   ├── Install_certificate.png
│   ├── intercept_off_after_forwarding.png
│   ├── Intercept_on.png
│   ├── lancement_serveur_minicible_http.png
│   ├── nettoyage_emulator_pshell.png
│   ├── nettoyage_proxy_none.png
│   ├── new-request_intercept_on.png
│   ├── POST.png
│   ├── POST_burp.png
│   ├── POST_Inspector1.png
│   ├── POST_Inspector2.png
│   └── POST_raw.png
│
└── target/
    └── demo_server.py
```
