#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build cheatsheet_<lang>.html — the 12-principle exam cheatsheet (EN/ES/PT).

Usage: python3 utils/build_cheatsheet.py

Self-contained static pages in the repo's light/Inter theme with the Ravn topbar.
Stats are kept in sync with the 136-question, 5-domain exam; domain names match
utils/exam_data.py (DOMAIN_NAMES). The deploy workflow does not run this script —
it copies the committed cheatsheet_*.html via scripts/build-pages.mjs — so re-run
this only when editing the cheatsheet content, then commit the regenerated files."""
import re, os, json, html

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(UTILS_DIR)

# --- reuse the favicon data-URI from exam_en.html ---
exam = open(os.path.join(REPO, "exam_en.html"), encoding="utf-8").read()
favicon = re.search(r'href="(data:image/png;base64,[A-Za-z0-9+/=]+)"', exam).group(1)

# --- exam questions per language (for the per-principle dropdowns) ---
def _load_exam(lang):
    s = open(os.path.join(REPO, f"exam_{lang}.html"), encoding="utf-8").read()
    i = s.find("const QUESTIONS = ")
    arr = json.JSONDecoder().raw_decode(s[s.find("[", i):])[0]
    d, order = {}, []
    for x in arr:
        corr = next((o for o in x["options"] if o.get("correct")), None)
        d[x["id"]] = {
            "scenario": x.get("scenario") or "",
            "situation": x.get("situation") or "",
            "prompt": x.get("question") or "",
            "letter": corr["letter"] if corr else "",
            "text": corr["text"] if corr else "",
            "exp": (corr.get("explanation") or "") if corr else "",
        }
        order.append(x["id"])
    return d, order

QDATA = {}
_order = None
for _l in ("en", "es", "pt"):
    QDATA[_l], _o = _load_exam(_l)
    if _order is None:
        _order = _o
# global 1-based question number by bank order (identical across languages)
QNUM = {qid: i + 1 for i, qid in enumerate(_order)}

# id -> principle (1-12), and principle -> [ids] preserving exam order
PRINCIPLE_MAP = json.load(open(os.path.join(REPO, "data", "principle_map.json")))
PMAP_IDS = {}
for _qid, _p in PRINCIPLE_MAP.items():
    PMAP_IDS.setdefault(int(_p), []).append(_qid)

# domain weight (official blueprint) and count (items in this bank)
WEIGHT = {1: 27, 2: 18, 3: 20, 4: 20, 5: 15}
COUNT  = {1: 43, 2: 20, 3: 16, 4: 38, 5: 19}
LETTERS = [("A", 39), ("B", 32), ("C", 36), ("D", 29)]

DOMAIN_NAMES = {
    "en": {1: "Agent Architecture and Orchestration", 2: "Tool Design and MCP Integration",
           3: "Claude Code Configuration and Workflows", 4: "Prompt Engineering and Structured Output",
           5: "Context Management and Reliability"},
    "es": {1: "Arquitectura y Orquestación de Agentes", 2: "Diseño de Herramientas e Integración MCP",
           3: "Configuración y Flujos de Claude Code", 4: "Ingeniería de Prompts y Salida Estructurada",
           5: "Gestión de Contexto y Confiabilidad"},
    "pt": {1: "Arquitetura e Orquestração de Agentes", 2: "Design de Ferramentas e Integração MCP",
           3: "Configuração e Fluxos do Claude Code", 4: "Engenharia de Prompts e Saída Estruturada",
           5: "Gerenciamento de Contexto e Confiabilidade"},
}

# principle -> (domains, scenario-families)
PMETA = [
    (1,  [1],    ["research", "support"]),
    (2,  [5, 1], ["research"]),
    (3,  [2],    ["research"]),
    (4,  [2],    ["research", "support"]),
    (5,  [4],    ["ci", "codegen", "support"]),
    (6,  [4],    ["ci", "support"]),
    (7,  [5],    ["ci"]),
    (8,  [5],    ["codegen"]),
    (9,  [3],    ["codegen"]),
    (10, [4, 1], ["support"]),
    (11, [3, 1], ["codegen"]),
    (12, [1],    ["research", "support"]),
]

# --- per-language UI strings ---
UI = {
"en": {
  "title": "English — Cheatsheet · Ravn",
  "study": "Study", "exam": "Exam",
  "eyebrow": "Claude Certified Architect · Study Cheatsheet",
  "h1": 'Every question has <span class="key">one correct move</span> and three traps.',
  "lede": "The exam tests the same twelve principles over and over. Learn the principle, not the wording — the scenario changes, the underlying idea does not.",
  "s_q": "Questions", "s_d": "Domains", "s_p": "Principles",
  "lg1": "What the correct answer does", "lg2": "What the traps do", "lg3": "The domain it maps to",
  "sec1h": "The 12 principles",
  "sec1p": "Each card states the principle, what the correct answer does, the trap to avoid, and the domain(s) it maps to.",
  "sec2h": "How to read any question",
  "sec2p": "When two answers both look right, ask these five questions. The correct answer usually passes all five.",
  "sec3h": "What's on the exam",
  "sec3p": "How the 136 practice questions break down by domain, and why you shouldn't guess by the answer letter.",
  "p1h": "Domains · weight = official blueprint; count = items in this bank",
  "p2h": "Correct-answer letter (of 136)",
  "note": "Fairly even — so don't guess by letter. A longer option that 'does the work AND preserves the information AND escalates appropriately' is often correct, but confirm it against the five questions above rather than choosing it for its length.",
  "footer": "Based on the 136-question exam (<span class=\"mono\">exam_en.html</span>) and the official 5-domain blueprint.",
  "badgeDo": "Correct", "badgeNo": "Trap",
  "scn": {"research": "Multi-agent", "ci": "CI/CD", "codegen": "Claude Code", "support": "Support"},
  "q_label": "exam questions that test this", "q_correct": "Correct",
},
"es": {
  "title": "Español — Hoja de Referencia · Ravn",
  "study": "Estudio", "exam": "Examen",
  "eyebrow": "Claude Certified Architect · Hoja de Referencia",
  "h1": 'Mirá: cada pregunta tiene <span class="key">una sola jugada correcta</span> y tres trampas.',
  "lede": "El examen te va a evaluar una y otra vez sobre los mismos doce principios. Aprendete el principio, no el enunciado: el escenario cambia, pero la idea de fondo es siempre la misma.",
  "s_q": "Preguntas", "s_d": "Dominios", "s_p": "Principios",
  "lg1": "Lo que hace la respuesta correcta", "lg2": "Lo que hacen las trampas", "lg3": "El dominio al que corresponde",
  "sec1h": "Los 12 principios que tenés que dominar",
  "sec1p": "Cada tarjeta te muestra el principio, lo que hace la respuesta correcta, la trampa que tenés que esquivar y los dominios en los que aparece.",
  "sec2h": "Cómo encarar cualquier pregunta",
  "sec2p": "Cuando dos respuestas te parecen buenas, hacete estas cinco preguntas. La correcta casi siempre pasa las cinco.",
  "sec3h": "Qué hay en el examen",
  "sec3p": "Mirá cómo se reparten las 136 preguntas de práctica por dominio, y por qué no te conviene adivinar por la letra de la respuesta.",
  "p1h": "Dominios · peso = temario oficial; conteo = ítems de este banco",
  "p2h": "Letra de la respuesta correcta (de 136)",
  "note": "Está bastante parejo, así que no adivines por la letra. Una opción más larga que 'hace el trabajo Y conserva la información Y escala como corresponde' suele ser la correcta, pero confirmala con las cinco preguntas de arriba; no la elijas solo porque es la más larga.",
  "footer": "Basado en el examen de 136 preguntas (<span class=\"mono\">exam_es.html</span>) y el temario oficial de 5 dominios.",
  "badgeDo": "Correcta", "badgeNo": "Trampa",
  "scn": {"research": "Multiagente", "ci": "CI/CD", "codegen": "Claude Code", "support": "Soporte"},
  "q_label": "preguntas del examen que lo evalúan", "q_correct": "Correcta",
},
"pt": {
  "title": "Português — Folha de Referência · Ravn",
  "study": "Estudo", "exam": "Exame",
  "eyebrow": "Claude Certified Architect · Folha de Referência",
  "h1": 'Cada questão tem <span class="key">uma jogada correta</span> e três armadilhas.',
  "lede": "O exame avalia repetidamente os mesmos doze princípios. Aprenda o princípio, não o enunciado: o cenário muda, a ideia de fundo não.",
  "s_q": "Questões", "s_d": "Domínios", "s_p": "Princípios",
  "lg1": "O que a resposta correta faz", "lg2": "O que as armadilhas fazem", "lg3": "O domínio a que corresponde",
  "sec1h": "Os 12 princípios",
  "sec1p": "Cada cartão indica o princípio, o que a resposta correta faz, a armadilha a evitar e os domínios a que corresponde.",
  "sec2h": "Como ler qualquer questão",
  "sec2p": "Quando duas respostas parecem corretas, faça estas cinco perguntas. A correta costuma passar nas cinco.",
  "sec3h": "O que cai no exame",
  "sec3p": "Como as 136 questões de prática se distribuem por domínio, e por que não convém adivinhar pela letra da resposta.",
  "p1h": "Domínios · peso = conteúdo oficial; contagem = itens deste banco",
  "p2h": "Letra da resposta correta (de 136)",
  "note": "Bastante equilibrado, então não adivinhe pela letra. Uma opção mais longa que 'faz o trabalho E preserva a informação E escala adequadamente' costuma ser correta, mas confirme-a com as cinco perguntas acima em vez de escolhê-la pelo tamanho.",
  "footer": "Baseado no exame de 136 questões (<span class=\"mono\">exam_pt.html</span>) e no conteúdo oficial de 5 domínios.",
  "badgeDo": "Correta", "badgeNo": "Armadilha",
  "scn": {"research": "Multiagente", "ci": "CI/CD", "codegen": "Claude Code", "support": "Suporte"},
  "q_label": "questões do exame que o avaliam", "q_correct": "Correta",
},
}

# --- the 12 principles: (title, correct-approach, trap) in numeric order ---
PRIN = {
"en": [
 ("Surface conflicts; let the orchestrator or a human decide",
  "When two credible sources disagree, do not silently choose one. Complete your portion, record both values with their provenance, flag the contradiction explicitly, and escalate the decision to the orchestrating agent or a human reviewer.",
  "Quietly selecting one value, merging the figures without noting the conflict, halting the entire workflow, or inventing a resolution rule that was never defined."),
 ("Recover from transient failures yourself; escalate only when genuinely blocked",
  "For recoverable issues such as a timeout or a rate limit, retry with backoff on your own. Escalate to the orchestrator only when you cannot proceed, and include what failed and what you already attempted.",
  "Escalating every minor hiccup to the orchestrator, or suppressing the failure and continuing as if nothing happened."),
 ("Address the root cause, and scope each tool to least privilege",
  "If a tool repeatedly performs an unsafe action, constrain it to a narrower, safer capability rather than appending 'be careful' to the prompt. Grant each tool only the access it genuinely requires.",
  "Leaving the over-powered tool unchanged and adding more warnings, or cleaning up the damage afterward instead of preventing it."),
 ("When the wrong tool is selected, fix the names and descriptions first",
  "An agent chooses a tool from its name and description. If it keeps selecting the wrong one, clarify those labels so each tool is distinct and unambiguous before changing anything else.",
  "Blaming the model or re-architecting the system before simply disambiguating the tool definitions."),
 ("Demonstrate with examples; don't just restate the instructions",
  "When instructions yield inconsistent output, add three to six concrete examples covering the tricky cases. Worked examples teach the desired behavior more reliably than additional prose rules.",
  "Rewriting the same instructions at greater length and hoping for a different result."),
 ("Define 'unacceptable' with precise, testable criteria",
  "Replace vague directives like 'flag bad comments' with an explicit rule, e.g. 'flag a comment only when it states the opposite of what the code does.' Make the boundary checkable.",
  "Leaving the criterion subjective and hoping the model infers it, or correcting the mistakes downstream."),
 ("Use the interactive API for urgent work and the Batch API for deferrable work",
  "When a person is waiting (e.g., a pre-merge review), use the interactive, real-time path. For work that can finish later (e.g., overnight jobs), use the Batch API — slower but roughly half the cost.",
  "Making users wait on batch jobs to save money, or paying interactive rates for work nobody is waiting on."),
 ("Run high-volume, noisy work in an isolated context",
  "Large, verbose tasks consume the main context window and crowd out the primary objective. Execute them in a separate context (e.g., <code>context: fork</code>) and return only a concise summary.",
  "Performing the entire noisy task in the main context, diluting it until the original goal is lost."),
 ("Put each instruction in the configuration file built for it",
  "Route guidance to the right place: <code>CLAUDE.md</code> for always-on rules, Skills for on-demand capabilities, <code>.claude/rules/</code> for file-type rules, <code>.claude/commands/</code> for shared team commands. Reference secrets securely — never hard-code them.",
  "Dumping everything into a single file, or writing a credential directly into the code."),
 ("Enforce mandatory steps in code, not in prose",
  "When a step is non-negotiable — e.g., verifying a customer's identity before issuing a refund — enforce it programmatically so it cannot be skipped, rather than relying on the model to remember.",
  "Adding 'always verify first' to the prompt and trusting the instruction to hold; a request is not a guarantee."),
 ("Plan before building when several viable approaches exist",
  "For large or ambiguous tasks with multiple possible designs, investigate, weigh the options, and agree on an approach before implementation begins.",
  "Starting to code immediately, before it is clear which approach is best."),
 ("Decompose large requests, parallelize, and share context",
  "When a request contains several independent parts, split them and process them concurrently against shared context, rather than handling them one slow step at a time and re-deriving the same information.",
  "Processing sequentially and repeatedly looking up the same information."),
],
"es": [
 ("Mostrá los conflictos: que decida el orquestador o una persona",
  "Mirá, cuando dos fuentes confiables se contradicen, no elijas una por tu cuenta y en silencio. Terminá tu parte, dejá registrados los dos valores con su origen, marcá clarito que se contradicen y pasale la decisión al agente orquestador o a un revisor humano.",
  "Elegir un valor en silencio, mezclar las cifras sin avisar del conflicto, frenar todo el flujo o inventar una regla de resolución que nunca se definió."),
 ("Recuperate solo de los fallos pasajeros; escalá solo cuando estés realmente trabado",
  "Si el problema se puede recuperar —un timeout, un límite de tasa— reintentá con backoff por tu cuenta. Escalá al orquestador solo cuando de verdad no puedas seguir, y cuando lo hagas, contá qué falló y qué ya probaste.",
  "Escalar cada problemita al orquestador, o tapar el fallo y seguir como si nada."),
 ("Andá a la causa raíz y dale a cada herramienta el mínimo privilegio",
  "Si una herramienta hace algo inseguro una y otra vez, limitala a una capacidad más chica y segura en lugar de sumarle un 'tené cuidado' al prompt. Dale a cada herramienta solo el acceso que de verdad necesita.",
  "Dejar la herramienta con permisos de más y sumar más advertencias, o limpiar el desastre después en vez de evitarlo."),
 ("Si elige la herramienta equivocada, arreglá primero los nombres y las descripciones",
  "El agente elige una herramienta por su nombre y su descripción. Si sigue agarrando la que no es, dejá esas etiquetas bien claras para que cada herramienta sea distinta e inconfundible antes de tocar cualquier otra cosa.",
  "Echarle la culpa al modelo o rehacer todo el sistema antes de simplemente diferenciar las definiciones de las herramientas."),
 ("Mostrá ejemplos; no te quedes en repetir las instrucciones",
  "Si las instrucciones te dan resultados disparejos, sumá entre tres y seis ejemplos concretos que cubran los casos difíciles. Fijate que los ejemplos enseñan el comportamiento que querés mucho mejor que más reglas escritas.",
  "Reescribir las mismas instrucciones con más palabras y esperar un resultado distinto."),
 ("Definí qué es 'inaceptable' con criterios precisos y verificables",
  "Cambiá las indicaciones vagas tipo 'marcá los comentarios malos' por una regla explícita; por ejemplo: 'marcá un comentario solo cuando diga lo contrario de lo que hace el código'. Hacé que el límite se pueda chequear.",
  "Dejar el criterio subjetivo esperando que el modelo lo adivine, o corregir los errores más adelante."),
 ("Usá la API interactiva para lo urgente y la API Batch para lo que puede esperar",
  "Si hay una persona esperando —por ejemplo, una revisión antes del merge— usá la vía interactiva, en tiempo real. Para lo que puede salir más tarde —tareas nocturnas, digamos— usá la API Batch: es más lenta, pero te sale casi la mitad.",
  "Hacer esperar a la gente en tareas por lotes para ahorrar, o pagar tarifa interactiva por trabajo que nadie está esperando."),
 ("El trabajo pesado y ruidoso, hacelo en un contexto aparte",
  "Las tareas grandes y verbosas te llenan la ventana de contexto principal y te tapan el objetivo. Corrélas en un contexto separado (por ejemplo, <code>context: fork</code>) y traé de vuelta solo un resumen cortito.",
  "Hacer toda la tarea ruidosa en el contexto principal hasta diluirlo y perder de vista el objetivo original."),
 ("Poné cada instrucción en el archivo de configuración pensado para ella",
  "Mandá cada indicación a su lugar: <code>CLAUDE.md</code> para reglas siempre activas, Skills para capacidades bajo demanda, <code>.claude/rules/</code> para reglas por tipo de archivo, y <code>.claude/commands/</code> para los comandos compartidos del equipo. A los secretos referencialos de forma segura; nunca los escribas en el código.",
  "Meter todo en un solo archivo, o escribir una credencial directo en el código."),
 ("Los pasos obligatorios, hacelos cumplir en el código, no en el texto",
  "Cuando un paso es innegociable —por ejemplo, verificar la identidad del cliente antes de dar un reembolso— hacelo cumplir por código para que no se pueda saltear, en lugar de confiar en que el modelo se acuerde.",
  "Sumar un 'verificá siempre primero' al prompt y confiar en que se respete; un pedido no es una garantía."),
 ("Planificá antes de construir cuando hay varios caminos posibles",
  "Para tareas grandes o ambiguas, con varios diseños posibles, primero investigá, compará las opciones y ponete de acuerdo en un enfoque antes de arrancar a implementar.",
  "Largarte a programar de una, antes de tener claro cuál es el mejor enfoque."),
 ("Partí los pedidos grandes, paralelizá y compartí el contexto",
  "Cuando un pedido trae varias partes independientes, separalas y procesalas en paralelo sobre un contexto compartido, en vez de ir una por una y volver a deducir la misma información cada vez.",
  "Ir de forma secuencial y buscar la misma información una y otra vez."),
],
"pt": [
 ("Exponha os conflitos; deixe o orquestrador ou uma pessoa decidir",
  "Quando duas fontes confiáveis se contradizem, não escolha uma em silêncio. Conclua a sua parte, registre ambos os valores com sua procedência, sinalize explicitamente a contradição e escale a decisão ao agente orquestrador ou a um revisor humano.",
  "Escolher um valor em silêncio, combinar os números sem avisar do conflito, interromper todo o fluxo ou inventar uma regra de resolução que nunca foi definida."),
 ("Recupere-se sozinho de falhas transitórias; escale apenas quando estiver realmente bloqueado",
  "Diante de problemas recuperáveis, como um tempo limite ou um limite de taxa, tente novamente com recuo por conta própria. Escale ao orquestrador apenas quando não conseguir prosseguir, e inclua o que falhou e o que já tentou.",
  "Escalar cada incidente menor ao orquestrador, ou silenciar a falha e continuar como se nada tivesse acontecido."),
 ("Ataque a causa raiz e limite cada ferramenta ao menor privilégio",
  "Se uma ferramenta realiza repetidamente uma ação insegura, restrinja-a a uma capacidade mais estreita e segura em vez de acrescentar 'tenha cuidado' ao prompt. Conceda a cada ferramenta apenas o acesso de que realmente precisa.",
  "Deixar intacta a ferramenta com excesso de permissões e acrescentar mais avisos, ou limpar o dano depois em vez de evitá-lo."),
 ("Quando a ferramenta errada é escolhida, corrija primeiro os nomes e descrições",
  "Um agente escolhe uma ferramenta a partir de seu nome e descrição. Se continuar escolhendo a errada, esclareça esses rótulos para que cada ferramenta seja distinta e inequívoca antes de mudar qualquer outra coisa.",
  "Culpar o modelo ou redesenhar o sistema antes de simplesmente diferenciar as definições das ferramentas."),
 ("Demonstre com exemplos; não se limite a repetir as instruções",
  "Quando as instruções produzem resultados inconsistentes, acrescente de três a seis exemplos concretos que cubram os casos difíceis. Exemplos resolvidos ensinam o comportamento desejado de forma mais confiável do que mais regras em texto.",
  "Reescrever as mesmas instruções com mais palavras e esperar um resultado diferente."),
 ("Defina 'inaceitável' com critérios precisos e verificáveis",
  "Substitua orientações vagas como 'sinalize os comentários ruins' por uma regra explícita, p. ex. 'sinalize um comentário apenas quando ele afirmar o contrário do que o código faz'. Torne o limite verificável.",
  "Deixar o critério subjetivo esperando que o modelo o infira, ou corrigir os erros mais adiante."),
 ("Use a API interativa para o urgente e a API Batch para o que pode esperar",
  "Quando uma pessoa está esperando (p. ex., uma revisão antes do merge), use a via interativa, em tempo real. Para trabalho que pode ser concluído depois (p. ex., tarefas noturnas), use a API Batch: mais lenta, mas a aproximadamente metade do custo.",
  "Fazer os usuários esperarem em tarefas em lote para economizar, ou pagar tarifa interativa por trabalho que ninguém espera."),
 ("Execute o trabalho volumoso e ruidoso em um contexto isolado",
  "Tarefas grandes e verbosas consomem a janela de contexto principal e expulsam o objetivo principal. Execute-as em um contexto separado (p. ex., <code>context: fork</code>) e devolva apenas um resumo conciso.",
  "Realizar toda a tarefa ruidosa no contexto principal até diluí-lo e perder o objetivo original."),
 ("Coloque cada instrução no arquivo de configuração feito para ela",
  "Direcione cada orientação ao seu lugar: <code>CLAUDE.md</code> para regras sempre ativas, Skills para capacidades sob demanda, <code>.claude/rules/</code> para regras por tipo de arquivo, <code>.claude/commands/</code> para comandos compartilhados da equipe. Referencie segredos de forma segura; nunca os escreva no código.",
  "Despejar tudo em um único arquivo, ou escrever uma credencial diretamente no código."),
 ("Garanta os passos obrigatórios no código, não no texto",
  "Quando um passo é inegociável — p. ex., verificar a identidade do cliente antes de emitir um reembolso — garanta-o por código para que não possa ser pulado, em vez de confiar que o modelo se lembre.",
  "Acrescentar 'sempre verifique primeiro' ao prompt e confiar que a instrução será respeitada; um pedido não é uma garantia."),
 ("Planeje antes de construir quando há vários enfoques viáveis",
  "Para tarefas grandes ou ambíguas com vários designs possíveis, investigue, compare as opções e combine um enfoque antes de começar a implementar.",
  "Começar a programar de imediato, antes de saber qual enfoque é o melhor."),
 ("Decomponha as solicitações grandes, paralelize e compartilhe o contexto",
  "Quando uma solicitação contém várias partes independentes, divida-as e processe-as em paralelo sobre um contexto compartilhado, em vez de resolvê-las passo a passo e deduzir novamente a mesma informação.",
  "Processar de forma sequencial e buscar repetidamente a mesma informação."),
],
}

# --- the 5 reading questions: (strong, gloss) ---
KEYS = {
"en": [
 ("Does it address the root cause, or only the symptom?", "The correct answer fixes why the failure occurred; traps merely tidy up the visible effect."),
 ("Does it preserve all the information?", "Strong answers retain the facts and their provenance; weak ones discard or obscure information."),
 ("Does it resolve the issue at the smallest, simplest level?", "Recover locally and scope tools to least privilege — neither escalate everything nor rely on luck."),
 ("Is it the right mechanism for the job?", "Enforce in code vs. request in prose · interactive vs. batch · the correct file for each instruction."),
 ("Is it the smallest change that works?", "The simplest effective fix beats rebuilding everything — and beats doing nothing."),
],
"es": [
 ("¿Ataca la causa raíz o solo el síntoma?", "Fijate: la respuesta correcta arregla por qué se rompió; las trampas solo acomodan lo que se ve."),
 ("¿Conserva toda la información?", "Las buenas respuestas guardan los datos y de dónde salieron; las malas descartan u ocultan información."),
 ("¿Resuelve el problema en el punto más chico y simple?", "Recuperate ahí mismo y dale a cada herramienta el mínimo privilegio: ni escales todo ni te confíes de la suerte."),
 ("¿Es el mecanismo adecuado para la tarea?", "Hacerlo cumplir en código vs. pedirlo en texto · interactivo vs. batch · el archivo correcto para cada instrucción."),
 ("¿Es el cambio más chico que funciona?", "El arreglo más simple que resuelve le gana a reconstruir todo, y le gana a no hacer nada."),
],
"pt": [
 ("Ataca a causa raiz ou apenas o sintoma?", "A resposta correta corrige por que a falha ocorreu; as armadilhas apenas arrumam o efeito visível."),
 ("Preserva toda a informação?", "Boas respostas mantêm os dados e sua procedência; as ruins descartam ou ocultam informação."),
 ("Resolve o problema no nível mais simples e localizado?", "Recupere-se localmente e limite as ferramentas ao menor privilégio: nem escale tudo nem confie na sorte."),
 ("É o mecanismo adequado para a tarefa?", "Garantir no código vs. pedir no texto · interativo vs. batch · o arquivo correto para cada instrução."),
 ("É a menor mudança que funciona?", "A correção eficaz mais simples vence reconstruir tudo, e vence não fazer nada."),
],
}

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: calc(var(--topbar-h, 58px) + 16px); }
body { font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.65; background: #f0f2f5; color: #1a202c;
  -webkit-font-smoothing: antialiased; }
.mono { font-family: ui-monospace, "SF Mono", Menlo, Monaco, monospace; }

.ravn-topbar { position: sticky; top: 0; z-index: 20; display: flex; align-items: center;
  justify-content: space-between; padding: 12px 32px; background: #0f1019; color: #f5f5f0;
  border-bottom: 1px solid #2c2c4a; }
.ravn-brand { display: inline-flex; align-items: baseline; gap: 14px; color: #f5f5f0;
  text-decoration: none; font-weight: 600; letter-spacing: -0.01em; }
.ravn-brand:hover { color: #f6c87a; }
.ravn-brand svg { color: currentColor; flex-shrink: 0; }
.ravn-brand-tagline { font-size: 13px; color: #9aa0b3; text-transform: uppercase; letter-spacing: 0.14em; }
.topbar-kicker { font-size: 12px; color: #9aa0b3; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; }

.wrap { max-width: 940px; margin: 0 auto; padding: 0 24px; }

header.hero { padding: 60px 0 44px; border-bottom: 1px solid #e2e8f0; }
.eyebrow { font-family: ui-monospace, Menlo, monospace; font-size: 12.5px; letter-spacing: .22em;
  text-transform: uppercase; color: #2b6cb0; margin-bottom: 18px; }
h1 { font-size: clamp(30px, 5vw, 50px); line-height: 1.08; letter-spacing: -.02em; font-weight: 800; margin-bottom: 18px; }
h1 .key { color: #2b6cb0; }
.lede { font-size: clamp(16px, 2vw, 19px); color: #4a5568; max-width: 62ch; }
.stats { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 34px; }
.stat { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 20px; min-width: 128px;
  box-shadow: 0 1px 2px rgba(0,0,0,.04); }
.stat .n { font-size: 32px; font-weight: 800; color: #2b6cb0; line-height: 1; }
.stat .l { font-family: ui-monospace, Menlo, monospace; font-size: 11px; letter-spacing: .1em;
  text-transform: uppercase; color: #718096; margin-top: 8px; }
.legend { display: flex; flex-wrap: wrap; gap: 22px; padding-top: 26px; }
.legend span { display: inline-flex; align-items: center; gap: 9px; font-size: 13.5px; color: #4a5568; }
.swatch { width: 13px; height: 13px; border-radius: 4px; }

.section-head { padding: 54px 0 6px; }
.section-head h2 { font-size: 24px; font-weight: 800; letter-spacing: -.01em; }
.section-head p { color: #718096; margin-top: 8px; font-size: 15px; }

.grid { display: flex; flex-direction: column; gap: 16px; padding-top: 26px; }
.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px 26px;
  display: grid; grid-template-columns: 54px 1fr; gap: 4px 20px; box-shadow: 0 1px 3px rgba(0,0,0,.05);
  opacity: 0; transform: translateY(16px); transition: opacity .5s ease, transform .5s ease; }
.card.in { opacity: 1; transform: none; }
.card .num { font-family: Georgia, serif; font-style: italic; font-size: 34px; color: #cbd5e0;
  line-height: 1; grid-row: 1 / span 4; }
.card h3 { font-size: 18px; margin: 2px 0 4px; letter-spacing: -.01em; color: #1a202c; }
.card .tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.tag { font-family: ui-monospace, Menlo, monospace; font-size: 10.5px; letter-spacing: .03em;
  border-radius: 999px; padding: 3px 9px; border: 1px solid #e2e8f0; color: #718096; }
.tag.dom { background: #ebf8ff; color: #2b6cb0; border-color: #bee3f8; }
.tag.scn { background: #faf5ff; color: #6b46c1; border-color: #e9d8fd; }

.line-row { display: grid; grid-template-columns: 86px 1fr; gap: 14px; padding: 10px 0; align-items: baseline; }
.line-row + .line-row { border-top: 1px solid #edf2f7; }
.badge { font-family: ui-monospace, Menlo, monospace; font-size: 10.5px; letter-spacing: .06em;
  text-transform: uppercase; font-weight: 700; }
.badge.do { color: #2f855a; }
.badge.no { color: #c53030; }
.line-row p { margin: 0; font-size: 14.5px; }
.line-row.do p { color: #2d3748; }
.line-row.no p { color: #718096; }
code { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 13px; background: #edf2f7;
  color: #2b6cb0; padding: 1px 6px; border-radius: 5px; }

.qdrop { grid-column: 1 / -1; margin-top: 12px; border-top: 1px solid #edf2f7; }
.qdrop > summary { cursor: pointer; list-style: none; font-family: ui-monospace, Menlo, monospace;
  font-size: 11.5px; letter-spacing: .04em; text-transform: uppercase; color: #2b6cb0;
  padding: 11px 0 3px; display: flex; align-items: center; gap: 9px; }
.qdrop > summary::-webkit-details-marker { display: none; }
.qdrop > summary::after { content: "▸"; color: #a0aec0; transition: transform .15s; margin-left: auto; }
.qdrop[open] > summary::after { transform: rotate(90deg); }
.qdrop > summary:hover { color: #2c5282; }
.qdrop .qn { background: #ebf8ff; color: #2b6cb0; border: 1px solid #bee3f8; border-radius: 999px;
  padding: 1px 9px; font-size: 11px; font-weight: 700; }
.qlist { list-style: none; margin: 8px 0 4px; padding: 0; display: flex; flex-direction: column; gap: 18px; }
.qlist > li { border-left: 2px solid #e2e8f0; padding: 2px 0 2px 14px; }
.qhead { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-bottom: 6px; }
.qnum { font-family: ui-monospace, Menlo, monospace; font-size: 11px; font-weight: 700; color: #2b6cb0;
  background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 1px 7px; }
.qscenario { font-size: 11.5px; font-weight: 600; letter-spacing: .02em; text-transform: uppercase;
  color: #6b46c1; }
.qsituation { margin: 0 0 7px; font-size: 13.5px; color: #4a5568; line-height: 1.6; }
.qq { margin: 0 0 6px; font-size: 14px; font-weight: 600; color: #2d3748; }
.qa { margin: 0; font-size: 13.5px; color: #2d3748; }
.qa .qa-tag { font-family: ui-monospace, Menlo, monospace; font-size: 9.5px; text-transform: uppercase;
  letter-spacing: .07em; color: #2f855a; margin-right: 7px; }
.qa .qa-l { font-weight: 700; color: #2f855a; }
.qexp { margin: 6px 0 0; font-size: 13px; color: #718096; line-height: 1.55; }

.key-block { background: #fff; border: 1px solid #e2e8f0; border-left: 4px solid #2b6cb0; border-radius: 14px;
  padding: 26px 30px; margin-top: 26px; box-shadow: 0 1px 3px rgba(0,0,0,.05); }
.key-block ol { margin: 0; padding-left: 0; list-style: none; counter-reset: k; }
.key-block li { counter-increment: k; position: relative; padding: 13px 0 13px 44px; font-size: 15.5px; color: #2d3748; }
.key-block li + li { border-top: 1px solid #edf2f7; }
.key-block li::before { content: counter(k); position: absolute; left: 0; top: 11px; font-family: Georgia, serif;
  font-style: italic; font-size: 20px; color: #2b6cb0; }
.key-block strong { color: #1a202c; }
.key-block .q { color: #718096; }

.meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; padding-top: 26px; }
.panel { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 22px 24px; box-shadow: 0 1px 3px rgba(0,0,0,.05); }
.panel h4 { margin: 0 0 16px; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: #718096;
  font-family: ui-monospace, Menlo, monospace; line-height: 1.4; }
.bar-row { margin: 12px 0; font-size: 14px; }
.bar-row .top { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 5px; }
.bar-row .lab { color: #2d3748; }
.bar-row .ct { font-family: ui-monospace, Menlo, monospace; color: #2b6cb0; font-size: 12.5px; white-space: nowrap; }
.bar-track { height: 7px; background: #edf2f7; border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; background: #2b6cb0; border-radius: 999px; }
.lettr { display: flex; gap: 10px; }
.lettr div { flex: 1; text-align: center; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 0; }
.lettr .L { font-family: Georgia, serif; font-size: 24px; color: #2b6cb0; font-weight: 700; }
.lettr .V { font-family: ui-monospace, Menlo, monospace; font-size: 12px; color: #718096; margin-top: 4px; }
.note { color: #718096; font-size: 13.5px; margin-top: 16px; }

footer { padding: 48px 0 64px; color: #718096; font-size: 13px; border-top: 1px solid #e2e8f0; margin-top: 56px; }

@media (max-width: 680px) {
  .meta-grid { grid-template-columns: 1fr; }
  .card { grid-template-columns: 1fr; }
  .card .num { grid-row: auto; }
  .line-row { grid-template-columns: 1fr; gap: 4px; }
  .ravn-topbar { padding: 12px 18px; }
}
@media (prefers-reduced-motion: reduce) {
  .card { opacity: 1; transform: none; transition: none; }
  html { scroll-behavior: auto; }
}
"""

TOPBAR = ('<header class="ravn-topbar"><a class="ravn-brand" href="../index.html" '
  'aria-label="Ravn — Claude Certified Architect"><svg xmlns="http://www.w3.org/2000/svg" '
  'viewBox="0 0 200 64" aria-label="Ravn" role="img" width="86" height="22"><text x="0" y="48" '
  "font-family=\"Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif\" "
  'font-size="52" font-weight="800" letter-spacing="-2" fill="currentColor">ravn</text></svg>'
  '<span class="ravn-brand-tagline">Claude Certified Architect</span></a>'
  '<span class="topbar-kicker">{kicker}</span></header>')


def qdrop_html(lang, principle):
    u = UI[lang]
    qd = QDATA[lang]
    items = []
    for qid in PMAP_IDS.get(principle, []):
        q = qd.get(qid)
        if not q:
            continue
        head = '<span class="qnum">#%d</span>' % QNUM.get(qid, 0)
        if q["scenario"].strip():
            head += '<span class="qscenario">%s</span>' % html.escape(q["scenario"])
        situation = ('<p class="qsituation">%s</p>' % html.escape(q["situation"])
                     if q["situation"].strip() else "")
        items.append(
            '<li><div class="qhead">%s</div>%s'
            '<p class="qq">%s</p>'
            '<p class="qa"><span class="qa-tag">%s</span><span class="qa-l">%s)</span> %s</p>'
            '<p class="qexp">%s</p></li>' % (
                head, situation, html.escape(q["prompt"]), u["q_correct"],
                html.escape(q["letter"]), html.escape(q["text"]), html.escape(q["exp"])))
    return ('<details class="qdrop"><summary><span class="qn">%d</span> %s</summary>'
            '<ol class="qlist">%s</ol></details>' % (len(items), u["q_label"], "".join(items)))


def cards_html(lang):
    u = UI[lang]
    out = []
    for (n, doms, scns), (title, do, no) in zip(PMETA, PRIN[lang]):
        tags = "".join('<span class="tag dom">D%d</span>' % d for d in doms)
        tags += "".join('<span class="tag scn">%s</span>' % u["scn"][s] for s in scns)
        out.append(
            '<article class="card">'
            '<div class="num">%02d</div>'
            '<div><h3>%s</h3><div class="tags">%s</div></div>'
            '<div class="line-row do"><span class="badge do">%s</span><p>%s</p></div>'
            '<div class="line-row no"><span class="badge no">%s</span><p>%s</p></div>'
            '%s'
            '</article>' % (n, title, tags, u["badgeDo"], do, u["badgeNo"], no, qdrop_html(lang, n)))
    return "\n".join(out)


def keys_html(lang):
    return "\n".join('<li><strong>%s</strong> <span class="q">%s</span></li>' % (s, q)
                     for s, q in KEYS[lang])


def domain_rows(lang):
    names = DOMAIN_NAMES[lang]
    rows = []
    for d in range(1, 6):
        rows.append(
            '<div class="bar-row"><div class="top"><span class="lab">D%d · %s</span>'
            '<span class="ct">%d%% · %d q</span></div>'
            '<div class="bar-track"><div class="bar-fill" style="width:%d%%"></div></div></div>'
            % (d, names[d], WEIGHT[d], COUNT[d], WEIGHT[d]))
    return "\n".join(rows)


def letters_html():
    return "".join('<div><div class="L">%s</div><div class="V">%d</div></div>' % (L, v)
                   for L, v in LETTERS)


def build(lang):
    u = UI[lang]
    return """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" type="image/png" href="{favicon}">
<style>{css}</style>
</head>
<body>
{topbar}
<header class="hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="stats">
      <div class="stat"><div class="n">136</div><div class="l">{s_q}</div></div>
      <div class="stat"><div class="n">5</div><div class="l">{s_d}</div></div>
      <div class="stat"><div class="n">12</div><div class="l">{s_p}</div></div>
    </div>
    <div class="legend">
      <span><span class="swatch" style="background:#48bb78"></span>{lg1}</span>
      <span><span class="swatch" style="background:#fc8181"></span>{lg2}</span>
      <span><span class="swatch" style="background:#2b6cb0"></span>{lg3}</span>
    </div>
  </div>
</header>

<main class="wrap">
  <div class="section-head"><h2 id="principles">{sec1h}</h2><p>{sec1p}</p></div>
  <div class="grid">
{cards}
  </div>

  <div class="section-head"><h2 id="how-to-read">{sec2h}</h2><p>{sec2p}</p></div>
  <div class="key-block"><ol>
{keys}
  </ol></div>

  <div class="section-head"><h2 id="whats-on-the-exam">{sec3h}</h2><p>{sec3p}</p></div>
  <div class="meta-grid">
    <div class="panel">
      <h4>{p1h}</h4>
{domains}
    </div>
    <div class="panel">
      <h4>{p2h}</h4>
      <div class="lettr">{letters}</div>
      <p class="note">{note}</p>
    </div>
  </div>
</main>

<footer class="wrap"><span>{footer}</span></footer>

<script>
(function () {{
  function setTopbarH() {{
    var tb = document.querySelector(".ravn-topbar");
    if (tb) document.documentElement.style.setProperty("--topbar-h", tb.offsetHeight + "px");
  }}
  setTopbarH();
  window.addEventListener("resize", setTopbarH);

  var cards = document.querySelectorAll(".card");
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    cards.forEach(function (c) {{ c.classList.add("in"); }});
    return;
  }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }}
    }});
  }}, {{ threshold: 0.12 }});
  cards.forEach(function (c) {{ io.observe(c); }});
}})();
</script>
</body>
</html>
""".format(
        lang=lang, title=u["title"], favicon=favicon, css=CSS,
        topbar=TOPBAR.format(kicker=u["eyebrow"].split("·")[-1].strip()),
        eyebrow=u["eyebrow"], h1=u["h1"], lede=u["lede"],
        s_q=u["s_q"], s_d=u["s_d"], s_p=u["s_p"],
        lg1=u["lg1"], lg2=u["lg2"], lg3=u["lg3"],
        sec1h=u["sec1h"], sec1p=u["sec1p"], sec2h=u["sec2h"], sec2p=u["sec2p"],
        sec3h=u["sec3h"], sec3p=u["sec3p"], p1h=u["p1h"], p2h=u["p2h"],
        cards=cards_html(lang), keys=keys_html(lang),
        domains=domain_rows(lang), letters=letters_html(),
        note=u["note"], footer=u["footer"])


for lang in ("en", "es", "pt"):
    path = os.path.join(REPO, "cheatsheet_%s.html" % lang)
    open(path, "w", encoding="utf-8").write(build(lang))
    print("wrote", path, os.path.getsize(path), "bytes")
