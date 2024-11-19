const express = require("express");
const bodyParser = require("body-parser");
const { EAFCApiService } = require("eafc-clubs-api");

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post("/fetch-club-info", async (req, res) => {
  const { clubName, platform } = req.body;

  // Instância da API da EAFC
  const apiService = new EAFCApiService();

  try {
    // Validar parâmetros recebidos
    if (!clubName || !platform) {
      console.log("Erro: Nome do clube ou plataforma não fornecidos.");
      return res.status(400).json({ error: "Nome do clube e plataforma são obrigatórios." });
    }

    console.log(`Buscando clube: ${clubName} na plataforma: ${platform}`);

    // Buscar clubes com base no nome e plataforma
    const clubs = await apiService.searchClub({ clubName, platform });
    console.log("Resposta da busca de clubes:", clubs);

    if (!clubs || clubs.length === 0) {
      console.log(`Nenhum clube encontrado para o nome: ${clubName} na plataforma: ${platform}`);
      return res.status(404).json({ error: "Clube não encontrado." });
    }

    const clubId = clubs[0].clubId;
    console.log(`Clube encontrado. ID do Clube: ${clubId}`);

    // Buscar informações detalhadas do clube
    const clubInfo = await apiService.clubInfo({ clubIds: clubId, platform });
    console.log("Informações detalhadas do clube:", clubInfo);

    // Buscar estatísticas dos jogadores
    const memberStats = await apiService.memberStats({ clubId, platform });
    console.log("Estatísticas dos jogadores (raw):", memberStats);

    if (!memberStats || !memberStats.members || memberStats.members.length === 0) {
      console.log(`Nenhum jogador encontrado para o clube: ${clubName}`);
      return res.status(404).json({ error: "Nenhum jogador encontrado para este clube." });
    }

    // Processar estatísticas dos jogadores
    const players = memberStats.members.map((player) => ({
      name: player.name || "Desconhecido",
      level: player.proOverall || 0, // Nível do jogador
      goals: player.goals || 0,
      assists: player.assists || 0,
      matchesPlayed: player.gamesPlayed || 0,
      totalGames: player.gamesPlayed || 0, // Total de jogos como fallback para matchesPlayed
      motm: player.manOfTheMatch || 0, // Man of the Match
      averageRating: player.ratingAve || 0.0,
      favoritePosition: player.favoritePosition || "Desconhecida", // Posição favorita
      passRate: player.passSuccessRate || 0.0,
      shootRate: player.shotSuccessRate || 0.0,
      winRate: player.winRate || 0.0,
      tackles: player.tackleSuccessRate || 0.0,
    }));

    console.log("Jogadores processados:", players);

    // Análise do time
    const totalGoals = players.reduce((sum, p) => sum + p.goals, 0);
    const totalAssists = players.reduce((sum, p) => sum + p.assists, 0);
    const totalMatches = players.reduce((sum, p) => sum + p.matchesPlayed, 0);

    const analysis = {
      totalGoals,
      totalAssists,
      goalsPerMatch: totalMatches > 0 ? (totalGoals / totalMatches).toFixed(2) : 0,
      assistsPerMatch: totalMatches > 0 ? (totalAssists / totalMatches).toFixed(2) : 0,
      style: totalGoals > totalAssists ? "Forte no ataque" : "Equilibrado ou mais focado em assistências",
    };

    console.log("Análise do time:", analysis);

    // Retornar informações do clube, jogadores e análise
    return res.json({
      clubInfo,
      players,
      analysis,
    });
  } catch (error) {
    console.error("Erro ao buscar informações do clube:", error.message);
    console.error("Stacktrace:", error.stack);
    return res.status(500).json({ error: "Erro interno no servidor. Tente novamente mais tarde." });
  }
});

app.listen(port, () => {
  console.log(`API rodando em http://localhost:${port}`);
});
