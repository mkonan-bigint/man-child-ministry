# Format des documents de prédication

Ce document décrit **le format recommandé** pour les fichiers de prédication (nom et en-tête), puis liste **les documents actuels qui ne le respectent pas**, avec la correction à faire.

Un document conforme est lu sans aucune approximation par l'import (`tools\importer.ps1`). Un document non conforme est quand même importé, mais certaines informations peuvent manquer (matin ou soir, prédicateur, salle…).

> Le **thème de la série** n'est plus lu dans les documents. Il se saisit à la main, pour chaque convention, dans **`conventions.xlsx`** (à la racine du projet).

---

## 1. Rangement : un sous-dossier par convention

```
Man Child Ministry\
├── 2025-12 Abidjan\
├── 2026-05 Abidjan\
└── 2026-09 Tamatave\
```

- Nom du dossier : **`AAAA-MM Ville`**, avec l'année et le mois du début de la convention.
- **La ville du nom de dossier est celle affichée dans l'application.** Elle doit être identique à celle de l'en-tête des documents.

---

## 2. Nom de fichier

```
AAAA MMJJX Titre de la prédication _ Pst Prénom Nom.pdf
```

| Élément | Règle | Exemple |
|---|---|---|
| `AAAA MMJJ` | Date : année, espace, mois et jour sur 2 chiffres chacun | `2025 1225` |
| `X` | **`M`** = matin, **`S`** = soir, collé à la date. Toujours le renseigner | `2025 1225M` |
| Titre | Titre exact, avec ses accents et sa casse normale (pas tout en majuscules) | `Père, que le feu tombe` |
| Partie | Si le message est en plusieurs parties : `(partie 1)`, `(partie 2)` à la fin du titre | `… la Pierre de Faîte (partie 1)` |
| ` _ ` | Espace, tiret bas, espace avant le prédicateur | ` _ ` |
| Prédicateur | `Pst` suivi du prénom et du nom, en casse normale | `Pst John Conteh` |
| Extension | `.pdf` (PDF texte, **pas un scan**) ou `.docx` | `.pdf` |

À éviter dans le nom de fichier :
- un tiret après la date (`2021 1224 - Titre`) ;
- les mentions `docx`, `CONV`, `prt 1`, `Part1` ;
- un double point final (`Conteh..pdf`) ;
- un prédicateur absent ou tronqué (`_ Pst .pdf`, `_.pdf`).

**Exemples conformes :**

```
2025 1225M Père, que le feu tombe _ Pst John Conteh.pdf
2025 0607S La révélation de Jésus-Christ en tant que Roi Melchisédech, la Pierre de Faîte (partie 1) _ Pst John Conteh.pdf
```

---

## 3. En-tête du document (première page)

```
PÈRE, QUE LE FEU TOMBE
Pasteur John Conteh
Jeudi matin, 25 Décembre 2025
ACL Dynastie Éternelle _ Abidjan-Côte d'Ivoire
________________________________________________________________

(texte de la prédication)
```

| Ligne | Contenu | Règle |
|---|---|---|
| 1 | **Titre** | En MAJUSCULES, sur une ou deux lignes |
| 2 | **Prédicateur** | Commence par « Pasteur » |
| 3 | **Jour, moment, date** | `Jour matin, JJ Mois AAAA` ou `Jour soir, JJ Mois AAAA`, avec le mois en toutes lettres |
| 4 | **Lieu** | `Salle _ Ville-Pays` : la salle, puis espace, tiret bas, espace, puis la ville et le pays reliés par un tiret |
| 5 | **Séparateur** | Une ligne de tirets bas `______` qui marque le début du texte |

Bon à savoir :
- La ligne « *L'ordre de Melchisédech, le secret de l'immortalité dans la plénitude des temps* » en haut des documents **peut rester** : elle est ignorée.
- Les lignes « broch - N° », « Sujet : » et « Inspiration : » sont aussi ignorées. Il vaut mieux les retirer de l'en-tête.
- Ne pas répéter l'en-tête deux fois (fichiers Word).
- La date, le moment et le lieu doivent être sur **deux lignes séparées** (lignes 3 et 4), pas réunis sur une seule.
- Ne rien placer entre le séparateur et le début de la prédication, sauf un chant entre crochets : `[Chant : Majesté]`.

---

## 4. Documents à corriger

État au 19 novembre 2026, **après** le renommage fait par `tools\renommer-fichiers.ps1`. Cocher chaque ligne une fois corrigée, puis relancer l'import.

### 2019-04 Abidjan

**`2019 0421 Michaël la voix de l'archange il est ici maintenant pour la délivrance de chaque nom qui est dans ce livre _ Pst John Conteh.pdf`**

- [ ] **Matin ou soir inconnu** : ajouter `M` ou `S` après la date dans le nom (`2019 0421M …`) et dans l'en-tête.
- [ ] **Pas de ligne « Pasteur »** dans l'en-tête : le nom n'apparaît qu'en pied de page. Ajouter `Pasteur John Conteh` sous le titre.
- [ ] Date et lieu sur une seule ligne (`Le 21 Avril 2019 / Abidjan - Côte D'Ivoire`) : séparer en deux lignes, `Dimanche matin, 21 Avril 2019` puis `Salle _ Abidjan-Côte d'Ivoire`.
- [ ] Pas de salle : la préciser si elle est connue.
- [ ] Lignes « broch - N°4 » et bandeau « Les 7 tonnerres sont les 7 esprits d'Elohim… » en tête de page : à retirer de l'en-tête.
- [ ] Pas de ligne de séparation `______` sous l'en-tête.
- [ ] **À vérifier** : le texte commence par un bloc « La Manifestation des Sept Voix Vécues – Frère Joseph Coleman – Forest Hills Gospel Tabernacle – 26 décembre 2004 ». S'il ne fait pas partie de la prédication, le retirer.

### 2021-12 Dabou

**`2021 1224 La Vertu-Puissance pour le service est ici pour une Naissance et l'Adoption (partie 1) _ Pst John Conteh.docx`**

- [ ] **Matin ou soir inconnu** : ajouter `M` ou `S` dans le nom et dans l'en-tête.
- [ ] Ligne « broch - N°1 » : à retirer.
- [ ] Date et lieu sur une seule ligne (`Le 24 Décembre 2021 / Dabou - Côte D'Ivoire`) : séparer en deux lignes, `Vendredi …, 24 Décembre 2021` puis `Salle _ Dabou-Côte d'Ivoire`.
- [ ] Pas de salle ni de ligne de séparation `______`.
- [ ] **À vérifier** : bloc « Frère Joseph Coleman … 26 décembre 2004 » au début du texte.

**`2021 1225 Né de nouveau de la parole et l'esprit comme parlé par Mal 4 (partie 2) _ Pst John Conteh.docx`**

- [ ] **Matin ou soir inconnu** : ajouter `M` ou `S` dans le nom et dans l'en-tête.
- [ ] **Pas de titre en MAJUSCULES** : l'en-tête contient « Sujet : … – Partie 2 », « Inspiration : » puis le titre en minuscules sur deux lignes. Remplacer par une ligne de titre en majuscules.
- [ ] Ligne « broch - N°2 » : à retirer.
- [ ] Date et lieu sur une seule ligne : séparer comme ci-dessus.
- [ ] Pas de salle ni de ligne de séparation `______`.
- [ ] **À vérifier** : bloc « Frère Joseph Coleman … » au début du texte.
- [ ] **À vérifier** : titre. Le nom de fichier abrège « Malachie 4 » en « Mal 4 ».

### 2023-05 Abidjan

Concerne les trois documents :
- `2023 0527S Reconstruisant l'Epouse par la puissance de l'Esprit _ Pst John Conteh.docx`
- `2023 0528M Qui est ce Melchisédek _ Pst John Conteh.docx`
- `2023 0528S La résurrection est là _ Pst John Conteh.docx`

- [ ] **En-tête répété deux fois** (titre, pasteur, lieu) : n'en garder qu'un.
- [ ] Lieu, date et moment sur une seule ligne (`Abidjan – Côte d'Ivoire, 28 Mai 2023 Matin`) : séparer en deux lignes, `Dimanche matin, 28 Mai 2023` puis `Salle _ Abidjan-Côte d'Ivoire`.
- [ ] Pas de salle ni de ligne de séparation `______`.
- [ ] `Reconstruisant l'Epouse…` : le texte est très peu ponctué. Les paragraphes sont découpés automatiquement tous les 100 mots environ.

### 2025-06 Abidjan

- [ ] `2025 0608M La révélation de Jésus-Christ en tant que Roi Melchisédek, la Pierre de Faîte _ Pst John Conteh.pdf` : **à vérifier**. Le titre est le même que celui du 7 juin au soir, qui est la partie 1. S'il s'agit de la partie 2, ajouter `(partie 2)` au nom du fichier et au titre de l'en-tête.
- [ ] `2025 0607S … (partie 1) _ Pst John Conteh.pdf` : l'en-tête contient « _ PARTIE 1 : » dans le titre et une ligne de sous-titre « (Corps En Morphe/Corps Théophanie) ». C'est toléré. Il est plus propre d'écrire `… LA PIERRE DE FAÎTE (PARTIE 1)` et de placer le sous-titre sous le séparateur.

Les autres documents de ce dossier sont conformes.

### 2025-08 Tananarive

Concerne :
- `2025 0814M …`
- `2025 0814S Guerre dans le ciel …`
- `2025 0815M La dispensation de la plénitude des temps …`
- `2025 0817S Les Fils de Dieu sont de retour …`

- [ ] Lieu, date et moment sur une seule ligne (`Tananarive, Madagascar - Jeudi 14 Août 2025 _ Matin`) : séparer en deux lignes, `Jeudi matin, 14 Août 2025` puis `Salle _ Tananarive-Madagascar`.
- [ ] Pas de salle.

Concerne `2025 0815S Vous devez naître de nouveau pour entrer dans les Ephésiens …` :

- [ ] Ligne de lieu `Tananarive, Madagascar` : la remplacer par `Salle _ Tananarive-Madagascar`.

### 2025-12 Abidjan

Conforme. Deux corrections facultatives, car le titre affiché vient du nom de fichier :

- [ ] `2025 1226S …` : le titre de l'en-tête est « PREDICATION ». Le remplacer par « LA DISPENSATION DE LA PLÉNITUDE DES TEMPS (PARTIE 2) ».
- [ ] `2025 1228S …` : le titre de l'en-tête est « LA VENUE PIERRE DE FAÎTE ». Le corriger en « LA VENUE DE LA PIERRE DE FAÎTE ».

### Pour toutes les conventions

- [ ] Saisir le **thème de la série** de chaque dossier dans `conventions.xlsx`.
