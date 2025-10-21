import './PersonaForm.css';

function PersonaForm({
  persona, index, requiereVestimenta, onChange,
}) {
  const talles = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];

  const handleNombreChange = (e) => {
    const valor = e.target.value;
    // Solo permite letras, espacios, acentos y guiones
    const valorLimpio = valor.replace(/[0-9]/g, '');
    onChange(index, 'nombre', valorLimpio);
  };

  const handleDNIChange = (e) => {
    const valor = e.target.value;
    // Solo permite números y máximo 10 caracteres
    const valorLimpio = valor.replace(/[^0-9]/g, '').slice(0, 10);
    onChange(index, 'DNI', valorLimpio);
  };

  const handleEdadChange = (e) => {
    let valor = e.target.value;
    // Filtrar solo números, sin símbolos ni letras
    valor = valor.replace(/[^0-9]/g, '');
    
    // No permitir 0 como edad
    if (valor === '0' || valor === '00' || valor === '000') {
      valor = '';
    }
    
    // Limitar a 3 dígitos y máximo 120
    if (valor.length > 0) {
      const numValue = parseInt(valor, 10);
      if (numValue > 120) {
        valor = '120';
      }
    }
    
    onChange(index, 'edad', valor);
  };

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
              onChange={handleNombreChange}
              placeholder="Ej: Juan Pérez"
              pattern="[A-Za-zÀ-ÿ\s\-']+"
              title="Solo se permiten letras, espacios y guiones"
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
              onChange={handleDNIChange}
              placeholder="Ej: 12345678"
              pattern="[0-9]{6,10}"
              title="Debe contener entre 6 y 10 números"
              minLength="6"
              maxLength="10"
              required
            />
            <small className="helper-text-dni">
              Entre 6 y 10 números
            </small>
          </label>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor={`edad-${index}`}>
            Edad *
            <input
              id={`edad-${index}`}
              type="text"
              inputMode="numeric"
              value={persona.edad}
              onChange={handleEdadChange}
              placeholder="Ej: 25"
              pattern="[1-9][0-9]?|1[01][0-9]|120"
              title="Edad debe ser un número entre 1 y 120"
              maxLength="3"
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
