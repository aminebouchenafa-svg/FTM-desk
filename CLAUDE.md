# FTM Desk — notes pour Claude

Tableau de bord du Fleet Training Manager B737 NG/MAX (Cpt Bouchenafa).
Page : `ftm-desk.html`, publiée sur https://claude.ai/artifact/CuN5Hm9Jh3zk6uKbjzKkBM
(capacité `db`). Les données vivent dans la base de l'artifact, pas dans la page.
Mettre à jour avec l'outil ArtifactData (toujours lire le doc avant, passer `if_version`).

## Collections
- `opl/<matricule>` : OPL en checks ou en vols d'évaluation (`evalsRestantes`, `exclus` = TRI ayant déjà évalué, `programmes`).
- `ref/tri` {evaluateurs (noms de famille), secteur (tous les TRI), tre} : modifiés depuis la fiche (interrupteurs TRI / TRE / Évaluateur), `ref/licences` (état de validité), `ref/equipes` (safety pilots, candidats TRI).
- `simu/<AAAA-MM>` : planning simu par mois (créneaux S1..S5).
- `vols/<début>_<fin>` : exports TrainerU « Crew Training Schedule ».
- `memos/*` : mémos et rappels {texte, echeance, source (DO, SDF, SDPNT, Chef secteur ligne, Adjoint, Formation, Programmes, Moi), horizon, cat pro|projet, fait}.
- `events/*` : événements {nom, date, objectifs[{id, texte, date, fait}]}.
- `instr/*` : pilotes en instruction ligne {nom, pos, legsInit, vols[{id, date, instr, vols, legs, safety}], preControle, cl{requis 2|4, faits}, lache}.
- `init/*` : initiation (< 150 h après lâcher) {nom, pos, heures, lacheLe}.
- `valid/*` : validités {nom, fonction, items{CL, IC, IL, Check TRI, CRM, DGR, SMS, Sûreté, SSP1, SSP2: date d'expiration AAAA-MM-JJ}}.
- `max/*` : formation MAX {nom, pos, etape, licenceOk, suiviInforme, progInforme}.
- `simulog/*` : changements simu à notifier au CSV Kouba {date, texte, notifie}.
- `ref/linecheck` : état DO du contrôle en ligne {rows[{id, nom, base, ac, pos CP|FO, last, expiry, planned (date = échéance suivante), plannedTxt (P = programmé, ABS = absent, a suivre), note}]} ; fallback du line check sur la fiche et tableau dans Validités.
- `ref/pilotes` : annuaire {rows[{id, nom, mat, fonction CPT|FO, sources}]} ; la fiche pilote relie les modules par matricule, sinon par NOM + 3 lettres du prénom.
- `fiches/<id pilote>` : saisies manuelles de la fiche {dernierSimu, prochainSimu, licence, note, fonction (prioritaire sur l'annuaire), sorti{motif, date}} ; `sorti` = hors secteur (caché des listes, filtre « Sortis »).
- Dans `opl`, `college` {date, resultat Admis|Ajourné, qtDate} après les 5 évals : parcours PL → check local → check nav → évals → collège CDB → QT ATR.
- `ref/regles` (seuils modifiables), `ref/dim` (dimensionnement), `perso/moi` (mon temps).
- Dans `opl`, `groupe` = OPL | CDB | CIBLE ; `total` évals ; programmes statut programmé | fait | raté (+ cause CGML, ABS, IRGAV, AMP, ABSTRI, SOLL).
- Cahier des charges complet : `CAHIER_DES_CHARGES.md`.

## Quand l'utilisateur envoie un export TrainerU (vols d'instruction)
1. `python3 tools/import_trainer_u.py <fichier.xlsx> <sortie.json>` → affiche le doc_id.
2. `set` sur `vols/<doc_id>` avec `file_path`.
3. Pour chaque vol code `v` (Inst contrôle évaluation) d'un OPL présent dans `opl` :
   ajouter un programme `fait`, ajouter le TRI à `exclus`, décrémenter `evalsRestantes`.
   Un même TRI sur plusieurs jours pour le même OPL = une seule éval (règle : un TRI différent par vol).
4. Signaler à l'utilisateur les cas ambigus.

## Quand l'utilisateur envoie un planning simu (Excel)
`python3 tools/import_simu.py <fichier> "<feuille>" <AAAA-MM> <sortie.json>` puis `set` sur `simu/<AAAA-MM>` (lire la version avant ; si le mois a des modifications non notifiées dans `simulog`, demander avant d'écraser).

## Calculateur simu
Dans l'onglet Simu : remplacer un TRI, déplacer une séance, TRI indisponible sur une période. Contraintes dures : créneau libre, pas de personne en double, TRI ≤ 2 séances/jour, stagiaire 1/jour, repos S5→S1, ordre des séances d'une PEQ. Score = charge du TRI, séances voisines, écart de date. `ref/regles.plMode` = "ou" | "et" pour la fin d'instruction PL.

## Fichiers Apple Numbers
`tools/import_simu_numbers.py <fichier.numbers> <sortie.json>` (dans un venv avec `pip install numbers-parser`, lancer avec `python -I`) : lit NOV/DEC/JAN et sort un JSON par mois. Archiver l'ancienne version d'un mois dans la collection `archive` avant de la remplacer.

## Règle métier
Aucun pilote ne fait deux vols d'évaluation avec le même TRI (règle confirmée par le FTM).
Des vols du même TRI sur des jours consécutifs = une seule rotation, donc une seule éval.
Un même TRI sur des jours non consécutifs pour un même OPL = infraction à signaler.

## Interface
Thème violet façon captures du FTM : mode jour (lavande) et mode nuit (indigo étoilé), bouton soleil/lune (localStorage ftm.theme), police Poppins, boutons en dégradé indigo→violet. Fiche pilote avec interrupteurs d'affectation.
Briefing push chaque matin à 06:44 (Alger) : tâche planifiée « Briefing FTM Desk » (lecture seule de la base).

## GitHub Pages
`index.html` = `ftm-desk.html` + squelette HTML, généré par `python3 tools/build_pages.py` (à relancer après chaque modification de `ftm-desk.html`).
Hors claude.ai, la page utilise une base locale (localStorage `ftmdesk.db.v1`) avec export/import JSON (module Règles). Ne jamais mettre de données pilotes dans le dépôt : le site est public.
Adresse : https://aminebouchenafa-svg.github.io/FTM-desk/ (branche claude/ftm-desk-dashboard, dossier racine).
Application installable (PWA) : manifest.webmanifest, sw.js (cache hors connexion, changer CACHE à chaque version), icons/.
