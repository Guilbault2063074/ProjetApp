# 📐 Document de Conception - Architecture Technique

Ce document détaille les patrons de conception (*design patterns*), les structures de données normalisées et les contraintes métiers implémentées pour l'application de fidélité de café.

---

## 📋 Règles Métiers & Logique de Fidélisation

### 🎯 Boucle de Fidélité Standard (Timbres)
* **Incrémentation :** Le système comptabilise les achats réguliers jusqu'à un maximum strict de **10/10**.
* **Gel d'État :** Dès que le client atteint 10/10, l'interface graphique fige le processus d'achat standard et transforme le bouton de facturation principal en **`🎁 Give Free Coffee`** (Couleur orange distinctive).
* **Réinitialisation :** Un clic sur ce bouton alerte le bariste d'offrir la boisson gratuite et réinitialise proprement le compteur sous-jacent à **0/10** pour relancer un cycle sain.

### 💳 Pipeline des Cartes Prépayées (11 Tasses)
* **Gestion des Cartes :** Le bariste peut vendre une carte prépayée directement depuis le tableau de bord pour incrémenter l'inventaire entier du compte client.
* **Perforation :** L'utilisation d'une boisson prépayée fait avancer un compteur de perforation de **1 à 11**.
* **Fin de cycle automatique :** À la 11e perforation, le cycle de la carte expire instantanément. Le système remet le nombre de perforations actives à 0 et soustrait précisément `1` carte de l'inventaire global du client.

---

## 📐 Choix Architecturaux et Justifications

### 🔍 1. Stratégie d'Identification Unique
L'application utilise le **numéro de téléphone** du client comme clé d'indexation principale unique dans la base de données, écartant la recherche par nom de famille.
* *Justification :* En environnement commercial, les collisions de noms de famille et de prénoms sont fréquentes. L'utilisation du numéro de téléphone garantit une isolation absolue de l'identité lors des requêtes de recherche asynchrones en caisse.

### 🗄️ 2. Normalisation de la Base de Données & Propriétés Calculées
Afin de respecter la troisième forme normale (3NF) et d'éviter les redondances de données, aucun champ de stockage historique passif (tel que `prepaid_cards_bought`) n'est conservé en table.
* *Justification :* Stocker des totaux cumulatifs statiques induit des risques majeurs de désynchronisation lors des mises à jour manuelles. La colonne **"Coffees left on active card"** est calculée dynamiquement au niveau applicatif (`11 minus active card punches`), gardant la structure SQLite saine et légère.

### 🧠 3. Logique Métier Encapsulée ("Fat Models")
Toutes les règles de calcul de points, de perforation et de destruction de jetons de cartes prépayées sont programmées en tant que méthodes internes directement dans la couche modèle (`loyalty/models.py`).
* *Justification :* Aligner les contraintes métiers sur le modèle de données empêche tout contournement. Les règles de validation restent inchangées, que la transaction provienne d'une action Fetch sur le tableau de bord ou d'une modification en grille sur la console d'administration.

### ⚡ 4. Architecture Single-Page App (SPA) Sans Surcharge de Framework
La recherche en temps réel, l'autocomplétion des formulaires et l'enregistrement instantané des profils fonctionnent sans aucun rechargement complet du navigateur.
* *Justification :* Cette fluidité est obtenue en connectant les vues Django à l'API native JavaScript `Fetch` du navigateur. Cette approche évite le déploiement de frameworks lourds (comme React ou Vue) et permet à l'application de démarrer instantanément sur la machine d'évaluation.
