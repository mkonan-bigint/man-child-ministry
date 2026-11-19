# Man Child Ministry

> Mise en place, ajout de prédications, publication et dépannage : voir le **[Guide technique](GUIDE-TECHNIQUE.md)**.

Application pour lire, rechercher et étudier les prédications des conventions.

- **Android** : APK téléchargeable depuis la dernière *Release* du dépôt (`ManChildMinistry.apk`).
- **iPhone** (et tout navigateur) : version web installable publiée sur GitHub Pages. Dans Safari : Partager → « Sur l'écran d'accueil ».
- **Hors connexion** : toute la bibliothèque est enregistrée sur le téléphone. Quand il y a Internet, l'application télécharge automatiquement les nouvelles prédications, sans réinstallation.

## Ajouter des prédications

1. Dans le dossier source, créer un sous-dossier par convention, par exemple `2025-12 Abidjan` ou `2026-04 Lomé`, et y déposer les PDF ou Word.
2. Nommer chaque fichier : `AAAA MMJJ[M|S] Titre _ Prédicateur.pdf` (M = matin, S = soir), par exemple `2025 1225M Père, que le feu tombe _ Pst John Conteh.pdf`.
3. Lancer l'import :

   ```
   powershell -ExecutionPolicy Bypass -File "tools\importer.ps1"
   ```

4. Publier avec Git (add, commit, push). GitHub recompile l'APK et met à jour la version web en quelques minutes.

Le script lit dans l'en-tête de chaque document : série (thème de la convention), titre, prédicateur, jour et date, lieu (« Lieu _ Ville-Pays »).

## Structure

| Dossier | Contenu |
|---|---|
| `www/` | L'application (HTML/JS), la bibliothèque `library.json`, les icônes et les polices |
| `tools/` | Script d'import (`extract.py`) et commande Windows (`importer.ps1`) |
| `assets/` | Sources des icônes et de l'écran de démarrage Android |
| `.github/workflows/` | Compilation de l'APK et publication de la version web |
