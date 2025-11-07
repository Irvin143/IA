REGLAS_PRODUCCION = {
    'asma': [
        {
            'condiciones': ['sibilancias', 'tos', 'antecedentes_alergicos'],
            'factor_certeza': 0.9,
            'descripcion': 'Sibilancias + Tos + Antecedentes alérgicos'
        },
        {
            'condiciones': ['sibilancias', 'opresion_pecho', 'dificultad_respirar'],
            'factor_certeza': 0.85,
            'descripcion': 'Sibilancias + Opresión pecho + Dificultad respirar'
        },
        {
            'condiciones': ['tos', 'dificultad_respirar', 'historia_familiar_asma'],
            'factor_certeza': 0.8,
            'descripcion': 'Tos + Dificultad respirar + Historia familiar asma'
        },
        {
            'condiciones': ['espiracion_prolongada', 'sibilancias', 'atopia'],
            'factor_certeza': 0.85,
            'descripcion': 'Espiración prolongada + Sibilancias + Atopia'
        }
    ],
    'bronquitis': [
        {
            'condiciones': ['tos_productiva', 'flemas', 'tabaquismo'],
            'factor_certeza': 0.9,
            'descripcion': 'Tos productiva + Flemas + Tabaquismo'
        },
        {
            'condiciones': ['tos_productiva', 'fiebre_moderada', 'malestar_general'],
            'factor_certeza': 0.85,
            'descripcion': 'Tos productiva + Fiebre moderada + Malestar general'
        },
        {
            'condiciones': ['tos', 'flemas', 'exposicion_contaminantes'],
            'factor_certeza': 0.8,
            'descripcion': 'Tos + Flemas + Exposición a contaminantes'
        },
        {
            'condiciones': ['dificultad_respirar', 'tos_productiva', 'infecciones_virales_previas'],
            'factor_certeza': 0.75,
            'descripcion': 'Dificultad respirar + Tos productiva + Infecciones previas'
        }
    ],
    'epoc': [
        {
            'condiciones': ['tos_cronica', 'dificultad_respirar_esfuerzo', 'tabaquismo', 'edad_mayor_40'],
            'factor_certeza': 0.95,
            'descripcion': 'Tos crónica + Disnea de esfuerzo + Tabaquismo + Mayor de 40 años'
        },
        {
            'condiciones': ['produccion_esputo', 'uso_musculos_accesorios', 'tabaquismo'],
            'factor_certeza': 0.9,
            'descripcion': 'Producción esputo + Uso músculos accesorios + Tabaquismo'
        },
        {
            'condiciones': ['tos_cronica', 'fatiga', 'exposicion_polvo_quimicos'],
            'factor_certeza': 0.85,
            'descripcion': 'Tos crónica + Fatiga + Exposición a polvos/químicos'
        },
        {
            'condiciones': ['sibilancias', 'dificultad_respirar', 'exposicion_profesional'],
            'factor_certeza': 0.8,
            'descripcion': 'Sibilancias + Dificultad respirar + Exposición profesional'
        }
    ],
    'neumonia': [
        {
            'condiciones': ['fiebre_alta', 'tos', 'dolor_pecho', 'dificultad_respirar'],
            'factor_certeza': 0.95,
            'descripcion': 'Fiebre alta + Tos + Dolor pecho + Dificultad respirar'
        },
        {
            'condiciones': ['fiebre_alta', 'escalofrios', 'tos', 'grupo_edad_vulnerable'],
            'factor_certeza': 0.9,
            'descripcion': 'Fiebre alta + Escalofríos + Tos + Edad vulnerable'
        },
        {
            'condiciones': ['dolor_pecho', 'dificultad_respirar', 'fiebre_alta', 'inmunosupresion'],
            'factor_certeza': 0.92,
            'descripcion': 'Dolor pecho + Dificultad respirar + Fiebre alta + Inmunosupresión'
        },
        {
            'condiciones': ['tos', 'fiebre_alta', 'enfermedades_cronicas'],
            'factor_certeza': 0.8,
            'descripcion': 'Tos + Fiebre alta + Enfermedades crónicas'
        }
    ],
    'covid19': [
        {
            'condiciones': ['perdida_gusto_olfato', 'fiebre', 'tos', 'contacto_casos_positivos'],
            'factor_certeza': 0.95,
            'descripcion': 'Pérdida gusto/olfato + Fiebre + Tos + Contacto casos positivos'
        },
        {
            'condiciones': ['perdida_gusto_olfato', 'fatiga', 'dolores_musculares'],
            'factor_certeza': 0.9,
            'descripcion': 'Pérdida gusto/olfato + Fatiga + Dolores musculares'
        },
        {
            'condiciones': ['dificultad_respirar', 'fiebre', 'tos', 'edad_avanzada'],
            'factor_certeza': 0.85,
            'descripcion': 'Dificultad respirar + Fiebre + Tos + Edad avanzada'
        },
        {
            'condiciones': ['fatiga', 'tos', 'fiebre', 'diabetes_hipertension'],
            'factor_certeza': 0.8,
            'descripcion': 'Fatiga + Tos + Fiebre + Diabetes/Hipertensión'
        }
    ],
    'iras': [
        {
            'condiciones': ['congestion_nasal', 'estornudos', 'dolor_garganta', 'contacto_virus'],
            'factor_certeza': 0.9,
            'descripcion': 'Congestión nasal + Estornudos + Dolor garganta + Contacto con virus'
        },
        {
            'condiciones': ['fiebre', 'tos', 'congestion_nasal'],
            'factor_certeza': 0.85,
            'descripcion': 'Fiebre + Tos + Congestión nasal'
        },
        {
            'condiciones': ['estornudos', 'dolor_garganta', 'tos'],
            'factor_certeza': 0.8,
            'descripcion': 'Estornudos + Dolor garganta + Tos'
        },
        {
            'condiciones': ['congestion_nasal', 'tos', 'grupo_edad_vulnerable'],
            'factor_certeza': 0.75,
            'descripcion': 'Congestión nasal + Tos + Edad vulnerable'
        }
    ],
    'influenza': [
        {
            'condiciones': ['fiebre_alta', 'dolores_musculares', 'fatiga', 'dolor_cabeza'],
            'factor_certeza': 0.95,
            'descripcion': 'Fiebre alta + Dolores musculares + Fatiga + Dolor cabeza'
        },
        {
            'condiciones': ['fiebre_alta', 'dolores_musculares', 'tos_seca', 'no_vacunado'],
            'factor_certeza': 0.9,
            'descripcion': 'Fiebre alta + Dolores musculares + Tos seca + No vacunado'
        },
        {
            'condiciones': ['dolores_musculares', 'fatiga', 'contacto_infectados'],
            'factor_certeza': 0.85,
            'descripcion': 'Dolores musculares + Fatiga + Contacto con infectados'
        },
        {
            'condiciones': ['fiebre_alta', 'tos_seca', 'dolor_cabeza', 'grupo_edad_vulnerable'],
            'factor_certeza': 0.85,
            'descripcion': 'Fiebre alta + Tos seca + Dolor cabeza + Edad vulnerable'
        }
    ],
    'faringoamigdalitis': [
        {
            'condiciones': ['dolor_garganta', 'dificultad_tragar', 'fiebre', 'ganglios_inflamados'],
            'factor_certeza': 0.95,
            'descripcion': 'Dolor garganta + Dificultad tragar + Fiebre + Ganglios inflamados'
        },
        {
            'condiciones': ['dolor_garganta', 'fiebre', 'contacto_casos'],
            'factor_certeza': 0.85,
            'descripcion': 'Dolor garganta + Fiebre + Contacto con casos'
        },
        {
            'condiciones': ['dificultad_tragar', 'ganglios_inflamados', 'edad_joven'],
            'factor_certeza': 0.8,
            'descripcion': 'Dificultad tragar + Ganglios inflamados + Edad joven'
        },
        {
            'condiciones': ['dolor_garganta', 'fiebre', 'guarderias_colegios'],
            'factor_certeza': 0.8,
            'descripcion': 'Dolor garganta + Fiebre + Asiste guarderías/colegios'
        }
    ],
    'rinitis': [
        {
            'condiciones': ['congestion_nasal', 'estornudos', 'picor_nariz', 'alergia_estacional'],
            'factor_certeza': 0.95,
            'descripcion': 'Congestión nasal + Estornudos + Picor nariz + Alergia estacional'
        },
        {
            'condiciones': ['estornudos', 'secrecion_nasal', 'exposicion_alergenos'],
            'factor_certeza': 0.9,
            'descripcion': 'Estornudos + Secreción nasal + Exposición a alérgenos'
        },
        {
            'condiciones': ['congestion_nasal', 'picor_nariz', 'antecedentes_familiares_alergia'],
            'factor_certeza': 0.85,
            'descripcion': 'Congestión nasal + Picor nariz + Antecedentes familiares'
        },
        {
            'condiciones': ['estornudos', 'secrecion_nasal', 'congestion_nasal'],
            'factor_certeza': 0.8,
            'descripcion': 'Estornudos + Secreción nasal + Congestión nasal'
        }
    ],
    'tuberculosis': [
        {
            'condiciones': ['tos_prolongada', 'tos_con_sangre', 'sudoracion_nocturna', 'perdida_peso'],
            'factor_certeza': 0.95,
            'descripcion': 'Tos prolongada + Hemoptisis + Sudoración nocturna + Pérdida peso'
        },
        {
            'condiciones': ['tos_prolongada', 'perdida_peso', 'contacto_tuberculosis'],
            'factor_certeza': 0.9,
            'descripcion': 'Tos prolongada + Pérdida peso + Contacto con tuberculosis'
        },
        {
            'condiciones': ['tos_prolongada', 'sudoracion_nocturna', 'fiebre_baja', 'infeccion_vih'],
            'factor_certeza': 0.92,
            'descripcion': 'Tos prolongada + Sudoración nocturna + Febrícula + VIH'
        },
        {
            'condiciones': ['tos_con_sangre', 'perdida_peso', 'viajes_zonas_endemicas'],
            'factor_certeza': 0.85,
            'descripcion': 'Hemoptisis + Pérdida peso + Viajes a zonas endémicas'
        }
    ]
}

INFORMACION_ENFERMEDADES = {
    'asma': {
        'nombre': 'Asma',
        'descripcion': 'Enfermedad crónica de las vías respiratorias que causa inflamación y estrechamiento',
        'hallazgos': 'Sibilancias audibles al auscultar, espiración prolongada, signos de hiperinsuflación en radiografía',
        'recomendacion': 'Consultar con neumólogo, evitar alérgenos, tratamiento con broncodilatadores',
        'urgencia': 'MEDIA'
    },
    'bronquitis': {
        'nombre': 'Bronquitis',
        'descripcion': 'Inflamación de los bronquios que puede ser aguda o crónica',
        'hallazgos': 'Presencia de roncus y sibilancias, murmullo vesicular conservado, posible infiltrado peribronquial en radiografía',
        'recomendacion': 'Reposo, hidratación, evitar irritantes. Consultar si persiste más de 3 semanas',
        'urgencia': 'BAJA'
    },
    'epoc': {
        'nombre': 'EPOC (Enfermedad Pulmonar Obstructiva Crónica)',
        'descripcion': 'Enfermedad pulmonar obstructiva crónica, principalmente causada por tabaquismo',
        'hallazgos': 'Murmullo vesicular disminuido, uso de músculos accesorios para respirar, sibilancias, hiperinflación visible en radiografía',
        'recomendacion': 'IMPORTANTE: Consultar neumólogo urgentemente, dejar de fumar, rehabilitación pulmonar',
        'urgencia': 'ALTA'
    },
    'neumonia': {
        'nombre': 'Neumonía',
        'descripcion': 'Infección que inflama los sacos aéreos de uno o ambos pulmones',
        'hallazgos': 'Crepitantes localizados, disminución del murmullo vesicular, matidez a la percusión, egofonía, presencia de infiltrado en radiografía',
        'recomendacion': 'URGENTE: Acudir INMEDIATAMENTE al médico o servicio de urgencias',
        'urgencia': 'URGENTE'
    },
    'covid19': {
        'nombre': 'COVID-19',
        'descripcion': 'Infección viral por SARS-CoV-2 que afecta principalmente al sistema respiratorio',
        'hallazgos': 'Crepitantes bibasales, hipoxemia (bajo oxígeno en sangre), respiración acelerada (taquipnea), infiltrados en vidrio despulido en TAC',
        'recomendacion': 'Realizar prueba COVID, aislamiento, consultar médico si hay dificultad respiratoria importante',
        'urgencia': 'ALTA'
    },
    'iras': {
        'nombre': 'IRAS (Infección Respiratoria Aguda)',
        'descripcion': 'Infección aguda del tracto respiratorio superior o inferior',
        'hallazgos': 'Faringe enrojecida (hiperemia), rinorrea, adenopatías cervicales leves, auscultación generalmente normal',
        'recomendacion': 'Reposo, hidratación abundante, antipiréticos si hay fiebre. Consultar si empeora',
        'urgencia': 'BAJA'
    },
    'influenza': {
        'nombre': 'Influenza (Gripe)',
        'descripcion': 'Infección viral aguda del sistema respiratorio causada por virus influenza',
        'hallazgos': 'Fiebre alta, congestión de mucosas, dolores musculares generalizados, auscultación pulmonar normal (salvo complicaciones)',
        'recomendacion': 'Reposo, hidratación, antivirales si se inicia temprano. Vacunación preventiva',
        'urgencia': 'MEDIA'
    },
    'faringoamigdalitis': {
        'nombre': 'Faringoamigdalitis',
        'descripcion': 'Inflamación de la faringe y las amígdalas',
        'hallazgos': 'Faringe enrojecida, posible exudado en amígdalas, adenopatías cervicales dolorosas',
        'recomendacion': 'Analgésicos, líquidos tibios. Consultar si persiste o hay dificultad para respirar',
        'urgencia': 'BAJA'
    },
    'rinitis': {
        'nombre': 'Rinitis',
        'descripcion': 'Inflamación de la mucosa nasal, puede ser alérgica o no alérgica',
        'hallazgos': 'Mucosa nasal congestionada, rinorrea, engrosamiento de la mucosa visible en la rinofaringoscopia',
        'recomendacion': 'Antihistamínicos, evitar alérgenos. Considerar consulta con alergólogo',
        'urgencia': 'BAJA'
    },
    'tuberculosis': {
        'nombre': 'Tuberculosis Pulmonar',
        'descripcion': 'Infección bacteriana crónica causada por Mycobacterium tuberculosis',
        'hallazgos': 'Crepitantes en zonas apicales del pulmón, pérdida de peso, adenopatías, cavitaciones visibles en radiografía o TAC',
        'recomendacion': 'URGENTE: Consultar INMEDIATAMENTE. Requiere tratamiento prolongado específico',
        'urgencia': 'URGENTE'
    }
}

SINTOMAS_DISPONIBLES = {
    'sibilancias': '¿Presenta silbidos al respirar (sibilancias)?',
    'dificultad_respirar': '¿Tiene dificultad para respirar?',
    'dificultad_respirar_esfuerzo': '¿Tiene dificultad para respirar específicamente al hacer esfuerzo físico?',
    'tos': '¿Tiene tos?',
    'tos_productiva': '¿La tos produce flemas (tos productiva)?',
    'tos_seca': '¿La tos es seca (sin flemas)?',
    'tos_cronica': '¿La tos ha durado más de 3 semanas (tos crónica)?',
    'tos_prolongada': '¿Ha tenido tos por más de 2-3 semanas consecutivas?',
    'tos_con_sangre': '¿Ha tosido sangre (hemoptisis)?',
    'flemas': '¿Produce flemas/esputo regularmente?',
    'produccion_esputo': '¿Produce esputo de manera frecuente o abundante?',
    'opresion_pecho': '¿Siente opresión en el pecho?',
    'dolor_pecho': '¿Tiene dolor en el pecho?',
    'espiracion_prolongada': '¿Le cuesta más trabajo exhalar (sacar el aire) que inhalar?',
    'uso_musculos_accesorios': '¿Usa los músculos del cuello u hombros para ayudarse a respirar?',
    'fiebre': '¿Tiene fiebre?',
    'fiebre_alta': '¿La fiebre es alta (más de 38.5°C)?',
    'fiebre_moderada': '¿La fiebre es moderada (entre 38-38.5°C)?',
    'fiebre_baja': '¿La fiebre es baja/febrícula (menos de 38°C)?',
    'escalofrios': '¿Tiene escalofríos?',
    'fatiga': '¿Se siente muy cansado/fatigado?',
    'dolores_musculares': '¿Tiene dolores musculares generalizados?',
    'dolor_cabeza': '¿Tiene dolor de cabeza?',
    'congestion_nasal': '¿Tiene congestión nasal (nariz tapada)?',
    'secrecion_nasal': '¿Tiene secreción nasal o moqueo (rinorrea)?',
    'estornudos': '¿Estornuda frecuentemente?',
    'picor_nariz': '¿Le pica la nariz o tiene comezón nasal?',
    'dolor_garganta': '¿Tiene dolor de garganta?',
    'dificultad_tragar': '¿Tiene dificultad o dolor al tragar?',
    'ganglios_inflamados': '¿Tiene ganglios inflamados o bolitas en el cuello?',
    'perdida_gusto_olfato': '¿Ha perdido el gusto o el olfato?',
    'malestar_general': '¿Tiene malestar general o se siente mal en general?',
    'perdida_peso': '¿Ha perdido peso recientemente sin proponérselo?',
    'sudoracion_nocturna': '¿Tiene sudoración nocturna abundante (empapa la ropa)?'
}

FACTORES_RIESGO_DISPONIBLES = {
    'grupo_edad_vulnerable': '¿Es menor de 5 años O mayor de 65 años?',
    'edad_joven': '¿Es menor de 18 años?',
    'edad_mayor_40': '¿Tiene más de 40 años?',
    'edad_avanzada': '¿Tiene más de 65 años?',
    'tabaquismo': '¿Fuma o ha fumado regularmente?',
    'tabaquismo_pasivo': '¿Está expuesto al humo del tabaco (fumadores a su alrededor)?',
    'antecedentes_alergicos': '¿Tiene antecedentes de alergias (rinitis alérgica, alergias alimentarias, etc.)?',
    'atopia': '¿Tiene dermatitis atópica (eccema) o rinitis alérgica?',
    'alergia_estacional': '¿Tiene alergia estacional (síntomas en primavera u otoño)?',
    'antecedentes_familiares_alergia': '¿Tiene familiares directos con alergias?',
    'historia_familiar_asma': '¿Tiene familiares directos con asma?',
    'exposicion_contaminantes': '¿Está expuesto frecuentemente a contaminantes ambientales (smog, tráfico pesado)?',
    'exposicion_polvo_quimicos': '¿Está expuesto regularmente a polvo o químicos?',
    'exposicion_profesional': '¿Su trabajo lo expone a irritantes respiratorios de manera prolongada?',
    'exposicion_alergenos': '¿Está expuesto a alérgenos conocidos (polen, ácaros, mascotas)?',
    'enfermedades_cronicas': '¿Tiene enfermedades crónicas como diabetes, cardiopatía u otras?',
    'diabetes_hipertension': '¿Tiene diabetes o hipertensión?',
    'inmunosupresion': '¿Tiene el sistema inmune debilitado (VIH, medicamentos inmunosupresores, quimioterapia)?',
    'infeccion_vih': '¿Tiene VIH/SIDA?',
    'contacto_casos_positivos': '¿Ha tenido contacto cercano con casos positivos de COVID-19?',
    'contacto_infectados': '¿Ha tenido contacto cercano con personas enfermas con gripe u otras infecciones?',
    'contacto_casos': '¿Ha estado en contacto con personas enfermas recientemente?',
    'contacto_virus': '¿Ha estado en contacto con personas con resfriado o gripe?',
    'contacto_tuberculosis': '¿Ha tenido contacto con personas diagnosticadas con tuberculosis?',
    'no_vacunado': '¿NO está vacunado contra influenza o COVID-19?',
    'infecciones_virales_previas': '¿Ha tenido infecciones virales respiratorias recientemente (últimas semanas)?',
    'guarderias_colegios': '¿Asiste o trabaja en guarderías, colegios o lugares con muchos niños?',
    'viajes_zonas_endemicas': '¿Ha viajado recientemente a zonas con alta prevalencia de tuberculosis?'
}

# REGLAS DE INFERENCIA: Define qué preguntas omitir basándose en respuestas previas
REGLAS_OMISION = {
    # Si ya dijo que es menor de 18, no preguntar otras edades incompatibles
    'edad_joven': ['edad_mayor_40', 'edad_avanzada'],
    
    # Si ya dijo que es mayor de 65, no preguntar si es menor de 18
    'edad_avanzada': ['edad_joven', 'grupo_edad_vulnerable'],  # Ya sabemos que es vulnerable
    
    # Si ya dijo que tiene más de 40, y luego dice que tiene más de 65, omitir grupo vulnerable
    'edad_mayor_40': [],  # Esta puede convivir con edad_avanzada
    
    # Si es vulnerable (menor de 5 o mayor de 65), no preguntar edad_joven ni edad_mayor_40
    'grupo_edad_vulnerable': ['edad_joven'],  # Puede ser <5 o >65
    
    # Si tiene tos productiva, no preguntar si es tos seca
    'tos_productiva': ['tos_seca'],
    'tos_seca': ['tos_productiva'],
    
    # Si tiene tos crónica o prolongada, implica que tiene tos
    'tos_cronica': ['tos'],
    'tos_prolongada': ['tos'],
    
    # Si tiene fiebre alta, no preguntar moderada ni baja
    'fiebre_alta': ['fiebre_moderada', 'fiebre_baja', 'fiebre'],
    'fiebre_moderada': ['fiebre_alta', 'fiebre_baja', 'fiebre'],
    'fiebre_baja': ['fiebre_alta', 'fiebre_moderada', 'fiebre'],
    
    # Si tiene dificultad respirar al esfuerzo, obvio tiene dificultad respirar
    'dificultad_respirar_esfuerzo': ['dificultad_respirar'],
    
    # Si produce esputo frecuente/abundante, ya sabemos que produce flemas
    'produccion_esputo': ['flemas'],
    'flemas': [],  # flemas puede convivir con produccion_esputo
    
    # Si tiene VIH, ya tiene inmunosupresión
    'infeccion_vih': ['inmunosupresion'],
    
    # Si tiene diabetes/hipertensión, ya tiene enfermedades crónicas
    'diabetes_hipertension': ['enfermedades_cronicas'],
    
    # Si tiene atopia, ya tiene antecedentes alérgicos
    'atopia': ['antecedentes_alergicos'],
    
    # Si tiene alergia estacional, ya tiene antecedentes alérgicos
    'alergia_estacional': ['antecedentes_alergicos'],
    
    # Contactos redundantes
    'contacto_casos_positivos': ['contacto_casos', 'contacto_infectados'],
    'contacto_infectados': ['contacto_casos'],
    'contacto_tuberculosis': ['contacto_casos'],
}