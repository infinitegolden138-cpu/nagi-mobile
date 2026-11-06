# Nagi Mobile v0.2

Interface personnelle statique hébergée sur GitHub Pages. Aucun serveur payant, aucune API, aucune clé secrète.

## Fonctionnement

- Discussion : recherche des connaissances déjà enseignées (ce n'est **pas** encore un chatbot IA).
- Enseigner : stocke des connaissances dans le stockage local de l'application sur **cet appareil uniquement**.
- Mémoire : export/import au format `nagi.memory.v1` JSON.
- Installation : Safari → Partager → Sur l'écran d'accueil.
- Hors ligne : cache d'application après un premier chargement connecté. Le stockage peut être effacé par iOS ; exporter souvent.

## Important : confidentialité et synchronisation

GitHub Pages est **public** et ne stocke aucune mémoire personnelle. Les conversations restent dans le stockage local du navigateur. Safari et une app ajoutée à l'écran d'accueil peuvent avoir des stockages distincts : évitez de les confondre. Le fichier exporté peut contenir des informations privées ; ne le publiez jamais dans le dépôt public.

La synchronisation automatique et le moteur IA actif quand Shadow est éteint ne sont pas encore développés. Pour le moment, l'import/export JSON est **manuel**.

## Pont Shadow expérimental

`shadow_bridge.py` fonctionne en Python standard, en local. Il fusionne des exports JSON, sans accès réseau ni modification de l'installation existante de Nagi.

Exemple sous Windows :

```powershell
python shadow_bridge.py "C:\\Users\\Shadow\\Downloads\\nagi-memoire-2026-11-06.json"
python shadow_bridge.py --export
```

Les fichiers se trouvent dans `nagi_data/`. Les connecter à la vraie mémoire de Nagi sur Shadow exigera de vérifier le format de son installation existante avant toute modification.
