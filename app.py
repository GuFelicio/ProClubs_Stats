import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configurações da página
st.set_page_config(page_title="Estatísticas do Clube", layout="wide")

st.title("Estatísticas do Clube")

# Formulário para entrada de dados
with st.form("club_form"):
    club_name = st.text_input("Nome do Clube:", placeholder="Digite o nome do clube...")
    platform = st.selectbox("Plataforma:", ["common-gen5", "common-gen4", "nx"], index=0)
    submit = st.form_submit_button("Buscar Informações")

if submit:
    if club_name:
        # Faz requisição ao servidor Node.js
        api_url = "https://proclubs-stats.onrender.com/fetch-club-info"
        payload = {"clubName": club_name, "platform": platform}

        with st.spinner("Buscando informações..."):
            try:
                response = requests.post(api_url, json=payload)

                if response.status_code == 200:
                    data = response.json()

                    # Exibir informações do clube
                    st.header(f"Estatísticas do Clube: {club_name}")
                    club_info = data.get("clubInfo", {})
                    st.subheader("Informações do Clube")
                    st.write(f"**Nome:** {club_info.get('name', '-')}")
                    st.write(f"**ID do Clube:** {club_info.get('clubId', '-')}")

                    # Exibir análise do time
                    analysis = data.get("analysis", {})
                    st.subheader("Análise do Time")
                    st.write(f"**Total de Gols:** {analysis.get('totalGoals', 0)}")
                    st.write(f"**Total de Assistências:** {analysis.get('totalAssists', 0)}")
                    st.write(f"**Gols por Partida:** {analysis.get('goalsPerMatch', 0)}")
                    st.write(f"**Assistências por Partida:** {analysis.get('assistsPerMatch', 0)}")
                    st.write(f"**Estilo de Jogo:** {analysis.get('style', '-')}")

                    # Exibir informações dos jogadores
                    players = data.get("players", [])
                    if players:
                        player_df = pd.DataFrame(players)

                        # Exibir informações dos jogadores
                    players = data.get("players", [])
                    if players:
                        st.subheader("Jogadores")
                        cols = st.columns(3)  # Cria 3 colunas por linha

                        for idx, player in enumerate(players):
                            col = cols[idx % 3]  # Alterna entre as colunas
                            with col:
                                # Função para garantir conversão de strings para números
                                def safe_to_int(value):
                                    try:
                                        return int(value)
                                    except (ValueError, TypeError):
                                        return 0

                                def safe_to_float(value):
                                    try:
                                        return float(value)
                                    except (ValueError, TypeError):
                                        return 0.0

                                # Garantir que os valores estejam no formato correto
                                name = player.get("name", "Desconhecido")
                                favorite_position = player.get("favoritePosition", "Desconhecida")
                                goals = safe_to_int(player.get("goals", 0))
                                assists = safe_to_int(player.get("assists", 0))
                                matches_played = safe_to_int(player.get("totalGames", 0))
                                total_games = safe_to_int(player.get("totalGames", matches_played))
                                motm = safe_to_int(player.get("motm", 0))
                                average_rating = safe_to_float(player.get("averageRating", 0.0))
                                level = safe_to_int(player.get("level", 0))
                                passSuccess = safe_to_int(player.get("passRate", 0.0))
                                winRate = safe_to_int(player.get("winRate", 0.0))
                                tackles = safe_to_int(player.get("tackles", 0.0))


                                # Cálculo de G+A por jogo
                                games_played = matches_played if matches_played > 0 else 1
                                ga_per_game = round((goals + assists) / games_played, 2)

                                # Exibir informações do jogador
                                st.markdown(f"### {name}")
                                st.markdown(f"**📌 Posição Preferida:** {favorite_position}")
                                st.markdown(f"**🔢 Overall:** {level}")
                                st.markdown(f"**⚽ Gols:** {goals}")
                                st.markdown(f"**🅰️ Assistências:** {assists}")
                                st.markdown(f"**🎮 Jogos Disputados:** {total_games}")
                                st.markdown(f"**📈 Total de Jogos:** {total_games}")
                                st.markdown(f"**📊 G+A por Jogo:** {ga_per_game}")
                                st.markdown(f"**🏆 Man of the Match:** {motm}")
                                st.markdown(f"**⭐ Nota Média:** {average_rating}")
                                st.markdown(f"**📋 Porcentagem de passe certo:**{passSuccess}**%**")
                                st.markdown(f"**😡 Porcentagem de ações defensivas certas:**{tackles}**%**")
                                st.markdown(f"**✅ Win Rate:** {winRate}**%**")



                        # Garantir que os valores numéricos estejam corretos
                        numeric_columns = [
                            "goals",
                            "assists",
                            "matchesPlayed",
                            "passRate",
                            "winRate",
                            "averageRating",
                            "tackles",
                        ]
                        for col in numeric_columns:
                            player_df[col] = pd.to_numeric(player_df[col], errors="coerce").fillna(0)

                        # Cálculo de G+A por jogo
                        player_df["ga_per_game"] = player_df.apply(
                            lambda row: (row["goals"] + row["assists"]) / row["matchesPlayed"]
                            if row["matchesPlayed"] > 0 else 0,
                            axis=1
                        )

                        # Adicionar gráficos
                        st.subheader("Gráficos Estatísticos")
                        chart_cols = st.columns(3)  # Dividir os gráficos em 3 colunas por linha

                        # Gráfico de Gols e Assistências por Jogador
                        with chart_cols[0]:
                            st.markdown("### Gols e Assistências por Jogador")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y=["goals", "assists"], ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                        # Gráfico de Taxa de Passes Certos por Jogador
                        with chart_cols[1]:
                            st.markdown("### Taxa de Passes Certos (%)")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y="passRate", color="orange", ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                        # Gráfico de Taxa de Vitória por Jogador
                        with chart_cols[2]:
                            st.markdown("### Taxa de Vitória (%)")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y="winRate", color="green", ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                        chart_cols = st.columns(3)

                        # Gráfico de G+A por Jogo
                        with chart_cols[0]:
                            st.markdown("### G+A por Jogo")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y="ga_per_game", color="purple", ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                        # Gráfico de Nota Média por Jogador
                        with chart_cols[1]:
                            st.markdown("### Nota Média por Jogador")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y="averageRating", color="red", ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                        # Gráfico de Contribuição Total (Gols + Assistências)
                        with chart_cols[2]:
                            st.markdown("### Contribuição Total (Gols + Assistências)")
                            fig, ax = plt.subplots()
                            player_df["totalContribution"] = player_df["goals"] + player_df["assists"]
                            player_df.plot.bar(x="name", y="totalContribution", color="blue", ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                           # Gráfico de Ações defensivas
                        with chart_cols[0]:
                            st.markdown("### Ações defensivas por jogador")
                            fig, ax = plt.subplots()
                            player_df.plot.bar(x="name", y=["tackles"], ax=ax, figsize=(6, 4))
                            st.pyplot(fig)

                    else:
                        st.warning("Nenhum jogador encontrado para o time.")

                elif response.status_code == 404:
                    st.error("Clube não encontrado.")
                else:
                    st.error(f"Erro ao buscar informações: {response.json().get('error')}")

            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")
    else:
        st.warning("Por favor, insira o nome do clube.")

    st.markdown("Feito por Gustavo Felício")
