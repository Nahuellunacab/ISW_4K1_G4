import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const obtenerActividades = async () => {
  const response = await apiClient.get('/actividades');
  return response.data;
};

export const obtenerHorarios = async (nombreActividad) => {
  const response = await apiClient.get(`/actividades/${nombreActividad}/horarios`);
  return response.data;
};

export const crearInscripcion = async (datosInscripcion) => {
  const response = await apiClient.post('/inscripciones', datosInscripcion);
  return response.data;
};

export default apiClient;
