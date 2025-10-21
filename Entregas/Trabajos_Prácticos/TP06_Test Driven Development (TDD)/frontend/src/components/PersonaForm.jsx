import './PersonaForm.css';

function PersonaForm({
  persona, index, requiereVestimenta, onChange,
}) {
  const talles = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];

  return (
    <div className="persona-form">
      <h4>
        Persona
        {' '}
        {index + 1}
      </h4>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor={`nombre-${index}`}>
            Nombre Completo *
            <input
              id={`nombre-${index}`}
              type="text"
              value={persona.nombre}
              onChange={(e) => onChange(index, 'nombre', e.target.value)}
              placeholder="Ej: Juan Pérez"
              required
            />
          </label>
        </div>

        <div className="form-group">
          <label htmlFor={`dni-${index}`}>
            DNI *
            <input
              id={`dni-${index}`}
              type="text"
              value={persona.DNI}
              onChange={(e) => onChange(index, 'DNI', e.target.value)}
              placeholder="Ej: 12345678"
              required
            />
          </label>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor={`edad-${index}`}>
            Edad *
            <input
              id={`edad-${index}`}
              type="number"
              min="0"
              max="120"
              value={persona.edad}
              onChange={(e) => onChange(index, 'edad', e.target.value)}
              placeholder="Ej: 25"
              required
            />
          </label>
        </div>

        {requiereVestimenta && (
          <div className="form-group">
            <label htmlFor={`talla-${index}`}>
              Talla de Vestimenta *
              <select
                id={`talla-${index}`}
                value={persona.tallaVestimenta}
                onChange={(e) => onChange(index, 'tallaVestimenta', e.target.value)}
                required
              >
                <option value="">Seleccione una talla</option>
                {talles.map((talla) => (
                  <option key={talla} value={talla}>
                    {talla}
                  </option>
                ))}
              </select>
            </label>
          </div>
        )}
      </div>
    </div>
  );
}

export default PersonaForm;
