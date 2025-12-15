"""
LogiFlow CRM - Google Distance Matrix API
Cálculo de distâncias e tempos de viagem
"""

import requests
from typing import Dict, List, Optional, Tuple
import logging
from utils.quota_monitor import quota_monitor

logger = logging.getLogger(__name__)


class DistanceMatrixClient:
    """
    Cliente para Google Distance Matrix API
    Documentação: https://developers.google.com/maps/documentation/distance-matrix
    """
    
    BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    def __init__(self, api_key: str):
        """
        Inicializa cliente Distance Matrix
        
        Args:
            api_key: Chave da API Google Maps
        """
        self.api_key = api_key

    @classmethod
    def from_settings(cls):
        from config import settings
        key = getattr(settings, "GOOGLE_MAPS_DISTANCE_MATRIX_KEY", None) or getattr(settings, "GOOGLE_MAPS_API_KEY", None)
        if not key:
            raise ValueError("Chave do Google Maps não configurada (GOOGLE_MAPS_DISTANCE_MATRIX_KEY ou GOOGLE_MAPS_API_KEY).")
        return cls(api_key=key)
    
    def calcular_distancia(
        self,
        origem: str,
        destino: str,
        modo: str = "driving",
        unidades: str = "metric"
    ) -> Dict:
        """
        Calcula distância e tempo entre dois pontos
        
        Args:
            origem: Endereço ou coordenadas de origem
            destino: Endereço ou coordenadas de destino
            modo: driving, walking, bicycling, transit
            unidades: metric ou imperial
            
        Returns:
            Distância e tempo de viagem
        """
        # Verificar quota
        is_available, error_msg = quota_monitor.check_quota("google_maps_distance_matrix")
        if not is_available:
            logger.warning(f"Quota exceeded for Google Maps: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "quota_exceeded": True
            }
        
        try:
            params = {
                "origins": origem,
                "destinations": destino,
                "mode": modo,
                "units": unidades,
                "key": self.api_key,
                "language": "pt-BR"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "OK":
                return {
                    "success": False,
                    "error": data.get("error_message", "Erro ao calcular distância"),
                    "status": data.get("status")
                }
            
            # Extrair resultado
            rows = data.get("rows", [])
            if not rows or not rows[0].get("elements"):
                return {
                    "success": False,
                    "error": "Nenhum resultado encontrado"
                }
            
            element = rows[0]["elements"][0]
            
            if element.get("status") != "OK":
                return {
                    "success": False,
                    "error": f"Rota não encontrada: {element.get('status')}"
                }
            
            distancia = element.get("distance", {})
            duracao = element.get("duration", {})
            
            # Registrar chamada bem-sucedida
            quota_monitor.record_call("google_maps_distance_matrix", success=True, cost=0.005)
            
            return {
                "success": True,
                "origem": data.get("origin_addresses", [""])[0],
                "destino": data.get("destination_addresses", [""])[0],
                "distancia": {
                    "valor": distancia.get("value", 0),  # metros
                    "texto": distancia.get("text", ""),  # formatado
                    "km": round(distancia.get("value", 0) / 1000, 2)
                },
                "duracao": {
                    "valor": duracao.get("value", 0),  # segundos
                    "texto": duracao.get("text", ""),  # formatado
                    "minutos": round(duracao.get("value", 0) / 60, 2),
                    "horas": round(duracao.get("value", 0) / 3600, 2)
                },
                "modo": modo
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao calcular distância: {e}")
            # Registrar chamada com falha
            quota_monitor.record_call("google_maps_distance_matrix", success=False)
            return {
                "success": False,
                "error": str(e)
            }
    
    def calcular_distancia_por_cep(
        self,
        cep_origem: str,
        cep_destino: str,
        modo: str = "driving"
    ) -> Dict:
        """
        Calcula distância entre dois CEPs
        
        Args:
            cep_origem: CEP de origem
            cep_destino: CEP de destino
            modo: Modo de transporte
            
        Returns:
            Distância e tempo
        """
        origem = f"{cep_origem}, Brasil"
        destino = f"{cep_destino}, Brasil"
        
        return self.calcular_distancia(origem, destino, modo)
    
    def calcular_matriz_distancias(
        self,
        origens: List[str],
        destinos: List[str],
        modo: str = "driving"
    ) -> Dict:
        """
        Calcula matriz de distâncias (múltiplas origens e destinos)
        
        Args:
            origens: Lista de endereços de origem
            destinos: Lista de endereços de destino
            modo: Modo de transporte
            
        Returns:
            Matriz de distâncias
        """
        try:
            params = {
                "origins": "|".join(origens),
                "destinations": "|".join(destinos),
                "mode": modo,
                "units": "metric",
                "key": self.api_key,
                "language": "pt-BR"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "OK":
                return {
                    "success": False,
                    "error": data.get("error_message", "Erro ao calcular matriz")
                }
            
            # Processar matriz
            matriz = []
            rows = data.get("rows", [])
            origem_enderecos = data.get("origin_addresses", [])
            destino_enderecos = data.get("destination_addresses", [])
            
            for i, row in enumerate(rows):
                linha = {
                    "origem": origem_enderecos[i] if i < len(origem_enderecos) else "",
                    "destinos": []
                }
                
                for j, element in enumerate(row.get("elements", [])):
                    if element.get("status") == "OK":
                        distancia = element.get("distance", {})
                        duracao = element.get("duration", {})
                        
                        linha["destinos"].append({
                            "destino": destino_enderecos[j] if j < len(destino_enderecos) else "",
                            "distancia_km": round(distancia.get("value", 0) / 1000, 2),
                            "duracao_minutos": round(duracao.get("value", 0) / 60, 2),
                            "distancia_texto": distancia.get("text", ""),
                            "duracao_texto": duracao.get("text", "")
                        })
                    else:
                        linha["destinos"].append({
                            "destino": destino_enderecos[j] if j < len(destino_enderecos) else "",
                            "erro": element.get("status")
                        })
                
                matriz.append(linha)
            
            return {
                "success": True,
                "matriz": matriz,
                "total_origens": len(origens),
                "total_destinos": len(destinos)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao calcular matriz: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def calcular_rota_otimizada(
        self,
        origem: str,
        destino: str,
        pontos_intermediarios: List[str],
        otimizar: bool = True
    ) -> Dict:
        """
        Calcula rota otimizada com múltiplas paradas
        
        Args:
            origem: Ponto de partida
            destino: Ponto final
            pontos_intermediarios: Paradas no meio do caminho
            otimizar: Se True, otimiza ordem das paradas
            
        Returns:
            Rota otimizada
        """
        # Para otimização de rota, usar Directions API
        # Aqui calculamos distâncias entre todos os pontos
        
        todos_pontos = [origem] + pontos_intermediarios + [destino]
        
        resultado = self.calcular_matriz_distancias(
            origens=todos_pontos,
            destinos=todos_pontos
        )
        
        if not resultado.get("success"):
            return resultado
        
        # Calcular distância total da rota sequencial
        distancia_total = 0
        tempo_total = 0
        
        for i in range(len(todos_pontos) - 1):
            if i < len(resultado["matriz"]):
                destinos = resultado["matriz"][i]["destinos"]
                if i + 1 < len(destinos):
                    destino_info = destinos[i + 1]
                    if "distancia_km" in destino_info:
                        distancia_total += destino_info["distancia_km"]
                        tempo_total += destino_info["duracao_minutos"]
        
        return {
            "success": True,
            "rota": todos_pontos,
            "distancia_total_km": round(distancia_total, 2),
            "tempo_total_minutos": round(tempo_total, 2),
            "tempo_total_horas": round(tempo_total / 60, 2),
            "numero_paradas": len(pontos_intermediarios),
            "matriz_completa": resultado["matriz"]
        }
    
    def estimar_custo_frete(
        self,
        cep_origem: str,
        cep_destino: str,
        valor_por_km: float = 2.50,
        valor_base: float = 50.00
    ) -> Dict:
        """
        Estima custo de frete baseado na distância
        
        Args:
            cep_origem: CEP de origem
            cep_destino: CEP de destino
            valor_por_km: Valor cobrado por km
            valor_base: Valor base do frete
            
        Returns:
            Estimativa de custo
        """
        resultado = self.calcular_distancia_por_cep(cep_origem, cep_destino)
        
        if not resultado.get("success"):
            return resultado
        
        distancia_km = resultado["distancia"]["km"]
        tempo_horas = resultado["duracao"]["horas"]
        
        # Calcular custo
        custo_distancia = distancia_km * valor_por_km
        custo_total = valor_base + custo_distancia
        
        # Adicionar custo de tempo (se viagem muito longa)
        if tempo_horas > 8:
            custo_adicional_tempo = (tempo_horas - 8) * 20  # R$ 20/hora extra
            custo_total += custo_adicional_tempo
        else:
            custo_adicional_tempo = 0
        
        return {
            "success": True,
            "origem": resultado["origem"],
            "destino": resultado["destino"],
            "distancia_km": distancia_km,
            "tempo_horas": tempo_horas,
            "custos": {
                "valor_base": valor_base,
                "custo_distancia": round(custo_distancia, 2),
                "custo_tempo_extra": round(custo_adicional_tempo, 2),
                "custo_total": round(custo_total, 2)
            },
            "detalhamento": {
                "valor_por_km": valor_por_km,
                "km_rodados": distancia_km,
                "horas_viagem": tempo_horas
            }
        }
    
    def comparar_rotas(
        self,
        origem: str,
        destino: str,
        modos: List[str] = None
    ) -> Dict:
        """
        Compara diferentes modos de transporte
        
        Args:
            origem: Ponto de origem
            destino: Ponto de destino
            modos: Lista de modos (driving, walking, bicycling, transit)
            
        Returns:
            Comparação entre modos
        """
        if modos is None:
            modos = ["driving", "transit"]
        
        comparacao = []
        
        for modo in modos:
            resultado = self.calcular_distancia(origem, destino, modo)
            
            if resultado.get("success"):
                comparacao.append({
                    "modo": modo,
                    "distancia_km": resultado["distancia"]["km"],
                    "tempo_minutos": resultado["duracao"]["minutos"],
                    "distancia_texto": resultado["distancia"]["texto"],
                    "tempo_texto": resultado["duracao"]["texto"]
                })
        
        # Ordenar por tempo
        comparacao.sort(key=lambda x: x["tempo_minutos"])
        
        return {
            "success": True,
            "origem": origem,
            "destino": destino,
            "comparacao": comparacao,
            "modo_mais_rapido": comparacao[0] if comparacao else None
        }
    
    def calcular_raio_entrega(
        self,
        centro: str,
        raio_km: float,
        pontos: List[str]
    ) -> Dict:
        """
        Verifica quais pontos estão dentro de um raio de entrega
        
        Args:
            centro: Ponto central (endereço ou CEP)
            raio_km: Raio máximo de entrega em km
            pontos: Lista de endereços a verificar
            
        Returns:
            Pontos dentro e fora do raio
        """
        resultado = self.calcular_matriz_distancias(
            origens=[centro],
            destinos=pontos
        )
        
        if not resultado.get("success"):
            return resultado
        
        dentro_raio = []
        fora_raio = []
        
        if resultado["matriz"]:
            for destino_info in resultado["matriz"][0]["destinos"]:
                if "distancia_km" in destino_info:
                    if destino_info["distancia_km"] <= raio_km:
                        dentro_raio.append(destino_info)
                    else:
                        fora_raio.append(destino_info)
        
        return {
            "success": True,
            "centro": centro,
            "raio_km": raio_km,
            "dentro_raio": dentro_raio,
            "fora_raio": fora_raio,
            "total_dentro": len(dentro_raio),
            "total_fora": len(fora_raio),
            "cobertura_percentual": round((len(dentro_raio) / len(pontos)) * 100, 2) if pontos else 0
        }
