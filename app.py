import pandas as pd
import streamlit as st
import altair as alt


@st.cache
def get_data():
    df = pd.read_csv("datahackers.csv")
    df.columns = [eval(col)[1] for col in df.columns]
    df = df[df['living_in_brasil'] == 1]

    # aqui vamos alterar os valores de 1 para Sim e 0 para não, para facilitar a visualização
    df['is_data_science_professional'] = df.is_data_science_professional.map({
                                                                             1: 'Sim', 0: 'Não'})

    return df


df = get_data()


'''
# Pesquisa DataHackers 2019

A comunidade DataHackers realizou no mês de Novembro de 2019 uma pesquisa online sobre o mercado de DataSciente no Brasil e disponibilizou o resultado para que possamos analisar. 

Link para o dataset no kaggle: https://www.kaggle.com/datahackers/pesquisa-data-hackers-2019/

Com base no dataset, vamos realizar algumas análises e verificar como o anda o mercado aqui no Brasil. Para isto, vamos filtrar para que exiba somente as informações onde o campo **living_in_brasil** for **True**

'''

st.subheader('Quantidade de respostas a serem analisadas: %i' %
             (df["is_data_science_professional"].count()))
'''
## Você se considera um profissional que atua na área de Data Science?
'''

is_datascience = pd.DataFrame({
    "Resposta": df['is_data_science_professional'].unique(),
    "Valor": df['is_data_science_professional'].groupby(df["is_data_science_professional"]).value_counts()
})

st.altair_chart(alt.Chart(is_datascience).mark_bar().encode(
    alt.Y("Valor", title=""),
    alt.X("Resposta", title=""),
    color="Resposta",
    tooltip=["Resposta", "Valor"]
), use_container_width=True)

st.write("Aqui vemos que o percentual de entrevistados que se consideram **Data Scientists** é de **%.00f%%**." % (
    (is_datascience[is_datascience["Resposta"] == 'Sim'].Valor.sum() / df["is_data_science_professional"].count()) * 100)
)

st.write("A partir de agora vamos trabalhar com um filtro de se o entrevistado é profissional de DataScience ou não, que você pode selecionar no menu lateral.")

datascience = st.sidebar.multiselect("É profissional de DataScience?", list(
    df["is_data_science_professional"].unique()), ['Sim', 'Não'])


if len(datascience) > 0:
    df_dados_selecionados = df[df['is_data_science_professional'].isin(
        datascience)]

    df_living_state = pd.DataFrame(
        df_dados_selecionados["living_state"].value_counts())

    df_living_state = pd.DataFrame({
        "Estados": df_living_state.index,
        "Total": df_living_state.living_state,
    })

    st.subheader("Em quais estados estão os entrevistados?")
    st.altair_chart(alt.Chart(df_living_state).mark_bar().encode(
        x="Total",
        y=alt.Y("Estados:N", sort="-x"),
        color="Estados",
        tooltip=["Estados", "Total"],
    ), use_container_width=True)

    st.write("Podemos ver que o estado de **%s** ocupa a primeira posição, representando **%.00f%%** dos dados selecionados, enquanto **%s** ocupa a última posição, com **%.00f%%**." %
             (df_living_state['Estados'].max(), (df_living_state['Total'].max() / df_living_state['Total'].sum()) * 100, df_living_state['Estados'].min(),
              (df_living_state['Total'].min() / df_living_state['Total'].sum()) * 100)
             )

    st.subheader("Qual a formação destes profissionais?")
    df_degreee_level = pd.DataFrame(
        df_dados_selecionados["degreee_level"].value_counts())

    df_degreee_level = pd.DataFrame({
        "Graduação": df_degreee_level.index,
        "Total": df_degreee_level.degreee_level,
    })

    st.altair_chart(alt.Chart(df_degreee_level).mark_bar().encode(
        x="Total",
        y=alt.Y("Graduação:N", sort="-x"),
        color="Graduação",
        tooltip=["Graduação", "Total"],
    ), use_container_width=True)

    '''
        Aqui podemos ver que a grande maioria dos profissionais possui pelo menos uma Graduação ou Bacharelado, e que tem profissionais que não possui uma graduação formal.
        Isto está cada vez mais comum, visto que cada ano que se passa o acesso a conteúdos estão maiores e muitas das vezes não é necessário ter uma formação para se trabalhar com tecnologia.
    '''

    st.subheader("Qual o salário destes profissionais?")
    st.write("O grande atrativo desta área talvez seja os salários pagos. Afinal, quem não gostaria de ganhar R$ 25.000 por mês como diz o artigo https://exame.com/carreira/por-que-o-nubank-sempre-busca-cientistas-de-dados-e-paga-ate-r-25-mil ?")

    df_salary_range = pd.DataFrame(
        df_dados_selecionados["salary_range"].value_counts())

    df_salary_range = pd.DataFrame({
        "Faixa": df_salary_range.index,
        "Total": df_salary_range.salary_range,
    })

    st.altair_chart(alt.Chart(df_salary_range).mark_bar().encode(
        x="Total",
        y=alt.Y("Faixa:N", sort="-x"),
        tooltip=["Faixa", "Total"],
    ), use_container_width=True)

    st.write("Vemos que sim, existem pessoas que ganham mais de **R$ 20.000 por mês** mas que a realidade é um pouco diferente, tendo profissionais que recebem até menos de **R$ 1000**.")

    st.subheader("E qual a situação de trabalho destes profissionais?")
    df_job_situation = pd.DataFrame(
        df_dados_selecionados["job_situation"].value_counts())

    df_job_situation = pd.DataFrame({
        "Situação": df_job_situation.index,
        "Total": df_job_situation.job_situation,
    })

    st.altair_chart(alt.Chart(df_job_situation).mark_bar().encode(
        y=alt.Y("Situação", sort="-x"),
        x="Total",
        tooltip=["Situação", "Total"],
    ), use_container_width=True)

    st.write("Este gráfico nos mostra que na terceira posição temos **Estagiário** como situação profissional dos entrevistados, mas quanto está recebendo um estágiário?")

    df_salary_range = df_dados_selecionados[df["job_situation"]
                                            == "Estagiário"]

    df_salary_range = pd.DataFrame(
        df_dados_selecionados[df["job_situation"] == "Estagiário"].salary_range.value_counts())
    df_salary_range = pd.DataFrame({
        "Faixa": df_salary_range.index,
        "Total": df_salary_range.salary_range,
    })

    st.altair_chart(alt.Chart(df_salary_range).mark_bar().encode(
        x="Total",
        y=alt.Y("Faixa:N", sort="-x"),
        tooltip=["Faixa", "Total"],
    ), use_container_width=True)

    st.write("A maioria dos estágiários estão recebendo entre R$ 1001 e R$2000 mês, e em segundo lugar vem os abaixo de R$ 1000. Um fator interessante é que temos 1 sortudo recebendo entre R$ 3001 e R$ 4000, ou será uma resposta errada?")

    st.subheader("Existe equilíbrio de gênero entre os profissionais?")
    st.write("Sabemos que o desenquilíbrio de gênero é uma realidade e que existem várias iniciativas para conscientização em nossa sociedade.")

    df_gender = pd.DataFrame(
        df_dados_selecionados["gender"].value_counts())

    df_gender = pd.DataFrame({
        "Gênero": df_gender.index,
        "Total": df_gender.gender,
    })

    st.altair_chart(alt.Chart(df_gender).mark_bar().encode(
        x=alt.X("Gênero", sort="-y"),
        y="Total",
        tooltip=["Gênero", "Total"],
    ), use_container_width=True)

    st.write("Podemos ver que o desequilíbrio ainda é grande nos profissionais entrevistados.")

    st.write("Em contrução...")

    st.write("Código fonte disponível em: https://github.com/luizhfraraujo/datahackers_survey_2019")
else:
    st.write("**Você precisa selecionar uma informação no filtro acima**")
# estados = st.multiselect("Estados", list(df["living_state"].unique()))

# df_estados_selecionados = df[df['living_state'].isin(estados)]

# st.dataframe(df_estados_selecionados)

# st.altair_chart(alt.Chart(is_datascience).mark_bar().encode(
#     alt.Y("value",title=""),
#     alt.X("Resposta", title=""),
#     color="Resposta",
#     tooltip=["Resposta","value"]
# ), use_container_width=True)
