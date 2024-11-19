const { EAFCApiService } = require('eafc-clubs-api');

// Inicializa o serviço da API
const apiService = new EAFCApiService();

// Função para buscar o ID do clube pelo nome
const searchClub = async (clubName, platform) => {
  try {
    console.log(`Buscando o clube: ${clubName} na plataforma: ${platform}`);
    const clubs = await apiService.searchClub({ clubName, platform });

    if (clubs.length > 0) {
      const clubId = clubs[0].clubId;
      console.log(`ID do clube '${clubName}': ${clubId}`);
      return clubId;
    } else {
      console.error(`Clube '${clubName}' não encontrado na plataforma '${platform}'.`);
      return null;
    }
  } catch (error) {
    console.error('Erro ao buscar o clube:', error.message);
    return null;
  }
};

// Função para buscar informações detalhadas do clube pelo ID
const fetchClubInfo = async (clubId, platform) => {
  try {
    console.log(`Buscando informações do clube com ID: ${clubId} na plataforma: ${platform}`);
    const clubInfo = await apiService.clubInfo({ clubIds: clubId, platform });

    if (clubInfo && typeof clubInfo === 'object') {
      console.log('Informações do Clube:', JSON.stringify(clubInfo, null, 2));
    } else {
      console.error('Resposta inesperada:', clubInfo);
    }
  } catch (error) {
    console.error('Erro ao buscar informações do clube:', error.message);
  }
};

// Função principal para executar as etapas
const main = async () => {
  const clubName = 'EC Paraguaio'; // Nome do clube a ser buscado
  const platform = 'common-gen5'; // Plataforma (ex: common-gen5, common-gen4, etc.)

  // 1. Buscar o ID do clube pelo nome
  const clubId = await searchClub(clubName, platform);

  // 2. Buscar informações detalhadas do clube pelo ID
  if (clubId) {
    await fetchClubInfo(clubId, platform);
  } else {
    console.error('Não foi possível obter o ID do clube. Verifique os dados e tente novamente.');
  }
};

// Executa o script
main();
