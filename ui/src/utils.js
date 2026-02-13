
/**
 * Función genérica para llamar a la API
 * @param {string} endpoint - Endpoint de la API (ej: '/players')
 * @param {object} options - Opciones de fetch (method, body, headers, etc.)
 * @returns {Promise} - Datos de la respuesta o null si hay error
 */
export async function callApi(endpoint, options = {}) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    
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

    // Si hay body, convertirlo a JSON
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
    throw error; // Re-lanzar el error para que el componente pueda manejarlo
  }
}

/**
 * Obtiene los jugadores de un club y temporada
 * @param {string} club - Nombre del club (ej: 'boca juniors')
 * @param {string} temporada - Año de la temporada (ej: '2025')
 * @returns {Promise<Array>} - Lista de jugadores
 */
export async function getPlayers(club, temporada) {
  // Usa el endpoint /api/squad/{club}/{season} que devuelve { status, source, data: [...] }
  const response = await callApi(
    `/squad/${encodeURIComponent(club)}/${encodeURIComponent(temporada)}`
  )
  return response?.data || []
}

/**
 * Obtiene las transferencias (altas y bajas) de un club y temporada
 * @param {string} club - Nombre del club
 * @param {string} temporada - Año de la temporada
 * @returns {Promise<Object>} - Objeto con {altas: [], bajas: []}
 */
export async function getTransfers(club, season) {
  const url = "/api/transfers";

  const payload = {
    club,
    season,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const result = await response.json();
    console.log("Transferencias (altas/bajas):", result);

    return result; // { altas: [], bajas: [] }
  } catch (error) {
    console.error("Error obteniendo transferencias:", error);
    return { altas: [], bajas: [] };
  }
}

/**
 * Obtiene las valoraciones de los jugadores de un club y temporada
 * @param {string} club - Nombre del club
 * @param {string} temporada - Año de la temporada
 * @returns {Promise<Array>} - Lista de valoraciones
 */
export async function getValuations(club, season) {
  const url = "/api/transfers";

  const payload = {
    club,
    season,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resultado de simulación:", result);

    return result; // Ahora sí retornamos la respuesta del servidor
  } catch (error) {
    console.error("Error calculando ganancia:", error);
    return null;
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
      getValuations(club, temporada),
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

export async function getPlayerInfo({ nombre, club, season }){
  const url = "/api/playerInfo"
  const payload = { name: nombre, club, season }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resultado de simulación:", result);

    return result; // Ahora sí retornamos la respuesta del servidor
  } catch (error) {
    console.error("Error calculando ganancia:", error);
    return null;
  }
}


export async function getRevenue({ club, season, transfer_budget }) {
  const url = "/api/transfers/revenue";

  const payload = {
    club,
    season,
    transfer_budget: Number(transfer_budget),
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resultado de simulación:", result);

    return result; // Ahora sí retornamos la respuesta del servidor
  } catch (error) {
    console.error("Error calculando ganancia:", error);
    return null;
  }
}

export async function playerValuation({player, season, club}){
  const url = "/api/valuations";

  const payload = {
    club,
    season,
    player,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Error en la API: ${response.status}`);
    }

    const result = await response.json();
    console.log("Resultado de simulación:", result);

    return result; 
  } catch (error) {
    console.error("Error calculando ganancia:", error);
    return null;
  }
}


/**
 * Obtiene la lista de clubes disponibles
 * @returns {Promise<Array>} - Lista de clubes disponibles
 */
export async function getAvailableClubs() {
  return callApi('/clubs');
}

