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

- **Sous-dossiers : recommandés mais pas obligatoires.** Les fichiers posés à la racine sont regroupés automatiquement par thème de la série, ville et mois, lus dans l'en-tête.
- Formats acceptés : **PDF** (texte, pas de scan) et **Word (.docx)**.

### 4.2 Nom des fichiers

```
AAAA MMJJ[M|S] Titre _ Prédicateur.pdf
```

- `AAAA MMJJ` : la date, par exemple `2025 1225` pour le 25 décembre 2025.
- `M` = matin, `S` = soir.
- Le **titre affiché** dans l'application est celui du nom de fichier. On corrige un titre en renommant le fichier.

Exemple : `2025 1225M Père, que le feu tombe _ Pst John Conteh.pdf`

### 4.3 En-tête attendu dans chaque document

Le script lit les informations de la convention dans les premières lignes du document :

```
L'ordre de Melchisédech, le secret de l'immortalité dans la plénitude des temps   ← thème (série)
PÈRE, QUE LE FEU TOMBE                                                            ← titre
Pasteur John Conteh                                                               ← prédicateur (ligne commençant par « Pasteur »)
Jeudi matin, 25 Décembre 2025                                                     ← jour, moment, date
ACL Dynastie Éternelle _ Abidjan-Côte d'Ivoire                                    ← lieu _ Ville-Pays
________________________________________________                                  ← séparateur (facultatif)
```

- Le lieu doit suivre le format **`Lieu _ Ville-Pays`**. La ville et le pays sont séparés par le premier tiret.
- Les en-têtes et pieds de page répétés ainsi que la page finale « Ce message du Pasteur… » sont retirés automatiquement.

### 4.4 Lancer l'import

```
powershell -ExecutionPolicy Bypass -File "C:\Dev Projects\Man Child Ministry\tools\importer.ps1"
```

Pour un autre dossier source :

```
powershell -ExecutionPolicy Bypass -File "C:\Dev Projects\Man Child Ministry\tools\importer.ps1" -Source "D:\Prédications"
```

Le script affiche une ligne par prédication : identifiant, titre, nombre de paragraphes, versets trouvés et principaux thèmes. **Contrôler cette liste avant de publier.**

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
| L'import s'arrête sur un fichier | En-tête différent du format attendu (§ 4.3) | Corriger l'en-tête du document, ou envoyer le fichier pour adapter le script |
| Une prédication a un titre vide ou faux | Nom de fichier hors format (§ 4.2) | Renommer le fichier puis relancer l'import |
| Une recherche ne trouve rien dans un PDF | PDF scanné (image, pas de texte) | Passer le PDF à la reconnaissance de caractères (OCR) ou utiliser la version Word |
| La tâche **pages** échoue | Pages pas configuré | Settings → Pages → Source : **GitHub Actions** |
| La tâche **android** échoue à l'étape « Signature » | Secret incomplet | Recopier **tout** le contenu de `signature-android.keystore.base64.txt` dans `ANDROID_KEYSTORE_BASE64` |
| « Application non installée » sur Android | APK signé avec une autre clé que la version installée | Désinstaller l'ancienne version, puis installer la nouvelle |
| Les nouvelles prédications n'apparaissent pas | Téléphone hors ligne, ou publication pas terminée | Vérifier l'onglet Actions, puis rouvrir l'application avec Internet |
