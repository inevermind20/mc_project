import streamlit as st
import pandas as pd

# Carregar os dados
@st.cache_data
def load_data():
    df_machine = pd.read_excel("teste.xlsx", sheet_name="Machine price", engine="openpyxl")
    df_options = pd.read_excel("teste.xlsx", sheet_name="TC MC option price", engine="openpyxl")
    return df_machine, df_options

df_machine, df_options = load_data()

# Título da aplicação
st.title("Configurador de Máquinas")

# Seleção do modelo
modelos = df_machine[["Model Code", "Model Name"]].drop_duplicates()
modelos["Modelo"] = modelos["Model Code"] + " - " + modelos["Model Name"]
modelo_selecionado = st.selectbox("Selecione o modelo da máquina:", modelos["Modelo"])

# Extrair código e nome
codigo_modelo, nome_modelo = modelo_selecionado.split(" - ", 1)

# Mostrar configurações base disponíveis (colunas D, E, F, G)
config_base = df_machine[(df_machine["Model Code"] == codigo_modelo) & (df_machine["Model Name"] == nome_modelo)]
colunas_base = config_base.columns[3:7]  # D, E, F, G
st.subheader("Configurações base disponíveis")
st.dataframe(config_base[colunas_base], use_container_width=True)

# Selecionar configuração base (colunas E, F, G como rótulo)
config_base["Label"] = config_base[colunas_base[1]].astype(str) + " | " + config_base[colunas_base[2]].astype(str) + " | " + config_base[colunas_base[3]].astype(str)
codigo_base = st.selectbox("Escolha a configuração base:", config_base["Label"])
linha_base = config_base[config_base["Label"] == codigo_base].iloc[0]
preco_base = linha_base["mPrice"] if "mPrice" in linha_base else 0

# Filtrar opções disponíveis
opcoes = df_options[(df_options["Model Code"] == codigo_modelo) & (df_options["Model Name"] == nome_modelo)]

# Agrupar por categoria e característica
st.subheader("Opções adicionais")
preco_total = preco_base
opcoes_selecionadas = []

for (categoria, caracteristica), grupo in opcoes.groupby(["Category I", "Characteristic"]):
    grupo = grupo.copy()
    grupo["mPrice"] = grupo["mPrice"].fillna("0")
    std_valores = grupo[grupo["mPrice"].astype(str).str.upper() == "STD"]["Value"].tolist()
    std_valor = std_valores[0] if std_valores else grupo["Value"].iloc[0]
    with st.expander(f"{categoria} - {caracteristica}", expanded=False):
        st.markdown(f"**Padrão:** {std_valor}")
        for _, row in grupo.iterrows():
            valor = row["Value"]
            preco = row["mPrice"]
            if str(preco).upper() not in ["STD", "ASK DNS"]:
                try:
                    preco_valor = float(preco)
                    if st.checkbox(f"{valor} (+{preco_valor:,.0f} €)", key=f"{categoria}-{caracteristica}-{valor}"):
                        preco_total += preco_valor
                        opcoes_selecionadas.append((f"{categoria} - {caracteristica}", valor, preco_valor))
                except:
                    pass

# Botão fixo com resumo
with st.sidebar:
    st.markdown("### Resumo da Configuração")
    st.markdown(f"**Modelo:** {modelo_selecionado}")
    st.markdown(f"**Configuração Base:** {codigo_base}")
    st.markdown(f"**Preço Base:** {preco_base:,.0f} €")
    if opcoes_selecionadas:
        st.markdown("**Opções Selecionadas:**")
        for cat, val, preco in opcoes_selecionadas:
            st.markdown(f"- {cat}: {val} (+{preco:,.0f} €)")
    st.markdown(f"### 💰 Preço Total: {preco_total:,.0f} €")
    if st.button("Exportar para Excel"):
        resumo = pd.DataFrame(opcoes_selecionadas, columns=["Categoria", "Opção", "Preço"])
        resumo.loc[len(resumo.index)] = ["TOTAL", "", preco_total]
        resumo.to_excel("resumo_configuracao.xlsx", index=False)
        st.success("Resumo exportado para 'resumo_configuracao.xlsx'")
