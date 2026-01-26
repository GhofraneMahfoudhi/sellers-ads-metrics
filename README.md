# 📊 Sellers Ads Metrics - Intelligence Marketing Meta Ads

## 📌 Contexte
Converty est une startup tunisienne spécialisée dans la création de sites e-commerce. Son modèle économique dépend directement des performances commerciales de ses clients. Ce projet vise à fournir une **visibilité stratégique** sur l’activité publicitaire Facebook des clients, en identifiant ceux qui utilisent des plateformes concurrentes et en permettant une intervention proactive.

## 🎯 Vue d'ensemble

Système d'analyse automatisé pour monitorer et classifier les publicités Meta (Facebook) de **21,764 clients e-commerce**. Le projet identifie les clients actifs, analyse leurs stratégies publicitaires et détecte la concurrence via un pipeline en deux phases + dashboard interactif.

---
## 🎯 Objectifs
- Identifier automatiquement les pages Facebook associées aux clients e-commerce
- Collecter et analyser leurs publicités actives sur Meta Ads
- Classifier les publicités selon leur provenance (Converty / Concurrent / Inconnu)
- Générer des rapports analytiques et un dashboard interactif pour la prise de décision

## ✨ Fonctionnalités principales
Le système repose sur une **architecture bi-phasée** :

### 📍 Phase 1 : Discovery & Mapping
- **Scraping automatisé** via Apify Meta Ad Library Actor
- **Classification activité** : Actifs (avec publicités) vs Inactifs (sans publicités)
- **Tracking des coûts** en temps réel (budget $5 Apify freemium puis passage au plan premium de 39$/mois)
- **Résultat** : 4343 clients traités (20%)

### 🎯 Phase 2 : Classification Intelligence
- **Analyse sémantique** des URLs de destination des publicités
- **Classification multi-catégories** :
  - ✅ **Converty Ads** : Publicités pointant vers domaines Converty
  - 🎯 **Concurrent Ads** : Publicités pointant vers concurrents identifiés
  - ❓ **Unknown Ads** : Publicités non classifiées
- **Détection concurrence** : Identification automatique des plateformes concurrentes
- **Métriques calculées** : Ratios Converty vs Concurrent par client

### 📊 Dashboard Streamlit
Interface interactive avec 5 sections analytiques :

1. **📈 Vue d'ensemble** : KPIs clés (clients traités, taux d'activité, volume publicités)
2. **⏱️ Analyse temporelle** : Évolution quotidienne et cumulative du traitement
3. **🏆 Analyse concurrentielle** : Top concurrents, distribution des plateformes
4. **🔍 Détails clients** : Table interactive avec recherche et filtres
5. **⚠️ Alertes & Recommandations** : Insights automatiques

---

## 🚀 Démarrage Rapide

## 🚀 Installation et exécution

### 1. Cloner le dépôt
```bash
git clone <repository-url>
cd sellers_ads_metrics

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv venv
# Windows :
venv\Scripts\activate
# Linux/Mac :
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Configuration

```bash
# .env
APIFY_API_TOKEN=your_token_here
MONGODB_URI=votre_uri_mongodb
```
**Phase 1 : Discovery**
```bash
python phase1_main.py
```
**Phase 2 : Classification**
```bash
python phase2_main.py
```

**Dashboard Interactif**
```bash
streamlit run dashboard.py
```

---

## 🏗️ Architecture

```
sellers-ads-metrics/
├── phase1_main.py              # Pipeline Phase 1 (Discovery)
├── phase2_main.py              # Pipeline Phase 2 (Classification)
├── dashboard.py                # Dashboard Streamlit interactif
│
├── config/
│   └── settings.py             # Configuration centralisée
│
├── src/
│   ├── discovery/              # Phase 1: Scraping & Mapping
│   │   ├── apify_client.py
│   │   ├── mapper.py
│   │   └── cost_tracker.py
│   ├── classification/         # Phase 2: Analyse & Classification
│   │   ├── analyzer.py
│   │   └── detector.py
│   ├── analytics/              # Dashboard: Métriques & Visualisations
│   │   ├── data_loader.py
│   │   ├── metrics_calculator.py
│   │   └── charts.py
│   ├── database/               # MongoDB Integration
│   │   └── mongodb_client.py
│   └── utils/                  # Utilitaires partagés
│       └── logger.py
│
├── scripts/
│   ├── check_mongodb.py
│   ├── view_costs.py
│   └── report_inactive_clients.py
│
└── data/
    └── cache/
```

---

## 📊 Résultats Clés

### 🔍 Phase 1 - Discovery (718 clients analysés avec un budget de 5$ freemium)

| Métrique | Valeur | Détail |
|----------|--------|--------|
| **Clients totaux** | 21,764 | Base MongoDB `stores` |
| **Clients traités** | 718 | 3.3% (limité budget Apify $5) |
| **Clients actifs** | 40 | 5.6% ont des publicités |
| **Clients inactifs** | 678 | 94.4% sans publicités |
| **Publicités totales** | 1,317 | Découvertes dans Meta Ads Library |
| **Budget consommé** | $5.00 | Limite Apify mensuelle |

### 🎯 Phase 2 - Classification (40 clients actifs)

| Métrique | Valeur | Ratio |
|----------|--------|-------|
| **Publicités classifiées** | 1,366 | 100% |
| **Converty Ads** | 1,354 | 99.1% |
| **Concurrent Ads** | 12 | 0.9% |
| **Unknown Ads** | 0 | 0% |
| **Concurrents uniques** | 3 | WhatsApp API, autres |

---

## 📊 Structure des Données

### MongoDB - Collection `ads_metrics`

**Phase 1 - Documents Mapping** (`type='mapping'`)
```json
{
  "client_id": "vervane",
  "type": "mapping",
  "status": "active",
  "domain": "vervane.converty.shop",
  "processing_metadata": {
    "total_ads": 12,
    "facebook_pages": ["110379551822943"],
    "scraping_cost": 0.007
  },
  "sites_mapping": {
    "vervane.converty.shop": {
      "facebook_pages": ["110379551822943"],
      "total_ads": 12
    }
  },
  "timestamp": "2025-12-29T16:30:00.000Z"
}
```

**Phase 2 - Documents Report** (`type='report'`)
```json
{
  "client_id": "vervane",
  "type": "report",
  "domain": "vervane.converty.shop",
  "metrics": {
    "total_ads": 94,
    "converty_ads": 94,
    "concurrent_ads": 0,
    "unknown_ads": 0,
    "converty_ratio": 100.0,
    "concurrent_ratio": 0.0
  },
  "facebook_pages": [
    {
      "page_id": "110379551822943",
      "page_name": "Vervane Store",
      "total_ads": 94,
      "converty_ads": 94,
      "concurrent_ads": 0,
      "converty_ratio": 100
    }
  ],
  "competitors": [],
  "analyzed_at": "2025-12-29T17:45:00.000Z"
}
```

---

## 🎨 Dashboard - Sections

### 1️⃣ Vue d'ensemble
**KPIs principaux**
- Total clients : 21,764
- Clients traités : 718 (3.3%)
- Clients actifs : 40 (5.6%)
- Publicités Converty : 1,354 (99.1%)
- Publicités Concurrents : 12 (0.9%)

**Graphiques**
- Jauge de progression (718/21,764)
- Ratio actifs/inactifs (pie chart)

### 2️⃣ Analyse Temporelle
- Évolution cumulative des clients traités
- Nouveaux clients par jour
- Filtres : 7/30/90 jours ou historique complet

### 3️⃣ Analyse Concurrentielle
- Top 10 concurrents (bar chart)
- Distribution des plateformes (pie chart)
- Détection automatique des URL concurrentes

### 4️⃣ Détails Clients
**Table interactive avec :**
- Client ID, Status, Total ads
- % Converty, Top concurrent
- Dernière activité

**Fonctionnalités :**
- 🔍 Recherche par client_id
- 📊 Filtres status (actif/inactif)
- 📥 Export CSV
- 🔄 Auto-refresh (60s)

### 5️⃣ Alertes & Recommandations
- Alertes critiques (clients à fort volume concurrent)
- Recommandations stratégiques
- Tendances détectées

---

## 💡 Insights & Stratégie

### 📈 Analyse des Résultats

**✅ Points forts**
- **99.1% Converty Ads** → Forte adoption de la plateforme Converty
- **5.6% taux d'activité** → Opportunité de réactivation pour les 94.4% inactifs
- **Concurrence faible** → Position dominante avec seulement 0.9% de concurrent ads

**⚠️ Points d'attention**
- **20% clients traités** → 80% restent à analyser (4343 / 21,046 clients)
- **Budget de 5$ (freemium)** → **Upgrade Apify (Premium 39$/mois)**
- **Concurrents émergents**

### 🎯 Recommandations

1. **Court terme** (1 mois)
   - Analyser les 21,046 clients restants (budget additionnel)
   - Cibler les clients inactifs pour campagnes de réactivation

2. **Moyen terme** (3 mois)
   - Automatiser le scraping incrémental (hebdomadaire)
   - Créer des alertes en temps réel sur nouveaux concurrents
   - Segmenter les clients par volume publicitaire

3. **Long terme** (6 mois)
   - Analyse prédictive : identifier clients à fort potentiel
   - Benchmarking concurrentiel automatisé
   - API publique pour exports automatisés

---

## 🔧 Technologies & Stack

| Catégorie | Technologies |
|-----------|-------------|
| **Backend** | Python 3.11+ |
| **Scraping** | Apify API, Meta Ad Library Actor |
| **Database** | MongoDB (collections: stores, ads_metrics) |
| **Analytics** | pandas, numpy |
| **Visualization** | Streamlit, Plotly |
| **Costs Tracking** | Apify API (monthly_usage) |
| **Logging** | Python logging |

---

## 🚨 Gestion des Coûts

### Budget Tracking en Temps Réel

Le système intègre un **CostTracker** qui :
- ✅ Lit les coûts depuis l'API Apify (`monthly_usage`)
- ✅ Alerte à 60%, 80%, 90%, 100% du budget
- ✅ Arrête automatiquement à 100%
- ✅ Estime les clients restants possibles

**Exemple output :**
```
💰 COÛT SESSION
──────────────────────────────────────────────────────
   Batch actuel : $0.0234
   Session totale : $4.87 / $5.00 🟠
   Restant : $0.13 (2.6%)
   Clients traités : 718
──────────────────────────────────────────────────────
```
---

## 🛠️ Développement & Maintenance

### Ajouter un nouveau client

```python
from src.discovery.mapper import SiteMapper

mapper = SiteMapper()
result = mapper.process_client("nouveau-client")
```

### Réanalyser un client existant

```bash
python phase2_main.py --client vervane
```

### Nettoyer le cache

```bash
rm -rf data/cache/*
```
🔮 Perspectives d'évolution

- Extension à d’autres plateformes (Instagram Ads, Google Ads)
- Intégration de l’IA pour la détection prédictive de churn
- Automatisation des alertes par email
- Conteneurisation avec Docker et déploiement cloud

👥 Auteurs

- Ghofrane Mahfoudhi

- Sirine Makni

📄 Licence

Ce projet est développé dans le cadre d’un projet tutoré à SUP'COM. Tous droits réservés aux auteurs et à Converty.
---


