import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class Interfaz:
    def __init__(self, motor, sintomas_disponibles, factores_riesgo_disponibles, reglas_omision=None):
        self.motor = motor
        self.sintomas_disponibles = sintomas_disponibles
        self.factores_riesgo_disponibles = factores_riesgo_disponibles
        self.reglas_omision = reglas_omision or {}

        # Preparar lista ordenada de preguntas: síntomas primero, luego factores
        self.todas_preguntas = []  # list of (clave, texto)
        for k, q in self.sintomas_disponibles.items():
            self.todas_preguntas.append((k, q))
        for k, q in self.factores_riesgo_disponibles.items():
            self.todas_preguntas.append((k, q))

        # Datos recogidos
        self.datos_usuario = []
        self.preguntas_omitidas = set()  # Preguntas que no se haran
        self.index_pregunta = 0

        # Tk root y frames
        self.root = tk.Tk()
        self.root.title("Sistema Experto de Enfermedades Respiratorias")
        self.root.geometry("700x520")
        self.root.minsize(600, 420)

        # Container frames
        self.frame_current = None

        # Estilos
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass

    def _clear_frame(self):
        if self.frame_current is not None:
            self.frame_current.destroy()
            self.frame_current = None

    def _actualizar_omisiones(self, clave_respondida):
        """Actualiza las preguntas que deben omitirse basándose en la respuesta actual"""
        if clave_respondida in self.reglas_omision:
            omitir = self.reglas_omision[clave_respondida]
            self.preguntas_omitidas.update(omitir)

    def _debe_omitir_pregunta(self, clave):
        """Verifica si una pregunta debe omitirse"""
        return clave in self.preguntas_omitidas

    def mostrar_bienvenida(self):
        self._clear_frame()
        f = ttk.Frame(self.root)
        self.frame_current = f

        title = ttk.Label(f, text="Sistema Experto de Enfermedades Respiratorias",
                          font=(None, 18, 'bold'), anchor='center')

        start_btn = ttk.Button(f, text="Iniciar", command=self.start_cuestionario)

        title.pack(pady=(28, 4))
        start_btn.pack()

        # Footer
        footer = ttk.Label(f, text="Por favor responda Sí o No a cada pregunta.", font=(None, 9))
        footer.pack(side='bottom', pady=12)
        f.pack(fill='both', expand=True)

    def start_cuestionario(self):
        self.datos_usuario = []
        self.preguntas_omitidas = set()
        self.index_pregunta = 0
        if not self.todas_preguntas:
            tk.messagebox.showinfo("Atención", "No hay preguntas configuradas.")
            return
        self._avanzar_a_siguiente_pregunta()

    def _avanzar_a_siguiente_pregunta(self):
        """Avanza a la siguiente pregunta que NO deba omitirse"""
        while self.index_pregunta < len(self.todas_preguntas):
            clave, _ = self.todas_preguntas[self.index_pregunta]
            if not self._debe_omitir_pregunta(clave):
                self.mostrar_pregunta()
                return
            else:
                # Omitir esta pregunta, avanzar
                self.index_pregunta += 1
        
        # Si llegamos aquí, terminamos todas las preguntas
        self.mostrar_resumen_y_resultados()

    def mostrar_pregunta(self):
        self._clear_frame()
        f = ttk.Frame(self.root)
        self.frame_current = f

        clave, texto = self.todas_preguntas[self.index_pregunta]

        q_label = ttk.Label(f, text=f"{self.index_pregunta + 1}. {texto}", wraplength=640,
                            font=(None, 13))

        # Buttons Sí / No
        btn_frame = ttk.Frame(f)
        yes_btn = ttk.Button(btn_frame, text="Sí", command=lambda: self._responder(True))
        no_btn = ttk.Button(btn_frame, text="No", command=lambda: self._responder(False))

        q_label.pack(pady=(60, 18))
        btn_frame.pack()
        yes_btn.pack(side='left', padx=12, ipadx=10, ipady=6)
        no_btn.pack(side='left', padx=12, ipadx=10, ipady=6)

        progreso = ttk.Label(f, text=f"Pregunta {self.index_pregunta + 1} de {len(self.todas_preguntas)}",
                             font=(None, 9))
        progreso.pack(side='bottom', pady=10)

        f.pack(fill='both', expand=True)

    def _responder(self, afirmativo: bool):
        clave, _ = self.todas_preguntas[self.index_pregunta]
        
        if afirmativo:
            self.datos_usuario.append(clave)
            # Actualizar reglas de omisión basándose en esta respuesta
            self._actualizar_omisiones(clave)

        self.index_pregunta += 1
        self._avanzar_a_siguiente_pregunta()

    def mostrar_resumen_y_resultados(self):
        self._clear_frame()
        f = ttk.Frame(self.root)
        self.frame_current = f

        header = ttk.Label(f, text="Resultados del Diagnóstico", font=(None, 16, 'bold'))
        header.pack(pady=(10, 6))

        # Caja de texto desplazable para mostrar resumen + diagnóstico
        caja = scrolledtext.ScrolledText(f, wrap='word', width=80, height=20)
        caja.configure(state='normal')

        # Mostrar resumen de datos ingresados
        datos = self.datos_usuario
        sintomas_ingresados = [d for d in datos if d in self.sintomas_disponibles]
        factores_ingresados = [d for d in datos if d in self.factores_riesgo_disponibles]

        """caja.insert('end', f"Total de datos proporcionados: {len(datos)}\n")
        caja.insert('end', f" - Síntomas: {len(sintomas_ingresados)}\n")
        caja.insert('end', f" - Factores de riesgo: {len(factores_ingresados)}\n")
        caja.insert('end', f" - Preguntas omitidas (por inferencia): {len(self.preguntas_omitidas)}\n\n")

        if sintomas_ingresados:
            caja.insert('end', "Síntomas identificados:\n")
            for s in sintomas_ingresados:
                nombre_legible = self.sintomas_disponibles.get(s, s).replace('¿', '').replace('?', '')
                caja.insert('end', f"  - {nombre_legible}\n")
            caja.insert('end', "\n")

        if factores_ingresados:
            caja.insert('end', "Factores de riesgo identificados:\n")
            for fct in factores_ingresados:
                nombre_legible = self.factores_riesgo_disponibles.get(fct, fct).replace('¿', '').replace('?', '')
                caja.insert('end', f"  - {nombre_legible}\n")
            caja.insert('end', "\n") """

        # Realizar diagnóstico llamando al motor
        try:
            diagnosticos = self.motor.diagnosticar(datos)
        except Exception as e:
            caja.insert('end', f"Error al diagnosticar: {e}\n")
            diagnosticos = []

        if not diagnosticos:
            caja.insert('end', "No se encontraron reglas que coincidan con los datos proporcionados.\n")
            caja.insert('end', "RECOMENDACIÓN: Consulte a un médico para evaluación completa.\n")
        else:
            for i, (enfermedad, datos_calc) in enumerate(diagnosticos, 1):
                info = self.motor.obtener_info_enfermedad(enfermedad)
                fc = datos_calc.get('factor_certeza', 0.0)
                probabilidad = datos_calc.get('probabilidad', 0.0)
    
                caja.insert('end', f"{i} {info.get('nombre','').upper()}\n")
                caja.insert('end', f"   Factor de Certeza: {fc:.2f}\n")
                caja.insert('end', f"   Probabilidad: {probabilidad:.1f}%\n")
                caja.insert('end', f"   Nivel de urgencia: {info.get('urgencia','')}\n")
                caja.insert('end', f"   Reglas activadas: {datos_calc.get('num_reglas_activadas',0)}\n\n")

                caja.insert('end', "   Reglas que se cumplieron:\n")
                for j, regla in enumerate(datos_calc.get('reglas_activadas', []), 1):
                    caja.insert('end', f"      {j}. SI ({regla.get('descripcion','')})\n")
                    caja.insert('end', f"         [Factor de certeza: {regla.get('factor_certeza',0.0):.2f}]\n")
                    caja.insert('end', f"         [Cumplimiento: {regla.get('condiciones_cumplidas',0)}/{regla.get('condiciones_totales',0)} condiciones = {regla.get('porcentaje_cumplimiento',0):.0f}%]\n")
                caja.insert('end', "\n")

                caja.insert('end', f"   Descripción:\n      {info.get('descripcion','')}\n\n")
                caja.insert('end', f"   Recomendación:\n      {info.get('recomendacion','')}\n\n")

        caja.configure(state='disabled')
        caja.pack(fill='both', expand=True, padx=12, pady=(6, 12))

        # Buttons abajo
        btn_frame = ttk.Frame(f)
        nueva_btn = ttk.Button(btn_frame, text="Nueva consulta", command=self.mostrar_bienvenida)
        salir_btn = ttk.Button(btn_frame, text="Salir", command=self.root.quit)
        nueva_btn.pack(side='left', padx=8, ipadx=6, ipady=4)
        salir_btn.pack(side='left', padx=8, ipadx=6, ipady=4)
        btn_frame.pack(pady=10)

        f.pack(fill='both', expand=True)

    def ejecutar(self):
        """Inicia la interfaz gráfica."""
        self.mostrar_bienvenida()
        try:
            self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        except Exception:
            pass
        self.root.mainloop()