# LogiFlow CRM - Google Maps Service
# Serviço para geocodificação, rotas e cálculo de distâncias

import httpx
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from loguru import logger
from config import settings


class MapsService:
    """
    Serviço de integração com Google Maps API
    
    Funcionalidades:
    - Geocodificação (endereço → coordenadas)
    - Geocodificação reversa (coordenadas → endereço)
    - Cálculo de rotas e distâncias
    - Matriz de distâncias (múltiplas origens/destinos)
    - Estimativa de tempo de chegada (ETA)
    """
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY or ""
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.timeout = 30.0
    
    # ==========================================
    # Geocodificação
    # ==========================================
    
    async def geocodificar(self, endereco: str) -> Dict[str, Any]:
        """
        Converte endereço em coordenadas (latitude/longitude)
        
        Args:
            endereco: Endereço completo (ex: "Av. Paulista, 1000, São Paulo, SP")
        
        Returns:
            {
                "success": True,
                "latitude": -23.5505,
                "longitude": -46.6333,
                "endereco_formatado": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP",
                "componentes": {...}
            }
        """
        if not self.api_key:
            return self._geocodificar_mock(endereco)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/geocode/json",
                    params={
                        "address": endereco,
                        "key": self.api_key,
                        "language": "pt-BR",
                        "region": "br"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                if data["status"] == "OK" and data["results"]:
                    result = data["results"][0]
                    location = result["geometry"]["location"]
                    
                    return {
                        "success": True,
                        "latitude": location["lat"],
                        "longitude": location["lng"],
                        "endereco_formatado": result["formatted_address"],
                        "place_id": result.get("place_id"),
                        "componentes": self._extrair_componentes(result)
                    }
                else:
                    return {"success": False, "error": f"Status: {data['status']}"}
                    
        except Exception as e:
            logger.error(f"Erro na geocodificação: {e}")
            return {"success": False, "error": str(e)}
    
    async def geocodificar_reverso(
        self, 
        latitude: float, 
        longitude: float
    ) -> Dict[str, Any]:
        """
        Converte coordenadas em endereço
        
        Args:
            latitude: Latitude
            longitude: Longitude
        
        Returns:
            Endereço formatado e componentes
        """
        if not self.api_key:
            return self._geocodificar_reverso_mock(latitude, longitude)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/geocode/json",
                    params={
                        "latlng": f"{latitude},{longitude}",
                        "key": self.api_key,
                        "language": "pt-BR"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                if data["status"] == "OK" and data["results"]:
                    result = data["results"][0]
                    
                    return {
                        "success": True,
                        "endereco_formatado": result["formatted_address"],
                        "componentes": self._extrair_componentes(result)
                    }
                else:
                    return {"success": False, "error": f"Status: {data['status']}"}
                    
        except Exception as e:
            logger.error(f"Erro na geocodificação reversa: {e}")
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # Rotas e Distâncias
    # ==========================================
    
    async def calcular_rota(
        self,
        origem: str,
        destino: str,
        waypoints: Optional[List[str]] = None,
        evitar: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calcula rota entre origem e destino
        
        Args:
            origem: Endereço ou coordenadas de origem
            destino: Endereço ou coordenadas de destino
            waypoints: Lista de paradas intermediárias
            evitar: Lista do que evitar (tolls, highways, ferries)
        
        Returns:
            Rota com distância, duração e instruções
        """
        if not self.api_key:
            return self._calcular_rota_mock(origem, destino)
        
        try:
            params = {
                "origin": origem,
                "destination": destino,
                "key": self.api_key,
                "language": "pt-BR",
                "units": "metric",
                "mode": "driving"
            }
            
            if waypoints:
                params["waypoints"] = "|".join(waypoints)
            
            if evitar:
                params["avoid"] = "|".join(evitar)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/directions/json",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if data["status"] == "OK" and data["routes"]:
                    route = data["routes"][0]
                    leg = route["legs"][0]
                    
                    return {
                        "success": True,
                        "distancia_metros": leg["distance"]["value"],
                        "distancia_texto": leg["distance"]["text"],
                        "duracao_segundos": leg["duration"]["value"],
                        "duracao_texto": leg["duration"]["text"],
                        "origem_endereco": leg["start_address"],
                        "destino_endereco": leg["end_address"],
                        "origem_coords": leg["start_location"],
                        "destino_coords": leg["end_location"],
                        "polyline": route["overview_polyline"]["points"],
                        "passos": self._extrair_passos(leg["steps"])
                    }
                else:
                    return {"success": False, "error": f"Status: {data['status']}"}
                    
        except Exception as e:
            logger.error(f"Erro ao calcular rota: {e}")
            return {"success": False, "error": str(e)}
    
    async def calcular_distancia(
        self,
        origem: str,
        destino: str
    ) -> Dict[str, Any]:
        """
        Calcula distância e tempo entre dois pontos (simplificado)
        """
        rota = await self.calcular_rota(origem, destino)
        
        if rota.get("success"):
            return {
                "success": True,
                "distancia_km": round(rota["distancia_metros"] / 1000, 1),
                "duracao_minutos": round(rota["duracao_segundos"] / 60),
                "distancia_texto": rota["distancia_texto"],
                "duracao_texto": rota["duracao_texto"]
            }
        
        return rota
    
    async def matriz_distancias(
        self,
        origens: List[str],
        destinos: List[str]
    ) -> Dict[str, Any]:
        """
        Calcula matriz de distâncias entre múltiplas origens e destinos
        Útil para otimização de rotas
        """
        if not self.api_key:
            return self._matriz_distancias_mock(origens, destinos)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/distancematrix/json",
                    params={
                        "origins": "|".join(origens),
                        "destinations": "|".join(destinos),
                        "key": self.api_key,
                        "language": "pt-BR",
                        "units": "metric",
                        "mode": "driving"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                if data["status"] == "OK":
                    matriz = []
                    for i, row in enumerate(data["rows"]):
                        linha = []
                        for j, element in enumerate(row["elements"]):
                            if element["status"] == "OK":
                                linha.append({
                                    "origem": data["origin_addresses"][i],
                                    "destino": data["destination_addresses"][j],
                                    "distancia_metros": element["distance"]["value"],
                                    "distancia_texto": element["distance"]["text"],
                                    "duracao_segundos": element["duration"]["value"],
                                    "duracao_texto": element["duration"]["text"]
                                })
                            else:
                                linha.append({"status": element["status"]})
                        matriz.append(linha)
                    
                    return {
                        "success": True,
                        "origens": data["origin_addresses"],
                        "destinos": data["destination_addresses"],
                        "matriz": matriz
                    }
                else:
                    return {"success": False, "error": f"Status: {data['status']}"}
                    
        except Exception as e:
            logger.error(f"Erro na matriz de distâncias: {e}")
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # ETA (Estimated Time of Arrival)
    # ==========================================
    
    async def calcular_eta(
        self,
        posicao_atual: Tuple[float, float],
        destino: str
    ) -> Dict[str, Any]:
        """
        Calcula tempo estimado de chegada baseado na posição atual
        
        Args:
            posicao_atual: Tupla (latitude, longitude)
            destino: Endereço ou coordenadas do destino
        
        Returns:
            ETA com horário previsto de chegada
        """
        origem = f"{posicao_atual[0]},{posicao_atual[1]}"
        rota = await self.calcular_rota(origem, destino)
        
        if rota.get("success"):
            duracao_segundos = rota["duracao_segundos"]
            from datetime import timedelta
            
            agora = datetime.now()
            chegada = agora + timedelta(seconds=duracao_segundos)
            
            return {
                "success": True,
                "distancia_restante_km": round(rota["distancia_metros"] / 1000, 1),
                "tempo_restante_minutos": round(duracao_segundos / 60),
                "tempo_restante_texto": rota["duracao_texto"],
                "horario_atual": agora.strftime("%H:%M"),
                "horario_chegada_previsto": chegada.strftime("%H:%M"),
                "data_chegada": chegada.strftime("%d/%m/%Y %H:%M")
            }
        
        return rota
    
    # ==========================================
    # Utilitários
    # ==========================================
    
    def _extrair_componentes(self, result: Dict) -> Dict[str, str]:
        """Extrai componentes do endereço"""
        componentes = {}
        for comp in result.get("address_components", []):
            for tipo in comp["types"]:
                if tipo == "street_number":
                    componentes["numero"] = comp["long_name"]
                elif tipo == "route":
                    componentes["logradouro"] = comp["long_name"]
                elif tipo == "sublocality_level_1":
                    componentes["bairro"] = comp["long_name"]
                elif tipo == "administrative_area_level_2":
                    componentes["cidade"] = comp["long_name"]
                elif tipo == "administrative_area_level_1":
                    componentes["estado"] = comp["short_name"]
                elif tipo == "postal_code":
                    componentes["cep"] = comp["long_name"]
                elif tipo == "country":
                    componentes["pais"] = comp["short_name"]
        return componentes
    
    def _extrair_passos(self, steps: List) -> List[Dict]:
        """Extrai passos da navegação"""
        passos = []
        for step in steps:
            passos.append({
                "instrucao": step.get("html_instructions", "").replace("<b>", "").replace("</b>", ""),
                "distancia": step["distance"]["text"],
                "duracao": step["duration"]["text"],
                "manobra": step.get("maneuver", "")
            })
        return passos
    
    # ==========================================
    # Mocks (quando não há API key)
    # ==========================================
    
    def _geocodificar_mock(self, endereco: str) -> Dict[str, Any]:
        """Mock para testes sem API key"""
        # Coordenadas aproximadas de São Paulo
        return {
            "success": True,
            "latitude": -23.5505 + (hash(endereco) % 100) / 10000,
            "longitude": -46.6333 + (hash(endereco) % 100) / 10000,
            "endereco_formatado": endereco,
            "mock": True,
            "componentes": {
                "cidade": "São Paulo",
                "estado": "SP",
                "pais": "BR"
            }
        }
    
    def _geocodificar_reverso_mock(self, lat: float, lng: float) -> Dict[str, Any]:
        return {
            "success": True,
            "endereco_formatado": f"Localização aproximada ({lat:.4f}, {lng:.4f})",
            "mock": True,
            "componentes": {
                "cidade": "São Paulo",
                "estado": "SP"
            }
        }
    
    def _calcular_rota_mock(self, origem: str, destino: str) -> Dict[str, Any]:
        """Mock para testes sem API key"""
        # Simula distância baseada no hash dos endereços
        dist_base = abs(hash(origem + destino)) % 200 + 10  # 10-210 km
        tempo_base = dist_base * 1.5  # ~40 km/h médio
        
        return {
            "success": True,
            "distancia_metros": dist_base * 1000,
            "distancia_texto": f"{dist_base} km",
            "duracao_segundos": int(tempo_base * 60),
            "duracao_texto": f"{int(tempo_base)} min",
            "origem_endereco": origem,
            "destino_endereco": destino,
            "mock": True,
            "passos": [
                {"instrucao": "Siga em frente", "distancia": f"{dist_base} km", "duracao": f"{int(tempo_base)} min"}
            ]
        }
    
    def _matriz_distancias_mock(self, origens: List[str], destinos: List[str]) -> Dict[str, Any]:
        """Mock para matriz de distâncias"""
        matriz = []
        for origem in origens:
            linha = []
            for destino in destinos:
                dist = abs(hash(origem + destino)) % 200 + 10
                linha.append({
                    "origem": origem,
                    "destino": destino,
                    "distancia_metros": dist * 1000,
                    "distancia_texto": f"{dist} km",
                    "duracao_segundos": dist * 90,
                    "duracao_texto": f"{dist * 90 // 60} min"
                })
            matriz.append(linha)
        
        return {
            "success": True,
            "origens": origens,
            "destinos": destinos,
            "matriz": matriz,
            "mock": True
        }


# Instância global do serviço
maps_service = MapsService()
