# Sistema de Gestión de Clínica

## Ejecución

**Iniciar el sistema:**
```bash
python sistema_clinica.py
```

**Ejecutar pruebas:**
```bash
python sistema_clinica.py test
```

## Funcionalidades

- Gestión de pacientes y médicos
- Asignación de especialidades por días
- Agendamiento de turnos con validaciones
- Emisión de recetas médicas
- Consulta de historias clínicas

## Diseño

### Arquitectura
```
CLI → Clinica → Entidades (Paciente, Medico, Turno, etc.)
```

### Clases Principales
- **Clinica**: Lógica central y validaciones
- **ClinicaCLI**: Interfaz de usuario
- **Entidades**: Paciente, Medico, Turno, Receta, HistoriaClinica, Especialidad

### Características
- **Validaciones**: Previene duplicados, verifica disponibilidad
- **Encapsulación**: Atributos privados, acceso controlado
- **Manejo de errores**: Excepciones específicas y mensajes claros
- **Modularidad**: Separación clara de responsabilidades

### Flujo Típico
1. Registrar médicos y pacientes
2. Asignar especialidades a médicos
3. Agendar turnos (valida disponibilidad)
4. Emitir recetas
5. Consultar historias clínicas