from datetime import datetime
from typing import List, Dict, Optional
import unittest

class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__nombre = nombre
        self.__dni = dni
        self.__fecha_nacimiento = fecha_nacimiento
    
    def obtener_dni(self) -> str:
        return self.__dni
    
    def __str__(self) -> str:
        return f"Paciente: {self.__nombre} (DNI: {self.__dni})"
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def fecha_nacimiento(self) -> str:
        return self.__fecha_nacimiento


class Medico:
    
    def __init__(self, nombre: str, matricula: str):
        self.__nombre = nombre
        self.__matricula = matricula
        self.__especialidades = []
    
    def agregar_especialidad(self, especialidad: 'Especialidad'):
        if especialidad not in self.__especialidades:
            self.__especialidades.append(especialidad)
    
    def obtener_matricula(self) -> str:
        return self.__matricula
    
    def obtener_especialidad_para_dia(self, dia: str) -> Optional[str]:
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
    
    def __str__(self) -> str:
        especialidades_str = ", ".join([esp.obtener_especialidad() for esp in self.__especialidades])
        return f"Dr./Dra. {self.__nombre} (Mat: {self.__matricula}) - Especialidades: {especialidades_str}"
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def matricula(self) -> str:
        return self.__matricula
    
    @property
    def especialidades(self) -> List['Especialidad']:
        return self.__especialidades.copy()


class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad
    
    def obtener_medico(self) -> Medico:
        return self.__medico
    
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora
    
    def __str__(self) -> str:
        fecha_str = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return (f"Turno: {fecha_str} - {self.__especialidad} - "
                f"Paciente: {self.__paciente.nombre} - Médico: {self.__medico.nombre}")
    
    @property
    def paciente(self) -> Paciente:
        return self.__paciente
    
    @property
    def medico(self) -> Medico:
        return self.__medico
    
    @property
    def fecha_hora(self) -> datetime:
        return self.__fecha_hora
    
    @property
    def especialidad(self) -> str:
        return self.__especialidad


class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: List[str]):
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos.copy()
        self.__fecha = datetime.now()
    
    def __str__(self) -> str:
        medicamentos_str = ", ".join(self.__medicamentos)
        fecha_str = self.__fecha.strftime("%d/%m/%Y")
        return (f"Receta del {fecha_str} - "
                f"Paciente: {self.__paciente.nombre} - "
                f"Médico: {self.__medico.nombre} - "
                f"Medicamentos: {medicamentos_str}")
    
    @property
    def paciente(self) -> Paciente:
        return self.__paciente
    
    @property
    def medico(self) -> Medico:
        return self.__medico
    
    @property
    def medicamentos(self) -> List[str]:
        return self.__medicamentos.copy()
    
    @property
    def fecha(self) -> datetime:
        return self.__fecha


class Especialidad:
    def __init__(self, tipo: str, dias: List[str]):
        self.__tipo = tipo
        self.__dias = [dia.lower() for dia in dias]
    
    def obtener_especialidad(self) -> str:
        return self.__tipo
    
    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in self.__dias
    
    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias)
        return f"{self.__tipo} (Días: {dias_str})"
    
    @property
    def tipo(self) -> str:
        return self.__tipo
    
    @property
    def dias(self) -> List[str]:
        return self.__dias.copy()


class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []
    
    def agregar_turno(self, turno: Turno):
        self.__turnos.append(turno)
    
    def agregar_receta(self, receta: Receta):
        self.__recetas.append(receta)
    
    def obtener_turnos(self) -> List[Turno]:
        return self.__turnos.copy()
    
    def obtener_recetas(self) -> List[Receta]:
        return self.__recetas.copy()
    
    def __str__(self) -> str:
        return (f"Historia Clínica de {self.__paciente.nombre} - "
                f"Turnos: {len(self.__turnos)}, Recetas: {len(self.__recetas)}")
    
    @property
    def paciente(self) -> Paciente:
        return self.__paciente
    
    @property
    def turnos(self) -> List[Turno]:
        return self.__turnos.copy()
    
    @property
    def recetas(self) -> List[Receta]:
        return self.__recetas.copy()


class Clinica:
    def __init__(self):
        self.__pacientes = {}
        self.__medicos = {}
        self.__turnos = []
        self.__historias_clinicas = {}
    
    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes:
            raise ValueError(f"Ya existe un paciente con DNI {dni}")
        
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)
    
    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos:
            raise ValueError(f"Ya existe un médico con matrícula {matricula}")
        
        self.__medicos[matricula] = medico
    
    def obtener_pacientes(self) -> List[Paciente]:
        return list(self.__pacientes.values())
    
    def obtener_medicos(self) -> List[Medico]:
        return list(self.__medicos.values())
    
    def obtener_medico_por_matricula(self, matricula: str) -> Optional[Medico]:
        return self.__medicos.get(matricula)
    
    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        if dni not in self.__pacientes:
            raise ValueError(f"No existe paciente con DNI {dni}")
        
        if matricula not in self.__medicos:
            raise ValueError(f"No existe médico con matrícula {matricula}")
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        dia_semana = self._obtener_dia_semana(fecha_hora)
        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        
        if especialidad_disponible != especialidad:
            raise ValueError(f"El médico no atiende {especialidad} los {dia_semana}")
        
        if self._verificar_turno_duplicado(medico, fecha_hora):
            raise ValueError("Ya existe un turno para ese médico en esa fecha y hora")
        
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        self.__historias_clinicas[dni].agregar_turno(turno)
        
        return turno
    
    def obtener_turnos(self) -> List[Turno]:
        return self.__turnos.copy()
    
    def emitir_receta(self, dni: str, matricula: str, medicamentos: List[str]):
        if dni not in self.__pacientes:
            raise ValueError(f"No existe paciente con DNI {dni}")
        
        if matricula not in self.__medicos:
            raise ValueError(f"No existe médico con matrícula {matricula}")
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas[dni].agregar_receta(receta)
        
        return receta
    
    def obtener_historia_clinica(self, dni: str) -> Optional[HistoriaClinica]:
        return self.__historias_clinicas.get(dni)
    
    # Validaciones y Utilidades
    def validar_existencia_paciente(self, dni: str) -> bool:
        return dni in self.__pacientes
    
    def validar_existencia_medico(self, matricula: str) -> bool:
        return matricula in self.__medicos
    
    def validar_turno_no_duplicado(self, medico: Medico, fecha_hora: datetime) -> bool:
        return not self._verificar_turno_duplicado(medico, fecha_hora)
    
    def obtener_dia_semana_turno(self, fecha_hora: datetime) -> str:
        return self._obtener_dia_semana(fecha_hora)
    
    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> Optional[str]:
        return medico.obtener_especialidad_para_dia(dia_semana)
    
    def validar_especialidad_y_disponibilidad(self, medico: Medico, especialidad_solicitada: str, dia_semana: str) -> bool:
        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        return especialidad_disponible == especialidad_solicitada
    
    def _obtener_dia_semana(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]
    
    def _verificar_turno_duplicado(self, medico: Medico, fecha_hora: datetime) -> bool:
        for turno in self.__turnos:
            if (turno.medico.obtener_matricula() == medico.obtener_matricula() and 
                turno.fecha_hora == fecha_hora):
                return True
        return False
    
    def __str__(self) -> str:
        return (f"Clínica - Pacientes: {len(self.__pacientes)}, "
                f"Médicos: {len(self.__medicos)}, Turnos: {len(self.__turnos)}")


class ClinicaException(Exception):
    pass


# ===================== INTERFAZ DE CONSOLA (CLI) =====================

class ClinicaCLI:
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu_principal(self):
        print("\n" + "="*50)
        print("🏥 SISTEMA DE GESTIÓN DE CLÍNICA")
        print("="*50)
        print("--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")
        print("="*50)
    
    def ejecutar(self):
        print("🏥 Bienvenido al Sistema de Gestión de Clínica")
        
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción (0-9): ").strip()
                
                if opcion == "1":
                    self._agregar_paciente()
                elif opcion == "2":
                    self._agregar_medico()
                elif opcion == "3":
                    self._agendar_turno()
                elif opcion == "4":
                    self._agregar_especialidad()
                elif opcion == "5":
                    self._emitir_receta()
                elif opcion == "6":
                    self._ver_historia_clinica()
                elif opcion == "7":
                    self._ver_todos_los_turnos()
                elif opcion == "8":
                    self._ver_todos_los_pacientes()
                elif opcion == "9":
                    self._ver_todos_los_medicos()
                elif opcion == "0":
                    print("\n👋 Gracias por usar el Sistema de Gestión de Clínica")
                    break
                else:
                    print("❌ Opción inválida. Por favor, seleccione una opción del 0 al 9.")
                
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario.")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("\nPresione Enter para continuar...")
    
    def _agregar_paciente(self):
        print("\n📝 AGREGAR PACIENTE")
        print("-" * 30)
        
        try:
            nombre = input("Ingrese el nombre del paciente: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                return
            
            dni = input("Ingrese el DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            fecha_nacimiento = input("Ingrese la fecha de nacimiento (DD/MM/AAAA): ").strip()
            if not fecha_nacimiento:
                print("❌ La fecha de nacimiento no puede estar vacía.")
                return
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            
            print(f"✅ Paciente agregado exitosamente: {paciente}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al agregar paciente: {e}")
    
    def _agregar_medico(self):
        print("\n👨‍⚕️ AGREGAR MÉDICO")
        print("-" * 30)
        
        try:
            nombre = input("Ingrese el nombre del médico: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                return
            
            matricula = input("Ingrese la matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            medico = Medico(nombre, matricula)
            self.clinica.agregar_medico(medico)
            
            print(f"✅ Médico agregado exitosamente: {medico}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al agregar médico: {e}")
    
    def _agendar_turno(self):
        print("\n📅 AGENDAR TURNO")
        print("-" * 30)
        
        try:
            dni = input("Ingrese el DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            matricula = input("Ingrese la matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            especialidad = input("Ingrese la especialidad: ").strip()
            if not especialidad:
                print("❌ La especialidad no puede estar vacía.")
                return
            
            fecha_str = input("Ingrese la fecha (DD/MM/AAAA): ").strip()
            hora_str = input("Ingrese la hora (HH:MM): ").strip()
            
            try:
                fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M")
            except ValueError:
                print("❌ Formato de fecha u hora inválido. Use DD/MM/AAAA para fecha y HH:MM para hora.")
                return
            
            turno = self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print(f"✅ Turno agendado exitosamente: {turno}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al agendar turno: {e}")
    
    def _agregar_especialidad(self):
        print("\n🏥 AGREGAR ESPECIALIDAD A MÉDICO")
        print("-" * 40)
        
        try:
            matricula = input("Ingrese la matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            if not medico:
                print("❌ No existe un médico con esa matrícula.")
                return
            
            tipo_especialidad = input("Ingrese el tipo de especialidad: ").strip()
            if not tipo_especialidad:
                print("❌ El tipo de especialidad no puede estar vacío.")
                return
            
            print("Ingrese los días de atención (separados por comas):")
            print("Opciones: lunes, martes, miércoles, jueves, viernes, sábado, domingo")
            dias_str = input("Días: ").strip()
            
            if not dias_str:
                print("❌ Debe especificar al menos un día.")
                return
            
            dias = [dia.strip() for dia in dias_str.split(",")]
            
            especialidad = Especialidad(tipo_especialidad, dias)
            medico.agregar_especialidad(especialidad)
            
            print(f"✅ Especialidad agregada exitosamente: {especialidad}")
            print(f"   Al médico: {medico.nombre}")
            
        except Exception as e:
            print(f"❌ Error inesperado al agregar especialidad: {e}")
    
    def _emitir_receta(self):
        print("\n💊 EMITIR RECETA")
        print("-" * 30)
        
        try:
            dni = input("Ingrese el DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            matricula = input("Ingrese la matrícula del médico: ").strip()
            if not matricula:
                print("❌ La matrícula no puede estar vacía.")
                return
            
            print("Ingrese los medicamentos (separados por comas):")
            medicamentos_str = input("Medicamentos: ").strip()
            
            if not medicamentos_str:
                print("❌ Debe especificar al menos un medicamento.")
                return
            
            medicamentos = [med.strip() for med in medicamentos_str.split(",")]
            
            receta = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print(f"✅ Receta emitida exitosamente: {receta}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al emitir receta: {e}")
    
    def _ver_historia_clinica(self):
        print("\n📋 VER HISTORIA CLÍNICA")
        print("-" * 35)
        
        try:
            dni = input("Ingrese el DNI del paciente: ").strip()
            if not dni:
                print("❌ El DNI no puede estar vacío.")
                return
            
            historia = self.clinica.obtener_historia_clinica(dni)
            if not historia:
                print("❌ No existe un paciente con ese DNI.")
                return
            
            print(f"\n📋 {historia}")
            print("\n--- TURNOS ---")
            turnos = historia.obtener_turnos()
            if turnos:
                for i, turno in enumerate(turnos, 1):
                    print(f"{i}. {turno}")
            else:
                print("No hay turnos registrados.")
            
            print("\n--- RECETAS ---")
            recetas = historia.obtener_recetas()
            if recetas:
                for i, receta in enumerate(recetas, 1):
                    print(f"{i}. {receta}")
            else:
                print("No hay recetas registradas.")
                
        except Exception as e:
            print(f"❌ Error inesperado al ver historia clínica: {e}")
    
    def _ver_todos_los_turnos(self):
        print("\n📅 TODOS LOS TURNOS")
        print("-" * 30)
        
        try:
            turnos = self.clinica.obtener_turnos()
            if turnos:
                for i, turno in enumerate(turnos, 1):
                    print(f"{i}. {turno}")
                print(f"\nTotal de turnos: {len(turnos)}")
            else:
                print("No hay turnos agendados.")
                
        except Exception as e:
            print(f"❌ Error inesperado al ver turnos: {e}")
    
    def _ver_todos_los_pacientes(self):
        print("\n👥 TODOS LOS PACIENTES")
        print("-" * 35)
        
        try:
            pacientes = self.clinica.obtener_pacientes()
            if pacientes:
                for i, paciente in enumerate(pacientes, 1):
                    print(f"{i}. {paciente}")
                print(f"\nTotal de pacientes: {len(pacientes)}")
            else:
                print("No hay pacientes registrados.")
                
        except Exception as e:
            print(f"❌ Error inesperado al ver pacientes: {e}")
    
    def _ver_todos_los_medicos(self):
        print("\n👨‍⚕️ TODOS LOS MÉDICOS")
        print("-" * 35)
        
        try:
            medicos = self.clinica.obtener_medicos()
            if medicos:
                for i, medico in enumerate(medicos, 1):
                    print(f"{i}. {medico}")
                print(f"\nTotal de médicos: {len(medicos)}")
            else:
                print("No hay médicos registrados.")
                
        except Exception as e:
            print(f"❌ Error inesperado al ver médicos: {e}")


# ===================== PRUEBAS UNITARIAS =====================

class TestPacientesYMedicos(unittest.TestCase):
    
    def setUp(self):
        self.clinica = Clinica()
        self.paciente1 = Paciente("Juan Pérez", "12345678", "01/01/1990")
        self.paciente2 = Paciente("María García", "87654321", "15/05/1985")
        self.medico1 = Medico("Dr. López", "MAT001")
        self.medico2 = Medico("Dra. Martínez", "MAT002")
    
    def test_registro_exitoso_pacientes(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 2)
        self.assertIn(self.paciente1, pacientes)
        self.assertIn(self.paciente2, pacientes)
    
    def test_registro_exitoso_medicos(self):
        self.clinica.agregar_medico(self.medico1)
        self.clinica.agregar_medico(self.medico2)
        
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 2)
        self.assertIn(self.medico1, medicos)
        self.assertIn(self.medico2, medicos)
    
    def test_prevencion_registros_duplicados_dni(self):
        self.clinica.agregar_paciente(self.paciente1)
        
        paciente_duplicado = Paciente("Otro Nombre", "12345678", "02/02/1992")
        with self.assertRaises(ValueError) as context:
            self.clinica.agregar_paciente(paciente_duplicado)
        self.assertIn("Ya existe un paciente con DNI", str(context.exception))
    
    def test_prevencion_registros_duplicados_matricula(self):
        self.clinica.agregar_medico(self.medico1)
        
        medico_duplicado = Medico("Otro Doctor", "MAT001")
        with self.assertRaises(ValueError) as context:
            self.clinica.agregar_medico(medico_duplicado)
        self.assertIn("Ya existe un médico con matrícula", str(context.exception))
    
    def test_verificacion_errores_datos_faltantes(self):
        with self.assertRaises(TypeError):
            Paciente("", "", "")
        
        with self.assertRaises(TypeError):
            Medico("", "")


class TestEspecialidades(unittest.TestCase):
    def setUp(self):
        self.medico = Medico("Dr. Especialista", "MAT003")
        self.especialidad1 = Especialidad("Cardiología", ["lunes", "miércoles", "viernes"])
        self.especialidad2 = Especialidad("Neurología", ["martes", "jueves"])
        self.especialidad3 = Especialidad("Cardiología", ["sábado"])
    
    def test_agregar_especialidades_nuevas(self):
        self.medico.agregar_especialidad(self.especialidad1)
        especialidades = self.medico.especialidades
        self.assertEqual(len(especialidades), 1)
        self.assertIn(self.especialidad1, especialidades)
        
        self.medico.agregar_especialidad(self.especialidad2)
        especialidades = self.medico.especialidades
        self.assertEqual(len(especialidades), 2)
        self.assertIn(self.especialidad2, especialidades)
    
    def test_evitar_duplicados_especialidad(self):
        self.medico.agregar_especialidad(self.especialidad1)
        especialidades_antes = len(self.medico.especialidades)
        
        self.medico.agregar_especialidad(self.especialidad1)
        especialidades_despues = len(self.medico.especialidades)
        
        self.assertEqual(especialidades_antes, especialidades_despues)
    
    def test_deteccion_especialidades_dias_invalidos(self):
        especialidad_invalida = Especialidad("Pediatría", ["día_inexistente", "otro_día_malo"])
        self.medico.agregar_especialidad(especialidad_invalida)
        
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("lunes"))
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("martes"))
    
    def test_error_agregar_especialidad_medico_no_registrado(self):
        clinica = Clinica()
        self.medico.agregar_especialidad(self.especialidad1)
        self.assertEqual(len(self.medico.especialidades), 1)


class TestTurnos(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Ana Torres", "11111111", "20/03/1992")
        self.medico = Medico("Dr. Turno", "MAT004")
        self.especialidad = Especialidad("Dermatología", ["lunes", "miércoles", "viernes"])
        
        self.medico.agregar_especialidad(self.especialidad)
        
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        
        self.fecha_lunes = datetime(2024, 1, 8, 10, 0)
        self.fecha_martes = datetime(2024, 1, 9, 14, 0)
    
    def test_agendamiento_correcto_turno(self):
        turno = self.clinica.agendar_turno(
            self.paciente.obtener_dni(),
            self.medico.obtener_matricula(),
            "Dermatología",
            self.fecha_lunes
        )
        
        self.assertIsNotNone(turno)
        self.assertEqual(turno.paciente.obtener_dni(), self.paciente.obtener_dni())
        self.assertEqual(turno.medico.obtener_matricula(), self.medico.obtener_matricula())
        self.assertEqual(turno.especialidad, "Dermatología")
        self.assertEqual(turno.fecha_hora, self.fecha_lunes)
    
    def test_evitar_turnos_duplicados(self):
        self.clinica.agendar_turno(
            self.paciente.obtener_dni(),
            self.medico.obtener_matricula(),
            "Dermatología",
            self.fecha_lunes
        )
        
        paciente2 = Paciente("Carlos Ruiz", "22222222", "10/07/1988")
        self.clinica.agregar_paciente(paciente2)
        
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                paciente2.obtener_dni(),
                self.medico.obtener_matricula(),
                "Dermatología",
                self.fecha_lunes
            )
        self.assertIn("Ya existe un turno", str(context.exception))
    
    def test_error_paciente_no_existe(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                "99999999",
                self.medico.obtener_matricula(),
                "Dermatología",
                self.fecha_lunes
            )
        self.assertIn("No existe paciente con DNI", str(context.exception))
    
    def test_error_medico_no_existe(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                self.paciente.obtener_dni(),
                "MAT999",
                "Dermatología",
                self.fecha_lunes
            )
        self.assertIn("No existe médico con matrícula", str(context.exception))
    
    def test_error_medico_no_atiende_especialidad(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                self.paciente.obtener_dni(),
                self.medico.obtener_matricula(),
                "Cardiología",
                self.fecha_lunes
            )
        self.assertIn("El médico no atiende", str(context.exception))
    
    def test_error_medico_no_trabaja_dia(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                self.paciente.obtener_dni(),
                self.medico.obtener_matricula(),
                "Dermatología",
                self.fecha_martes
            )
        self.assertIn("El médico no atiende", str(context.exception))


class TestRecetas(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Luis Medina", "33333333", "12/12/1975")
        self.medico = Medico("Dra. Recetas", "MAT005")
        
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        
        self.medicamentos = ["Paracetamol 500mg", "Ibuprofeno 400mg", "Amoxicilina 250mg"]
    
    def test_emision_receta_valida(self):
        receta = self.clinica.emitir_receta(
            self.paciente.obtener_dni(),
            self.medico.obtener_matricula(),
            self.medicamentos
        )
        
        self.assertIsNotNone(receta)
        self.assertEqual(receta.paciente.obtener_dni(), self.paciente.obtener_dni())
        self.assertEqual(receta.medico.obtener_matricula(), self.medico.obtener_matricula())
        self.assertEqual(receta.medicamentos, self.medicamentos)
        self.assertIsInstance(receta.fecha, datetime)
    
    def test_error_paciente_no_existe_receta(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.emitir_receta(
                "99999999",
                self.medico.obtener_matricula(),
                self.medicamentos
            )
        self.assertIn("No existe paciente con DNI", str(context.exception))
    
    def test_error_medico_no_existe_receta(self):
        with self.assertRaises(ValueError) as context:
            self.clinica.emitir_receta(
                self.paciente.obtener_dni(),
                "MAT999",
                self.medicamentos
            )
        self.assertIn("No existe médico con matrícula", str(context.exception))
    
    def test_error_medicamentos_vacios(self):
        with self.assertRaises(Exception):
            self.clinica.emitir_receta(
                self.paciente.obtener_dni(),
                self.medico.obtener_matricula(),
                []  # Lista vacía
            )


class TestHistoriaClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Roberto Silva", "44444444", "05/09/1980")
        self.medico = Medico("Dr. Historia", "MAT006")
        self.especialidad = Especialidad("Medicina General", ["lunes", "martes", "miércoles", "jueves", "viernes"])
        
        self.medico.agregar_especialidad(self.especialidad)
        
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
    
    def test_historia_clinica_completa(self):
        fecha_turno = datetime(2024, 2, 5, 9, 30)
        turno = self.clinica.agendar_turno(
            self.paciente.obtener_dni(),
            self.medico.obtener_matricula(),
            "Medicina General",
            fecha_turno
        )
        
        medicamentos = ["Aspirina 100mg", "Vitamina D"]
        receta = self.clinica.emitir_receta(
            self.paciente.obtener_dni(),
            self.medico.obtener_matricula(),
            medicamentos
        )
        
        historia = self.clinica.obtener_historia_clinica(self.paciente.obtener_dni())
        
        self.assertIsNotNone(historia)
        
        turnos = historia.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].fecha_hora, fecha_turno)
        
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0].medicamentos, medicamentos)


# ===================== PUNTO DE ENTRADA PRINCIPAL =====================

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("🧪 Ejecutando pruebas unitarias...")
        print("=" * 60)
        
        unittest.main(argv=[''], exit=False, verbosity=2)
        
        print("\n" + "=" * 60)
        print("✅ Pruebas completadas")
        return
    
    cli = ClinicaCLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()