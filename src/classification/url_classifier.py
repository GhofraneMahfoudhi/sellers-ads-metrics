"""
Classification des publicités: CONVERTY vs CONCURRENT
"""
from typing import Dict, Any, Optional, List
import re
from urllib.parse import urlparse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class URLClassifier:
    """Classifier pour identifier CONVERTY vs CONCURRENT"""
    
    # Domaines à ignorer (pas des concurrents commerciaux)
    IGNORED_DOMAINS = [
        'facebook.com',
        'instagram.com',
        'fb.com',
        'fb.me',
        'bit.ly',
        'tinyurl.com',
        'l.facebook.com',
        'l.instagram.com',
    ]
    
    def classify_ad(
        self, 
        ad: Dict[str, Any], 
        converty_domain: str
    ) -> Dict[str, Any]:
        """
        Classifier une publicité
        
        Args:
            ad: Données de la publicité
            converty_domain: Domaine Converty du client (ex: "tbshopp.com")
            
        Returns:
            {
                'classification': 'CONVERTY' | 'CONCURRENT' | 'UNKNOWN',
                'confidence': 'high' | 'medium' | 'low',
                'reason': str,
                'destination_url': str,
                'competitor_domain': str | None
            }
        """
        # Extraire les URLs de la publicité
        urls = self._extract_urls_from_ad(ad)
        
        if not urls:
            return {
                'classification': 'UNKNOWN',
                'confidence': 'low',
                'reason': 'Aucune URL trouvée dans la publicité',
                'destination_url': None,
                'competitor_domain': None
            }
        
        # Analyser chaque URL
        for url in urls:
            url_lower = url.lower()
            
            # 1. Vérifier si c'est le domaine Converty
            if converty_domain.lower() in url_lower:
                return {
                    'classification': 'CONVERTY',
                    'confidence': 'high',
                    'reason': f'URL contient le domaine Converty: {converty_domain}',
                    'destination_url': url,
                    'competitor_domain': None
                }
            
            # 2. Extraire le domaine de l'URL
            domain = self._extract_domain(url)
            
            if not domain:
                continue
            
            # 3. Vérifier si c'est un domaine ignoré (Facebook, etc.)
            if self._is_ignored_domain(domain):
                continue
            
            # 4. C'est un concurrent !
            return {
                'classification': 'CONCURRENT',
                'confidence': 'high',
                'reason': f'URL pointe vers un domaine concurrent: {domain}',
                'destination_url': url,
                'competitor_domain': domain
            }
        
        # Aucune URL commerciale trouvée
        return {
            'classification': 'UNKNOWN',
            'confidence': 'medium',
            'reason': 'Aucune URL commerciale identifiée',
            'destination_url': urls[0] if urls else None,
            'competitor_domain': None
        }
    
    def _extract_urls_from_ad(self, ad: Dict[str, Any]) -> List[str]:
        """
        Extraire toutes les URLs d'une publicité
        
        Args:
            ad: Données de la publicité
            
        Returns:
            Liste des URLs trouvées
        """
        urls = []
        snapshot = ad.get('snapshot', {})
        
        # 1. URL principale (link_url)
        link_url = snapshot.get('link_url')
        if link_url:
            urls.append(link_url)
        
        # 2. URLs dans les cards (carousel)
        cards = snapshot.get('cards', [])
        for card in cards:
            card_url = card.get('link_url')
            if card_url:
                urls.append(card_url)
        
        # 3. Caption
        caption = snapshot.get('caption', '')
        if caption:
            found_urls = re.findall(r'https?://[^\s<>"]+', caption)
            urls.extend(found_urls)
        
        # 4. Body text
        body = snapshot.get('body', {})
        if isinstance(body, dict):
            body_text = body.get('text', '')
        else:
            body_text = str(body)
        
        if body_text:
            found_urls = re.findall(r'https?://[^\s<>"]+', body_text)
            urls.extend(found_urls)
        
        # Éliminer les doublons et nettoyer
        unique_urls = []
        seen = set()
        for url in urls:
            # Nettoyer l'URL
            url = url.strip().rstrip('.,;:!?)')
            if url and url not in seen:
                unique_urls.append(url)
                seen.add(url)
        
        return unique_urls
    
    def _extract_domain(self, url: str) -> Optional[str]:
        """
        Extraire le domaine principal d'une URL
        
        Args:
            url: URL complète
            
        Returns:
            Domaine (ex: "boutique.com")
        """
        try:
            # Parser l'URL
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            parsed = urlparse(url)
            domain = parsed.netloc
            
            if not domain:
                return None
            
            # Nettoyer
            domain = domain.lower()
            domain = domain.replace('www.', '')
            
            # Enlever le port si présent
            if ':' in domain:
                domain = domain.split(':')[0]
            
            return domain if domain else None
            
        except Exception as e:
            logger.debug(f"Erreur extraction domaine de {url}: {e}")
            return None
    
    def _is_ignored_domain(self, domain: str) -> bool:
        """Vérifier si le domaine doit être ignoré"""
        domain_lower = domain.lower()
        
        for ignored in self.IGNORED_DOMAINS:
            if ignored in domain_lower:
                return True
        
        return False