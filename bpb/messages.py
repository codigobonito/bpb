PLEASE_SCHEDULE = " Por favor marque um horário com o comando /setmeeting."

START = """
Olá, sou o BPB! 
O bot de Boas práticas do Código Bonito.

Use algum dos meus comandos:

/setmeeting - Marca as reuniões e configura os alarmes. 
    Por exemplo: /setmeeting 15-01-2021 18h.
/getmeeting - Retorna as reuniões marcadas
/clear - Limpa a agenda de reuniões
/links - Retorna links importantes do grupo
"""

WELCOME = (
    "Olá, {user_text}! Esse é o grupo do Código Bonito, "
    "um grupo de discussões sobre programação, "
    "bioinformática e ciência aberta. "
    "Se apresente e conte como encontrou o grupo!"
)

SEM_REUNIAO = "Nenhuma reunião agendada."

MARCADA_PARA = "A próxima reunião está marcada para:\n {parsed_date}.\n\n"

REPETIRA = "Esse horário irá se repetir pelas próximas 4 semanas:\n"

CLEAR = "Limpei a agenda de reuniões."

ERRO_AO_MARCAR = (
    "Não consegui marcar a reunião. Por favor verifique a mensagem submetida:\n\n"
)

SEM_VALOR = "Ué, você não enviou nada!"

LINKS_IMPORTANTES = """
[Site do grupo](https://codigobonito.github.io)
[Atas anteriores](https://docs.google.com/document/d/1w_w4O1lv5ZZwpw51G7ATd00hjdAGpkts6TLkd-Uvacc)
"""

LEMBRETE = """
#############################################
Atenção!! A reunião começará em 30 minutos...
#############################################
"""