#!/usr/bin/env python3
"""
Crear PDFs profesionales para todos los materiales del curso
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF"""
    replacements = {
        '•': '-', 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!', '·': '.'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

class ProfessionalPDF(FPDF):
    def header(self):
        # Encabezado elegante
        self.set_font('Arial', 'B', 20)
        self.set_text_color(0, 51, 102)
        self.cell(0, 15, self.title, 0, 1, 'C')

        self.set_font('Arial', 'I', 12)
        self.set_text_color(102, 102, 102)
        self.cell(0, 8, 'Curso Intensivo de Espanol - Nivel 3 CLM', 0, 1, 'C')

        self.set_text_color(0, 153, 51)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Periodo: 6 - 27 de noviembre de 2025', 0, 1, 'C')

        self.ln(10)

    def footer(self):
        # Pie de página elegante
        self.set_y(-25)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f'Pagina {self.page_no()} de {{nb}}', 0, 1, 'C')
        self.cell(0, 6, 'Profesor: Javier Benitez Lainez | Aula: A2', 0, 1, 'C')
        self.cell(0, 6, 'Universidad de Granada - Centro de Lenguas Modernas', 0, 0, 'C')

    def chapter_title(self, title):
        # Título de capítulo elegante
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, clean_text(title), 0, 1, 'L')
        self.ln(3)

    def section_title(self, title):
        # Título de sección
        self.set_font('Arial', 'B', 13)
        self.set_text_color(51, 102, 153)
        self.cell(0, 8, clean_text(title), 0, 1, 'L')
        self.ln(2)

    def body_text(self, text):
        # Texto del cuerpo
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, clean_text(text))
        self.ln(3)

    def highlight_box(self, title, content):
        # Caja resaltada con altura automática
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 102)

        # Calcular altura necesaria para el contenido
        lines = self.multi_cell(0, 5, clean_text(title), 0, 'L')
        title_height = len(title.split('\n')) * 5 + 5

        content_lines = content.split('\n')
        content_height = len(content_lines) * 5 + 10

        total_height = title_height + content_height + 10

        # Dibujar rectángulo con altura adecuada
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(100, 149, 237)
        self.rect(10, self.get_y(), 190, total_height, 'FD')

        # Agregar texto dentro del rectángulo
        self.set_y(self.get_y() + 3)
        self.cell(0, 5, clean_text(title), 0, 1, 'L')

        self.set_font('Arial', '', 11)
        self.set_text_color(51, 51, 51)
        for line in content_lines:
            self.cell(0, 5, clean_text(line), 0, 1, 'L')

        self.set_y(self.get_y() + 5)

    def bullet_point(self, text):
        # Punto de viñeta
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.cell(10, 5, '-', 0, 0)
        self.multi_cell(0, 5, clean_text(text))
        self.ln(1)

    def vocabulary_pair(self, spanish, english):
        # Par de vocabulario
        self.set_font('Arial', 'B', 11)
        self.cell(80, 6, clean_text(spanish), 0, 0)
        self.set_font('Arial', '', 10)
        self.set_text_color(102, 102, 102)
        self.cell(0, 6, f'- {english}', 0, 1)
        self.set_text_color(0, 0, 0)

def create_guia_curso_pdf():
    """Crear guía del curso profesional con espaciado optimizado"""

    pdf = ProfessionalPDF()
    pdf.title = 'Guia del Curso'
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)

    # Función para verificar espacio restante
    def check_space(required=30):
        if pdf.get_y() > 250:
            pdf.add_page()
            return True
        return False

    # Contenido principal
    pdf.chapter_title('Guia del Curso Intensivo de Espanol')

    pdf.highlight_box('Informacion del Curso',
                     'Profesor: Javier Benitez Lainez\n'
                     'Nivel: 3 CLM (A1.2-A2.1)\n'
                     'Periodo: 6 - 27 de noviembre de 2025\n'
                     'Duracion: 40 horas intensivas\n'
                     'Ubicacion: Centro de Lenguas Modernas, UGR')

    # Secciones optimizadas
    pdf.section_title('1. Informacion General')
    pdf.body_text('El Curso Intensivo de Espanol - Nivel 3 CLM esta disenado para estudiantes con '
                 'conocimientos basicos de espanol que desean alcanzar un nivel A2.1 en un corto '
                 'periodo de tiempo. Este curso de 40 horas combina clases teoricas con actividades '
                 'practicas para desarrollar las cuatro competencias linguisticas: '
                 'comprension auditiva, comprension lectora, expresion oral y expresion escrita.')

    check_space()
    pdf.section_title('2. Objetivos del Curso')
    pdf.body_text('Al finalizar el curso, los estudiantes seran capaces de:')

    objetivos = [
        'Participar en conversaciones basicas sobre temas cotidianos',
        'Comprender el lenguaje oral y escrito en espanol',
        'Producir textos sencillos en espanol (emails, mensajes, postales)',
        'Interactuar en situaciones practicas de la vida diaria',
        'Utilizar estructuras gramaticales basicas del espanol',
        'Apreciar aspectos culturales del mundo hispanohablante'
    ]

    for i, objetivo in enumerate(objetivos):
        if i > 0 and i % 3 == 0:  # Evitar grandes bloques
            check_space()
        pdf.bullet_point(objetivo)

    check_space()
    pdf.section_title('3. Metodologia')
    pdf.body_text('El curso utiliza una metodologia comunicativa y participativa que incluye:')

    metodologia = [
        'Clases interactivas con enfasis en la comunicacion',
        'Actividades en parejas y pequenos grupos',
        'Role-playing de situaciones reales',
        'Uso de materiales autenticos y adaptados',
        'Talleres practicos y actividades culturales',
        'Evaluacion continua para monitorear el progreso',
        'Feedback personalizado para cada estudiante'
    ]

    for i, metodo in enumerate(metodologia):
        if i > 0 and i % 3 == 0:
            check_space()
        pdf.bullet_point(metodo)

    check_space()
    pdf.section_title('4. Evaluacion')
    pdf.body_text('La evaluacion del curso combina componentes continuos y finales:')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, '60% - Evaluacion Continua:', 0, 1)
    pdf.set_font('Arial', '', 11)

    continua = [
        'Participacion activa en clase (20%)',
        'Tareas y actividades diarias (15%)',
        'Pruebas cortas semanales (15%)',
        'Proyecto final (10%)'
    ]

    for item in continua:
        pdf.bullet_point(f'{item}')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, '40% - Evaluacion Final:', 0, 1)
    pdf.set_font('Arial', '', 11)

    finales = [
        'Examen oral: Entrevista y conversacion (20%)',
        'Examen escrito: Comprension y expresion (20%)'
    ]

    for item in finales:
        pdf.bullet_point(f'{item}')

    check_space()
    pdf.section_title('5. Recursos y Materiales')
    pdf.body_text('Los estudiantes tendran acceso a:')

    recursos = [
        'Libro de texto principal: "Espanol en Vivo" Nivel A2',
        'Material complementario digital y fisico',
        'Plataforma online con ejercicios adicionales',
        'Biblioteca del Centro de Lenguas Modernas',
        'Laboratorio de idiomas con programas multimedia',
        'Tutorias individuales con el profesor'
    ]

    for i, recurso in enumerate(recursos):
        if i > 0 and i % 3 == 0:
            check_space()
        pdf.bullet_point(recurso)

    # Forzar nueva página para la sección de Horario y Asistencia
    pdf.add_page()
    pdf.section_title('6. Horario y Asistencia')
    pdf.body_text('El curso se desarrolla en el siguiente horario:')

    horario = [
        'Lunes y Miercoles: 08:30 - 10:30 (2 horas por dia)',
        'Jueves: 08:30 - 12:30 (4 horas)',
        'Total semanal: 8 horas de clase presencial',
        'Asistencia minima requerida: 85%',
        'Las faltas deben ser justificadas documentalmente'
    ]

    for item in horario:
        pdf.bullet_point(item)

    pdf.add_page()
    pdf.section_title('7. Contenido del Programa')

    pdf.body_text('El curso esta organizado en tres modulos principales:')

    # Modulo 1
    pdf.section_title('Modulo 1: Comunicacion Basica (Sesiones 1-4)')
    modulo1 = [
        'Saludos, presentaciones y despedidas',
        'Alfabeto espanol y pronunciacion',
        'Numeros, dias, meses y fechas',
        'Nacionalidades y paises hispanohablantes',
        'Familia y relaciones personales',
        'Descripciones fisicas y de caracter',
        'Rutina diaria y actividades habituales'
    ]

    for tema in modulo1:
        pdf.bullet_point(tema)

    # Modulo 2
    pdf.section_title('Modulo 2: Vida Cotidiana (Sesiones 5-8)')
    modulo2 = [
        'Comida, restaurantes y compras',
        'Transporte y direcciones',
        'Tiempo libre y hobbies',
        'Salud y emergencias medicas',
        'Bancos y dinero',
        'Hotel y aeropuerto',
        'Servicios y oficinas publicas',
        'Comunicacion telefonica y digital'
    ]

    for tema in modulo2:
        pdf.bullet_point(tema)

    # Modulo 3
    pdf.section_title('Modulo 3: Situaciones Especificas (Sesiones 9-12)')
    modulo3 = [
        'Trabajo y profesiones',
        'Educacion y estudios',
        'Cultura y costumbres espanolas',
        'Viajes y turismo',
        'Eventos sociales y celebraciones',
        'Medios de comunicacion',
        'Literatura y arte',
        'Proyectos integrados finales'
    ]

    for tema in modulo3:
        pdf.bullet_point(tema)

    pdf.section_title('8. Informacion de Contacto')
    pdf.body_text('Para cualquier duda o consulta:')

    contact = [
        'Profesor: Javier Benitez Lainez',
        'Ubicacion: Centro de Lenguas Modernas',
        'Secretaria: (+34) 958 24 27 28',
        'Email: clm@ugr.es',
        'Sitio web: www.clm.ugr.es'
    ]

    for info in contact:
        pdf.bullet_point(info)

    pdf.section_title('9. Recomendaciones')
    pdf.body_text('Para aprovechar al maximo el curso:')

    recomendaciones = [
        'Asistir puntualmente a todas las clases',
        'Participar activamente en las actividades',
        'Practicar espanol fuera del aula',
        'Utilizar los recursos adicionales proporcionados',
        'Formar grupos de estudio con companeros',
        'Preguntar cuando haya dudas',
        'Ser constante en el estudio'
    ]

    for recomendacion in recomendaciones:
        pdf.bullet_point(recomendacion)

    pdf.section_title('10. Politicas del Curso')
    pdf.body_text('Normas importantes:')

    politicas = [
        'Uso obligatorio de espanol en clase',
        'Respeto hacia companeros y profesor',
        'Puntualidad maxima y asistencia regular',
        'Entrega de tareas en las fechas establecidas',
        'Comunicacion previa de ausencias justificadas',
        'Cumplimiento con las normas del CLM'
    ]

    for politica in politicas:
        pdf.bullet_point(politica)

    pdf.set_y(pdf.get_y() + 20)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, 'Esta guia proporciona informacion basica del curso y puede estar', 0, 1, 'C')
    pdf.cell(0, 6, 'sujeta a cambios segun las necesidades del grupo.', 0, 0, 'C')

    pdf.output('materials/guia-curso.pdf')
    print("✅ Created professional guia-curso.pdf")

def create_vocabulario_esencial_pdf():
    """Crear vocabulario esencial profesional"""

    pdf = ProfessionalPDF()
    pdf.title = 'Vocabulario Esencial'
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title('Vocabulario Esencial - Nivel A1.2-A2.1')

    pdf.highlight_box('Objetivo',
                     'Este vocabulario cubre las palabras y expresiones mas importantes '
                     'para alcanzar el nivel A2.1 en espanol. Esta organizado por temas '
                     'utilidades para facilitar el aprendizaje.')

    # Saludos y presentaciones
    pdf.section_title('1. Saludos y Presentaciones')
    pdf.body_text('Expresiones basicas para conocerse y comunicarse en espanol:')

    saludos = [
        ('Hola', 'Hi / Hello'),
        ('Buenos dias', 'Good morning'),
        ('Buenas tardes', 'Good afternoon'),
        ('Buenas noches', 'Good evening / Good night'),
        ('Como estas?', 'How are you? (informal)'),
        ('Como esta usted?', 'How are you? (formal)'),
        ('Me llamo...', 'My name is...'),
        ('Mi nombre es...', 'My name is...'),
        ('Mucho gusto', 'Nice to meet you'),
        ('Encantado/a', 'Pleased to meet you'),
        ('Igualmente', 'Likewise'),
        ('Adios', 'Goodbye'),
        ('Hasta luego', 'See you later'),
        ('Hasta manana', 'See you tomorrow')
    ]

    for esp, ing in saludos:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('2. Tiempo y Fechas')
    pdf.body_text('Expresiones relacionadas con tiempo, dias y fechas:')

    tiempo = [
        ('Ahora', 'Now'),
        ('Despues', 'Later'),
        ('Antes', 'Before'),
        ('Hoy', 'Today'),
        ('Manana', 'Tomorrow'),
        ('Ayer', 'Yesterday'),
        ('La semana que viene', 'Next week'),
        ('La semana pasada', 'Last week'),
        ('Este fin de semana', 'This weekend'),
        ('En punto', 'Exactly, on the dot'),
        ('Tarde', 'Late'),
        ('Temprano', 'Early')
    ]

    dias_semana = [
        ('Lunes', 'Monday'),
        ('Martes', 'Tuesday'),
        ('Miercoles', 'Wednesday'),
        ('Jueves', 'Thursday'),
        ('Viernes', 'Friday'),
        ('Sabado', 'Saturday'),
        ('Domingo', 'Sunday'),
        ('Entre semana', 'Weekday'),
        ('Fin de semana', 'Weekend')
    ]

    meses = [
        ('Enero', 'January'),
        ('Febrero', 'February'),
        ('Marzo', 'March'),
        ('Abril', 'April'),
        ('Mayo', 'May'),
        ('Junio', 'June'),
        ('Julio', 'July'),
        ('Agosto', 'August'),
        ('Septiembre', 'September'),
        ('Octubre', 'October'),
        ('Noviembre', 'November'),
        ('Diciembre', 'December')
    ]

    for esp, ing in tiempo:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Dias de la Semana')
    for esp, ing in dias_semana:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Meses del Ano')
    for esp, ing in meses:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('3. Familia y Relaciones')
    pdf.body_text('Vocabulario para hablar sobre familia y relaciones personales:')

    familia = [
        ('La familia', 'The family'),
        ('Los padres', 'The parents'),
        ('El padre / papa', 'The father / dad'),
        ('La madre / mama', 'The mother / mom'),
        ('Los hijos', 'The children'),
        ('El hijo', 'The son'),
        ('La hija', 'The daughter'),
        ('El hermano', 'The brother'),
        ('La hermana', 'The sister'),
        ('Los abuelos', 'The grandparents'),
        ('El abuelo', 'The grandfather'),
        ('La abuela', 'The grandmother'),
        ('Los nietos', 'The grandchildren'),
        ('El nieto', 'The grandson'),
        ('La nieta', 'The granddaughter'),
        ('El tio', 'The uncle'),
        ('La tia', 'The aunt'),
        ('Los primos', 'The cousins'),
        ('El sobrino', 'The nephew'),
        ('La sobrina', 'The niece'),
        ('El esposo / marido', 'The husband'),
        ('La esposa / mujer', 'The wife'),
        ('El novio / pareja', 'The boyfriend / partner'),
        ('La novia / pareja', 'The girlfriend / partner'),
        ('El amigo', 'The friend (male)'),
        ('La amiga', 'The friend (female)'),
        ('Los amigos', 'The friends')
    ]

    for esp, ing in familia:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('4. Comida y Bebida')
    pdf.body_text('Vocabulario relacionado con comida, restaurantes y bebidas:')

    comidas_dia = [
        ('El desayuno', 'Breakfast'),
        ('La comida / almuerzo', 'Lunch'),
        ('La cena', 'Dinner'),
        ('La merienda', 'Snack'),
        ('Tener hambre', 'To be hungry'),
        ('Tener sed', 'To be thirsty'),
        ('Probar', 'To taste'),
        ('Saborear', 'To savor')
    ]

    alimentos = [
        ('La comida', 'Food'),
        ('La bebida', 'Drink'),
        ('El agua', 'Water'),
        ('El cafe', 'Coffee'),
        ('El te', 'Tea'),
        ('La leche', 'Milk'),
        ('El pan', 'Bread'),
        ('El arroz', 'Rice'),
        ('La pasta', 'Pasta'),
        ('La carne', 'Meat'),
        ('El pescado', 'Fish'),
        ('Las verduras', 'Vegetables'),
        ('La fruta', 'Fruit'),
        ('El postre', 'Dessert'),
        ('El helado', 'Ice cream'),
        ('El chocolate', 'Chocolate'),
        ('El azucar', 'Sugar'),
        ('La sal', 'Salt')
    ]

    for esp, ing in comidas_dia:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Alimentos y Bebidas')
    for esp, ing in alimentos:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('5. Lugares y Transporte')
    pdf.body_text('Vocabulario para lugares y medios de transporte:')

    lugares = [
        ('La casa', 'House / Home'),
        ('El apartamento', 'Apartment'),
        ('La ciudad', 'City'),
        ('El pueblo', 'Town'),
        ('La calle', 'Street'),
        ('La plaza', 'Square'),
        ('El parque', 'Park'),
        ('El hospital', 'Hospital'),
        ('La escuela', 'School'),
        ('La universidad', 'University'),
        ('El mercado', 'Market'),
        ('La tienda', 'Shop / Store'),
        ('El supermercado', 'Supermarket'),
        ('La farmacia', 'Pharmacy'),
        ('El restaurante', 'Restaurant'),
        ('El hotel', 'Hotel'),
        ('La estacion', 'Station'),
        ('El aeropuerto', 'Airport')
    ]

    transporte = [
        ('El coche', 'Car'),
        ('El autobus', 'Bus'),
        ('El metro', 'Subway / Metro'),
        ('El taxi', 'Taxi'),
        ('El tren', 'Train'),
        ('El avion', 'Airplane'),
        ('El barco', 'Boat / Ship'),
        ('La bicicleta', 'Bicycle'),
        ('El pie / a pie', 'On foot'),
        ('Ir', 'To go'),
        ('Venir', 'To come'),
        ('Llegar', 'To arrive'),
        ('Partir', 'To leave / depart'),
        ('Viajar', 'To travel')
    ]

    for esp, ing in lugares:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Transporte')
    for esp, ing in transporte:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('6. Actividades y Tiempo Libre')
    pdf.body_text('Vocabulario para actividades y tiempo libre:')

    actividades = [
        ('Trabajar', 'To work'),
        ('Estudiar', 'To study'),
        ('Leer', 'To read'),
        ('Escribir', 'To write'),
        ('Hablar', 'To speak'),
        ('Escuchar', 'To listen'),
        ('Mirar', 'To look at'),
        ('Ver', 'To see / watch'),
        ('Jugar', 'To play'),
        ('Bailar', 'To dance'),
        ('Cantar', 'To sing'),
        ('Comprar', 'To buy / shop'),
        ('Cocinar', 'To cook'),
        ('Limpiar', 'To clean'),
        ('Dormir', 'To sleep'),
        ('Descansar', 'To rest'),
        ('Nadar', 'To swim'),
        ('Correr', 'To run'),
        ('Caminar', 'To walk'),
        ('Viajar', 'To travel')
    ]

    tiempo_libre = [
        ('El tiempo libre', 'Free time'),
        ('El ocio', 'Leisure'),
        ('El hobby', 'Hobby'),
        ('El deporte', 'Sport'),
        ('El futbol', 'Soccer / Football'),
        ('El baloncesto', 'Basketball'),
        ('El tenis', 'Tennis'),
        ('La musica', 'Music'),
        ('El cine', 'Cinema / Movies'),
        ('La television', 'Television'),
        ('El libro', 'Book'),
        ('La revista', 'Magazine'),
        ('El partido', 'Match / Game'),
        ('El concierto', 'Concert'),
        ('La fiesta', 'Party')
    ]

    for esp, ing in actividades:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Tiempo Libre y Entretenimiento')
    for esp, ing in tiempo_libre:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('7. Adjetivos Utiles')
    pdf.body_text('Adjetivos comunes para describir personas y cosas:')

    adjetivos_personalidad = [
        ('Simpatico/a', 'Nice / Friendly'),
        ('Antipatico/a', 'Unfriendly'),
        ('Inteligente', 'Intelligent / Smart'),
        ('Tonto/a', 'Silly / Stupid'),
        ('Trabajador/a', 'Hard-working'),
        ('Vago/a', 'Lazy'),
        ('Divertido/a', 'Fun / Funny'),
        ('Aburrido/a', 'Boring'),
        ('Seriado/a', 'Serious'),
        ('Creativo/a', 'Creative'),
        ('Generoso/a', 'Generous'),
        ('Egoista', 'Selfish'),
        ('Amable', 'Kind / Friendly'),
        ('Rudo/a', 'Rude')
    ]

    adjetivos_fisicos = [
        ('Alto/a', 'Tall'),
        ('Bajo/a', 'Short'),
        ('Delgado/a', 'Thin'),
        ('Gordo/a', 'Fat'),
        ('Joven', 'Young'),
        ('Mayor', 'Old / Elderly'),
        ('Guapo/a', 'Handsome / Pretty'),
        ('Feo/a', 'Ugly'),
        ('Fuerte', 'Strong'),
        ('Debil', 'Weak'),
        ('Sano/a', 'Healthy'),
        ('Enfermo/a', 'Sick'),
        ('Cansado/a', 'Tired'),
        ('Feliz', 'Happy'),
        ('Triste', 'Sad'),
        ('Enamorado/a', 'In love')
    ]

    adjetivos_calidad = [
        ('Bueno/a', 'Good'),
        ('Malo/a', 'Bad'),
        ('Rico/a', 'Rich'),
        ('Pobre', 'Poor'),
        ('Nuevo/a', 'New'),
        ('Viejo/a', 'Old'),
        ('Grande', 'Big / Large'),
        ('Pequeno/a', 'Small'),
        ('Facil', 'Easy'),
        ('Dificil', 'Difficult'),
        ('Rapido/a', 'Fast / Quick'),
        ('Lento/a', 'Slow'),
        ('Barato/a', 'Cheap'),
        ('Caro/a', 'Expensive'),
        ('Caliente', 'Hot'),
        ('Frio/a', 'Cold'),
        ('Limpio/a', 'Clean'),
        ('Sucio/a', 'Dirty')
    ]

    pdf.section_title('Personalidad y Caracter')
    for esp, ing in adjetivos_personalidad:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Descripcion Fisica')
    for esp, ing in adjetivos_fisicos:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.section_title('Calidad y Estados')
    for esp, ing in adjetivos_calidad:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('8. Verbos Irregulares Importantes')
    pdf.body_text('Verbos irregulares mas comunes en espanol:')

    ser_estar = [
        ('Ser - soy, eres, es, somos, son', 'To be (permanent characteristics)'),
        ('Estar - estoy, estas, esta, estamos, estan', 'To be (temporary states/location)')
    ]

    tener = [
        ('Tener - tengo, tienes, tiene, tenemos, tienen', 'To have'),
        ('Tener hambre', 'To be hungry'),
        ('Tener sed', 'To be thirsty'),
        ('Tener que + infinitivo', 'To have to / Must')
    ]

    ir = [
        ('Ir - voy, vas, va, vamos, van', 'To go'),
        ('Ir + a + infinitivo', 'Going to + verb (future)')
    ]

    hacer = [
        ('Hacer - hago, haces, hace, hacemos, hacen', 'To do / to make'),
        ('Hacer calor / frio', 'To be hot / cold'),
        ('Hacer bien/mal', 'To do well/badly')
    ]

    poder = [
        ('Poder - puedo, puedes, puede, podemos, pueden', 'To be able to / Can'),
        ('Poder + infinitivo', 'To be able to')
    ]

    # Presentar cada irregular con conjugacion basica
    verbos_irregulares = [
        ('Decir', 'digo, dices, dice, decimos, dicen', 'To say / to tell'),
        ('Poner', 'pongo, pones, pone, ponemos, ponen', 'To put / to place'),
        ('Traer', 'traigo, traes, trae, traemos, traen', 'To bring'),
        ('Salir', 'salgo, sales, sale, salimos, salen', 'To leave / to go out'),
        ('Venir', 'vengo, vienes, viene, venimos, vienen', 'To come'),
        ('Querer', 'quiero, quieres, quiere, queremos, quieren', 'To want'),
        ('Saber', 'sé, sabes, sabe, sabemos, saben', 'To know (information)'),
        ('Conocer', 'conozco, conoces, conoce, conocemos, conocen', 'To know (people/places)'),
        ('Dar', 'doy, das, da, damos, dan', 'To give'),
        ('Ver', 'veo, ves, ve, vemos, ven', 'To see'),
        ('Oir', 'oigo, oyes, oye, oimos, oyen', 'To hear')
    ]

    # Ser y Estar
    pdf.vocabulary_pair('Ser', 'To be (permanent)')
    pdf.vocabulary_pair('Estar', 'To be (temporary)')
    pdf.ln(3)
    for esp, ing in ser_estar:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.vocabulary_pair('Tener', 'To have')
    for esp, ing in tener:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.vocabulary_pair('Ir', 'To go')
    for esp, ing in ir:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.vocabulary_pair('Hacer', 'To do / To make')
    for esp, ing in hacer:
        pdf.vocabulary_pair(esp, ing)

    pdf.ln(5)
    pdf.vocabulary_pair('Poder', 'To be able to / Can')
    for esp, ing in poder:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('Otros Verbos Irregulares')

    for verb, conjugacion, meaning in verbos_irregulares:
        pdf.vocabulary_pair(f'{verb} - {conjugacion}', meaning)

    pdf.section_title('9. Palabras de Transicion')
    pdf.body_text('Conectores y palabras de transicion:')

    transicion = [
        ('Y', 'And'),
        ('O', 'Or'),
        ('Pero', 'But'),
        ('Sin embargo', 'However'),
        ('Tambien', 'Also / Too'),
        ('Entonces', 'Then / So'),
        ('Porque', 'Because'),
        ('Aunque', 'Although / Even though'),
        ('Si', 'If'),
        ('Cuando', 'When'),
        ('Donde', 'Where'),
        ('Como', 'How / As'),
        ('Cuanto', 'How much / How many'),
        ('Que', 'That / Which / Who'),
        ('Para', 'For / In order to'),
        ('Por', 'For / By / Through'),
        ('Con', 'With'),
        ('Sin', 'Without'),
        ('Sobre', 'About / Over'),
        ('Debajo de', 'Under'),
        ('Detras de', 'Behind'),
        ('Delante de', 'In front of'),
        ('Encima de', 'On top of')
    ]

    for esp, ing in transicion:
        pdf.vocabulary_pair(esp, ing)

    pdf.add_page()
    pdf.section_title('10. Expresiones Utiles')
    pdf.body_text('Expresiones comunes y frases utiles:')

    expresiones = [
        ('Por favor', 'Please'),
        ('Gracias', 'Thank you'),
        ('De nada', 'You are welcome / No problem'),
        ('Lo siento', 'I am sorry'),
        ('Perdon / Disculpe', 'Excuse me / Pardon me'),
        ('Claro que si', 'Of course / Of course yes'),
        ('Por supuesto', 'Of course'),
        ('No hay problema', 'No problem'),
        ('No pasa nada', 'It is not a problem'),
        ('Es verdad', 'That is true'),
        ('No es verdad', 'That is not true'),
        ('Tienes razon', 'You are right'),
        ('No tienes razon', 'You are not right'),
        ('Me gustaria', 'I would like'),
        ('Quisiera', 'I would like'),
        ('Puede ayudarme?', 'Can you help me?'),
        ('No entiendo', 'I do not understand'),
        ('Puede repetir?', 'Can you repeat?'),
        ('Mas despacio, por favor', 'More slowly, please'),
        ('Como se dice...?', 'How do you say...?'),
        ('Que significa...?', 'What does... mean?'),
        ('Hablo espanol un poco', 'I speak a little Spanish'),
        ('Estoy aprendiendo espanol', 'I am learning Spanish')
    ]

    for esp, ing in expresiones:
        pdf.vocabulary_pair(esp, ing)

    pdf.set_y(pdf.get_y() + 20)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, 'Este vocabulario cubre las palabras mas importantes para', 0, 1, 'C')
    pdf.cell(0, 6, 'el nivel A2.1. Practica regularmente para dominarlas.', 0, 0, 'C')

    pdf.output('materials/vocabulario.pdf')
    print("✅ Created professional vocabulario.pdf")

def create_frases_utiles_pdf():
    """Crear frases útiles profesional"""

    pdf = ProfessionalPDF()
    pdf.title = 'Frases Utiles'
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title('Frases Utiles en Espanol')

    pdf.highlight_box('Objetivo',
                     'Coleccion de frases esenciales para comunicarse eficazmente '
                     'en espanol en diferentes situaciones de la vida diaria.')

    # Frases de presentacion
    pdf.section_title('1. Presentaciones')
    pdf.body_text('Frases para presentarse y conocer a otras personas:')

    presentaciones = [
        'Hola, me llamo [nombre].',
        'Mucho gusto en conocerte.',
        'Encantado/a de conocerte.',
        'Soy de [pais/ciudad].',
        'Tengo [edad] anos.',
        'Estudio espanol.',
        'Trabajo como [profesion].',
        'Vivo en [lugar].',
        '¿Como te llamas?',
        '¿De donde eres?',
        '¿Cuantos anos tienes?',
        '¿A que te dedicas?',
        '¿Estudias o trabajas?',
        '¿Vives solo o con familia?'
    ]

    for frase in presentaciones:
        pdf.bullet_point(frase)

    # Frases en restaurante
    pdf.section_title('2. En el Restaurante')
    pdf.body_text('Frases utiles para comer fuera de casa:')

    restaurante = [
        'Buenos dias, mesa para [numero] personas, por favor.',
        '¿Que recomienda para hoy?',
        'Que tal el plato del dia?',
        'Me gustaria...',
        'Quisiera pedir...',
        'Por favor, traigame...',
        'La cuenta, por favor.',
        '¿Cuesta mucho...?',
        '¿Tienen menu del dia?',
        '¿Son buenos los mariscos?',
        'Estoy vegetariano/a.',
        'No como carne.',
        '¿Tienen opcion sin gluten?',
        '¿Puede traernos agua?',
        'Postre, por favor.',
        'Cafe para mi, por favor.',
        'Estaba delicioso.',
        'La cuenta, por favor.',
        '¿Aceptan tarjetas de credito?'
    ]

    for frase in restaurante:
        pdf.bullet_point(frase)

    pdf.add_page()
    pdf.section_title('3. Haciendo Compras')
    pdf.body_text('Frases para comprar en tiendas:')

    compras = [
        'Busco...',
        '¿Dónde encuentro...?',
        '¿Cuanto cuesta?',
        '¿Está en oferta?',
        '¿Hay descuento?',
        '¿Puedo probarlo?',
        '¿Está en mi talla?',
        '¿Tienen en otro color?',
        '¿Aceptan devoluciones?',
        '¿Puedo pagar con tarjeta?',
        '¿Dónde estan los probadores?',
        '¿Me puede ayudar, por favor?',
        '¿Cuánto es en total?',
        '¿Puedo pagar en efectivo?',
        '¿Ofrecen garantía?',
        '¿Hay promociones especiales?'
    ]

    for frase in compras:
        pdf.bullet_point(frase)

    pdf.section_title('4. Pidiendo Direcciones')
    pdf.body_text('Frases para orientarse en la ciudad:')

    direcciones = [
        'Disculpe, ¿podría ayudarme?',
        '¿Dónde está [lugar]?',
        '¿Como llego a [lugar]?',
        '¿Está lejos de aquí?',
        '¿Puede indicarme en el mapa?',
        '¿Hay un... por aquí cerca?',
        'Siga todo recto hasta...',
        'Gire a la derecha/izquierda en...',
        'Suba por esta calle.',
        'Baje por esa avenida.',
        'Estoy perdido/a.',
        '¿Puede darme direcciones para...?',
        '¿Cuantas cuadras hay?',
        '¿A qué distancia está?',
        '¿Qué autobús tomo para ir a...?',
        '¿Dónde está la parada de metro más cercana?'
    ]

    for frase in direcciones:
        pdf.bullet_point(frase)

    pdf.add_page()
    pdf.section_title('5. En el Hotel y Transporte')
    pdf.body_text('Frases para alojamiento y transporte:')

    hotel = [
        'Tengo una reserva a nombre de...',
        '¿Hay una habitación disponible?',
        '¿Cuánto cuesta la habitación?',
        '¿Incluye el desayuno?',
        '¿A qué hora es el check-in/check-out?',
        '¿Hay wifi gratis?',
        '¿Dónde está el ascensor?',
        '¿Puede ayudarme con el equipaje?',
        'Necesito toallas adicionales.',
        'El aire acondicionado no funciona.',
        'No hay agua caliente.',
        '¿Puede hacerme una llamada despiertador?',
        '¿Hay servicio a la habitación?',
        '¿Dónde puedo encontrar...?'
    ]

    for frase in hotel:
        pdf.bullet_point(frase)

    pdf.ln(5)
    pdf.section_title('Transporte')

    transporte = [
        '¿Dónde está la estación de autobús?',
        '¿Qué autobús va a...?',
        '¿Cuánto es el billete para...?',
        '¿Necesito reservar con antelación?',
        '¿Está este asiento libre?',
        '¿Dónde está el metro?',
        '¿Qué línea de metro toma para ir a...?',
        '¿Cuántas paradas hay hasta...?',
        '¿El taxi está libre?',
        '¿Puede llevarme a [dirección]?',
        '¿Cuánto es la carrera hasta...?',
        '¿Acepta tarjeta de crédito?',
        '¿Hay servicio nocturno?'
    ]

    for frase in transporte:
        pdf.bullet_point(frase)

    pdf.add_page()
    pdf.section_title('6. En Situaciones Medicas')
    pdf.body_text('Frases para situaciones médicas:')

    medico = [
        'No me siento bien.',
        'Me duele [parte del cuerpo].',
        'Tengo dolor de cabeza.',
        'Tengo fiebre.',
        'Necesito ver a un médico.',
        '¿Hay una farmacia cerca?',
        '¿Qué horario tiene la farmacia?',
        '¿Podría recomendarme un médico?',
        'Tengo alergia a [medicamento].',
        '¿Tiene seguro médico?',
        '¿Puede recetarme algo para el dolor?',
        '¿Cuándo debo tomar este medicamento?',
        '¿Cuántas veces al día?',
        '¿Tiene efectos secundarios?',
        '¿Hay un hospital cerca de aquí?',
        'Es una emergencia.',
        'Llame una ambulancia, por favor.',
        '¿Habla inglés?'
    ]

    for frase in medico:
        pdf.bullet_point(frase)

    pdf.section_title('7. En el Trabajo')
    pdf.body_text('Frases útiles en contextos laborales:')

    trabajo = [
        'Buenos dias, compañeros.',
        '¿Cómo está el proyecto?',
        'Necesito ayuda con [tarea].',
        '¿Puedemos reunirnos a las [hora]?',
        'Tengo una reunión importante.',
        'El informe está listo.',
        '¿Cuándo es la fecha límite?',
        'Necesito más tiempo para terminar.',
        'Tengo algunas preguntas sobre...',
        '¿Podemos discutir este proyecto?',
        'Excelente trabajo, equipo.',
        'Felicidades por el éxito.',
        '¿Necesitas ayuda con algo?',
        '¿Cuál es el próximo paso?'
    ]

    for frase in trabajo:
        pdf.bullet_point(frase)

    pdf.add_page()
    pdf.section_title('8. En Situaciones Sociales')
    pdf.body_text('Frases para interacciones sociales:')

    sociales = [
        '¿Cómo estás?',
        '¿Qué tal todo?',
        '¿Qué tal tu fin de semana?',
        '¿Qué planes tienes para hoy/mañana?',
        'Te invito a cenar.',
        '¿Te gustaría tomar un café?',
        '¿Cuándo es tu cumpleaños?',
        '¡Felicidades!',
        'Muchas felicidades por...',
        'Te deseo mucho éxito.',
        'Pasa un buen fin de semana.',
        'Cuídate mucho.',
        'Nos vemos pronto.',
        'Te extraño.',
        'Mantenme informado/a.',
        '¿Hay algo nuevo interesante?'
    ]

    for frase in sociales:
        pdf.bullet_point(frase)

    pdf.section_title('9. Frases de Emergencia')
    pdf.body_text('Frases cruciales para emergencias:')

    emergencia = [
        '¡Ayuda!',
        '¡Socorro!',
        '¡Llame a la policía!',
        '¡Llame a una ambulancia!',
        '¡Hay un fuego!',
        'Peligro, salga.',
        'Es una emergencia.',
        '¿Hay alguien que hable inglés?',
        'Necesito ayuda urgente.',
        'No entiendo lo que está pasando.',
        '¿Dónde está el teléfono más cercano?',
        'Mi móvil está roto/perdido.',
        '¿Puede llamar al [número]?',
        '¡Cuidado!',
        '¡Peligro!',
        '¡Alto ahí!',
        '¡Váyase!',
        '¡Corra!'
    ]

    for frase in emergencia:
        pdf.bullet_point(frase)

    pdf.add_page()
    pdf.section_title('10. Frases Educativas')
    pdf.body_text('Frases útiles para estudiantes de español:')

    educativas = [
        'No entiendo esta palabra.',
        '¿Puede repetir, por favor?',
        '¿Puede hablar más despacio?',
        '¿Puede escribirlo, por favor?',
        '¿Cómo se pronuncia esta palabra?',
        '¿Qué significa esta expresión?',
        '¿Puede darme un ejemplo?',
        '¿Esta frase es formal o informal?',
        '¿Hay otra manera de decir esto?',
        '¿Cuándo se usa esta palabra?',
        '¿Puede corregir mi pronunciación?',
        'Estoy practicando mi español.',
        'Estoy aprendiendo.',
        'Necesito practicar más.',
        'Mi español no es muy bueno.',
        'Soy principiante.',
        '¿Podría explicarme otra vez?',
        '¿Podría darme más ejercicios?'
    ]

    for frase in educativas:
        pdf.bullet_point(frase)

    pdf.section_title('11. Expresiones de Tiempo y Clima')
    pdf.body_text('Frases sobre tiempo y clima:')

    tiempo_clima = [
        'Hace buen tiempo hoy.',
        'Está lloviendo.',
        'Hace sol.',
        'Hace frío.',
        'Hace calor.',
        'Hay nubes.',
        'Hace viento.',
        'Está nublado.',
        'El cielo está despejado.',
        '¿Cómo estará el tiempo mañana?',
        'Hace mucho frío calor hoy.',
        'Va a llover.',
        'El tiempo es cambiante.',
        '¿Cuál es la temperatura?',
        'Hace 25 grados centígrados.',
        '¿Qué tiempo hace en tu país?'
    ]

    for frase in tiempo_clima:
        pdf.bullet_point(frase)

    pdf.set_y(pdf.get_y() + 20)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, 'Estas frases cubren las situaciones mas comunes en la vida diaria.', 0, 1, 'C')
    pdf.cell(0, 6, 'Practícalas regularmente para mejorar tu fluidez en espanol.', 0, 0, 'C')

    pdf.output('materials/frases-utiles.pdf')
    print("✅ Created professional frases-utiles.pdf")

def create_verbos_irregulares_pdf():
    """Crear verbos irregulares profesional"""

    pdf = ProfessionalPDF()
    pdf.title = 'Verbos Irregulares'
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title('Verbos Irregulares Espanoles')

    pdf.highlight_box('Objetivo',
                     'Guía completa de los verbos irregulares mas importantes '
                     'del espanol con conjugaciones, usos y ejemplos prácticos.')

    pdf.section_title('SER vs ESTAR')
    pdf.body_text('Los dos verbos para "to be" en espanol:')

    pdf.body_text('SER - Características permanentes, identidad, profesión, nacionalidad:')
    ser_ejemplos = [
        'Soy estudiante.',
        'Eres español.',
        'El coche es rojo.',
        'Maria es alta.',
        'Somos amigos.',
        'Es importante.',
        'La clase es a las 10.',
        'El verano es caliente.'
    ]

    for ejemplo in ser_ejemplos:
        pdf.bullet_point(ejemplo)

    pdf.body_text('ESTAR - Ubicación, estado temporal, emociones, condiciones:')
    estar_ejemplos = [
        'Estoy en casa.',
        'Estás cansado.',
        'Está lloviendo.',
        'El café está caliente.',
        'Estamos contentos.',
        'El coche está en el aparcamiento.',
        'Mi celular está roto.',
        'Los niños están en la escuela.'
    ]

    for ejemplo in estar_ejemplos:
        pdf.bullet_point(ejemplo)

    # Presente simple
    pdf.add_page()
    pdf.section_title('Presente Simple - Tiempos y Conjugaciones')

    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 8, 'Presente Indicativo (Acciones habituales)', 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)

    # SER
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'SER:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    ser_presente = [
        'Yo soy',
        'Tú eres',
        'Él/ella/usted es',
        'Nosotros somos',
        'Vosotros sois',
        'Ellos/ellas/ustedes son'
    ]

    for forma in ser_presente:
        pdf.cell(80, 6, forma, 0, 1)

    pdf.ln(5)
    # ESTAR
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'ESTAR:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    estar_presente = [
        'Yo estoy',
        'Tú estás',
        'Él/ella/usted está',
        'Nosotros estamos',
        'Vosotros estáis',
        'Ellos/ellas/ustedes están'
    ]

    for forma in estar_presente:
        pdf.cell(80, 6, forma, 0, 1)

    # TENER
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'TENER:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    tener_presente = [
        'Yo tengo',
        'Tú tienes',
        'Él/ella/usted tiene',
        'Nosotros tenemos',
        'Vosotros tenéis',
        'Ellos/ellas/ustedes tienen'
    ]

    for forma in tener_presente:
        pdf.cell(80, 6, forma, 0, 1)

    # Verbos irregulares principales
    pdf.add_page()
    pdf.section_title('Verbos Irregulares Principales - Presente')

    verbos_irregulares = [
        {
            'verbo': 'IR (To go)',
            'presente': ['voy', 'vas', 'va', 'vamos', 'vais', 'van'],
            'usos': ['Voy al supermercado', 'Vas a la fiesta', 'Va a llover mañana'],
            'nota': 'Se usa IR A + infinitivo para expresar futuro inmediato'
        },
        {
            'verbo': 'TENER (To have)',
            'presente': ['tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen'],
            'usos': ['Tengo hambre', 'Tienes un coche nuevo', 'Tenemos mucha suerte'],
            'nota': 'Se usa TENER QUE + infinitivo para obligacion'
        },
        {
            'verbo': 'HACER (To do/make)',
            'presente': ['hago', 'haces', 'hace', 'hacemos', 'hacéis', 'hacen'],
            'usos': ['Hago la tarea', 'Haces buen trabajo', 'Hace calor hoy'],
            'nota': 'Tiene muchos significados diferentes'
        },
        {
            'verbo': 'PODER (Can/be able to)',
            'presente': ['puedo', 'puedes', 'puede', 'podemos', 'podéis', 'pueden'],
            'usos': ['Puedo hablar espanol', '¿Puedes ayudarme?', 'Puedes estudiar aqui'],
            'nota': 'Expresa habilidad o posibilidad'
        },
        {
            'verbo': 'DECIR (To say/tell)',
            'presente': ['digo', 'dices', 'dice', 'decimos', 'decís', 'dicen'],
            'usos': ['Digo la verdad', '¿Qué dices?', 'Dice que viene mañana'],
            'nota': 'Para reportar lo que alguien dijo'
        },
        {
            'verbo': 'PONER (To put/place)',
            'presente': ['pongo', 'pones', 'pone', 'ponemos', 'ponéis', 'ponen'],
            'usos': ['Pongo la mesa', 'Pones la música', 'Pone el libro en la mesa'],
            'nota': 'Para colocar o situar algo'
        },
        {
            'verbo': 'VENIR (To come)',
            'presente': ['vengo', 'vienes', 'viene', 'venimos', 'venís', 'vienen'],
            'usos': ['Vengo de España', '¿Viene con nosotros?', 'Viene mañana'],
            'nota': 'Expresa movimiento hacia el hablante'
        },
        {
            'verbo': 'TRAER (To bring)',
            'presente': ['traigo', 'traes', 'trae', 'traemos', 'traéis', 'traen'],
            'usos': ['Traigo mis libros', '¿Traes tu comida?', 'Trae los documentos'],
            'nota': 'Para transportar algo hacia aquí'
        },
        {
            'verbo': 'SALIR (To leave/go out)',
            'presente': ['salgo', 'sales', 'sale', 'salimos', 'salís', 'salen'],
            'usos': ['Salgo del trabajo a las 6', '¿Sales con nosotros?', 'Sale ahora'],
            'nota': 'Para salir de un lugar'
        },
        {
            'verbo': 'QUERER (To want)',
            'presente': ['quiero', 'quieres', 'quiere', 'queremos', 'queréis', 'quieren'],
            'usos': ['Quiero aprender español', '¿Quieres ir al cine?', 'Quiere viajar'],
            'nota': 'Para expresar deseos'
        },
        {
            'verbo': 'SABER (To know - information)',
            'presente': ['sé', 'sabes', 'sabe', 'sabemos', 'sabéis', 'saben'],
            'usos': ['Sé tu nombre', '¿Sabes la respuesta?', 'Sabe español muy bien'],
            'nota': 'Para conocimiento factual o habilidades'
        },
        {
            'verbo': 'CONOCER (To know - people/places)',
            'presente': ['conozco', 'conoces', 'conoce', 'conocemos', 'conocéis', 'conocen'],
            'usos': ['Conozco a tu hermana', '¿Conoces Granada?', 'Conoce muchos lugares'],
            'nota': 'Para familiaridad personal o lugares'
        },
        {
            'verbo': 'DAR (To give)',
            'presente': ['doy', 'das', 'da', 'damos', 'dais', 'dan'],
            'usos': ['Doy las gracias', 'Das un regalo', 'Da el dinero'],
            'nota': 'Para entregar algo a alguien'
        },
        {
            'verbo': 'VER (To see/watch)',
            'presente': ['veo', 'ves', 've', 'vemos', 'veis', 'ven'],
            'usos': ['Veo la televisión', '¿Ves ese coche?', 'Vemos la película'],
            'nota': 'Para percepción visual'
        },
        {
            'verbo': 'OIR (To hear)',
            'presente': ['oigo', 'oyes', 'oye', 'oímos', 'oís', 'oyen'],
            'usos': ['Oigo música', '¿Oyes ese ruido?', 'Oímos la noticia'],
            'nota': 'Para percepción auditiva'
        }
    ]

    for verbo_info in verbos_irregulares:
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 8, f'{verbo_info["verbo"]}:', 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(102, 102, 102)

        # Conjugaciones
        conjugacion_text = ', '.join(verbo_info['presente'])
        pdf.multi_cell(0, 6, f'Presente: {conjugacion_text}', 0, 1)

        # Usos
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(0, 102, 0)
        pdf.cell(0, 6, 'Ejemplos:', 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        for uso in verbo_info['usos']:
            pdf.bullet_point(uso)

        # Nota
        pdf.set_font('Arial', 'I', 9)
        pdf.set_text_color(102, 102, 102)
        pdf.set_x(20)
        pdf.multi_cell(0, 5, f'Nota: {verbo_info["nota"]}', 0, 1)

        pdf.ln(8)

    pdf.add_page()
    pdf.section_title('Participio Pasado y Participio Pasado')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Principales participios pasados:', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    participios = [
        ('SER', 'Fui, fuiste, fue, fuimos, fuisteis, fueron'),
        ('ESTAR', 'Estuve, estuviste, estuvo, estuvimos, estuvisteis, estuvieron'),
        ('TENER', 'Tuve, tuviste, tuvo, tuvimos, tuvisteis, tuvieron'),
        ('HACER', 'Hice, hiciste, hizo, hicimos, hicisteis, hicieron'),
        ('IR', 'Fui, fuiste, fue, fuimos, fuisteis, fueron'),
        ('DECIR', 'Dije, dijiste, dijo, dijimos, dijisteis, dijeron'),
        ('PONER', 'Puse, pusiste, puso, pusimos, pusisteis, pusieron'),
        ('VENIR', 'Vine, viniste, vino, vinimos, vinisteis, vinieron'),
        ('TRAER', 'Traje, trajiste, trajo, trajimos, trajisteis, trajeron'),
        ('SALIR', 'Salí, saliste, salió, salimos, salisteis, salieron'),
        ('QUERER', 'Quise, quisiste, quiso, quisimos, quisisteis, quisieron'),
        ('SABER', 'Supe, supiste, supo, supimos, supisteis, supieron'),
        ('CONOCER', 'Conocí, conociste, conoció, conocimos, conocisteis, conocieron')
    ]

    for verbo, participio in participios:
        pdf.vocabulary_pair(verbo, participio)

    pdf.add_page()
    pdf.section_title('Futuro Simple')

    pdf.body_text('El futuro simple se forma con el presente del IR + A + infinitivo:')

    futuro_ejemplos = [
        'Voy a estudiar mañana.',
        '¿Vas a venir a la fiesta?',
        'Va a llover más tarde.',
        'Vamos a comer restaurante.',
        'Van a viajar a España.',
        '¿Qué vas a hacer?',
        'No voy a trabajar el fin de semana.',
        'Van a construir una nueva casa.',
        '¿Van a empezar a las 3?',
        'Vamos a tener una reunión importante.'
    ]

    for ejemplo in futuro_ejemplos:
        pdf.bullet_point(ejemplo)

    pdf.section_title('Condicional Simple')
    pdf.body_text('Expresaría condicional con formas especiales:')

    condicional = [
        'Si tuviera dinero, compraría un coche.',
        'Si estuviera en casa, llamaría por teléfono.',
        'Si supieras la respuesta, me lo dirías.',
        'Si quisiera viajar, necesitaría un pasaporte.',
        'Si pudiera hablar japonés, viviría en Tokio.',
        'Si hiciera buen tiempo, iría a la playa.',
        'Si tuvieras tiempo, te ayudaría.',
        'Si hubiera más tiempo, terminaría el proyecto.',
        'Si supieras italiano, entenderíamos la conversación.'
    ]

    for ejemplo in condicional:
        pdf.bullet_point(ejemplo)

    pdf.section_title('Verbos con cambio radical')
    pdf.body_text('Verbos con cambios en la raíz en algunas formas:')

    cambios_radical = [
        ('EMPEZAR - empiezo, empiezas, empieza, empezamos, empiezan', 'Empezamos a las 9.'),
        ('ENTENDER - entiendo, entiendes, entiende, entendemos, entienden', '¿Entiendes la lección?'),
        ('PENSAR - pienso, piensas, piensa, pensamos, piensan', 'Pienso que es una buena idea.'),
        ('QUERER - quiero, quieres, quiere, queremos, quieren', 'Quiero aprender español.'),
        ('CERRAR - cierro, cierras, cierra, cerramos, cierran', 'Cierro la puerta.'),
        ('DEFENDER - defiendo, defiendes, defiende, defendemos, defienden', 'Defiendo mis amigos.'),
        ('VENCER - venzo, vences, vence, vencemos, vencen', 'Vencemos el obstáculo.'),
        ('PREFERIR - prefiero, prefieres, prefiere, preferimos, prefieren', 'Prefiero el chocolate.')
    ]

    for verbo, info in cambios_radical:
        if isinstance(info, list):
            pdf.vocabulary_pair(verbo, ', '.join(info))
            pdf.bullet_point(f'Ejemplo: {info[0]}')
        else:
            pdf.vocabulary_pair(verbo, info)

    pdf.add_page()
    pdf.section_title('Verbos con cambio vocálico')
    pdf.body_text('Verbos con cambios en la vocal en algunas personas:')

    cambios_vocalicos = [
        ('PODER - puedo, puedes, puede, podemos, pueden', 'Podemos ayudarte.'),
        ('DORMIR - duermo, duermes, duerme, dormimos, duermen', 'Duermo bien cada noche.'),
        ('MORIR - muero, mueres, muere, morimos, mueren', 'Los personajes mueren en la película.'),
        ('JUGAR - juego, juegas, juega, jugamos, juegan', '¿Jugamos al fútbol este fin de semana?'),
        ('CONTAR - cuento, cuentas, cuenta, contamos, cuentan', 'Cuento un chiste divertido.'),
        ('COSTAR - cuesto, cuestas, cuesta, costamos, cuestan', 'Cuánto cuesta este libro?'),
        ('VOLVER - vuelvo, vuelves, vuelve, volvemos, vuelven', 'Vuelvo a mi país cada año.')
    ]

    for verbo, info in cambios_vocalicos:
        pdf.vocabulary_pair(verbo, info)

    pdf.add_page()
    pdf.section_title('Verbos con cambio consonántico')
    pdf.body_text('Verbos con cambios en la consonante en algunas formas:')

    cambios_consonanticos = [
        ('CONOCER - conozco, conoces, conoce, conocemos, conocen', 'Conozco muy bien esta ciudad.'),
        ('CONDUCIR - conduzco, conduces, conduce, conducimos, conducen', 'Conduzco mi coche al trabajo.'),
        ('TRADUCIR - traduzco, traduces, traduce, traducimos, traducen', 'Traduzco este texto al inglés.'),
        ('PRODUCIR - produzco, produces, produce, producimos, producen', 'Esta fábrica produce coches.'),
        ('INTRODUCIR - introduzco, introduces, introduce, introducimos, introducen', 'Introduzco a mi familia.'),
        ('DEDUCIR - deduzco, deduces, deduce, deducimos, deducen', 'Deduzco que va a llover.'),
        ('REDUCIR - reduzco, reduces, reduce, reducimos, reducen', 'Reducimos los precios en las rebajas.'),
        ('ADQUIRIR - adquiero, adquieres, adquiere, adquirimos, adquieren', 'Adquirimos experiencia con el tiempo.')
    ]

    for verbo, info in cambios_consonanticos:
        pdf.vocabulary_pair(verbo, info)

    pdf.section_title('Verbos con irregularidades múltiples')
    pdf.body_text('Verbos con cambios irregulares en varias formas:')

    multiples = [
        ('TENER', 'tengo, tienes, tiene, tenemos, tienen; tuve, tuviste, tuvo, tuvimos, tuvieron'),
        ('ESTAR', 'estoy, estás, está, estamos, están; estuve, estuviste, estuvo, estuvimos, estuvieron'),
        ('ANDAR', 'ando, andas, anda, andamos, andan; anduve, anduviste, anduvo, anduvimos, anduvieron'),
        ('SABER', 'sé, sabes, sabe, sabemos, saben; supe, supiste, supo, supimos, supieron'),
        ('CABER', 'quepo, cabes, cabe, cabemos, caben; cupe, cupiste, cupo, cupimos, cupieron')
    ]

    for verbo, info in multiples:
        pdf.vocabulary_pair(verbo, info)

    pdf.set_y(pdf.get_y() + 20)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, 'Esta guía cubre los verbos irregulares mas importantes del espanol.', 0, 1, 'C')
    pdf.cell(0, 6, 'Practica las conjugaciones regularmente para dominarlos.', 0, 0, 'C')

    pdf.output('materials/verbos.pdf')
    print("✅ Created professional verbos.pdf")

def create_ejercicios_practicos_pdf():
    """Crear ejercicios prácticos profesional"""

    pdf = ProfessionalPDF()
    pdf.title = 'Ejercicios Practicos'
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title('Ejercicios Practicos de Espanol')

    pdf.highlight_box('Objetivo',
                     'Colección de ejercicios practicos para practicar y reforzar '
                     'los conceptos aprendidos en clase. Incluye respuestas para '
                     'autoevaluación.')

    # Ejercicio 1
    pdf.section_title('EJERCICIO 1: Ser o Estar')
    pdf.body_text('Completa con SER o ESTAR la forma correcta:')

    ser_estar_ejercicios = [
        ('1. Yo _____ estudiante de espanol.', 'soy'),
        ('2. La clase _____ muy interesante.', 'es'),
        ('3. Nosotros _____ en el aula.', ('estamos', 'somos')),
        ('4. Mi profesor _____ muy amable.', 'es'),
        ('5. Tu _____ de Estados Unidos.', 'eres'),
        ('6. Los libros _____ sobre la mesa.', ('estan', 'son')),
        ('7. Maria _____ en casa.', 'esta'),
        ('8. La clase _____ a las 9 de la manana.', 'es'),
        ('9. Espanol _____ un idioma muy bonito.', 'es'),
        ('10. Los estudiantes _____ muy aplicados.', ('están', 'son'))
    ]

    for i, (ejercicio, respuesta) in enumerate(ser_estar_ejercicios, 1):
        pdf.set_x(10)
        pdf.cell(0, 6, ejercicio, 0, 1)
        if isinstance(respuesta, tuple):
            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta: {respuesta[0]} o {respuesta[1]}', 0, 1)
        else:
            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta: {respuesta}', 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title('EJERCICIO 2: Presente de Indicativo')
    pdf.body_text('Completa las conjugaciones en presente:')

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Verbos terminados en -AR:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    ar_verbos = [
        ('HABLAR', 'hablo, hablas, habla, hablamos, hablan'),
        ('COMPRAR', 'compro, compras, compra, compramos, compran'),
        ('ESTUDIAR', 'estudio, estudias, estudia, estudiamos, estudian'),
        ('VIVIR', 'vivo, vives, vive, vivimos, viven')
    ]

    for verbo, conjugacion in ar_verbos:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(50, 6, f'{verbo}:', 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(102, 102, 102)
        pdf.cell(0, 6, conjugacion, 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(8)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Verbos terminados en -ER:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    er_verbos = [
        ('COMER', 'como, comes, come, comemos, comen'),
        ('BEBER', 'bebo, bebes, bebe, bebemos, beben'),
        ('VENDER', 'vendo, vendes, vende, vendemos, venden'),
        ('LEER', 'leo, lees, lee, leemos, leen'),
        ('ESCRIBIR', 'escribo, escribes, escribe, escribimos, escriben')
    ]

    for verbo, conjugacion in er_verbos:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(50, 6, f'{verbo}:', 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(102, 102, 102)
        pdf.cell(0, 6, conjugacion, 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(8)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Verbos terminados en -IR:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    ir_verbos = [
        ('VIVIR', 'vivo, vives, vive, vivimos, viven'),
        ('ESCRIBIR', 'escribo, escribes, escribe, escribimos, escriben'),
        ('ABRIR', 'abro, abres, abre, abrimos, abren'),
        ('PERMITIR', 'permito, permites, permite, permitimos, permiten'),
        ('RECIBIR', 'recibo, recibes, recibe, recibimos, reciben')
    ]

    for verbo, conjugacion in ir_verbos:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(50, 6, f'{verbo}:', 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(102, 102, 102)
        pdf.cell(0, 6, conjugacion, 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title('EJERCICIO 3: Numeros y Fechas')
    pdf.body_text('Escribe los siguientes numeros en espanol:')

    numeros_escribir = [
        ('15', 'quince'),
        ('23', 'veintitres'),
        ('31', ('treinta y uno', 'treinta y un')),
        ('42', 'cuarenta y dos'),
        ('58', 'cincuenta y ocho'),
        ('67', ('sesenta y siete', 'sesenta y siete')),
        ('74', 'setenta y cuatro'),
        ('89', 'ochenta y nueve'),
        ('95', 'noventa y cinco'),
        ('100', 'cien')
    ]

    for numero, respuesta in numeros_escribir:
        pdf.set_x(10)
        pdf.cell(0, 6, f'{numero} = ____________________', 0, 1)
        pdf.set_text_color(153, 0, 0)
        if isinstance(respuesta, tuple):
            pdf.cell(0, 6, f'Respuesta: {respuesta[0]} o {respuesta[1]}', 0, 1)
        else:
            pdf.cell(0, 6, f'Respuesta: {respuesta}', 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(10)
    pdf.body_text('Escribe la fecha completa de hoy:')
    pdf.set_x(10)
    pdf.cell(0, 6, 'Hoy es ____________________ de ____________________ de ________', 0, 1)

    pdf.add_page()
    pdf.section_title('EJERCICIO 4: Vocabulario de Familia')
    pdf.body_text('Completa las palabras que faltan:')

    familia_ejercicio = [
        ('1. El padre de mi padre es mi _____.', 'abuelo'),
        ('2. La hermana de mi madre es mi _____.', 'tia'),
        ('3. El hijo de mi hermano es mi _____.', 'sobrino'),
        ('4. La hija de mi tío es mi _____.', 'sobrina'),
        ('5. Los padres de mis padres son mis _____.', 'abuelos'),
        ('6. El hermano de mi madre es mi _____.', 'tio'),
        ('7. La mujer de mi tío es mi _____.', 'tia'),
        ('8. El hijo de mis padres es mi _____.', 'hermano', ['A. hermano', 'B. primo', 'C. compañero'], 'A'),
        ('9. La hija de mis padres es mi _____.', 'hermana', ['A. hermana', 'B. prima', 'C. compañera'], 'A'),
        ('10. El hermano de mi esposa es mi _____.', 'cuñado')
    ]

    for i, item in enumerate(familia_ejercicio, 1):
        ejercicio = item[0]
        respuesta = item[1]

        pdf.set_x(10)
        pdf.cell(0, 6, ejercicio, 0, 1)

        if len(item) > 2:  # Multiple choice question
            opciones = item[2]
            respuesta_correcta = item[3]

            for opcion in opciones:
                pdf.set_x(25)
                pdf.set_text_color(102, 102, 102)
                pdf.cell(0, 6, opcion, 0, 1)
                pdf.set_text_color(0, 0, 0)

            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta correcta: {respuesta_correcta}', 0, 1)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta: {respuesta}', 0, 1)
            pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title('EJERCICIO 5: Preposiciones')
    pdf.body_text('Completa con las preposiciones correctas (a, en, de, con, por, para):')

    preposiciones_ejercicios = [
        ('1. Voy ____ la escuela.', 'a'),
        ('2. Mi libro está ____ la mesa.', ('en', 'sobre')),
        ('3. Soy ____ España.', 'de'),
        ('4) ' + str(3), 'Hay ____ personas en la clase.', 'hay'),
        ('5) ' + str(5), 'Estudio español ____ 2 años.', ('desde', 'hace')),
        ('6. Comprocho leche ____ 2 euros.', 'por'),
        ('7. Este regalo es ____ ti.', 'para'),
        ('8) ' + str(8), 'Salgo ____ compras ____ mis amigos.', ('de', 'con')),
        ('9) ' + str(9), 'Pido ayuda ____ mis compañeros.', 'a'),
        ('10) ' + str(10), 'Hago la tarea ____ la tarde.', ('en', 'por'))
    ]

    for i, item in enumerate(preposiciones_ejercicios, 1):
        ejercicio = item[0]
        respuesta = item[1]

        pdf.set_x(10)
        pdf.cell(0, 6, ejercicio, 0, 1)

        if isinstance(respuesta, tuple):
            respuesta_text = ' o '.join(respuesta)
        else:
            respuesta_text = respuesta

        pdf.set_text_color(153, 0, 0)
        pdf.cell(0, 6, f'Respuesta: {respuesta_text}', 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title('EJERCICIO 6: Artículos Definidos e Indefinidos')
    pdf.body_text('Completa con EL, LA, LOS, LAS o UN, UNA, UNOS, UNAS:')

    articulos_ejercicios = [
        ('1. He comprado ____ coche nuevo.', 'un'),
        ('2. ____ clase es muy interesante.', 'La'),
        ('3. ____ niños juegan en el parque.', ('Los', 'Los niños')),
        ('4) ' + str(4), 'Necesito ____ diccionario.', ('un', 'el')),
        ('5) ' + str(5), '¿Dónde está ____ biblioteca?', ('la', 'la biblioteca')),
        ('6) ' + str(6), 'Leí ____ libro interesante.', ('un', 'un libro')),
        ('7) ' + str(7), 'Hace ____ día muy soleado.', ('un', 'el día')),
        ('8) ' + str(8), 'Quiero _____ café por favor.', ('un', 'un café')),
        ('9) ' + str(9), 'Me gustan ____ películas españolas.', ('las', 'las películas')),
        ('10) ' + str(10), 'Tengo ____ pregunta importante.', ('una', 'una pregunta'))
    ]

    for i, item in enumerate(articulos_ejercicios, 1):
        ejercicio = item[0]
        respuesta = item[1]

        pdf.set_x(10)
        pdf.cell(0, 6, ejercicio, 0, 1)
        if isinstance(respuesta, tuple):
            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta: {respuesta[0]}', 0, 1)
        else:
            pdf.set_text_color(153, 0, 0)
            pdf.cell(0, 6, f'Respuesta: {respuesta}', 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.section_title('EJERCICIO 7: Comparativos')
    pdf.body_text("Usa más que (más ... que), menos que (menos ... que) o tan ... como (tan ... como):")

    comparativos_ejercicios = [
        ('El elefante es ____ grande que el ratón.', 'más'),
        ('Esta calle es ____ larga que la anterior.', 'más'),
        ('Mi casa es ____ pequeña que tu casa.', 'más'),
        ('El español es ____ fácil que el chino.', 'más'),
        ('Este libro es ____ interesante que la película.', ('más', 'más')),
        ('El café está ____ caliente que el té.', 'más'),
        ('María es ____ alta que Ana.', 'más'),
        ('Este hotel es ____ caro que aquel.', 'más'),
        ('La vida en la ciudad es ____ rápida que en el pueblo.', 'más'),
        ('Este coche es ____ rápido que el autobús.', 'más'),
        ('La explicación es ____ clara que la del libro.', ('más', 'más')),
        ('El examen es ____ fácil que la práctica.', 'más')
    ]

    for i, (ejercicio, respuesta) in enumerate(comparativos_ejercicios, 1):
        pdf.set_x(10)
        pdf.multi_cell(0, 6, f'{i}. {ejercicio} {respuesta} [RESPUESTA]', 0, 1)
        pdf.ln(2)

    pdf.ln(5)
    pdf.body_text("Usa menos que (menos ... que):")

    menos_ejercicios = [
        ('Esta tarea es ____ fácil que la anterior.', 'menos'),
        ('Mi español es ____ bueno que el tuyo.', 'menos'),
        ('Este apartamento es ____ barato que el anterior.', 'menos'),
        ('El invierno es ____ frío que el verano.', 'menos'),
        ('Este trabajo es ____ aburrido que el anterior.', 'menos')
    ]

    for i, (ejercicio, respuesta) in enumerate(menos_ejercicios, len(comparativos_ejercicios) + 1):
        pdf.set_x(10)
        pdf.multi_cell(0, 6, f'{i}. {ejercicio} {respuesta} [RESPUESTA]', 0, 1)
        pdf.ln(2)

    pdf.ln(5)
    pdf.body_text("Usa tan ... como: (tan ... como):")

    tan_ejercicios = [
        ('Juan es ____ alto como Pedro.', 'tan'),
        ('María es ____ inteligente como su hermana.', 'tan'),
        ('Este coche es ____ caro como una casa.', 'tan'),
        ('La película es ____ larga como el libro.', 'tan'),
        ('El problema es ____ difícil como la solución.', 'tan')
    ]

    for i, (ejercicio, respuesta) in enumerate(tan_ejercicios, len(comparativos_ejercicios) + len(menos_ejercicios) + 1):
        pdf.set_x(10)
        pdf.multi_cell(0, 6, f'{i}. {ejercicio} {respuesta} [RESPUESTA]', 0, 1)
        pdf.ln(2)

    pdf.add_page()
    pdf.section_title('EJERCICIO 8: Diálogo Corto')
    pdf.body_text('Completa el siguiente diálogo:')

    dialogo = [
        'A: Hola, buenos días.',
        'B: ________________. Como estás?',
        'A: ________________, gracias. ¿Y tú?',
        'B: Muy bien. Me llamo Ana. Y tú?',
        'A: Me llamo ________________. Mucho gusto.',
        'B: ________________. De dónde eres?',
        'A: Soy de ________________. ¿Y tú?',
        'B: Yo soy de ________________.',
        'A: ¡Qué casual! Yo también soy de ese país.',
        'B: ¡Qué coincidencia! ¿Cuándo llegaste?',
        'A: Llegué el mes pasado para estudiar.',
        'B: Yo también. ¿Qué estás estudiando?',
        'A: Estudio _____. ¿Y tú?',
        'B: Yo estudio _____.'
    ]

    for i, linea in enumerate(dialogo, 1):
        pdf.set_x(10)
        if '________________' in linea or '_____' in linea:
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 6, linea, 0, 1)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 6, linea, 0, 1)

    pdf.set_y(pdf.get_y() + 10)
    pdf.section_title('Posibles Respuestas')
    pdf.set_text_color(153, 0, 0)

    dialogo_respuestas = [
        'A: Hola, buenos días.',
        'B: Estoy bien. Como estás?',
        'A: Estoy bien, gracias. ¿Y tú?',
        'B: Muy bien. Me llamo Ana. Y tú?',
        'A: Me llamo [nombre]. Mucho gusto.',
        'B: Encantada. De dónde eres?',
        'A: Soy de [país]. ¿Y tú?',
        'B: Yo soy de [país].',
        'A: ¡Qué coincidencia! Yo también soy de ese país.',
        'B: ¡Qué casualidad! ¿Cuándo llegaste?',
        'A: Llegué el mes pasado para estudiar.',
        'B: Yo también. ¿Qué estás estudiando?',
        'A: Estudio [materia]. ¿Y tú?',
        'B: Yo estudio [materia].'
    ]

    pdf.set_font('Arial', '', 11)
    for i, linea in enumerate(dialogo_respuestas, 1):
        pdf.set_x(10)
        pdf.cell(0, 6, linea, 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.set_y(pdf.get_y() + 15)
    pdf.section_title('EJERCICIO 9: Descripciones')
    pdf.body_text('Describe las siguientes imágenes (imagina que ves estas imágenes):')

    descripciones = [
        ('Imagen 1: Una persona sonriendo en la playa', 'Uso de ser/estar, adjetivos de personalidad'),
        ('Imagen 2: Una habitación moderna y ordenada', 'Uso de preposiciones, vocabulario de hogar'),
        ('Imagen 3: Un restaurante concurrido con gente comiendo', 'Vocabulario de comida, expresiones'),
        ('Imagen 4: Una persona trabajando con computadora', 'Profesiones, tecnología, acciones'),
        ('Imagen 5: Una clase de idiomas con estudiantes', 'Educación, actividades de clase')
    ]

    for i, (descripcion, nota) in enumerate(descripciones, 1):
        pdf.set_x(10)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 6, f'Foto {i}: {descripcion}', 0, 1)
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(102, 102, 102)
        pdf.cell(0, 5, f'Nota: {nota}', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.set_x(15)
        pdf.multi_cell(0, 4, 'Descripción:', 0, 1)
        pdf.ln(2)

    pdf.set_y(pdf.get_y() + 20)
    pdf.section_title('EJERCICIO 10: Comprensión Lectura')
    pdf.body_text('Lee el siguiente texto y responde las preguntas:')

    texto_comprension = '''
    Texto:
    María es estudiante del Centro de Lenguas Modernas de la Universidad de Granada. Ella viene de Estados Unidos y
    está aprendiendo español en un curso intensivo. Su clase es el nivel 3 CLM (A1.2-A2.1) y tiene clases
    todos los días excepto los fines de semana.

    María vive en un apartamento cerca del centro. Por las mañanas toma el autobús a la universidad.
    Le gusta el café español con leche y las tapas de Andalucía. Después de clase, generalmente almuerza
    en un bar tradicional con sus compañeros de clase.

    Por las tardes, María visita diferentes lugares turísticos de Granada como la Alhambra
    y los jardines del Generalife. Ella piensa que Granada es una ciudad muy bonita y segura.
    El tiempo es generalmente soleado y cálido, lo cual le permite disfrutar de las terrazas
    y plazas.

    Los fines de semana, María practica su español con amigos españoles. A veces preparan
    comida internacional donde cada uno trae platos de su país. María siempre lleva postres
    de manzana para compartir.

    A pesar de que su español no es perfecto, María puede mantener conversaciones básicas y
    entender la mayoría de las conversaciones cotidianas. Su meta es poder comunicarse
    eficazmente en español dentro de seis meses.
    '''

    pdf.multi_cell(0, 6, texto_comprension, 0, 1)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Preguntas:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)

    preguntas_comprension = [
        '1. ¿De dónde es María?',
        '2. ¿Qué nivel tiene en el CLM?',
        '3. ¿Cuándo tiene clases?',
        '4. ¿Cómo es el clima en Granada según el texto?',
        '5. ¿Qué le gusta hacer los fines de semana?',
        '6. ¿Cuál es su meta con el español?',
        '7. ¿Cómo es su español según el texto?'
    ]

    for i, pregunta in enumerate(preguntas_comprension, 1):
        pdf.set_x(20)
        pdf.cell(0, 6, pregunta, 0, 1)

    pdf.set_y(pdf.get_y() + 15)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, 'Espacio para respuestas:', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(20)
    pdf.multi_cell(0, 4, '________________________________________________________________', 0, 1)
    pdf.ln(2)
    pdf.set_x(20)
    pdf.multi_cell(0, 4, '________________________________________________________________', 0, 1)
    pdf.ln(2)
    pdf.set_x(20)
    pdf.multi_cell(0, 4, '________________________________________________________________', 0, 1)
    pdf.ln(2)
    pdf.set_x(20)
    pdf.multi_cell(0, 4, '________________________________________________________________', 0, 1)

    pdf.set_y(pdf.get_y() + 20)
    pdf.section_title('CLAVE DE RESPUESTAS')

    pdf.set_text_color(0, 153, 0)
    pdf.cell(0, 6, '1. Respuesta: Estados Unidos', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '2. Respuesta: Nivel 3 CLM (A1.2-A2.1)', 0, 1)
    pdf.set_text_color(0, 153, 0)
    pdf.cell(0, 6, '3. Respuesta: Todos los días excepto fines de semana', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '4. Respuesta: Soleado y cálido', 0, 1)
    pdf.set_text_color(0, 153, 0)
    pdf.cell(0, 6, '5. Respuesta: Practica español con amigos españoles', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '6. Respuesta: Comunicarse eficazmente en español en seis meses', 0, 1)
    pdf.set_text_color(0, 153, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '7. Respuesta: Puede mantener conversaciones básicas y entender la mayoría', 0, 1)

    pdf.set_y(pdf.get_y() + 20)
    pdf.set_font('Arial', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, '¡Buen trabajo con estos ejercicios! Practica regularmente para mejorar.', 0, 1, 'C')
    pdf.cell(0, 6, 'Recuerda que la práctica constante es clave para aprender español.', 0, 0, 'C')

    pdf.output('materials/ejercicios-practicos.pdf')
    print("✅ Created professional ejercicios-practicos.pdf")

def create_hoja_asistencia_pdf():
    """Crear hoja de asistencia para el curso"""

    pdf = ProfessionalPDF()
    pdf.title = 'Hoja de Asistencia'
    pdf.alias_nb_pages()
    pdf.add_page()

    # Título principal
    pdf.chapter_title('Hoja de Asistencia')
    pdf.chapter_title('Curso Intensivo de Espanol - Nivel 3 CLM')

    # Información del curso
    pdf.highlight_box('Informacion del Curso',
                     'Profesor: Javier Benitez Lainez\n'
                     'Periodo: 6 - 27 de noviembre de 2025\n'
                     'Duracion: 40 horas (8 horas semanales)\n'
                     'Asistencia minima requerida: 85%\n'
                     'Total de sesiones: 20 clases')

    # Instrucciones
    pdf.section_title('Instrucciones de Uso')
    pdf.body_text('Esta hoja de asistencia debe ser completada por el profesor en cada sesion. '
                 'Los estudiantes deben firmar para confirmar su presencia. '
                 'La asistencia se registra diariamente y se calcula el porcentaje acumulado.')

    # Tabla de asistencia
    pdf.section_title('Registro de Asistencia')
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0, 0, 0)

    # Encabezados de tabla
    headers = ['Fecha', 'Dia', 'Hora Inicio', 'Hora Fin', 'Firma']
    widths = [30, 20, 25, 25, 90]

    y_pos = pdf.get_y()

    # Línea de encabezado
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, y_pos, 200, y_pos)

    for i, header in enumerate(headers):
        x_pos = 10 + sum(widths[:i])
        pdf.set_x(x_pos)
        pdf.cell(widths[i], 8, header, 0, 0, 'C')

    y_pos += 8
    pdf.line(10, y_pos, 200, y_pos)

    # Filas de asistencia (20 sesiones)
    pdf.set_font('Arial', '', 10)
    sesiones = [
        ('6 nov', 'Jueves', '08:30', '12:30'),
        ('10 nov', 'Lunes', '08:30', '10:30'),
        ('12 nov', 'Miercoles', '08:30', '10:30'),
        ('13 nov', 'Jueves', '08:30', '12:30'),
        ('17 nov', 'Lunes', '08:30', '10:30'),
        ('19 nov', 'Miercoles', '08:30', '10:30'),
        ('20 nov', 'Jueves', '08:30', '12:30'),
        ('24 nov', 'Lunes', '08:30', '10:30'),
        ('26 nov', 'Miercoles', '08:30', '10:30'),
        ('27 nov', 'Jueves', '08:30', '12:30')
    ]

    for fecha, dia, inicio, fin in sesiones:
        y_pos += 10
        if y_pos > 260:  # Nueva página si es necesario
            pdf.add_page()
            y_pos = 50

        # Línea de separación
        pdf.line(10, y_pos - 1, 200, y_pos - 1)

        # Datos de la fila
        data = [fecha, dia, inicio, fin, '']
        for i, item in enumerate(data):
            x_pos = 10 + sum(widths[:i])
            pdf.set_x(x_pos)
            if i == 4:  # Columna de firma
                pdf.line(x_pos + 5, y_pos + 5, x_pos + 85, y_pos + 5)
                pdf.line(x_pos + 5, y_pos + 8, x_pos + 85, y_pos + 8)
            else:
                pdf.cell(widths[i], 8, item, 0, 0, 'C')

    # Línea final
    y_pos += 9
    pdf.line(10, y_pos, 200, y_pos)

    pdf.add_page()

    # Resumen de asistencia
    pdf.section_title('Resumen de Asistencia')
    pdf.body_text('Calculo del porcentaje de asistencia:')

    resumen_data = [
        ('Total de sesiones:', '20 clases'),
        ('Asistencia minima para aprobar:', '17 clases (85%)'),
        ('Total horas del curso:', '40 horas'),
        ('Horas minimas requeridas:', '34 horas')
    ]

    for concepto, valor in resumen_data:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(100, 8, concepto, 0, 0)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, valor, 0, 1)

    pdf.ln(10)

    # Sección de observaciones
    pdf.section_title('Observaciones y Notas')
    pdf.body_text('Espacio para registrar observaciones importantes sobre la asistencia:')

    pdf.set_font('Arial', '', 11)
    for i in range(8):
        pdf.set_x(15)
        pdf.cell(10, 6, f'{i+1}.', 0, 0)
        pdf.multi_cell(0, 6, '_________________________________________________________', 0, 1)

    # Firmas al final
    pdf.set_y(pdf.get_y() + 20)
    pdf.section_title('Firmas')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(90, 8, 'Firma del Profesor:', 0, 0)
    pdf.cell(0, 8, 'Firma del Coordinador:', 0, 1)

    pdf.ln(15)

    pdf.set_font('Arial', '', 11)
    pdf.cell(90, 6, '_______________________', 0, 0)
    pdf.cell(0, 6, '_______________________', 0, 1)

    pdf.cell(90, 6, 'Javier Benitez Lainez', 0, 0)
    pdf.cell(0, 6, 'Nombre y Apellidos', 0, 1)

    pdf.cell(90, 6, 'Profesor de Espanol', 0, 0)
    pdf.cell(0, 6, 'Coordinador CLM', 0, 1)

    pdf.output('materials/hoja-asistencia.pdf')
    print("✅ Created professional hoja-asistencia.pdf")

def main():
    """Crear todos los PDFs profesionales"""

    print("📚 Creating all professional PDFs for course materials...")

    # Asegurar que los directorios existan
    os.makedirs('materials', exist_ok=True)

    # Crear todos los PDFs
    create_guia_curso_pdf()
    create_vocabulario_esencial_pdf()
    create_frases_utiles_pdf()
    create_verbos_irregulares_pdf()
    create_ejercicios_practicos_pdf()
    create_hoja_asistencia_pdf()

    print("\n🎉 All professional PDFs created successfully!")
    print("📚 Course materials now have professional formatting and complete content")
    print("✨ Ready for students with educational value and beautiful presentation")

if __name__ == "__main__":
    main()