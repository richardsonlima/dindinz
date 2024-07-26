import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from requests.exceptions import RequestException

class SimulacaoInvestidorApp:
    def run(self):
        # Configurar a chave da API da OpenAI
        # openai.api_key = 'sk-xxx'  # Substitua pela sua chave da API

        # Função para verificar a conectividade com a URL da API
        def verificar_conectividade(url):
            try:
                response = requests.head(url)
                return response.status_code == 200
            except RequestException:
                return False

        # Função para obter a taxa de rendimento da poupança e CDI a partir da API do Banco Central
        def obter_taxa_bacen(endpoint, tentativas=3):
            url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{endpoint}/dados?formato=json'
            if not verificar_conectividade(url):
                st.error(f"Não foi possível conectar à URL: {url}")
                return None
            for tentativa in range(tentativas):
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Levanta uma exceção para respostas com erro
                    data = response.json()
                    if len(data) == 0:
                        raise ValueError("Nenhum dado retornado da API")
                    taxa = float(data[-1]['valor']) / 100
                    # Validação da taxa para garantir que está dentro de um intervalo esperado
                    if 0 <= taxa <= 0.3:
                        return taxa
                    else:
                        raise ValueError(f"Taxa fora do intervalo esperado: {taxa}")
                except (RequestException, ValueError, IndexError) as e:
                    st.error(f"Tentativa {tentativa + 1} de {tentativas}: Erro ao obter dados da API do Banco Central para o endpoint {endpoint}: {e}")
                    if tentativa == tentativas - 1:
                        return None
        
        # Função para calcular o rendimento
        def calcular_rendimento(valor_inicial, valor_mensal, taxa_anual, anos=30):
            meses = anos * 12
            taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1
            valores = []
            valor_atual = valor_inicial
            for mes in range(meses):
                valor_atual = valor_atual * (1 + taxa_mensal) + valor_mensal
                valores.append(valor_atual)
            return valores
        
        # Função para obter o rendimento anual médio das ações
        def obter_rendimento_acoes(tickers):
            retornos_anuais = {}
            for ticker in tickers:
                acao = yf.Ticker(f"{ticker}.SA")
                dados = acao.history(period="1y")
                if dados.empty:
                    retornos_anuais[ticker] = 0
                else:
                    retorno_anual = dados['Close'].pct_change().mean() * 252  # 252 é o número de dias de negociação em um ano
                    retornos_anuais[ticker] = retorno_anual
            return retornos_anuais
        
        # Função para obter informações atualizadas dos tickers das ações
        def obter_info_acoes(tickers):
            info_acoes = {}
            for ticker in tickers:
                acao = yf.Ticker(f"{ticker}.SA")
                info_acoes[ticker] = {
                    'Nome': acao.info.get('longName', 'N/A'),
                    'Setor': acao.info.get('sector', 'N/A'),
                    'Rendimento Anual (%)': acao.history(period="1y")["Close"].pct_change().mean() * 252 * 100
                }
            return info_acoes
        
        # Função para resumir os dados da tabela
        def resumir_dados(df):
            resumo = df.describe().transpose()
            resumo['Sum'] = df.sum()
            resumo['Mean'] = df.mean()
            resumo['Std'] = df.std()
            return resumo
        
        # Função para obter insights usando GPT-4
        # def obter_insights(texto):
        #     response = openai.ChatCompletion.create(
        #         model="gpt-4",
        #         messages=[
        #             {"role": "system", "content": "Você é um assistente útil e sabe muito sobre investimentos."},
        #             {"role": "user", "content": texto}
        #         ],
        #         max_tokens=1024,  # Ajuste o número de tokens conforme necessário
        #         n=1,
        #         stop=None,
        #         temperature=0.7
        #     )
        #     return response['choices'][0]['message']['content'].strip()
        
        # Função para exibir texto longo em múltiplos blocos
        def exibir_texto_longo(texto, max_length=1000):
            partes = [texto[i:i+max_length] for i in range(0, len(texto), max_length)]
            for parte in partes:
                st.write(parte)
        
        # Obter taxas de rendimento
        def obter_taxas_tesouro_direto():
            endpoints = {
                'Tesouro Prefixado 2029': '1784',
                'Tesouro Prefixado com Juros Semestrais 2033': '1785',
                'Tesouro IPCA+ 2045': '1786',
                'Tesouro Prefixado com Juros Semestrais 2031': '1787',
                'Tesouro Prefixado com Juros Semestrais 2029': '1788',
                'Tesouro IPCA+ com Juros Semestrais 2055': '1789',
                'Tesouro Prefixado com Juros Semestrais 2027': '1790',
                'Tesouro Prefixado 2026': '1791',
                'Tesouro IPCA+ com Juros Semestrais 2050': '1792',
                'Tesouro IPCA+ com Juros Semestrais 2045': '1793',
                'Tesouro IPCA+ 2035': '1794',
                'Tesouro IPCA+ com Juros Semestrais 2040': '1795',
                'Tesouro IPCA+ com Juros Semestrais 2035': '1796',
                'Tesouro IPCA+ com Juros Semestrais 2032': '1797',
                'Tesouro Prefixado 2025': '1798',
                'Tesouro IPCA+ com Juros Semestrais 2030': '1799',
                'Tesouro Prefixado com Juros Semestrais 2025': '1800',
                'Tesouro Prefixado 2024': '1801',
                'Tesouro IPCA+ 2026': '1802',
                'Tesouro IPCA+ com Juros Semestrais 2026': '1803',
                'Tesouro Selic 2027': '1804',
                'Tesouro Selic 2025': '1805',
                'Tesouro Selic 2024': '1806',
                'Tesouro IPCA+ 2024': '1807',
                'Tesouro IPCA+ com Juros Semestrais 2024': '1808',
                'Tesouro IGPM+ com Juros Semestrais 2031': '1809'
            }
            taxas = {}
            for nome, endpoint in endpoints.items():
                taxa = obter_taxa_bacen(endpoint)
                if taxa is not None:
                    taxas[nome] = taxa
                else:
                    st.warning(f"Usando valor default para {nome} devido a erro na API.")
                    taxas[nome] = 0.05  # Valor default ou fallback
            return taxas
        
        def obter_taxas():
            taxas = obter_taxas_tesouro_direto()
            taxas['Poupança'] = obter_taxa_bacen('7454')  # Poupança
            taxas['CDI'] = obter_taxa_bacen('12')  # CDI
            taxas['LCI'] = 0.06  # Placeholder para LCI, ajustar conforme necessário
            taxas['LCA'] = 0.06  # Placeholder para LCA, ajustar conforme necessário
            taxas['Previdência Privada PGBL'] = 0.07  # Placeholder para Previdência Privada PGBL, ajustar conforme necessário
            taxas['Previdência Privada VGBL'] = 0.07  # Placeholder para Previdência Privada VGBL, ajustar conforme necessário
            return taxas
        
        # Configuração inicial do Streamlit
        #st.set_page_config(page_title="Jornada de Investimento", page_icon="💰", layout="wide")
        
        # Título e animação
        st.title('💰 Simulador do Investidor')
        
        # Inputs do usuário com formatação após a entrada
        st.sidebar.header('Configurações de Investimento')
        valor_inicial = st.sidebar.number_input('Valor de Aporte Inicial', min_value=0.0, value=0.0, step=100.0, format="%0.2f")
        valor_mensal = st.sidebar.number_input('Valor de Aplicação Mensal', min_value=0.0, value=0.0, step=100.0, format="%0.2f")
        
        # Formatando valores para exibição com símbolo de moeda no início
        valor_inicial_formatado = f"R$ {valor_inicial:,.2f}"
        valor_mensal_formatado = f"R$ {valor_mensal:,.2f}"
        
        st.sidebar.write(f"Valor de Aporte Inicial: {valor_inicial_formatado}")
        st.sidebar.write(f"Valor de Aplicação Mensal: {valor_mensal_formatado}")
        
        # Obter taxas de rendimento
        taxas = obter_taxas()
        
        # Verifica se todas as taxas foram obtidas com sucesso
        if any(taxa is None for taxa in taxas.values()):
            st.error("Não foi possível obter todas as taxas de rendimento. Por favor, tente novamente mais tarde.")
        else:
            # Seção para exibir e editar taxas de juros
            st.sidebar.header('Taxas de Juros')
            for nome_titulo, taxa in taxas.items():
                taxas[nome_titulo] = st.sidebar.number_input(f'Taxa {nome_titulo} (%)', value=taxa * 100) / 100
        
            tickers_carteira_barsi = ['TAEE11', 'TRPL4', 'BBSE3', 'ITSA4', 'ABEV3', 'EGIE3', 'ENBR3', 'ETER3','CGRA4', 'BBAS3', 'PSSA3', 'SAPR11', 'LEVE3', 'CSMG3', 'CEEB3', 'CEEB5', 'GRND3', 'HYPE3', 'BBDC4']   
            retornos_anuais_barsi = obter_rendimento_acoes(tickers_carteira_barsi)
            taxas['Carteira Barsi'] = np.mean(list(retornos_anuais_barsi.values()))
            info_carteira_barsi = obter_info_acoes(tickers_carteira_barsi)
        
            # Obter e mostrar opções de taxas de rendimento
            st.header('Escolha a Taxa de Rendimento Anual')
            opcoes_taxas = list(taxas.keys())
            opcao_taxa = st.selectbox('Escolha a Taxa de Rendimento Anual', opcoes_taxas)
        
            tickers_customizados = []
            taxa_carteira_customizada = 0.0
            if opcao_taxa == 'TICKERS Customizados':
                tickers_customizados = st.text_input('Insira os TICKERS customizados separados por vírgula (e.g., BBAS3,ITUB4,SANB11)')
                if tickers_customizados:
                    tickers_customizados = [ticker.strip().upper() for ticker in tickers_customizados.split(',')]
                    retornos_anuais_customizados = obter_rendimento_acoes(tickers_customizados)
                    taxa_carteira_customizada = np.mean(list(retornos_anuais_customizados.values()))
                    info_carteira_customizada = obter_info_acoes(tickers_customizados)
                    st.write('Informações dos TICKERS customizados:')
                    for ticker, info in info_carteira_customizada.items():
                        st.write(f"{ticker}: {info['Nome']}, Setor: {info['Setor']}, Rendimento Anual: {info['Rendimento Anual (%)']:.2f}%")
                else:
                    st.error("Por favor, insira os TICKERS customizados.")
        
            if opcao_taxa in opcoes_taxas:
                taxa_selecionada = taxas[opcao_taxa]
                st.write(f'Taxa Anual: {taxa_selecionada * 100:.2f}%')
            elif opcao_taxa == 'Carteira Barsi':
                st.write('Informações dos TICKERS da Carteira Barsi:')
                for ticker, info in info_carteira_barsi.items():
                    st.write(f"{ticker}: {info['Nome']}, Setor: {info['Setor']}, Rendimento Anual: {info['Rendimento Anual (%)']:.2f}%")
                taxa_selecionada = taxas['Carteira Barsi']
            elif opcao_taxa == 'TICKERS Customizados' and tickers_customizados:
                taxa_selecionada = taxa_carteira_customizada
        
            # Calcular rendimentos para a opção selecionada
            anos = 30
            if valor_inicial > 0 and valor_mensal > 0:
                valores = calcular_rendimento(valor_inicial, valor_mensal, taxa_selecionada)
                
                # Gerar DataFrame para exibir os resultados
                df = pd.DataFrame({
                    'Mês': range(1, len(valores) + 1),
                    'Valor Investido sem Rentabilidade': np.cumsum([valor_inicial] + [valor_mensal] * (len(valores) - 1)),
                    'Rentabilidade Anual': [taxa_selecionada * 100] * len(valores),
                    'Valor Acumulado com Rentabilidade': valores,
                    'Rentabilidade Mensal': np.diff([valor_inicial] + valores).tolist()
                })
                
                st.write(df)
        
                # Mostrar gráfico dos resultados
                st.line_chart(df['Valor Acumulado com Rentabilidade'])
        
            # Calcular rendimentos para cada opção para visualização comparativa
            valores_comparacao = {nome: calcular_rendimento(valor_inicial, valor_mensal, taxa, anos) for nome, taxa in taxas.items()}
            
            # Gerar DataFrame para exibir os resultados comparativos
            df_comparativo = pd.DataFrame(valores_comparacao)
            df_comparativo.insert(0, 'Mês', range(1, anos * 12 + 1))
        
            st.header("Comparação dos diferentes investimentos")
            st.write(df_comparativo)
        
            # Mostrar gráfico dos resultados comparativos
            st.line_chart(df_comparativo.set_index('Mês'))
        
            # Solicitar insights do GPT-4
            # st.subheader("Receba insights sobre seus investimentos")
            # if st.button("Gerar Insights"):
            #     resumo_dados = resumir_dados(df_comparativo)
            #     prompt = f"Os resultados resumidos dos investimentos são os seguintes:\n\n{resumo_dados.to_string()}\n\nBaseado nesses dados, forneça insights e sugestões."
            #     insights = obter_insights(prompt)
            #     exibir_texto_longo(insights)

if __name__ == "__main__":
    app = SimulacaoInvestidorApp()
    app.run()
