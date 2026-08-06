# Publication et soumission ORAtlas

Le dépôt est préparé pour l’URL publique :

`https://github.com/LaurentHuzard/after-the-crash-oratlas`

## 1. Valider

```bash
python3 scripts/validate_repository.py
```

Le résultat attendu se termine par `VALIDATION PASSED`.

## 2. Publier sur GitHub

Depuis la racine du dossier :

```bash
bash scripts/publish_github.sh
```

Pré-requis : GitHub CLI installé et authentifié avec `gh auth login`.
Le script utilise le dépôt public existant, pousse `main`, puis crée la release `v0.1.0`.

## 3. Vérifier GitHub Pages

Dans GitHub :

1. ouvrir **Settings → Pages** ;
2. choisir **GitHub Actions** comme source si ce n’est pas déjà fait ;
3. vérifier l’action **Validate and deploy MyST review** ;
4. ouvrir `https://laurenthuzard.github.io/after-the-crash-oratlas/`.

La soumission ORAtlas peut fonctionner sans Pages, car le dépôt et les artefacts structurés
constituent la source canonique.

## 4. Soumettre dans ORAtlas

1. ouvrir `https://oratlas-ftpoygqvua-ew.a.run.app/submit` ;
2. se connecter avec GitHub ;
3. coller l’URL du dépôt public ;
4. choisir la release exacte `v0.1.0` plutôt que la branche mouvante ;
5. lancer l’inspection ;
6. vérifier les métadonnées extraites, les 12 claims,
   22 citations, 77 relations et
   77 TRUST ;
7. conserver les mentions **AI-assisted**, **pilot** et **human review pending** ;
8. valider puis soumettre la capture éditoriale.

## 5. Ce qu’il ne faut pas sur-vendre

- ce n’est pas encore une revue systématique exhaustive ;
- aucune recommandation clinique individuelle n’est formulée ;
- les évaluations TRUST sont des propositions d’agent ;
- l’évidence non-methamphetamine reste signalée comme historique ou lacunaire ;
- une acceptation ORAtlas est un archivage éditorial, pas une peer review scientifique.
