# Guide technique — Man Child Ministry

Application pour lire, rechercher et étudier les prédications des conventions, disponible sur **Android** (APK) et **iPhone** (application web installable), avec fonctionnement **hors connexion**.

---

## 1. Vue d'ensemble

```
Dossier des prédications (PDF / Word)
        │  tools\importer.ps1  (script Python extract.py)
        ▼
www\library.json  ── git push ──►  GitHub
                                     │  GitHub Actions (.github\workflows\build.yml)
                                     ├──► APK Android  → Releases (lien de téléchargement permanent)
                                     └──► Version web  → GitHub Pages (iPhone + bibliothèque en ligne)
```

- **Une seule application web** (`www\index.html`) sert pour les deux plateformes.
- **Android** : elle est emballée dans un APK avec Capacitor, compilé par GitHub Actions.
- **iPhone** : elle est publiée sur GitHub Pages. On l'installe depuis Safari, sans App Store ni compte Apple.
- **Mises à jour du contenu** : l'application embarque la bibliothèque. Quand le téléphone a Internet, elle télécharge la version publiée sur GitHub Pages si celle-ci est plus récente. Les nouvelles prédications arrivent **sans réinstaller l'APK**.

### Contenu du dossier

| Élément | Rôle |
|---|---|
| `www\index.html` | L'application : bibliothèque, lecteur, recherche, thèmes, favoris |
| `www\library.json` | La bibliothèque générée par l'import (ne pas modifier à la main) |
| `www\config.js` | Adresse de la bibliothèque en ligne, remplie automatiquement à la compilation |
| `www\sw.js`, `www\manifest.webmanifest` | Fonctionnement hors connexion et installation sur l'iPhone |
| `www\icons\`, `www\fonts\` | Logo, icônes et polices, embarqués pour fonctionner sans Internet |
| `assets\` | Sources de l'icône et de l'écran de démarrage Android |
| `tools\extract.py` | Lecture des PDF et Word, découpage, versets, thèmes |
| `tools\importer.ps1` | Commande Windows qui lance l'import |
| `tools\renommer-fichiers.ps1` | Renommage ponctuel des fichiers existants (novembre 2026) |
| `conventions.xlsx` | Thème de la série de chaque convention, saisi à la main. **Local, non versionné** |
| `FORMAT-DES-DOCUMENTS.md` | Format recommandé et liste des documents à corriger |
| `.github\workflows\build.yml` | Compilation de l'APK et publication de la version web |
| `package.json`, `capacitor.config.json` | Configuration du projet Android (Capacitor) |
| `signature-android.keystore` et fichiers `SECRETS-*` | Clé de signature de l'APK. **Confidentiel, exclu de Git** |

---

## 2. Mise en place initiale (une seule fois)

### 2.1 Prérequis sur le PC

- **Git** et un compte GitHub.
- **Python 3** pour l'import. Les modules `pymupdf` et `python-docx` sont installés automatiquement par `importer.ps1`.

### 2.2 Créer le dépôt GitHub

1. Sur github.com, créer le dépôt **`man-child-ministry`**, en **public** et **sans** README.
   - Le mode public est nécessaire pour GitHub Pages avec un compte gratuit.
2. Dans le dépôt, ouvrir **Settings → Pages**. Sous *Build and deployment*, choisir **GitHub Actions** comme *Source*.
3. Dans **Settings → Secrets and variables → Actions → New repository secret**, créer trois secrets. Leurs valeurs sont dans `SECRETS-A-NE-PAS-PUBLIER.txt` :

| Nom du secret | Valeur |
|---|---|
| `ANDROID_KEYSTORE_PASSWORD` | le mot de passe indiqué dans le fichier |
| `ANDROID_KEY_ALIAS` | `manchild` |
| `ANDROID_KEYSTORE_BASE64` | **tout** le contenu de `signature-android.keystore.base64.txt` |

> Sans ces secrets, l'APK est quand même compilé, mais avec une signature de test qui change à chaque compilation. Les mises à jour ne pourraient alors pas s'installer par-dessus l'ancienne version.

### 2.3 Premier envoi

Le fichier de compilation a été livré dans `tools\build.yml`. La deuxième commande ci-dessous le place dans `.github\workflows\`, où GitHub l'attend. Remplacer `mkonan-bigint` par l'organisation si le dépôt y a été créé.

```
cd "C:\Dev Projects\Man Child Ministry"
New-Item -ItemType Directory -Force .github\workflows | Out-Null
Move-Item tools\build.yml .github\workflows\build.yml
git init -b main
git add .
git commit -m "Man Child Ministry : application de lecture et d'étude des prédications (web + Android)"
git remote add origin https://github.com/mkonan-bigint/man-child-ministry.git
git push -u origin main
```

### 2.4 Vérifier la compilation

Dans l'onglet **Actions** du dépôt, le workflow **« Publier l'application »** lance deux tâches qui durent environ 5 minutes :

- **pages** : publie la version web ;
- **android** : compile l'APK et crée une *Release* `v1.0.<n>`.

Les deux doivent finir en vert. En cas d'échec, ouvrir la tâche en rouge et copier le message d'erreur.

---

## 3. Distribuer l'application

### Android

- Lien de téléchargement permanent, qui pointe toujours vers la dernière version :
  `https://github.com/mkonan-bigint/man-child-ministry/releases/latest/download/ManChildMinistry.apk`
- Le partager par WhatsApp, SMS ou e-mail.
- Sur le téléphone : ouvrir le fichier, puis autoriser « Installer des applications inconnues » pour le navigateur ou WhatsApp quand Android le demande.

### iPhone (et tout navigateur)

- Adresse : `https://mkonan-bigint.github.io/man-child-ministry/`
- L'ouvrir dans **Safari**, toucher **Partager** puis **« Sur l'écran d'accueil »**.
- L'application affiche elle-même ce conseil aux utilisateurs d'iPhone.

---

## 4. Ajouter des prédications

### 4.1 Organisation du dossier source

Dossier source par défaut : `C:\Users\HP\OneDrive - BigInt Analytics\Documents\Man Child Ministry`

```
Man Child Ministry\
├── 2025-12 Abidjan\        ← un sous-dossier par convention (recommandé)
│   ├── 2025 1225M Père, que le feu tombe _ Pst John Conteh.pdf
│   └── ...
└── 2026-04 Lomé\
    └── ...
```

- Nom des sous-dossiers : **`AAAA-MM Ville, Pays`**, par exemple `2025-12 Abidjan, Côte d'Ivoire`. `AAAA-MM Ville` est aussi accepté. La ville et le pays du dossier sont ceux affichés dans l'application.
- **Sous-dossiers : recommandés mais pas obligatoires.** Les fichiers posés à la racine sont regroupés automatiquement par thème de la série, ville et mois, lus dans l'en-tête.
- Formats acceptés : **PDF** (texte, pas de scan) et **Word (.docx)**.

### 4.2 Nom des fichiers

Format conseillé :

```
AAAA MMJJ[M|S] Titre _ Prédicateur.pdf
```

- `AAAA MMJJ` : la date, par exemple `2025 1225` pour le 25 décembre 2025.
- `M` = matin, `S` = soir. Facultatif si le moment figure dans l'en-tête.
- Le **titre affiché** dans l'application est celui du nom de fichier. On corrige un titre en renommant le fichier.

Le script tolère aussi les variantes rencontrées, par exemple :
- `2021 1224 - Titre _ Pasteur John Conteh. prt 1 docx.docx`
- `… _ Part1Pst J. CONTEH.pdf`
- `… _.pdf`

Les mentions « prt 1 », « Part1 » ou « Partie 2 » deviennent « (partie 1) » ou « (partie 2) » dans le titre. Les mentions « docx » ou « CONV » sont retirées.

> Le format recommandé, avec la liste des documents actuels à corriger, est détaillé dans **[FORMAT-DES-DOCUMENTS.md](FORMAT-DES-DOCUMENTS.md)**.

### 4.3 En-tête du document

Le script lit, dans les premières lignes du document :

| Information | Comment elle est trouvée | Si elle est absente |
|---|---|---|
| **Date** | Première date en toutes lettres (« 25 Décembre 2025 ») | Date du nom de fichier |
| **Matin / soir** | Mot « matin » ou « soir » près de la date | Lettre M ou S du nom de fichier, sinon aucun |
| **Prédicateur** | Ligne commençant par « Pasteur », « Pst », « Frère »… | Nom de fichier, sinon « Pasteur John Conteh » |
| **Lieu, ville, pays** | Ligne de la date ou ligne suivante. Le pays est reconnu dans une liste (Côte d'Ivoire, Madagascar, Togo…) et la ville est le mot qui le précède | Pays le plus fréquent de la convention |
| **Thème (série)** | **Pas lu dans le document** : saisi à la main dans `conventions.xlsx` (voir § 4.6) | Convention affichée sans thème |

Formats d'en-tête reconnus, par exemple :

```
ACL Dynastie Éternelle _ Abidjan-Côte d'Ivoire
Tananarive, Madagascar - Jeudi 14 Août 2025 _ Matin
Abidjan – Côte d'Ivoire, 28 Mai 2023 Matin
Le 24 Décembre 2021 / Dabou - Côte D'Ivoire
```

- **Ville de la convention** : si le sous-dossier est nommé `AAAA-MM Ville`, c'est cette ville qui est affichée. Le script signale par « ⚠ » une différence avec les en-têtes, par exemple « Tamatave » pour le dossier et « Tananarive » dans les PDF.
- La ligne « L'ordre de Melchisédech, le secret de l'immortalité dans la plénitude des temps », ainsi que les lignes « broch - N° », « Sujet : » et « Inspiration : », sont **ignorées**.
- Sont retirés automatiquement : les en-têtes et pieds de page répétés, les numéros de page, les numéros de paragraphe d'origine et la page finale « Ce message du Pasteur… ».
- Un fichier illisible (PDF scanné, document vide) est **ignoré** et signalé par « ✖ ». L'import continue avec les autres fichiers.

### 4.4 Lancer l'import

```
powershell -ExecutionPolicy Bypass -File "C:\Dev Projects\Man Child Ministry\tools\importer.ps1"
```

Pour un autre dossier source :

```
powershell -ExecutionPolicy Bypass -File "C:\Dev Projects\Man Child Ministry\tools\importer.ps1" -Source "D:\Prédications"
```

Le script affiche le résultat par convention : ville, pays, dates, thème, puis une ligne par prédication (date, moment, titre, nombre de paragraphes et de versets). Il affiche aussi les alertes « ⚠ » et les fichiers ignorés « ✖ ». **Contrôler ce résumé avant de publier.**

### 4.5 Publier

```
cd "C:\Dev Projects\Man Child Ministry"
git add www/library.json
git commit -m "Ajout des prédications de la convention de Lomé (avril 2026)"
git push
```

Quelques minutes plus tard :

- la version web est à jour ;
- un nouvel APK est publié ;
- les téléphones déjà installés reçoivent les nouvelles prédications à leur prochaine connexion, avec le message « X nouvelles prédications ajoutées ».

---

### 4.6 Thème de la série de chaque convention

Le thème de chaque convention se saisit dans **`conventions.xlsx`**, à la racine du projet :

- onglet **Conventions** : une ligne par sous-dossier, et le thème se tape dans la colonne **« Thème de la série »** (cellules jaunes) ;
- les colonnes Ville, Pays, Dates et Prédications sont remplies automatiquement à chaque import ;
- un nouveau sous-dossier est ajouté automatiquement au fichier lors de l'import. Il suffit ensuite de saisir son thème et de relancer l'import ;
- **fermer le fichier dans Excel avant de lancer l'import** ;
- ne pas renommer l'onglet « Conventions » ni les en-têtes « Dossier » et « Thème de la série ».

Après une modification des thèmes : relancer l'import, puis publier `www/library.json` avec Git.

> `conventions.xlsx` **n'est pas versionné** (exclu par `.gitignore`). C'est un fichier local : en garder une copie de sauvegarde, car sans lui un nouvel import produit une bibliothèque sans thèmes.

## 5. Fonctionnement de l'application

| Fonction | Détail |
|---|---|
| Bibliothèque | Conventions de la plus récente à la plus ancienne, prédications par jour (matin et soir), « Reprendre la lecture » |
| Lecteur | Paragraphes numérotés (§), taille du texte réglable, mode nuit, versets cités |
| Recherche | Ignore accents et majuscules. Plusieurs mots = tous présents. `"expression exacte"` entre guillemets. Filtre par convention |
| Variantes | Melchisédech, Melchisédek et Melchisédeck donnent les mêmes résultats. « Apocalypse 12 » trouve aussi « Apocalypse chapitre 12 » |
| Thèmes | 16 thèmes repérés par mots-clés, avec les passages clés et l'index des livres bibliques cités |
| Favoris et notes | Toucher un paragraphe pour l'ajouter aux favoris, noter ou copier la citation avec sa référence |

> Les favoris et les notes sont enregistrés **sur le téléphone de chaque utilisateur**. Ils ne sont ni partagés ni sauvegardés en ligne.

---

## 6. Personnaliser

Toutes ces modifications se font dans `tools\extract.py`. Il faut ensuite **relancer l'import** puis publier.

- **Thèmes** : liste `THEMES`. Chaque thème a un identifiant, un libellé et des mots-clés écrits sans accents, par exemple `("feu", "Le feu de Dieu", ["feu"])`.
- **Livres bibliques** : liste `BOOKS`, pour ajouter une orthographe à un livre.
- **Variantes de recherche** : liste `VARIANTS`, dans `www\index.html`.
- **Couleurs** : variables `--royal`, `--gold`, `--fire`… en haut de `www\index.html`.
- **Logo** : `www\icons\logo.svg`. Si on le change, il faut aussi régénérer les PNG de `www\icons\` et de `assets\`.

---

## 7. Sécurité et sauvegardes

- **`signature-android.keystore` et son mot de passe** : à sauvegarder **hors du PC**, par exemple dans un coffre de mots de passe ou sur une clé USB. S'ils sont perdus, aucune mise à jour de l'APK ne pourra s'installer : chaque utilisateur devra désinstaller puis réinstaller l'application.
- Ne **jamais** publier ces fichiers sur GitHub. Ils sont exclus par `.gitignore`.
- Le dépôt étant public, tout son contenu, prédications comprises, est consultable par tous. C'est le cas aussi de la version web.

---

## 8. Dépannage

| Problème | Cause probable | Solution |
|---|---|---|
| Un fichier est signalé « ✖ Ignoré » | Document illisible, scanné ou vide | Vérifier le fichier, ou l'envoyer pour adapter le script |
| Alerte « ⚠ » sur la ville | Nom du sous-dossier différent de la ville des en-têtes | Renommer le sous-dossier si la ville des en-têtes est la bonne |
| « Python est introuvable » | Seul le raccourci du Microsoft Store est présent | `importer.ps1` cherche aussi Miniconda et Anaconda. Sinon, installer Python depuis python.org |
| Une prédication a un titre vide ou faux | Nom de fichier hors format (§ 4.2) | Renommer le fichier puis relancer l'import |
| Une recherche ne trouve rien dans un PDF | PDF scanné (image, pas de texte) | Passer le PDF à la reconnaissance de caractères (OCR) ou utiliser la version Word |
| La tâche **pages** échoue | Pages pas configuré | Settings → Pages → Source : **GitHub Actions** |
| La tâche **android** échoue à l'étape « Signature » | Secret incomplet | Recopier **tout** le contenu de `signature-android.keystore.base64.txt` dans `ANDROID_KEYSTORE_BASE64` |
| « Application non installée » sur Android | APK signé avec une autre clé que la version installée | Désinstaller l'ancienne version, puis installer la nouvelle |
| Les nouvelles prédications n'apparaissent pas | Téléphone hors ligne, ou publication pas terminée | Vérifier l'onglet Actions, puis rouvrir l'application avec Internet |
