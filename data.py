import pandas as pd
import streamlit as st
import pydeck as pdk


class Data:

    @st.cache()
    def get_data():
        df = pd.read_csv("static/datahackers.csv")
        df.columns = [eval(col)[1] for col in df.columns]
        df = df[df['living_in_brasil'] == 1]

        # aqui vamos alterar os valores de 1 para Sim e 0 para não, para facilitar a visualização
        df['is_data_science_professional'] = df.is_data_science_professional.map({
                                                                                 1: 'Sim', 0: 'Não'})
        return df

    def get_is_datascientist(df):
        return pd.DataFrame({
            "Resposta": df['is_data_science_professional'].unique(),
            "Valor": df['is_data_science_professional'].groupby(df["is_data_science_professional"]).value_counts()
        })

    def get_selected_data(df, is_datascientist):
        return df[df['is_data_science_professional'].isin(is_datascientist)]

    def get_living_state(df):
        df_return = pd.DataFrame(df["living_state"].value_counts())
        df_return = pd.DataFrame(
            {"Estados": df_return.index, "Total": df_return.living_state})
        return df_return

    def get_degreee_level(df):
        df_return = pd.DataFrame(df["degreee_level"].value_counts())
        df_return = pd.DataFrame(
            {"Graduação": df_return.index, "Total": df_return.degreee_level})
        return df_return

    def get_salary_range(df, filter_data=""):
        if filter_data == "":
            df_return = pd.DataFrame(df["salary_range"].value_counts())
            df_return = pd.DataFrame(
                {"Faixa": df_return.index, "Total": df_return.salary_range})
            return df_return
        else:
            df_return = pd.DataFrame(
                df[df["job_situation"] == filter_data].salary_range.value_counts())
            df_return = pd.DataFrame(
                {"Faixa": df_return.index, "Total": df_return.salary_range})
            return df_return

    def get_job_situation(df):
        df_return = pd.DataFrame(df["job_situation"].value_counts())
        df_return = pd.DataFrame(
            {"Situação": df_return.index, "Total": df_return.job_situation})
        return df_return

    def get_gender(df):
        df_return = pd.DataFrame(df["gender"].value_counts())
        df_return = pd.DataFrame(
            {"Gênero": df_return.index, "Total": df_return.gender})
        return df_return
    
    def get_programming_language(df):
        df_return = pd.DataFrame(df["most_used_proggraming_languages"].value_counts())
        df_return = pd.DataFrame(
            {"Linguagem": df_return.index, "Total": df_return.most_used_proggraming_languages})
        return df_return

    def get_map_layers(df):
        df_return = pd.DataFrame(df["living_state"].value_counts())
        df_return = pd.DataFrame(
            {"estados": df_return.index, "total": df_return.living_state})

        # coordenadas dos estados, fonte: https://gist.github.com/ricardobeat/674646

        df_return['lat'] = df_return.estados.map(
            {"AC": -8.77, "AL": -9.71, "AM": -3.07, "AP":   1.41, "BA": -12.96,
             "CE": -3.71, "DF": -15.83, "Espírito Santo (ES)": -19.19,
             "GO": -16.64, "MA": -2.55, "MT": -12.64, "MS": -20.51, "Minas Gerais (MG)": -18.10,
             "PA": -5.53, "PB": -7.06, "Paraná (PR)": -24.89, "PE": -8.28, "PI": -8.28,
             "Rio de Janeiro (RJ)": -22.84, "RN": -5.22, "RO": -11.22, "Rio Grande do Sul (RS)": -30.01,
             "RR":   1.89, "Santa Catarina (SC)": -27.33, "SE": -10.90, "São Paulo (SP)": -23.55, "TO": -10.25})

        df_return['lon'] = df_return.estados.map(
            {"AC": -70.55, "AL": -35.73, "AM": -61.66, "AP": -51.77, "BA": -38.51,
             "CE": -38.54, "DF": -47.86, "Espírito Santo (ES)": -40.34,
             "GO": -49.31, "MA": -44.30, "MT": -55.42, "MS": -54.54, "Minas Gerais (MG)": -44.38,
             "PA": -52.29, "PB": -35.55, "Paraná (PR)": -51.55, "PE": -35.07, "PI": -43.68,
             "Rio de Janeiro (RJ)": -43.15, "RN": -36.52, "RO": -62.80, "Rio Grande do Sul (RS)": -51.22,
             "RR": -61.22, "Santa Catarina (SC)": -49.44, "SE": -37.07, "São Paulo (SP)": -46.64, "TO": -48.25
             })

        # layer = pdk.Layer(
        #     'ScatterplotLayer',
        #     data=df_return,
        #     get_position=['lon', 'lat'],
        #     auto_highlight=True,
        #     get_radius="[Total]",
        #     radius_scale=1.00,
        #     get_fill_color='[180, 0, 200, 140]',
        #     pickable=True,
        # )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_return,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[total]",
            pickable=True,
            radius_scale=200,
        )

        return layer
