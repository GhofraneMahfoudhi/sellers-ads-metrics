"""
Mapper entre sites et pages Facebook - AVEC FILTRAGE
"""
from typing import List, Dict, Any
from datetime import datetime
import json
import os
from src.discovery.ads_collector import AdsCollector
from src.discovery.page_extractor import PageExtractor
from src.utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)


class SiteMapper:
    """Crée le mapping entre sites et pages Facebook avec filtrage strict"""
    
    def __init__(self):
        self.ads_collector = AdsCollector()
        self.page_extractor = PageExtractor()
    
    def map_client_sites(
        self, 
        client_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Créer le mapping complet pour un client avec FILTRAGE
        
        Args:
            client_data: {
                "client_id": "ravino",
                "sites": ["ravino.converty.shop"]
            }
            
        Returns:
            Mapping complet avec uniquement les pages FB qui utilisent le domaine
        """
        client_id = client_data['client_id']
        sites = client_data['sites']
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 MAPPING CLIENT: {client_id} (AVEC FILTRAGE)")
        logger.info(f"{'='*60}\n")
        
        mappings = []
        
        for site in sites:
            logger.info(f"\n--- Traitement du site: {site} ---")
            
            # 1. Collecter UNIQUEMENT les ads qui contiennent le domaine exact
            ads = self.ads_collector.collect_ads_for_domain(site)
            
            # 2. Extraire les pages FB depuis les ads FILTRÉES
            pages = self.page_extractor.extract_pages_from_ads(ads)
            
            # 3. Calculer la confiance pour chaque page
            for page in pages:
                page['confidence'] = self._calculate_confidence(
                    page['ads_count'],
                    len(ads)
                )
            
            # 4. Créer le mapping
            mapping = {
                'site': site,
                'total_ads': len(ads),  # Nombre d'ads FILTRÉES
                'fb_pages': pages,
                'mapped_at': datetime.now().isoformat()
            }
            
            mappings.append(mapping)
            
            logger.info(f"✓ Mapping créé pour {site}: {len(pages)} page(s) utilisant le domaine\n")
        
        # Résultat final
        result = {
            'client_id': client_id,
            'total_sites': len(sites),
            'mappings': mappings,
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ MAPPING TERMINÉ POUR {client_id}")
        logger.info(f"{'='*60}\n")
        
        return result
    
    def _calculate_confidence(self, page_ads: int, total_ads: int) -> str:
        """
        Calculer le niveau de confiance du mapping
        """
        if total_ads == 0:
            return 'low'
        
        ratio = page_ads / total_ads
        
        if ratio >= 0.7:
            return 'high'
        elif ratio >= 0.3:
            return 'medium'
        else:
            return 'low'
    
    def save_mapping(
        self, 
        mapping: Dict[str, Any], 
        filename: str = None
    ) -> str:
        """
        Sauvegarder le mapping dans un fichier JSON
        """
        if not filename:
            client_id = mapping['client_id']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{client_id}_mapping_{timestamp}.json"
        
        filepath = os.path.join(settings.MAPPINGS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Mapping sauvegardé: {filepath}")
        
        return filepath