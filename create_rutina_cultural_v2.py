#!/usr/bin/env python3
"""
Crear presentación sobre Rutina Diaria y Choque Cultural para Sesión 4
VERSIÓN COMPLETA con ejemplos reales de choque cultural
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF"""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

class PresentationPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'Sesion 4: Rutina Diaria y Choque Cultural', border=0, align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Universidad de Granada - CLM | Pagina {self.page_no()}', border=0, align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 96, 150)
        self.cell(0, 10, clean_text(title), border=0, ln=True)
        self.ln(3)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(51, 102, 153)
        self.cell(0, 8, clean_text(title), border=0, ln=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, clean_text(text))
        self.ln(2)

    def bullet_point(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        self.cell(10, 6, '', border=0)
        self.cell(0, 6, clean_text('- ' + text), border=0, ln=True)

    def comparison_box(self, title, items):
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(100, 149, 237)
        y_start = self.get_y()
        self.rect(15, y_start, 180, 5 + len(items) * 6 + 8, 'FD')

        self.set_x(20)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 51, 102)
        self.cell(0, 6, clean_text(title), border=0, ln=True)
        self.ln(2)

        for item in items:
            self.set_x(20)
            self.set_font('Helvetica', '', 10)
            self.set_text_color(0, 0, 0)
            self.cell(0, 5, clean_text(item), border=0, ln=True)

        self.ln(3)

    def case_study_box(self, title, historia, choque, solucion):
        """Box para casos de choque cultural"""
        self.section_title(title)

        # Historia
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 6, 'HISTORIA:', border=0, ln=True)
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, clean_text(historia))
        self.ln(2)

        # Choque cultural
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(180, 0, 0)
        self.cell(0, 6, 'CHOQUE CULTURAL:', border=0, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 10)
        for item in choque:
            self.bullet_point(item)
        self.ln(2)

        # Solución
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 128, 0)
        self.cell(0, 6, 'SOLUCION:', border=0, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 10)
        for item in solucion:
            self.bullet_point(item)

# Crear PDF
pdf = PresentationPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Página 1: Portada
pdf.add_page()
pdf.ln(20)
pdf.set_font('Helvetica', 'B', 20)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 15, 'RUTINA DIARIA Y', border=0, align='C', ln=True)
pdf.cell(0, 15, 'CHOQUE CULTURAL', border=0, align='C', ln=True)
pdf.ln(10)

pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(51, 51, 51)
pdf.cell(0, 8, 'Curso Intensivo de Espanol - Nivel 3 CLM', border=0, align='C', ln=True)
pdf.cell(0, 8, 'Sesion 4: Verbos Reflexivos y Rutinas', border=0, align='C', ln=True)
pdf.ln(15)

pdf.set_font('Helvetica', 'I', 11)
pdf.multi_cell(0, 6, clean_text('Esta presentacion explora las diferencias culturales en las rutinas diarias entre Espana, Estados Unidos y Asia, con ejemplos reales que te ayudaran a comprender y adaptarte mejor al estilo de vida espanol.'))

# Página 2: La rutina española
pdf.add_page()
pdf.chapter_title('1. LA RUTINA ESPANOLA TIPICA')

pdf.section_title('Manana (7:00 - 14:00)')
pdf.body_text('Los espanoles suelen despertarse entre las 7:00 y 8:00. El desayuno es ligero:')
pdf.bullet_point('Cafe con leche o cafe solo')
pdf.bullet_point('Tostada con aceite de oliva, tomate o mermelada')
pdf.bullet_point('Zumo de naranja natural')
pdf.ln(2)

pdf.section_title('Comida - La comida principal (14:00 - 15:30)')
pdf.body_text('En Espana, la comida del mediodia es la mas importante del dia:')
pdf.bullet_point('Primer plato (ensalada, sopa, verduras)')
pdf.bullet_point('Segundo plato (carne o pescado con guarnicion)')
pdf.bullet_point('Postre (fruta o dulce)')
pdf.bullet_point('Cafe')
pdf.ln(2)

pdf.section_title('Tarde (17:00 - 21:00)')
pdf.bullet_point('Merienda ligera: cafe y galletas o bocadillo')
pdf.bullet_point('Muchas tiendas cierran entre 14:00-17:00 (siesta)')
pdf.bullet_point('La vida social empieza por la tarde')

# Página 3: Cena y vida nocturna
pdf.add_page()
pdf.section_title('Cena (21:00 - 22:30)')
pdf.body_text('La cena es mas tarde que en otros paises y suele ser mas ligera que la comida:')
pdf.bullet_point('Ensalada, tortilla, sopas ligeras')
pdf.bullet_point('Tapas o raciones para compartir')
pdf.bullet_point('Es comun cenar fuera de casa')
pdf.ln(3)

pdf.section_title('Vida nocturna')
pdf.bullet_point('Los espanoles salen tarde: a partir de las 22:00')
pdf.bullet_point('Los bares cierran sobre las 2:00-3:00 de la madrugada')
pdf.bullet_point('Los fines de semana la gente se acuesta muy tarde')
pdf.ln(5)

pdf.chapter_title('2. CHOQUE CULTURAL: COMPARACIONES')

# Página 4: Comparación EE.UU.
pdf.add_page()
pdf.section_title('ESPANA vs. ESTADOS UNIDOS')

pdf.comparison_box('Horarios de comidas', [
    'ESPANA: Desayuno 8:00, Comida 14:00-15:30, Cena 21:00-22:30',
    'EE.UU.: Breakfast 7:00, Lunch 12:00-13:00, Dinner 18:00-19:00'
])

pdf.comparison_box('El ritmo de vida', [
    'ESPANA: Mas relajado, importancia de la sobremesa',
    'EE.UU.: Mas rapido, "time is money", comida rapida muy comun'
])

pdf.comparison_box('Vida social', [
    'ESPANA: Muchas actividades sociales tarde/noche, vida en la calle',
    'EE.UU.: Actividades mas temprano, mas vida en casa'
])

pdf.comparison_box('Trabajo y descanso', [
    'ESPANA: Jornada partida comun (9-14h y 17-20h), siesta tradicional',
    'EE.UU.: Jornada continua (9-17h), lunch break corto'
])

# Página 5: Comparación Asia
pdf.add_page()
pdf.section_title('ESPANA vs. ASIA (China, Japon, Corea)')

pdf.comparison_box('Desayuno', [
    'ESPANA: Ligero y dulce (cafe, tostadas, bolleria)',
    'ASIA: Sustancioso y salado (arroz, sopa, pescado)'
])

pdf.comparison_box('Horarios laborales', [
    'ESPANA: Jornada partida, ritmo mas pausado',
    'ASIA: Jornadas muy largas, cultura del trabajo intenso'
])

pdf.comparison_box('Comida principal', [
    'ESPANA: Al mediodia, comida larga con sobremesa',
    'ASIA: Comidas rapidas, menos tiempo social en las comidas'
])

pdf.comparison_box('Vida nocturna', [
    'ESPANA: Muy activa, salir es parte de la cultura',
    'ASIA: Varia segun pais, karaoke muy popular'
])

# Página 6: Aspectos culturales
pdf.add_page()
pdf.chapter_title('3. ASPECTOS CULTURALES IMPORTANTES')

pdf.section_title('La sobremesa')
pdf.body_text('Es la costumbre de quedarse en la mesa despues de comer charlando. Puede durar 30-60 minutos. Es un momento muy importante de socializacion.')
pdf.ln(3)

pdf.section_title('La siesta')
pdf.body_text('Aunque ya no es tan comun, muchos espanoles descansan brevemente despues de comer, especialmente en verano. Las tiendas pequenas suelen cerrar de 14:00 a 17:00.')
pdf.ln(3)

pdf.section_title('Horarios de tiendas')
pdf.bullet_point('Supermercados: 9:00-21:00 (continuado)')
pdf.bullet_point('Tiendas pequenas: 10:00-14:00 y 17:00-20:30')
pdf.bullet_point('Centros comerciales: 10:00-22:00')
pdf.ln(3)

pdf.section_title('Puntualidad')
pdf.body_text('En contextos formales (trabajo, medico) se espera puntualidad. En contextos sociales, es comun llegar 10-15 minutos tarde. "Quedamos a las 20:00" puede significar 20:15.')

# PÁGINA 7-11: CASOS REALES DE CHOQUE CULTURAL
pdf.add_page()
pdf.chapter_title('4. CASOS REALES DE CHOQUE CULTURAL')

pdf.case_study_box(
    'Situacion 1: La hora de la cena',
    'Sarah (EE.UU.) llega a casa de su familia espanola a las 19:00 con mucha hambre. Pregunta: "When is dinner?" La familia responde: "A las 22:00". Sarah no puede creerlo.',
    [
        'Sarah esta acostumbrada a cenar a las 18:00-19:00',
        'Tiene que esperar 3 horas mas sin comer',
        'En EE.UU., 22:00 es hora de dormir, no de cenar',
        'Se siente hambrienta y frustrada'
    ],
    [
        'Tomar una merienda sustanciosa a las 18:00-19:00 (bocadillo, fruta)',
        'Adaptarse gradualmente: cenar cada dia 30 min mas tarde',
        'Recordar: en Espana la comida del mediodia es la principal',
        'Llevar siempre un snack en la mochila los primeros dias'
    ]
)

# Página 8
pdf.add_page()
pdf.case_study_box(
    'Situacion 2: Las tiendas cerradas',
    'Kenji (Japon) necesita comprar algo urgente a las 15:00. Va al centro y descubre que todas las tiendas pequenas estan cerradas. En Japon, las tiendas nunca cierran al mediodia. Kenji no sabe que hacer.',
    [
        'En Asia, las tiendas abren todo el dia sin interrupcion (cultura 24/7)',
        'La siesta espanola significa que muchos negocios cierran 14:00-17:00',
        'No puede comprar lo que necesita hasta 3 horas despues',
        'Siente que la ciudad "se apaga" en plena tarde'
    ],
    [
        'Hacer compras por la manana (10:00-14:00) o tarde (17:00-20:30)',
        'Usar supermercados grandes (abiertos todo el dia sin interrupcion)',
        'Planificar con anticipacion lo que necesitas',
        'Aprovecha la siesta para descansar o estudiar en casa'
    ]
)

pdf.ln(3)
pdf.case_study_box(
    'Situacion 3: La sobremesa eterna',
    'Michael (EE.UU.) termina de comer en 20 minutos en casa de una familia espanola. Todos siguen sentados charlando. Quiere levantarse pero nadie se mueve. Ya pasaron 45 minutos y todavia estan en la mesa.',
    [
        'En EE.UU.: comes y te vas rapidamente ("eat and go")',
        'En Espana: la comida es un evento social que puede durar 1-2 horas',
        'Sentirse incomodo sin saber que hacer',
        'Pensar que es raro quedarse tanto tiempo despues de terminar'
    ],
    [
        'Relajate y disfruta la conversacion - es cultura espanola',
        'Es de mala educacion levantarse inmediatamente',
        'Practica tu espanol durante la sobremesa',
        'La sobremesa es tan importante como la comida misma'
    ]
)

# Página 9
pdf.add_page()
pdf.case_study_box(
    'Situacion 4: La puntualidad flexible',
    'Li (China) queda con amigos espanoles a las 20:00 en una plaza. Llega exactamente a las 20:00 pero nadie esta ahi. Los amigos empiezan a llegar a las 20:15, 20:20, 20:25... El ultimo llega a las 20:35. En China, llegar tarde se considera irrespetuoso.',
    [
        'En Asia: la puntualidad es muy importante (muestra respeto)',
        'En Espana: 10-15 minutos tarde es "puntual" en contextos sociales',
        'Sentirse solo, confundido, pensar que algo esta mal',
        'Preguntarse si tal vez te dieron la hora o el lugar equivocado'
    ],
    [
        'Contexto FORMAL (trabajo, medico, clase): ser totalmente puntual',
        'Contexto SOCIAL: llegar 10-15 min tarde es perfectamente normal',
        'Si quedas a las 20:00, calcula llegar tu tambien 20:10-20:15',
        'No es falta de respeto - es simplemente la cultura social espanola'
    ]
)

pdf.ln(3)
pdf.case_study_box(
    'Situacion 5: Interrupciones en conversaciones',
    'Emma (EE.UU.) esta cenando con amigos espanoles. Cada vez que intenta decir algo, alguien la interrumpe o habla encima. En su pais, interrumpir es de muy mala educacion. Se siente invisible.',
    [
        'Espana: conversaciones rapidas, dinamicas, con interrupciones normales',
        'EE.UU./Asia: esperar tu turno pacientemente, no interrumpir',
        'Sentirse excluida de las conversaciones',
        'Pensar que los espanoles son maleducados o que no les interesa'
    ],
    [
        'No es personal - es el estilo comunicativo espanol (mas apasionado)',
        'Se mas asertiva, no esperes un silencio perfecto para hablar',
        'Participa activamente, esta bien interrumpir un poco',
        'Las interrupciones muestran interes, no falta de respeto'
    ]
)

# Página 10
pdf.add_page()
pdf.case_study_box(
    'Situacion 6: Salir de fiesta hasta el amanecer',
    'Yuki (Japon) sale con amigos espanoles un viernes. Le dicen "Nos vemos a las 23:00 para salir de fiesta". Yuki piensa que volveran a casa a la 1:00-2:00. Finalmente vuelve a casa a las 6:00 de la manana, completamente agotada.',
    [
        'En Espana: "salir de fiesta" = toda la noche (hasta las 5-7 AM)',
        'En muchos paises: salir = unas horas (hasta 1-2 AM maximo)',
        'Las discotecas espanolas ni siquiera se llenan hasta las 2:00 AM',
        'Agotamiento total al dia siguiente, no puede estudiar'
    ],
    [
        'Antes de salir, pregunta: "A que hora terminamos mas o menos?"',
        'Puedes irte antes si estas cansado - es totalmente aceptable',
        'Duerme siesta el sabado tarde si sales el viernes noche',
        'No tienes que quedarte hasta el final - cuida tu salud'
    ]
)

pdf.ln(3)
pdf.case_study_box(
    'Situacion 7: Los dos besos de saludo',
    'David (Corea) conoce a los amigos espanoles de su companero de piso. Sin previo aviso, una chica se acerca y le da dos besos en las mejillas (derecha-izquierda). David se pone muy rigido y se siente MUY incomodo. En su cultura, solo se da la mano o se hace una reverencia, especialmente con desconocidos.',
    [
        'Espana: 2 besos al saludar es lo normal (entre amigos, conocidos)',
        'Asia: minimo contacto fisico, mucha mas distancia personal',
        'Confusion sobre cuando dar besos vs. cuando dar la mano',
        'Sentirse invadido en su espacio personal'
    ],
    [
        'Contexto informal/entre amigos: dar 2 besos es normal',
        'Contexto formal/profesional: dar la mano',
        'Los besos NO son romanticos - son solo un saludo amistoso',
        'Si te sientes incomodo, puedes dar la mano primero'
    ]
)

# Página 11: Estrategias de adaptación
pdf.add_page()
pdf.chapter_title('5. ESTRATEGIAS DE ADAPTACION CULTURAL')

pdf.section_title('FASE 1: Observacion (Semana 1-2)')
pdf.bullet_point('Observa como los espanoles manejan diferentes situaciones')
pdf.bullet_point('No juzgues - solo toma nota de las diferencias')
pdf.bullet_point('Haz preguntas: "Es normal que...?" "Por que...?"')
pdf.bullet_point('Habla con otros estudiantes internacionales sobre sus experiencias')
pdf.ln(3)

pdf.section_title('FASE 2: Experimentacion (Semana 3-4)')
pdf.bullet_point('Prueba adaptar tu rutina gradualmente (no de golpe)')
pdf.bullet_point('Come un poco mas tarde cada dia')
pdf.bullet_point('Participa en actividades sociales espanolas')
pdf.bullet_point('Sal de tu zona de confort poco a poco')
pdf.ln(3)

pdf.section_title('FASE 3: Integracion (Mes 2+)')
pdf.bullet_point('Encuentra TU equilibrio personal hispano-internacional')
pdf.bullet_point('No tienes que hacer TODO igual que los espanoles')
pdf.bullet_point('Manten lo que funciona de tu cultura + adopta lo nuevo')
pdf.bullet_point('Crea tu propia rutina "hibrida" que funcione para ti')
pdf.ln(5)

pdf.section_title('Recuerda: El choque cultural es NORMAL y TEMPORAL')
pdf.body_text('Todas estas situaciones son experiencias comunes de estudiantes internacionales. No estas solo/a. El choque cultural tiene 4 fases predecibles:')
pdf.ln(2)
pdf.set_font('Courier', '', 10)
pdf.cell(0, 6, '1. Luna de miel    (Semana 1)     - Todo es emocionante y nuevo', border=0, ln=True)
pdf.cell(0, 6, '2. Frustracion     (Semana 2-4)   - Las diferencias te molestan', border=0, ln=True)
pdf.cell(0, 6, '3. Ajuste          (Mes 2)        - Empiezas a adaptarte', border=0, ln=True)
pdf.cell(0, 6, '4. Adaptacion      (Mes 3+)       - Te sientes comodo y bicultural', border=0, ln=True)

pdf.ln(5)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(0, 96, 150)
pdf.multi_cell(0, 6, clean_text('La fase de frustracion es la mas dificil, pero es NORMAL y PASARA. Ten paciencia contigo mismo/a. Cada persona se adapta a su propio ritmo.'))

# Página 12: Verbos reflexivos
pdf.add_page()
pdf.chapter_title('6. VERBOS REFLEXIVOS DE LA RUTINA DIARIA')

pdf.section_title('Conjugacion de verbos reflexivos (presente)')

pdf.set_font('Courier', '', 10)
pdf.cell(0, 6, 'LEVANTARSE          DUCHARSE           VESTIRSE (e>i)', border=0, ln=True)
pdf.cell(0, 5, 'Yo me levanto       me ducho           me visto', border=0, ln=True)
pdf.cell(0, 5, 'Tu te levantas      te duchas          te vistes', border=0, ln=True)
pdf.cell(0, 5, 'El/Ella se levanta  se ducha           se viste', border=0, ln=True)
pdf.cell(0, 5, 'Nos. nos levantamos nos duchamos       nos vestimos', border=0, ln=True)
pdf.cell(0, 5, 'Vos. os levantais   os duchais         os vestis', border=0, ln=True)
pdf.cell(0, 5, 'Ellos se levantan   se duchan          se visten', border=0, ln=True)
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 6, clean_text('Verbos reflexivos mas comunes:'), border=0, ln=True)
pdf.set_font('Helvetica', '', 10)
pdf.bullet_point('despertarse (e>ie) - to wake up')
pdf.bullet_point('levantarse - to get up')
pdf.bullet_point('ducharse / banarse - to shower / to bathe')
pdf.bullet_point('lavarse (la cara, los dientes) - to wash')
pdf.bullet_point('peinarse - to comb one\'s hair')
pdf.bullet_point('vestirse (e>i) - to get dressed')
pdf.bullet_point('desayunar - to have breakfast')
pdf.bullet_point('acostarse (o>ue) - to go to bed')
pdf.bullet_point('dormirse (o>ue) - to fall asleep')

# Página 13: Expresiones de frecuencia
pdf.add_page()
pdf.chapter_title('7. EXPRESIONES DE FRECUENCIA Y TIEMPO')

pdf.section_title('Adverbios de frecuencia')
pdf.set_font('Courier', '', 10)
pdf.cell(0, 6, 'Siempre          100%  - Me levanto siempre a las 7:00', border=0, ln=True)
pdf.cell(0, 6, 'Casi siempre     90%   - Casi siempre desayuno cafe', border=0, ln=True)
pdf.cell(0, 6, 'Normalmente      80%   - Normalmente voy al gimnasio', border=0, ln=True)
pdf.cell(0, 6, 'A menudo         70%   - A menudo como en casa', border=0, ln=True)
pdf.cell(0, 6, 'A veces          50%   - A veces salgo por la noche', border=0, ln=True)
pdf.cell(0, 6, 'Raramente        20%   - Raramente me acuesto antes de las 12', border=0, ln=True)
pdf.cell(0, 6, 'Casi nunca       10%   - Casi nunca duermo la siesta', border=0, ln=True)
pdf.cell(0, 6, 'Nunca            0%    - Nunca desayuno mucho', border=0, ln=True)
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 6, clean_text('Expresiones de tiempo:'), border=0, ln=True)
pdf.set_font('Helvetica', '', 10)
pdf.bullet_point('Por la manana / tarde / noche')
pdf.bullet_point('Todos los dias / todas las semanas')
pdf.bullet_point('Los lunes / los fines de semana')
pdf.bullet_point('Antes de + infinitivo: Antes de salir, me ducho')
pdf.bullet_point('Despues de + infinitivo: Despues de comer, descanso')

# Página 14: Consejos adaptación
pdf.add_page()
pdf.chapter_title('8. CONSEJOS PRACTICOS PARA ADAPTARTE')

pdf.section_title('Alimentacion y horarios de comida')
pdf.bullet_point('Acostumbrate gradualmente a comer mas tarde (30 min cada semana)')
pdf.bullet_point('Haz de la comida del mediodia tu comida principal (no la cena)')
pdf.bullet_point('Prueba el desayuno espanol tipico: cafe con leche y tostada')
pdf.bullet_point('No tengas prisa en las comidas - disfruta la sobremesa')
pdf.bullet_point('Lleva snacks contigo las primeras semanas')
pdf.ln(3)

pdf.section_title('Horarios y ritmo de vida')
pdf.bullet_point('Adapta tu horario de sueno gradualmente (no cambies todo de golpe)')
pdf.bullet_point('Aprovecha las horas 14:00-17:00 para descansar o estudiar')
pdf.bullet_point('Recuerda: muchas tiendas pequenas cierran en horario de siesta')
pdf.bullet_point('Los espanoles son mas activos por la tarde-noche que por la manana')
pdf.ln(3)

pdf.section_title('Vida social e interacciones')
pdf.bullet_point('No te sorprendas si te invitan a cenar a las 21:00-22:00')
pdf.bullet_point('La "puntualidad social" permite +10-15 minutos')
pdf.bullet_point('Participa en la vida en la calle: terrazas, paseos, plazas')
pdf.bullet_point('Los fines de semana la gente sale MUY tarde - puedes irte antes')
pdf.bullet_point('Los dos besos son un saludo normal, no romantico')

# Página 15: Actividades prácticas
pdf.add_page()
pdf.chapter_title('9. ACTIVIDADES PRACTICAS PARA LA CLASE')

pdf.section_title('Actividad 1: Compara tu rutina (15 min)')
pdf.body_text('Escribe tu rutina diaria en tu pais y comparala con la rutina espanola tipica. Usa verbos reflexivos y expresiones de frecuencia. Identifica 3 diferencias principales.')
pdf.ln(3)

pdf.section_title('Actividad 2: Role-play cultural (20 min)')
pdf.body_text('En parejas: Estudiante A es espanol, Estudiante B es de tu pais. Simulad estas situaciones:')
pdf.bullet_point('Quedais para cenar y discutis la hora')
pdf.bullet_point('B llega a las 15:00 y todas las tiendas estan cerradas')
pdf.bullet_point('Estais comiendo y B quiere irse pero A sigue charlando')
pdf.ln(3)

pdf.section_title('Actividad 3: Mi choque cultural (15 min)')
pdf.body_text('Responde y comparte con la clase:')
pdf.bullet_point('Que aspecto de la rutina espanola te resulta mas dificil? Por que?')
pdf.bullet_point('Que te gusta MAS de la cultura espanola?')
pdf.bullet_point('Que estrategia vas a usar para adaptarte mejor?')
pdf.ln(3)

pdf.section_title('Actividad 4: Entrevista a un espanol (Tarea)')
pdf.body_text('Entrevista a un espanol sobre su rutina. Pregunta:')
pdf.bullet_point('A que hora desayunas/comes/cenas normalmente?')
pdf.bullet_point('Que haces en tu tiempo libre? Cuando sales con amigos?')
pdf.bullet_point('Has notado diferencias con otros paises? Cuales?')
pdf.bullet_point('Que consejo le darias a un extranjero en Espana?')

pdf.ln(10)
pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(0, 96, 150)
pdf.cell(0, 8, clean_text('Comparte tus experiencias de choque cultural en clase!'), border=0, align='C', ln=True)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, clean_text('Recuerda: El choque cultural es temporal. En unas semanas te sentiras mucho mas comodo.'), border=0, align='C')

# Guardar PDF
os.makedirs('materials/presentaciones', exist_ok=True)
filename = 'materials/presentaciones/S4_Rutina_Diaria_Choque_Cultural.pdf'
pdf.output(filename)
print(f"\n✅ Presentacion completa creada: {filename}")
print(f"📄 Total de paginas: {pdf.page_no()}")
print(f"📦 Incluye 7 casos reales de choque cultural con soluciones practicas")
