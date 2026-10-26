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
- `taches/*` : tâches perso saisies dans la page.

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
