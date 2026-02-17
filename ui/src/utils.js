const INTERNAL_API_BASE_URL = 'https://winning-black.vercel.app/api';
//const INTERNAL_API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Función genérica para llamar a la API
 * @param {string} endpoint - Endpoint de la API (ej: '/players')
 * @param {object} options - Opciones de fetch (method, body, headers, etc.)
 * @returns {Promise} - Datos de la respuesta o null si hay error
 */
export async function callApi(endpoint, options = {}) {
  try {
    const url = `${INTERNAL_API_BASE_URL}${endpoint}`;
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };
    
    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }
    const respuesta = await fetch(url, config);
    
    if (!respuesta.ok) {
      const errorData = await respuesta.json().catch(() => ({}));
      throw new Error(
        errorData.message || `Error en la petición: ${respuesta.status} ${respuesta.statusText}`
      );
    }

    const datos = await respuesta.json();
    return datos;
    
  } catch (error) {
    console.error("Hubo un problema con la petición:", error);
    throw error;
  }
}

/**
 * Obtiene los jugadores de un club y temporada
 * @param {string} club - Nombre del club (ej: 'boca juniors')
 * @param {string} temporada - Año de la temporada (ej: '2025')
 * @returns {Promise<Array>} - Lista de jugadores
 */
export async function getPlayers(club, temporada) {
  const response = await callApi(
    `/squad/${encodeURIComponent(club)}/${encodeURIComponent(temporada)}`
  )
  return response?.data || []
}

/**
* Obtiene las transferencias (altas y bajas) de un club y temporada
* @param {string} club - Nombre del club
* @param {string} season - Año de la temporada
* @returns {Promise<Object>} - Objeto con {altas: [], bajas: []}
*/
export async function getTransfers(club, season) {
  try {
    const result = await callApi("/transfers", {
      method: "POST",
      body: { club, season },
    });
    console.log("Transferencias (altas/bajas):", result);
    return result || { altas: [], bajas: [] };
  } catch (error) {
    console.error("Error obteniendo transferencias:", error);
    return { altas: [], bajas: [] };
  }
}



/**
 * Obtiene todos los datos de un club (jugadores, transferencias y valoraciones)
 * @param {string} club - Nombre del club
 * @param {string} temporada - Año de la temporada
 * @returns {Promise<Object>} - Objeto con players, transfers y valuations
 */
export async function getClubData(club, temporada) {
  try {
    const [players, transfers, valuations] = await Promise.all([
      getPlayers(club, temporada),
      getTransfers(club, temporada),
    ]);
    return {
      players,
      transfers,
      valuations,
    };
  } catch (error) {
    console.error('Error obteniendo datos del club:', error);
    throw error;
  }
}

export async function getPlayerInfo({ nombre, club, season }) {
  const payload = { name: nombre, club, season };

  try {
    const result = await callApi("/playerInfo", {
      method: "POST",
      body: payload,
    });

    console.log("Info de jugador:", result);
    return result; 
  } catch (error) {
    console.error("Error obteniendo info del jugador:", error);
    return null;
  }
}


export async function getRevenue({ club, season, transfer_budget }) {
  const payload = {
    club,
    season,
    transfer_budget: Number(transfer_budget),
  };

  try {
    const result = await callApi("/transfers/revenue", {
      method: "POST",
      body: payload,
    });

    console.log("Resultado de simulación:", result);
    return result;
  } catch (error) {
    console.error("Error calculando ganancia:", error);
    return null;
  }
}

export async function playerValuation({ player, season, club }) {
  const payload = {
    club,
    season,
    player,
  };

  try {
    const result = await callApi("/valuations", {
      method: "POST",
      body: payload,
    });

    console.log("Historial de valoraciones:", result);
    return result;
  } catch (error) {
    console.error("Error obteniendo valoraciones:", error);
    return null;
  }
}

export async function launchIngestion({ club, season }) {
  try {
    const result = await callApi(
      `/ingest/${encodeURIComponent(club)}/${encodeURIComponent(season)}`,
      { method: 'POST' },
    );
    console.log('Ingesta lanzada:', result);
    return result;
  } catch (error) {
    console.error('Error lanzando ingesta:', error);
    throw error;
  }
}
/**
 * Obtiene la lista de clubes disponibles
 * @returns {Promise<Array>} - Lista de clubes disponibles
 */
export async function getAvailableClubs() {
  return callApi('/clubs');
}



export async function queryAgent(question, history = []) {
  try {
    const payload = {
      question,
      history: history.map((m) => ({
        from_role: m.from,
        text: m.text,
      })),
    }

    const result = await callApi('/agent', {
      method: 'POST',
      body: payload,
    })

    return result
  } catch (error) {
    console.error('Error consultando al agente:', error)
    throw error
  }
}