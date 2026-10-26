# FTM Desk — notes pour Claude

Tableau de bord du Fleet Training Manager B737 NG/MAX (Cpt Bouchenafa).
Page : `ftm-desk.html`, publiée sur https://claude.ai/artifact/CuN5Hm9Jh3zk6uKbjzKkBM
(capacité `db`). Les données vivent dans la base de l'artifact, pas dans la page.
Mettre à jour avec l'outil ArtifactData (toujours lire le doc avant, passer `if_version`).

## Collections
- `opl/<matricule>` : OPL en checks ou en vols d'évaluation (`evalsRestantes`, `exclus` = TRI ayant déjà évalué, `programmes`).
- `ref/tri` (TRI évaluateurs), `ref/licences` (état de validité), `ref/equipes` (safety pilots, candidats TRI).
- `simu/<AAAA-MM>` : planning simu par mois (créneaux S1..S5).
- `vols/<début>_<fin>` : exports TrainerU « Crew Training Schedule ».
- `memos/*` : mémos et rappels {texte, echeance, source (DO, SDF, SDPNT, Chef secteur ligne, Adjoint, Formation, Programmes, Moi), horizon, cat pro|projet, fait}.
- `events/*` : événements {nom, date, objectifs[{id, texte, date, fait}]}.
- `instr/*` : pilotes en instruction ligne {nom, pos, legsInit, vols[{id, date, instr, vols, legs, safety}], preControle, cl{requis 2|4, faits}, lache}.
- `init/*` : initiation (< 150 h après lâcher) {nom, pos, heures, lacheLe}.
- `valid/*` : validités {nom, fonction, items{CL, IC, IL, Check TRI, CRM, DGR, SMS, Sûreté, SSP1, SSP2: date d'expiration AAAA-MM-JJ}}.
- `max/*` : formation MAX {nom, pos, etape, licenceOk, suiviInforme, progInforme}.
- `simulog/*` : changements simu à notifier au CSV Kouba {date, texte, notifie}.
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

## Règle métier
Aucun pilote ne fait deux vols d'évaluation avec le même TRI (règle confirmée par le FTM).
Des vols du même TRI sur des jours consécutifs = une seule rotation, donc une seule éval.
Un même TRI sur des jours non consécutifs pour un même OPL = infraction à signaler.
