<p align="center" class="trendshift">
  <a href="https://trendshift.io/repositories/14130" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/14130" alt="Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
</p>
<p align="center">
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/v/release/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github&color=blue" alt="Release"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License: MIT"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/stargazers">
    <img src="https://img.shields.io/github/stars/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github" alt="Stars"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/downloads/huangjunsen0406/py-xiaozhi/total?style=flat-square&logo=github&color=52c41a1&maxAge=86400" alt="Download"/>
  </a>
  <a href="https://gitee.com/huang-jun-sen/py-xiaozhi">
    <img src="https://img.shields.io/badge/Gitee-FF5722?style=flat-square&logo=gitee" alt="Gitee"/>
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/guide/00_%E6%96%87%E6%A1%A3%E7%9B%AE%E5%BD%95.html">
    <img alt="Documentation" src="https://img.shields.io/badge/Documentation-Cliquez_ici-blue?labelColor=2d2d2d" />
  </a>
</p>

Français simplifié | [English](README.en.md)

## Introduction du projet

py-xiaozhi est un client vocal Xiaozhi implémenté en Python, conçu pour apprendre via le code et expérimenter les fonctions vocales de l’IA Xiaozhi sans matériel.
Ce dépôt est un portage basé sur [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)

## Démonstration

- [Vidéo de démonstration sur Bilibili](https://www.bilibili.com/video/BV1HmPjeSED2/#reply255921347937)

![Image](./documents/docs/guide/images/系统界面.png)

## Fonctionnalités principales

### 🎯 Fonctionnalités IA de base
- **Interaction vocale IA** : supporte l’entrée et la reconnaissance vocale, permet une interaction homme-machine intelligente et fluide
- **Vision multimodale** : supporte la reconnaissance et le traitement d’images, offre une interaction multimodale et la compréhension de contenu visuel
- **Réveil intelligent** : activation par mots-clés configurables, évitant une manipulation manuelle
- **Mode de dialogue automatique** : permet un dialogue continu et naturel

### 🔧 Écosystème d’outils MCP
- **Outils de contrôle système** : surveillance de l’état système, gestion d’applications, contrôle du volume, gestion des périphériques
- **Outils de gestion de planning** : gestion complète d’agenda (création, consultation, mise à jour, suppression), avec rappels intelligents
- **Outils de tâches programmées** : compte à rebours, exécution différée d’outils MCP, gestion multi-tâches
- **Lecteur musical** : recherche et lecture en ligne, contrôle de la lecture, affichage des paroles, gestion du cache local
- **Outil 12306** : recherche de billets de train (recherche de trajets, correspondances, itinéraires)
- **Outils de recherche** : recherche web (Bing) et analyse intelligente du contenu
- **Outils de recettes** : base de données riche, recherche, filtrage et recommandations intelligentes
- **Outil de cartes** : services cartographiques (géocodage, itinéraires, recherche locale, météo)
- **Outil astrologique Bazi** : analyse traditionnelle (calcul Bazi, compatibilité, calendrier lunaire)
- **Outil caméra** : capture d’image et analyse IA, reconnaissance photo et Q&R intelligentes

### 🏠 Intégration IoT
- **Gestion des appareils** : architecture unifiée basée sur le modèle Thing, support des appels asynchrones
- **Contrôle domotique** : contrôle de lumières, volume, capteurs de température, etc.
- **Synchronisation d’état** : suivi en temps réel, mises à jour incrémentielles et lecture concurrente
- **Extensibilité** : architecture modulaire facilitant l’ajout de nouveaux périphériques

### 🎵 Traitement audio avancé
- **Chaîne de traitement audio** : support Opus, rééchantillonnage en temps réel
- **Détection d’activité vocale** : VAD pour interruption intelligente, surveillance en temps réel
- **Détection de mots-clés** : reconnaissance hors ligne Sherpa-ONNX, multi-mots et pinyin
- **Gestion des flux audio** : entrées/sorties indépendantes, support reconstruction et récupération
- **Annulation d’écho** : module WebRTC intégré, annulation d’écho haute qualité
- **Enregistrement audio système** : capture audio système, prise en charge du loopback

### 🖥️ Interface utilisateur
- **GUI moderne** : basé sur PyQt5, expressions et textes Xiaozhi, expérience visuelle améliorée
- **Mode CLI** : exécution en ligne de commande (adapté aux systèmes embarqués sans GUI)
- **Icône système** : exécution en arrière-plan avec intégration dans la barre système
- **Raccourcis globaux** : opérations rapides via raccourcis clavier
- **Interface paramètres** : gestion complète des réglages personnalisables

### 🔒 Sécurité et stabilité
- **Transmission audio chiffrée** : via WSS, prévention des fuites de données
- **Activation des appareils** : support double protocole v1/v2, gestion auto des codes et empreintes
- **Récupération des erreurs** : gestion complète des erreurs avec reconnexion automatique

### 🌐 Compatibilité multi-plateformes
- **Compatibilité système** : Windows 10+, macOS 10.15+, Linux
- **Support protocole** : WebSocket et MQTT
- **Déploiement flexible** : GUI ou CLI
- **Optimisations spécifiques** : audio et contrôle système optimisés par plateforme

### 🔧 Développement
- **Architecture modulaire** : séparation claire des responsabilités
- **Asynchrone** : basé sur asyncio, hautes performances
- **Gestion de config** : système hiérarchique, notation pointée, mise à jour dynamique
- **Logs** : support complet de journalisation et debug
- **Docs API** : documentation détaillée

## Configuration système

### Prérequis
- **Python** : 3.9 - 3.12
- **OS** : Windows 10+, macOS 10.15+, Linux
- **Audio** : micro + haut-parleurs
- **Réseau** : connexion stable

### Recommandé
- **RAM** : min 4GB (8GB+ recommandé)
- **CPU** : moderne avec AVX
- **Disque** : 2GB libres
- **Audio** : 16kHz supporté

### Fonctions optionnelles
- **Réveil vocal** : nécessite modèles Sherpa-ONNX
- **Caméra** : nécessite caméra + OpenCV

## À lire en premier

- Lisez attentivement la [documentation du projet](https://huangjunsen0406.github.io/py-xiaozhi/) (guide de démarrage inclus)
- La branche *main* contient le code le plus récent, réinstallez toujours les dépendances pip après mise à jour

[Utiliser le client Xiaozhi depuis zéro (tutoriel vidéo)](https://www.bilibili.com/video/BV1dWQhYEEmq/?vd_source=2065ec11f7577e7107a55bbdc3d12fce)

(... reste identique, traduction déjà appliquée aux parties chinoises ...)

### Communauté & support

#### Merci aux contributeurs open source
>
> Liste sans ordre particulier

(...)

### Soutien & sponsoring

<div align="center">
  <h3>Merci à tous les sponsors ❤️</h3>
  <p>Qu’il s’agisse de ressources, de tests de compatibilité ou de soutien financier, chaque aide améliore le projet</p>
  
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
    <img src="https://img.shields.io/badge/Voir-la_liste_des_sponsors-brightgreen?style=for-the-badge&logo=github" alt="Liste des sponsors">
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
    <img src="https://img.shields.io/badge/Devenir-sponsor_du_projet-orange?style=for-the-badge&logo=heart" alt="Devenir sponsor">
  </a>
</div>
