"""
Script de Teste - Melhor Envio
Testa a integração com a API do Melhor Envio
"""
import sys
import os

# Adicionar path do backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.frete.melhor_envio import MelhorEnvioClient
from config import settings


def testar_conexao():
    """Testa conexão básica com a API"""
    print("=" * 60)
    print("🧪 TESTE MELHOR ENVIO - LogiFlow CRM")
    print("=" * 60)
    
    # Verificar configuração
    if not settings.MELHOR_ENVIO_TOKEN:
        print("❌ ERRO: MELHOR_ENVIO_TOKEN não configurado no .env")
        print("\n📝 Para configurar:")
        print("1. Acesse: https://melhorenvio.com.br/painel")
        print("2. Gere um token de API")
        print("3. Adicione ao .env: MELHOR_ENVIO_TOKEN=seu_token")
        return False
    
    print(f"\n✅ Token configurado: {settings.MELHOR_ENVIO_TOKEN[:20]}...")
    print(f"✅ Sandbox: {'SIM' if settings.MELHOR_ENVIO_SANDBOX else 'NÃO'}")
    
    return True


def testar_cotacao_simples():
    """Testa cotação simples"""
    print("\n" + "=" * 60)
    print("📦 TESTE 1: Cotação Simples")
    print("=" * 60)
    
    try:
        client = MelhorEnvioClient(
            token=settings.MELHOR_ENVIO_TOKEN,
            sandbox=settings.MELHOR_ENVIO_SANDBOX
        )
        
        # CEPs de teste (São Paulo)
        origem = "01310100"  # Av. Paulista
        destino = "04547130"  # Itaim Bibi
        peso = 5.0
        
        print(f"\n📍 Origem: {origem}")
        print(f"📍 Destino: {destino}")
        print(f"⚖️  Peso: {peso} kg")
        print(f"\n⏳ Calculando...")
        
        resultado = client.calcular_frete_simples(
            origem_cep=origem,
            destino_cep=destino,
            peso_kg=peso,
            valor_mercadoria=100.00
        )
        
        if not resultado.get("success"):
            print(f"\n❌ ERRO: {resultado.get('message', resultado.get('error'))}")
            return False
        
        cotacoes = resultado.get("data", [])
        print(f"\n✅ {len(cotacoes)} cotações encontradas:\n")
        
        for i, cot in enumerate(cotacoes, 1):
            if cot.get("error"):
                print(f"{i}. ❌ {cot.get('name')} - {cot.get('error')}")
            else:
                company_name = cot.get("company", {}).get("name", "N/A")
                service_name = cot.get("name", "N/A")
                price = cot.get("price", 0)
                delivery_time = cot.get("delivery_time", "N/A")
                
                print(f"{i}. ✅ {company_name} - {service_name}")
                print(f"   💰 R$ {price}")
                print(f"   📅 {delivery_time} dias úteis")
                print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_melhor_cotacao():
    """Testa busca pela melhor cotação"""
    print("\n" + "=" * 60)
    print("🏆 TESTE 2: Melhor Cotação (Menor Preço)")
    print("=" * 60)
    
    try:
        client = MelhorEnvioClient(
            token=settings.MELHOR_ENVIO_TOKEN,
            sandbox=settings.MELHOR_ENVIO_SANDBOX
        )
        
        resultado = client.obter_melhor_cotacao(
            origem_cep="01310100",
            destino_cep="04547130",
            peso_kg=10.0,
            valor_mercadoria=200.00,
            prioridade="preco"
        )
        
        if not resultado.get("success"):
            print(f"\n❌ ERRO: {resultado.get('message')}")
            return False
        
        melhor = resultado.get("data", {})
        total_opcoes = resultado.get("total_opcoes", 0)
        
        print(f"\n✅ Melhor opção (de {total_opcoes} disponíveis):\n")
        print(f"   🚚 Transportadora: {melhor.get('company', {}).get('name')}")
        print(f"   📦 Serviço: {melhor.get('name')}")
        print(f"   💰 Valor: R$ {melhor.get('price')}")
        print(f"   📅 Prazo: {melhor.get('delivery_time')} dias úteis")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False


def testar_comparacao_tabela():
    """Testa comparação com tabela própria"""
    print("\n" + "=" * 60)
    print("💡 TESTE 3: Comparação com Tabela Própria")
    print("=" * 60)
    
    try:
        client = MelhorEnvioClient(
            token=settings.MELHOR_ENVIO_TOKEN,
            sandbox=settings.MELHOR_ENVIO_SANDBOX
        )
        
        valor_tabela = 150.00  # Simulação: sua frota cobraria R$ 150
        
        print(f"\n💼 Valor da sua tabela: R$ {valor_tabela}")
        print(f"⏳ Comparando com mercado...")
        
        resultado = client.comparar_com_tabela_propria(
            origem_cep="01310100",
            destino_cep="04547130",
            peso_kg=15.0,
            valor_tabela_propria=valor_tabela,
            valor_mercadoria=300.00
        )
        
        if not resultado.get("success"):
            print(f"\n❌ ERRO: {resultado.get('message')}")
            return False
        
        data = resultado.get("data", {})
        
        print(f"\n✅ Análise:\n")
        print(f"   💼 Sua tabela: R$ {data.get('valor_tabela_propria')}")
        print(f"   🌐 Menor preço mercado: R$ {data.get('menor_preco_mercado')}")
        print(f"   💰 Economia: R$ {data.get('economia_potencial'):.2f} ({data.get('percentual_economia'):.1f}%)")
        print(f"   🎯 Recomendação: {data.get('recomendacao').upper()}")
        
        if data.get('recomendacao') == 'terceirizar':
            print(f"\n   ✅ Vale mais a pena terceirizar!")
        else:
            print(f"\n   ✅ Use sua frota própria!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("\n")
    
    if not testar_conexao():
        print("\n❌ Configuração inválida. Abortando testes.")
        return
    
    resultados = []
    
    # Teste 1: Cotação simples
    resultados.append(("Cotação Simples", testar_cotacao_simples()))
    
    # Teste 2: Melhor cotação
    resultados.append(("Melhor Cotação", testar_melhor_cotacao()))
    
    # Teste 3: Comparação com tabela
    resultados.append(("Comparação Tabela", testar_comparacao_tabela()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for nome, sucesso in resultados:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    total = len(resultados)
    sucessos = sum(1 for _, s in resultados if s)
    
    print(f"\n📈 {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("\n🎉 Todos os testes passaram! Melhor Envio está configurado corretamente!")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique as mensagens de erro acima.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

