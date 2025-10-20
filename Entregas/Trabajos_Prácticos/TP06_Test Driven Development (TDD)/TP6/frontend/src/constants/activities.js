export const activitiesData = {
  'Tirolesa': {
    description: 'Aventura y adrenalina recorriendo el parque desde las alturas.',
    requiresTalla: true,
    icon: '🧗',
    slots: [
      { time: '14:00 GMT-3', total: 10, booked: 8 },
      { time: '15:00 GMT-3', total: 10, booked: 8 },
      { time: '16:00 GMT-3', total: 10, booked: 5 },
    ]
  },
  'Safari': {
    description: 'Un recorrido guiado para descubrir la fauna más exótica.',
    requiresTalla: false,
    icon: '🦒',
    slots: [
      { time: '10:00 GMT-3', total: 20, booked: 15 },
      { time: '12:00 GMT-3', total: 20, booked: 18 },
      { time: '14:00 GMT-3', total: 20, booked: 20 },
    ]
  },
  'Palestra': {
    description: 'Desafía tus límites en nuestro muro de escalada para todas las edades.',
    requiresTalla: true,
    icon: '🧗‍♀️',
    slots: [
      { time: '09:30 GMT-3', total: 8, booked: 2 },
      { time: '11:30 GMT-3', total: 8, booked: 8 },
      { time: '13:30 GMT-3', total: 8, booked: 5 },
    ]
  },
  'Jardinería': {
    description: 'Conecta con la naturaleza en nuestro taller de jardinería sostenible.',
    requiresTalla: false,
    icon: '🌱',
    slots: [
      { time: '10:00 GMT-3', total: 15, booked: 12 },
      { time: '16:00 GMT-3', total: 15, booked: 10 },
    ]
  }
};
