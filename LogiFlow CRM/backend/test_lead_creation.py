"""
Teste de criação de lead via API
"""
import requests
import json

API_URL = "http://localhost:8000"

print("=" * 60)
print("🧪 Testando Criação de Lead via API")
print("=" * 60)

# Dados do lead de teste
lead_data = {
    "name": "João Silva Teste",
    "email": "joao.teste@empresa.com",
    "phone": "11987654321",
    "company": "Transportadora Teste Ltda",
    "vehicles": "15-50",
    "message": "Gostaria de conhecer o LogiFlow CRM para gerenciar minha frota"
}

print("\n📝 Dados do lead:")
print(json.dumps(lead_data, indent=2, ensure_ascii=False))

# Testar endpoint de demo request
print("\n🔄 Enviando requisição para /demo/request...")
try:
    response = requests.post(
        f"{API_URL}/demo/request",
        json=lead_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Lead criado com sucesso!")
        print(f"\nResposta:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        lead_id = result.get("lead_id")
        
        # Buscar o lead criado
        if lead_id:
            print(f"\n🔍 Buscando lead criado (ID: {lead_id})...")
            get_response = requests.get(f"{API_URL}/demo/requests/{lead_id}")
            
            if get_response.status_code == 200:
                lead_details = get_response.json()
                print("✅ Lead encontrado!")
                print(json.dumps(lead_details, indent=2, ensure_ascii=False))
            else:
                print(f"❌ Erro ao buscar lead: {get_response.status_code}")
    else:
        print(f"❌ Erro ao criar lead")
        print(f"Resposta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar ao servidor")
    print("   Certifique-se de que o servidor está rodando em http://localhost:8000")
except Exception as e:
    print(f"❌ Erro: {e}")

# Listar todos os leads
print("\n📋 Listando todos os leads...")
try:
    list_response = requests.get(f"{API_URL}/demo/requests")
    if list_response.status_code == 200:
        leads_list = list_response.json()
        print(f"✅ Total de leads: {leads_list.get('count', 0)}")
        
        if leads_list.get('data'):
            print("\nÚltimos 3 leads:")
            for lead in leads_list['data'][:3]:
                print(f"   - {lead['name']} ({lead['email']}) - Status: {lead['status']}")
    else:
        print(f"❌ Erro ao listar leads: {list_response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
print("=" * 60)
