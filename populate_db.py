from database import get_db_connection, init_db

EFOMM_SYLLABUS = {
    'Matemática': [
        'Teoria dos Conjuntos e Funções',
        'Funções Quadrática, Exponencial e Logarítmica',
        'Trigonometria (Identidades, Equações e Triângulos)',
        'Geometria Plana (Áreas, Semelhança, Polígonos)',
        'Geometria Espacial (Prismas, Pirâmides, Cilindros, Cones, Esferas)',
        'Geometria Analítica (Ponto, Reta, Circunferência e Cônicas)',
        'Números Complexos (Forma Algébrica e Trigonométrica)',
        'Polinômios e Equações Algébricas',
        'Matrizes, Determinantes e Sistemas Lineares',
        'Análise Combinatória e Probabilidade',
        'Progressão Aritmética (PA) e Geométrica (PG)',
        'Noções de Cálculo (Limites, Derivadas e Integrais)',
        'Álgebra Vetorial (Vetores no R2 e R3)'
    ],
    'Física': [
        'Cinemática Escalar e Vetorial (MUV, MCU, Lançamentos)',
        'Leis de Newton e suas Aplicações (Atrito, Plano Inclinado)',
        'Trabalho, Energia Cinética/Potencial e Conservação de Energia',
        'Impulso, Quantidade de Movimento e Colisões',
        'Estática dos Corpos Rígidos e Gravitação Universal',
        'Hidrostática (Pressão, Empuxo, Arquimedes, Pascal)',
        'Termometria, Dilatação Térmica e Calorimetria',
        'Gases Perfeitos e Leis da Termodinâmica',
        'Óptica Geométrica (Reflexão, Refração, Espelhos e Lentes)',
        'Movimento Harmônico Simples (MHS), Ondas e Acústica',
        'Eletrostática (Carga, Campo, Potencial e Trabalho)',
        'Eletrodinâmica (Resistores, Geradores, Receptores e Leis de Kirchhoff)',
        'Eletromagnetismo (Força Magnética, Campo Magnético e Indução)'
    ],
    'Português': [
        'Compreensão e Interpretação de Textos Literários e Não-literários',
        'Tipologia Textual e Gêneros de Discurso',
        'Morfologia (Substantivo, Adjetivo, Artigo, Numeral, Pronome)',
        'Morfologia (Verbo, Advérbio, Preposição, Conjunção, Interjeição)',
        'Sintaxe da Oração e do Período (Coordenação e Subordinação)',
        'Concordância Nominal e Concordância Verbal',
        'Regência Nominal e Regência Verbal',
        'Emprego do Sinal Indicativo de Crase',
        'Pontuação e seus Efeitos de Sentido',
        'Colocação Pronominal (Próclise, Ênclise, Mesóclise)',
        'Semântica (Sinonímia, Antonímia, Homonímia, Paronímia)',
        'Redação Dissertativa-Argumentativa (Estrutura e Coesão)'
    ],
    'Inglês': [
        'Reading Comprehension (Textos Técnicos e Gerais)',
        'Vocabulary (Synonyms, Antonyms, False Cognates)',
        'Nouns, Pronoms, Articles and Quantifiers',
        'Adjectives and Adverbs (Comparatives and Superlatives)',
        'Verb Tenses (Present, Past, Future - Simple/Continuous/Perfect)',
        'Active Voice vs. Passive Voice',
        'Modal Verbs (Can, Could, May, Might, Should, Must, etc.)',
        'Conditionals (Zero, First, Second, Third, Mixed)',
        'Direct and Indirect Speech (Reported Speech)',
        'Prepositions, Conjunctions and Linkers'
    ]
}

EFOMM_VIDEOS = {
    # ===================== MATEMÁTICA =====================
    'Teoria dos Conjuntos e Funções': [
        {'title': 'Conjuntos - Aula Completa (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=VRpmaeDniCo'},
        {'title': 'Funções: Noções Básicas (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=JlRMRnjCpec'},
    ],
    'Funções Quadrática, Exponencial e Logarítmica': [
        {'title': 'Função Quadrática - Aula Completa (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=hfIuCEBbJBo'},
        {'title': 'Função Exponencial e Logarítmica (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=b1lNL_2JQqU'},
    ],
    'Trigonometria (Identidades, Equações e Triângulos)': [
        {'title': 'Trigonometria no Triângulo Retângulo (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=u6e9PC0cE5A'},
        {'title': 'Círculo Trigonométrico - Aula Completa (Equaciona)', 'url': 'https://www.youtube.com/watch?v=6ywSfY5V9Rg'},
    ],
    'Geometria Plana (Áreas, Semelhança, Polígonos)': [
        {'title': 'Áreas de Figuras Planas (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=rOuu-eyWjhQ'},
        {'title': 'Semelhança de Triângulos (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=Z3e_2wR4mSU'},
    ],
    'Geometria Espacial (Prismas, Pirâmides, Cilindros, Cones, Esferas)': [
        {'title': 'Geometria Espacial - Prismas (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=xGS1ll9pS6s'},
        {'title': 'Cilindro, Cone e Esfera (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=qeBq5UGTksQ'},
    ],
    'Geometria Analítica (Ponto, Reta, Circunferência e Cônicas)': [
        {'title': 'Geometria Analítica: Ponto e Reta (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=0u7bIFwlftk'},
        {'title': 'Equação da Circunferência (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=tV83UW6Vfuc'},
    ],
    'Números Complexos (Forma Algébrica e Trigonométrica)': [
        {'title': 'Números Complexos - Introdução (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=pQSbKTq0YXA'},
        {'title': 'Forma Trigonométrica dos Complexos (Equaciona)', 'url': 'https://www.youtube.com/watch?v=6_VaOCjkFsE'},
    ],
    'Polinômios e Equações Algébricas': [
        {'title': 'Polinômios - Aula Completa (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=KNFrDwJkfPo'},
        {'title': 'Equações Polinomiais (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=o0SdeaOMRkk'},
    ],
    'Matrizes, Determinantes e Sistemas Lineares': [
        {'title': 'Matrizes - Aula Completa (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=r1k2Gm03hJY'},
        {'title': 'Determinantes e Sistemas Lineares (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=y70GZW0EdBg'},
    ],
    'Análise Combinatória e Probabilidade': [
        {'title': 'Análise Combinatória (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=OJnVJwC73OU'},
        {'title': 'Probabilidade - Aula Completa (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=KaR3cM-4c8s'},
    ],
    'Progressão Aritmética (PA) e Geométrica (PG)': [
        {'title': 'Progressão Aritmética PA (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=m7q46R_DNSk'},
        {'title': 'Progressão Geométrica PG (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=t8pJvVEPKxI'},
    ],
    'Noções de Cálculo (Limites, Derivadas e Integrais)': [
        {'title': 'Limites - Introdução ao Cálculo (Prof. Grings)', 'url': 'https://www.youtube.com/watch?v=VEb0Bk3oGQw'},
        {'title': 'Derivadas - Noções Básicas (Prof. Grings)', 'url': 'https://www.youtube.com/watch?v=YL_2L-eQEF0'},
    ],
    'Álgebra Vetorial (Vetores no R2 e R3)': [
        {'title': 'Vetores no Plano e no Espaço (Prof. Ferretto)', 'url': 'https://www.youtube.com/watch?v=GXqCAi5sOBM'},
        {'title': 'Produto Escalar e Vetorial (Matemática Rio)', 'url': 'https://www.youtube.com/watch?v=421FPJMn98Q'},
    ],

    # ===================== FÍSICA =====================
    'Cinemática Escalar e Vetorial (MUV, MCU, Lançamentos)': [
        {'title': 'Cinemática - MRU e MRUV (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=AZd1-hMN89Q'},
        {'title': 'Lançamento Oblíquo e MCU (Física Total)', 'url': 'https://www.youtube.com/watch?v=O5Z2k5NfLSI'},
    ],
    'Leis de Newton e suas Aplicações (Atrito, Plano Inclinado)': [
        {'title': 'Leis de Newton - Aula Completa (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=9YCaCHXCf2M'},
        {'title': 'Plano Inclinado e Atrito (Física Total)', 'url': 'https://www.youtube.com/watch?v=z6BFGDR0CRY'},
    ],
    'Trabalho, Energia Cinética/Potencial e Conservação de Energia': [
        {'title': 'Trabalho e Energia - Aula Completa (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=2F45ZBdvVww'},
        {'title': 'Conservação de Energia Mecânica (Física Total)', 'url': 'https://www.youtube.com/watch?v=RLaF_9Vz-d4'},
    ],
    'Impulso, Quantidade de Movimento e Colisões': [
        {'title': 'Impulso e Quantidade de Movimento (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=5h7VNqN3e6I'},
        {'title': 'Colisões - Elástica e Inelástica (Física Total)', 'url': 'https://www.youtube.com/watch?v=xG01GqjSAos'},
    ],
    'Estática dos Corpos Rígidos e Gravitação Universal': [
        {'title': 'Estática - Torque e Equilíbrio (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=uKlVOiQ3MjQ'},
        {'title': 'Gravitação Universal - Leis de Kepler (Física Total)', 'url': 'https://www.youtube.com/watch?v=7KG14gcIWDQ'},
    ],
    'Hidrostática (Pressão, Empuxo, Arquimedes, Pascal)': [
        {'title': 'Hidrostática - Pressão e Empuxo (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=kEROZqKSmFM'},
        {'title': 'Princípio de Pascal e Arquimedes (Física Total)', 'url': 'https://www.youtube.com/watch?v=MJj2aYqSMFI'},
    ],
    'Termometria, Dilatação Térmica e Calorimetria': [
        {'title': 'Termologia - Escalas e Dilatação (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=0PYDI-4lN0c'},
        {'title': 'Calorimetria - Aula Completa (Física Total)', 'url': 'https://www.youtube.com/watch?v=3z_F1HVBAOQ'},
    ],
    'Gases Perfeitos e Leis da Termodinâmica': [
        {'title': 'Estudo dos Gases - Clapeyron (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=njcEiBMhOHM'},
        {'title': 'Termodinâmica - 1ª e 2ª Lei (Física Total)', 'url': 'https://www.youtube.com/watch?v=U-wW0WlSddo'},
    ],
    'Óptica Geométrica (Reflexão, Refração, Espelhos e Lentes)': [
        {'title': 'Óptica - Reflexão e Espelhos (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=FS_V50w_R_4'},
        {'title': 'Refração e Lentes (Física Total)', 'url': 'https://www.youtube.com/watch?v=TiGYi2dBQBs'},
    ],
    'Movimento Harmônico Simples (MHS), Ondas e Acústica': [
        {'title': 'MHS - Movimento Harmônico Simples (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=Bp1-kkJLU_A'},
        {'title': 'Ondas - Aula Completa (Física Total)', 'url': 'https://www.youtube.com/watch?v=0Nw8VQq-jYY'},
    ],
    'Eletrostática (Carga, Campo, Potencial e Trabalho)': [
        {'title': 'Eletrostática - Lei de Coulomb (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=IJfrkLqvv_Y'},
        {'title': 'Campo Elétrico e Potencial (Física Total)', 'url': 'https://www.youtube.com/watch?v=VcJm5bS8GbE'},
    ],
    'Eletrodinâmica (Resistores, Geradores, Receptores e Leis de Kirchhoff)': [
        {'title': 'Eletrodinâmica - Leis de Ohm (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=Mx1XBZH4qJA'},
        {'title': 'Circuitos Elétricos - Kirchhoff (Física Total)', 'url': 'https://www.youtube.com/watch?v=B-QW6twei30'},
    ],
    'Eletromagnetismo (Força Magnética, Campo Magnético e Indução)': [
        {'title': 'Eletromagnetismo - Campo Magnético (Prof. Boaro)', 'url': 'https://www.youtube.com/watch?v=2-s_9K7GZXE'},
        {'title': 'Indução Eletromagnética - Faraday (Física Total)', 'url': 'https://www.youtube.com/watch?v=sVP6m1j-O7o'},
    ],

    # ===================== PORTUGUÊS =====================
    'Compreensão e Interpretação de Textos Literários e Não-literários': [
        {'title': 'Interpretação de Texto - Dicas (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=b-VCzLiyFxk'},
        {'title': 'Como Interpretar Textos para Concursos (Grancursos)', 'url': 'https://www.youtube.com/watch?v=o6fN_gUfPIg'},
    ],
    'Tipologia Textual e Gêneros de Discurso': [
        {'title': 'Tipos de Texto - Narrativo, Descritivo, Dissertativo (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=pPmMGHYxv2A'},
        {'title': 'Gêneros Textuais (Brasil Escola)', 'url': 'https://www.youtube.com/watch?v=T5TmK9-c_qA'},
    ],
    'Morfologia (Substantivo, Adjetivo, Artigo, Numeral, Pronome)': [
        {'title': 'Classes de Palavras - Substantivo e Adjetivo (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=RjOLvVAYrag'},
        {'title': 'Pronomes - Aula Completa (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=UcGM9Pg0P6Q'},
    ],
    'Morfologia (Verbo, Advérbio, Preposição, Conjunção, Interjeição)': [
        {'title': 'Verbos - Aula Completa (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=gxdqWCqBJ4s'},
        {'title': 'Conjunções Coordenativas e Subordinativas (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=wy4IWsHpxpQ'},
    ],
    'Sintaxe da Oração e do Período (Coordenação e Subordinação)': [
        {'title': 'Análise Sintática - Termos da Oração (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=t6WsgwSQsKY'},
        {'title': 'Orações Subordinadas (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=x16SHk3bv2c'},
    ],
    'Concordância Nominal e Concordância Verbal': [
        {'title': 'Concordância Verbal - Regras (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=58BRYNEiJGs'},
        {'title': 'Concordância Nominal (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=dHUQVPIEbDE'},
    ],
    'Regência Nominal e Regência Verbal': [
        {'title': 'Regência Verbal (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=VCMCjkzrE2E'},
        {'title': 'Regência Nominal (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=4_J68d7M10Y'},
    ],
    'Emprego do Sinal Indicativo de Crase': [
        {'title': 'Crase - Quando Usar e Quando Não Usar (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=Q0NVGlXqH0I'},
        {'title': 'Crase - Exercícios Resolvidos (Grancursos)', 'url': 'https://www.youtube.com/watch?v=Kh8c71dQn14'},
    ],
    'Pontuação e seus Efeitos de Sentido': [
        {'title': 'Uso da Vírgula - Regras Essenciais (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=KtTATGXAfwE'},
        {'title': 'Sinais de Pontuação (Brasil Escola)', 'url': 'https://www.youtube.com/watch?v=FrtXvuLsOIs'},
    ],
    'Colocação Pronominal (Próclise, Ênclise, Mesóclise)': [
        {'title': 'Colocação Pronominal (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=QWG2RhIbBvo'},
        {'title': 'Próclise, Ênclise e Mesóclise - Exercícios (Grancursos)', 'url': 'https://www.youtube.com/watch?v=dZNs3q_jh3o'},
    ],
    'Semântica (Sinonímia, Antonímia, Homonímia, Paronímia)': [
        {'title': 'Semântica - Sinônimos, Antônimos, Parônimos (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=r-MHFET_dxQ'},
        {'title': 'Figuras de Linguagem (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=kORCAhJ8Yuw'},
    ],
    'Redação Dissertativa-Argumentativa (Estrutura e Coesão)': [
        {'title': 'Como Fazer uma Redação Nota 1000 (Prof. Noslen)', 'url': 'https://www.youtube.com/watch?v=M33FHIuxCOo'},
        {'title': 'Estrutura do Texto Dissertativo (Brasil Escola)', 'url': 'https://www.youtube.com/watch?v=ZqFjBJcFG2g'},
    ],

    # ===================== INGLÊS =====================
    'Reading Comprehension (Textos Técnicos e Gerais)': [
        {'title': 'Reading Comprehension Tips (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=dMTw_M8Xdnk'},
        {'title': 'Interpretação de Textos em Inglês (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=DFP_MxPuLzI'},
    ],
    'Vocabulary (Synonyms, Antonyms, False Cognates)': [
        {'title': 'Falsos Cognatos em Inglês (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=gxX6_EgAFXk'},
        {'title': '100 Palavras Mais Usadas em Inglês (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=yd9T1rMjBV8'},
    ],
    'Nouns, Pronoms, Articles and Quantifiers': [
        {'title': 'Pronouns in English - Pronomes (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=ykhbXnIYnIg'},
        {'title': 'Articles A, An, The (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=Sq8hTYI7r60'},
    ],
    'Adjectives and Adverbs (Comparatives and Superlatives)': [
        {'title': 'Comparatives and Superlatives (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=CQ4G8SNkrWw'},
        {'title': 'Adjectives em Inglês (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=UDR0G4W5QCc'},
    ],
    'Verb Tenses (Present, Past, Future - Simple/Continuous/Perfect)': [
        {'title': 'Todos os Tempos Verbais em Inglês (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=JwBEyKcDQps'},
        {'title': 'Present Perfect x Simple Past (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=ykQ8JFG3frI'},
    ],
    'Active Voice vs. Passive Voice': [
        {'title': 'Passive Voice - Voz Passiva (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=sMtjE7-fyyg'},
        {'title': 'Active vs Passive Voice (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=3w-lVmmP9aQ'},
    ],
    'Modal Verbs (Can, Could, May, Might, Should, Must, etc.)': [
        {'title': 'Modal Verbs - Verbos Modais (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=UKq-M9ms7Ic'},
        {'title': 'Can, Could, May, Might, Should (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=B92QHeFKxKU'},
    ],
    'Conditionals (Zero, First, Second, Third, Mixed)': [
        {'title': 'If Clauses - Condicionais em Inglês (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=H-eSFm2s5Gw'},
        {'title': 'Conditionals Explicados (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=GjLB3k5se68'},
    ],
    'Direct and Indirect Speech (Reported Speech)': [
        {'title': 'Reported Speech - Discurso Indireto (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=0Q0z9EKTCGM'},
        {'title': 'Direct and Indirect Speech (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=YvV9c6F0OHw'},
    ],
    'Prepositions, Conjunctions and Linkers': [
        {'title': 'Prepositions In, On, At (English in Brazil)', 'url': 'https://www.youtube.com/watch?v=pFh5kv6UD60'},
        {'title': 'Linking Words - Conectivos (Mairo Vergara)', 'url': 'https://www.youtube.com/watch?v=x6sKfYvPeIU'},
    ],
}

def populate_topics():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM efomm_topics')
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Os tópicos já foram populados anteriormente (total: {count}). Pulando...")
        conn.close()
        return

    print("Populando banco de dados com os tópicos da EFOMM...")
    
    for subject, topics in EFOMM_SYLLABUS.items():
        for topic in topics:
            cursor.execute(
                'INSERT INTO efomm_topics (subject, topic_name, status, notes) VALUES (?, ?, ?, ?)',
                (subject, topic, 'not_started', '')
            )
            
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM efomm_topics')
    new_count = cursor.fetchone()[0]
    print(f"Inseridos {new_count} tópicos no banco de dados!")
    conn.close()

def populate_videos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM efomm_videos')
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Os vídeos já foram populados anteriormente (total: {count}). Pulando...")
        conn.close()
        return

    print("Populando banco de dados com os vídeos da EFOMM...")
    
    cursor.execute('SELECT id, topic_name FROM efomm_topics')
    topics_list = cursor.fetchall()
    topic_map = {row['topic_name']: row['id'] for row in topics_list}
    
    inserted_count = 0
    for topic_name, videos in EFOMM_VIDEOS.items():
        if topic_name in topic_map:
            topic_id = topic_map[topic_name]
            for video in videos:
                cursor.execute(
                    'INSERT INTO efomm_videos (topic_id, title, url) VALUES (?, ?, ?)',
                    (topic_id, video['title'], video['url'])
                )
                inserted_count += 1
                
    conn.commit()
    print(f"Inseridos {inserted_count} vídeos no banco de dados!")
    conn.close()

if __name__ == '__main__':
    populate_topics()
    populate_videos()
