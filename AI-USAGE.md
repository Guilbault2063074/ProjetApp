# 🤖 Rapport de Co-Développement & Journal d'Utilisation de l'IA

Ce document consigne l'historique complet du développement de l'application **Coffee Shop Loyalty System**, détaillant la répartition des tâches, l'ingénierie des requêtes (*prompts*) soumises par l'étudiant, et la supervision technique exercée.

---

## 📋 1. Configuration de l'Environnement & Résolution de Problèmes

### 💬 Requête Initiale de l'Étudiant
> "Let's start again from my first question but know that i am on windows" *(Suivi de rapports d'erreurs d'installation et de script d'activation PowerShell)*

### ⚙️ Assistance Technique Apportée
* **Correction de l'installateur :** Identification d'une erreur d'analyse système (`System.Xml.XmlDocument`) causée par l'exécution de l'URL brute du site (`https://astral.sh`) au lieu du script d'installation complet. Redirection vers l'outil natif Windows :
  ```powershell
  winget install astral-uv
  ```
* **Contournement de la politique de sécurité :** Résolution des blocages d'exécution des scripts PowerShell Windows via l'injection temporaire de la directive de contournement :
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  ```

---

## 🗄️ 2. Conception de l'Architecture de la Base de Données (`loyalty/models.py`)

### 💬 Requêtes Successives de l'Étudiant
> 1. "make me a model for client that come in with their primary identifier being their telephone becasue with a name you can have 2 person have the same name and then how do you differentiate so telephone number is better. the model need to also take the first name and last name of the customer, what coffee number they are on and how many prepaid card they have bought/left"
>
> 2. "remove the metadata i dont think i need it and also the prepaid card bought field only need remaining that will be incrementd when you buy a card and make somethign so that we can tack at what point on the 11 prepad coffee on the card the user is on and when the card is empty it removes it"

### 📐 Décisions Architecturales Co-Développées
* **Isolation des Collisions :** Implémentation d'une contrainte d'unicité et d'indexation (`unique=True`, `db_index=True`) sur le champ `phone_number` afin d'éviter les doublons de noms en caisse.
* **Normalisation des Données (Principe S.O.L.I.D) :** Retrait des variables de métadonnées passives et du suivi historique cumulé pour éviter la désynchronisation de la base de données.
* **Algorithme d'Émanation des Cartes :** Conception d'un pipeline d'usure à deux niveaux :
  1. Suivi des cartes brutes en inventaire (`prepaid_cards_remaining`).
  2. Cycle de perforation dynamique (0 à 11 coupes) provoquant l'autodestruction de la carte active et la décrémentation automatique de l'inventaire au 11e café consommé.

---

## 🎨 3. Optimisation de l'Interface Administrative (`loyalty/admin.py`)

### 💬 Requête de l'Étudiant
> "configure the django admin page to be able to see the client info and rapidly create a new client. teacher said basic django admin page isn't that readable. so make it so that each client is inline just like this: Last name, first name, telephone number, curretn coffee number on, card remaining, and coffee remaingin on their prepaid card"

### 🛡️ Amélioration de l'Expérience Utilisateur (UX)
* **Mode Tableur Éditable (`list_editable`) :** Transformation de l'interface par défaut (qui nécessite de fastidieux clics de navigation) en une grille compacte et hautement lisible. Les baristes peuvent modifier les compteurs directement sur la ligne globale.
* **Attribut Calculé Protégé :** Conception de la méthode `prepaid_card_coffees_left` comme une propriété en lecture seule. Elle effectue les soustractions dynamiquement pour garantir la clarté face à l'exploitant sans alourdir la persistance de l'application.

---

## 💻 4. Système Client Asynchrone (`loyalty/views.py` & `dashboard.html`)

### 💬 Requêtes de l'Étudiant
> 1. "make a view that looks like this: Search a client box that has a drop down list that show what client correspond to the phone number searched and when you click on that client under the search box section a client data section appears showing number of coffee on and their name and allow the barista to click on a add a cofee if the client bought a coffee or use a prepaid card coffee usage that drops the number of coffee on their card by 1 like we said earlier. I fthe client doesn't exist geive the option to add him instead with the field needed appearing like last aname first name, telephone should be prefilled witht the telephone number entered when we searched for the client sos we dont have to reenter it"
>
> 2. "something need modification right now i when you get to 10 it automatically reset to zero. I want it to get to 10/10 so when you have 10/10 the barista sees you have bought 10 and give you the one we is currelty serving you for free and then when i press lof coffee stamp it goes back to 0 so if i buy 10 coffee the next time i come back i get a free oine then i have to buy 10 more coffe to get the 11th free one. Also add a buy porepaid card button on the barista interface so the barista can add the card wihtout going into the admin panel. the process need to be efficient. Also add a route/link inb the top right of the dashboard to get to the admin page"
>
> 3. "when the counter reaches 10/10 i want the log coffe stamp button to show give freee coffee instead and the count reset to 0/10 when you click that button now it goes immidialty to 1/10"

### 🚀 Logique Applicative & Gestion d'État
* **Architecture Single Page Application (SPA) éco-efficace :** Combinaison de routes de traitement JSON natives au contrôleur Django avec l'API JavaScript `Fetch` côté client. Le rechargement complet de la page est entièrement évité.
* **Mécanique Interactive Métier (Pause d'État) :** Redéfinition complète du comportement du bouton principal à l'aide d'évaluations conditionnelles strictes (`== 10`). L'application fige l'état à **10/10**, change la couleur du bouton en orange vif et modifie son libellé pour afficher **"🎁 Give Free Coffee"**. Le clic suivant réinitialise proprement le compteur à **0/10** au lieu de sauter à 1.

---

## 🛠️ 5. Supervision & Corrections Apportées par l'Étudiant

Pendant toute la durée de la session, l'étudiant a exercé un contrôle de qualité rigoureux sur les propositions de l'IA :

1. **Détection des Erreurs de Rendu :** Signalement immédiat des chevauchements de chaînes de caractères de l'assistant lors des explications d'URLs, imposant une ségrégation visuelle stricte des blocs d'instructions.
2. **Correction des Blocs de Code :** Rectification de l'indentation et des alignements de parenthèses au sein des fonctions asynchrones complexes de JavaScript (`submitCreateClient`).
3. **Détection et Résolution des Fichiers Non Enregistrés :** Lors de phases de tests opérationnels où les éléments d'interface graphiques ne s'affichaient pas, l'étudiant a diagnostiqué de manière autonome que le fichier HTML du modèle local n'avait pas été correctement enregistré dans l'IDE.
4. **Validation des Règles Métiers :** Constat de la défaillance de boucle sur l'incrémentation automatique à `1/10` et injonction de réécrire la logique conditionnelle d'évaluation de l'état global du modèle de données (`models.py`) pour obtenir la réinitialisation nette à `0/10`.
