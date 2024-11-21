introduction_text = {
    'POR':
        """
         Esta Ferramenta de Visualização SkillCorner é um produto protótipo que visa possibilitar uma visualização fácil e 
         conveniente dos benchmarks Físicos e de Inteligência de Jogo da SkillCorner. Utilizando a ferramenta, os dados podem 
         ser agregados ao nível de jogador, equipe ou competição. Atualmente, quatro gráficos padrão da SkillCorner 
         estão disponíveis: gráfico de dispersão, gráfico de barras, tabela formatada e gráfico de radar. 
         Por favor, envie qualquer feedback sobre a aplicação para a equipe de Análise da SkillCorner. O aplicativo funciona em duas etapas:
        
         1. Solicitação dos dados da API.
         2. Agrupamento, filtragem e plotagem dos dados.
        
         [Open user guide](https://drive.google.com/file/d/1Z9xi1J_TXjsZf3funuHXAkgHc14a13IN/view?usp=sharing)
        """,
    'ENG':
        """
         This SkillCorner Visualisation Tool aims to enable easy & convenient
         visualisation of SkillCorner Physical & Game Intelligence benchmarks. Using the tool, data can be
         aggregated at player, team or competition level. Currently, four standard SkillCorner charts are
         available: scatter plot, bar chart, formatted table and radar plot. Please send any feedback on the application to the
         SkillCorner Analysis team. The app works in two stages:
    
         1. Requesting the data from the API.
         2. Grouping, filtering & plotting data. 
    
         [Open user guide](https://drive.google.com/file/d/1Z9xi1J_TXjsZf3funuHXAkgHc14a13IN/view?usp=sharing)\n
         """,
    'ESP':
        """
        Esta Herramienta de Visualización SkillCorner es un producto prototipo que tiene como objetivo permitir una 
        visualización fácil y conveniente de los benchmarks Físicos y de Inteligencia de Juego de SkillCorner. 
        Usando la herramienta, los datos se pueden agregar a nivel de jugador, equipo o competición. Actualmente, hay  
        cuatro gráfico estándar de SkillCorner disponibles: diagrama de dispersión, gráfico de barras, tabla formateada y gráfico de radar.
         Por favor, envíe cualquier comentario sobre la aplicación al equipo de Análisis de SkillCorner. 
         La aplicación funciona en dos etapas:
         
         1. Solicitud de los datos de la API.
         2. Agrupación, filtrado y visualización de los datos.
         
         [Open user guide](https://drive.google.com/file/d/1Z9xi1J_TXjsZf3funuHXAkgHc14a13IN/view?usp=sharing)
         """,
    'ITA':
        """
        Questo Strumento di Visualizzazione SkillCorner è un prodotto prototipo che mira a consentire una visualizzazione
        facile e conveniente dei benchmark Fisici e di Intelligenza di Gioco di SkillCorner. Utilizzando lo strumento,
        i dati possono essere aggregati a livello di giocatore, squadra o competizione. Attualmente, sono disponibili
        quattro grafici standard di SkillCorner: diagramma di dispersione, grafico a barre, tabella formattata e grafico radar. 
        Si prega di inviare qualsiasi feedback sull'applicazione al team di Analisi di SkillCorner. L'app funziona in due fasi:

        1. Richiesta dei dati dall'API.
        2. Raggruppamento, filtraggio e visualizzazione dei dati.
         
         [Open user guide](https://drive.google.com/file/d/1Z9xi1J_TXjsZf3funuHXAkgHc14a13IN/view?usp=sharing)
         """
}


RUN_TYPES_COUNT_READABLE = {
    'ENG':
        {'count_cross_receiver_runs_per_30_tip': 'Cross Receiver Runs',
         'count_runs_in_behind_per_30_tip': 'Runs in behind',
         'count_runs_ahead_of_the_ball_per_30_tip': 'Runs Ahead of the ball',
         'count_support_runs_per_30_tip': 'Support Runs',
         'count_coming_short_runs_per_30_tip': 'Coming short Runs',
         'count_dropping_off_runs_per_30_tip': 'Dropping Off Runs',
         'count_pulling_half_space_runs_per_30_tip': 'Pulling Half-space Runs',
         'count_pulling_wide_runs_per_30_tip': 'Pulling Wide Runs',
         'count_overlap_runs_per_30_tip': 'Overlap Runs',
         'count_underlap_runs_per_30_tip': 'Underlap Runs'},
    'ESP': {
        'count_cross_receiver_runs_per_30_tip': 'Carrera para recibir un centro',
        'count_runs_in_behind_per_30_tip': 'Carrera a espaldas de la defensa',
        'count_underlap_runs_per_30_tip': 'Desdoblamiento por dentro',
        'count_overlap_runs_per_30_tip': 'Desdoblamiento por fuera',
        'count_runs_ahead_of_the_ball_per_30_tip': 'Carrera delante del balon',
        'count_support_runs_per_30_tip': 'Carrera de apoyo',
        'count_pulling_half_space_runs_per_30_tip': 'Carrera al espacio entre lineas',
        'count_pulling_wide_runs_per_30_tip': 'Carrera de apertura a la banda',
        'count_coming_short_runs_per_30_tip': 'Carrera para recibir al pie',
        'count_dropping_off_runs_per_30_tip': 'Carrera de apoyo retrasado'
    },
    'FRA': {
        'count_cross_receiver_runs_per_30_tip': "Course pour être à la reception d'un centre",
        'count_runs_in_behind_per_30_tip': 'Course dans le dos de la défense',
        'count_underlap_runs_per_30_tip': 'Dédoubelement intérieur',
        'count_overlap_runs_per_30_tip': 'Dédoubelement extérieur',
        'count_runs_ahead_of_the_ball_per_30_tip': 'Courir devant le ballon',
        'count_support_runs_per_30_tip': 'Course de soutien',
        'count_pulling_half_space_runs_per_30_tip': 'Course pour écarter dans le demi-espace',
        'count_pulling_wide_runs_per_30_tip': 'Course pour écarter dans la largeur',
        'count_coming_short_runs_per_30_tip': 'Venir chercher dans les pieds',
        'count_dropping_off_runs_per_30_tip': 'Décrochage'
    },
    'GER': {
        'count_cross_receiver_runs_per_30_tip': 'Flanke erlaufen',
        'count_runs_in_behind_per_30_tip': 'Hinter die Kette',
        'count_underlap_runs_per_30_tip': 'Underlap',
        'count_overlap_runs_per_30_tip': 'Hinterlaufen',
        'count_runs_ahead_of_the_ball_per_30_tip': 'Nach vorne freilaufen',
        'count_support_runs_per_30_tip': 'Support-Run',
        'count_pulling_half_space_runs_per_30_tip': 'In den Halbraum ziehen',
        'count_pulling_wide_runs_per_30_tip': 'Auf den Flügel ziehen',
        'count_coming_short_runs_per_30_tip': 'Kurz kommen',
        'count_dropping_off_runs_per_30_tip': 'Fallen lassen'
    },
    'ITA': {
        'count_cross_receiver_runs_per_30_tip': 'Inserimento su cross',
        'count_runs_in_behind_per_30_tip': 'Superare la linea difensiva',
        'count_underlap_runs_per_30_tip': 'Sovrapposizione interna',
        'count_overlap_runs_per_30_tip': 'Sovrapposizione esterna',
        'count_runs_ahead_of_the_ball_per_30_tip': 'Corsa davanti alla palla',
        'count_support_runs_per_30_tip': 'Appoggio',
        'count_pulling_half_space_runs_per_30_tip': "Inserimento nell'half-space",
        'count_pulling_wide_runs_per_30_tip': 'Allargarsi',
        'count_coming_short_runs_per_30_tip': 'Accorciare',
        'count_dropping_off_runs_per_30_tip': 'Staccarsi dietro'
    },
    'POR': {
        'count_cross_receiver_runs_per_30_tip': 'Receptor de cruzamento',
        'count_runs_in_behind_per_30_tip': 'Superar a defesa',
        'count_underlap_runs_per_30_tip': 'Underlap',
        'count_overlap_runs_per_30_tip': 'Overlap',
        'count_runs_ahead_of_the_ball_per_30_tip': 'Correr na frente',
        'count_support_runs_per_30_tip': 'Suporte',
        'count_pulling_half_space_runs_per_30_tip': 'Entrar no half-space',
        'count_pulling_wide_runs_per_30_tip': 'Dar largura',
        'count_coming_short_runs_per_30_tip': 'Aproximar-se',
        'count_dropping_off_runs_per_30_tip': 'Baixar no espaço vazio'
    }
}

PASS_ATTEMPT_RUN_TYPES_COUNT_READABLE = {
    'ENG': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': 'Cross Receiver Runs',
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Runs in behind',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Runs Ahead of the ball',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Support Runs',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Coming short Runs',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Dropping Off Runs',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': 'Pulling Half-space Runs',
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Pulling Wide Runs',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Overlap Runs',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Underlap Runs'},
    'ESP': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': 'Carrera para recibir un centro',
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Carrera a espaldas de la defensa',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Desdoblamiento por dentro',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Desdoblamiento por fuera',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Carrera delante del balon',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Carrera de apoyo',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': 'Carrera al espacio entre lineas',
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Carrera de apertura a la banda',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Carrera para recibir al pie',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Carrera de apoyo retrasado'
    },
    'FRA': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': "Course pour être à la reception d'un centre",
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Course dans le dos de la défense',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Dédoubelement intérieur',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Dédoubelement extérieur',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Course devant le ballon',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Course de soutien',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': 'Course pour écarter dans le demi-espace',
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Course pour écarter dans la largeur',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Venir chercher dans les pieds',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Décrochage'
    },
    'GER': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': 'Flanke erlaufen',
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Hinter die Kette',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Underlap',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Hinterlaufen',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Nach vorne freilaufen',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Support-Run',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': 'In den Halbraum ziehen',
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Auf den Flügel ziehen',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Kurz kommen',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Fallen lassen'
    },
    'ITA': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': 'Inserimento su cross',
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Superare la linea difensiva',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Sovrapposizione interna',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Sovrapposizione esterna',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Corsa davanti alla palla',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Appoggio',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': "Inserimento nell'half-space",
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Allargarsi',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Accorciare',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Staccarsi dietro'
    },
    'POR': {
        'count_pass_attempts_to_cross_receiver_runs_per_30_tip': 'Receptor de cruzamento',
        'count_pass_attempts_to_runs_in_behind_per_30_tip': 'Superar a defesa',
        'count_pass_attempts_to_underlap_runs_per_30_tip': 'Underlap',
        'count_pass_attempts_to_overlap_runs_per_30_tip': 'Overlap',
        'count_pass_attempts_to_runs_ahead_of_the_ball_per_30_tip': 'Correr na frente',
        'count_pass_attempts_to_support_runs_per_30_tip': 'Suporte',
        'count_pass_attempts_to_pulling_half_space_runs_per_30_tip': 'Entrar no half-space',
        'count_pass_attempts_to_pulling_wide_runs_per_30_tip': 'Dar largura',
        'count_pass_attempts_to_coming_short_runs_per_30_tip': 'Aproximar-se',
        'count_pass_attempts_to_dropping_off_runs_per_30_tip': 'Baixar no espaço vazio'
    }

}

