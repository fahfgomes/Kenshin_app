import flet as ft
import requests
import json
import geocoder
from datetime import datetime, timedelta
from flet import *



# Função para enviar localização e confirmar presença
def enviar_localizacao(page, lat, lon):
    url = "http://localhost:5000/confirmar-presenca"
    data = {
        "location": [lat, lon]
    }
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    
    if response.status_code == 200:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Presença Confirmada", color=ft.colors.BLUE_GREY),
            content=ft.Text("Sua presença foi confirmada com sucesso!", color=ft.colors.BLUE_GREY),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
    else:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Falha na Confirmação", color=ft.colors.BLUE_GREY),
            content=ft.Text("Você precisa estar na academia para confirmar a presença", color=ft.colors.BLUE_GREY),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
    
    page.dialog.open = True
    page.update()


def faixa_widget(cor_faixa):
    return ft.Container(
        width=100,
        height=20,
        bgcolor=cor_faixa,
        border_radius=10,
        alignment=ft.alignment.center,
    )

# Verificação do dia e horário para confirmar presença
def verificar_dia_horario(page, treino_dia, treino_horario):
    agora = datetime.now()
    
    dias_semana = {
        "Segunda-feira": 0,
        "Terça-feira": 1,
        "Quarta-feira": 2,
        "Quinta-feira": 3,
        "Sexta-feira": 4,
        "Sábado": 5,
        "Domingo": 6
    }
    
    horario_treino = datetime.strptime(treino_horario, '%H:%M').time()
    
    if agora.weekday() != dias_semana[treino_dia]:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Erro", color=ft.colors.BLUE_GREY),
            content=ft.Text(f"Você só pode confirmar presença no dia de {treino_dia}.", color=ft.colors.BLUE_GREY),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()
        return False

    horario_treino_completo = datetime.combine(agora.date(), horario_treino)
    horario_permitido_inicio = horario_treino_completo - timedelta(hours=1)
    horario_permitido_fim = horario_treino_completo + timedelta(hours=3)

    if agora < horario_permitido_inicio or agora > horario_permitido_fim:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Erro", color=ft.colors.BLUE_GREY),
            content=ft.Text(f"Você pode confirmar presença entre {horario_permitido_inicio.time()} e 12h do dia seguinte.", color=ft.colors.BLUE_GREY),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()
        return False

    return True

# Página de confirmação de presença
def confirmacao_presenca(page, treino_dia, treino_horario):
    if not verificar_dia_horario(page, treino_dia, treino_horario):
        return

    g = geocoder.ip('me')
    latitude, longitude = g.latlng

    def confirmar_presenca(e):
        enviar_localizacao(page, latitude, longitude)
    
    page.controls.clear()
    page.add(
        ft.Text(f"Confirmação de Presença - Treino de {treino_dia}", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        ft.ElevatedButton("Confirmar Presença", on_click=confirmar_presenca),
        ft.ElevatedButton("Voltar", on_click=lambda _: horarios_treinos(page))
    )
    page.update()

# Página de horários de treinos
def horarios_treinos(page):
    def selecionar_treino(e):
        treino_dia = e.control.data['dia']
        treino_horario = e.control.data['horario']
        confirmacao_presenca(page, treino_dia, treino_horario)
    
    treinos = {
        "Segunda-feira": "19:00",
        "Segunda-feira": "15:30",
        "Terça-feira": "19:00",
        "Quarta-feira": "15:30",
        "Quarta-feira": "19:00",
        "Quinta-feira": "19:00",
        "Sexta-feira": "15:30",
        "Sábado": "18:00",
        "Domingo": "09:00"
    }
    
    treino_widgets = []
    
    for dia, horario in treinos.items():
        treino_widgets.append(
            ft.ElevatedButton(
                f"{dia} - {horario}",
                data={"dia": dia, "horario": horario},
                on_click=selecionar_treino
            )
        )
    
    page.controls.clear()
    page.add(
        ft.Text("Selecione o Treino", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        *treino_widgets,
        ft.ElevatedButton("Sair", on_click=lambda _: login_page(page)),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()

# Página de avisos
def avisos_page(page):
    # Lista de avisos (simulação)
    avisos = [
        "Festa de dia das crianças dia 12/10",
        "Evento de graduação no próximo mês, estudem",
        "Lembre-se de contribuir com a associação"
    ]
    
    page.controls.clear()
    page.add(
        ft.Text("Avisos", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        *[ft.Text(aviso, size=18, color=ft.colors.BLUE_GREY) for aviso in avisos],
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()

# Página de contribuição
def contribuicao_page(page):
    # Informações de pagamento (simulação)
    dados_deposito = {
        "Banco": "ITAÚ UNIBANCO S.A",
        "Chave Pix (CNPJ)": "44.329.704/0001-88",
        "Titular": "ASSOCIAÇÃO DE JUDO KENSHIN"
    }

    # Função para copiar o CNPJ
    def copiar_cnpj(e):
        # Coloca o CNPJ na área de transferência utilizando Flet
        page.set_clipboard(dados_deposito["Chave Pix (CNPJ)"])
        page.dialog = ft.AlertDialog(
            title=ft.Text("CNPJ Copiado!", color=ft.colors.BLUE_GREY),
            content=ft.Text("A chave Pix foi copiada para a área de transferência.", color=ft.colors.BLUE_GREY),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()

    page.controls.clear()
    page.add(
        ft.Text("Contribuição Mensalidade", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        *[ft.Text(f"{key}: {value}", color=ft.colors.BLUE_GREY) for key, value in dados_deposito.items()],
        ft.Row(
            controls=[
                ft.Text(dados_deposito["Chave Pix (CNPJ)"], color=ft.colors.BLUE_GREY),
                ft.IconButton(icon=ft.icons.COPY, on_click=copiar_cnpj, tooltip="Copiar Chave Pix (CNPJ)")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()

# Página de apostila
def apostila_page(page):
    page.controls.clear()
    page.add(
        ft.Text("Apostila de Estudos", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        ft.ElevatedButton("Abrir Apostila", on_click=lambda _: abrir_apostila()),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()

def abrir_apostila():
    import webbrowser
    webbrowser.open("https://www.judokenshin-osasco.com.br/apostila.pdf")


def editar_perfil_page(page):
    page.controls.clear()
    
    # Dados do aluno que podem ser editados
    nome_input = ft.TextField(label="Nome", value="João da Silva")
    email_input = ft.TextField(label="E-mail", value="joao.silva@email.com")
    faixa_input = ft.Dropdown(
        label="Faixa",
        value="Faixa Amarela",
        options=[
            ft.dropdown.Option("Faixa Branca"),
            ft.dropdown.Option("Faixa Amarela"),
            ft.dropdown.Option("Faixa Laranja"),
            ft.dropdown.Option("Faixa Verde"),
            ft.dropdown.Option("Faixa Azul"),
            ft.dropdown.Option("Faixa Marrom"),
            ft.dropdown.Option("Faixa Preta"),
        ]
    )
    
    # Layout da página de edição de perfil
    page.add(
        ft.Text("Editar Perfil", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY),
        ft.Divider(height=1, color=ft.colors.GREY_300),
        ft.Column(
            [
                nome_input,
                email_input,
                faixa_input,
            ],
            spacing=10
        ),
        ft.ElevatedButton("Salvar", on_click=lambda _: salvar_perfil(nome_input.value, email_input.value, faixa_input.value, page)),
        ft.ElevatedButton("Cancelar", on_click=lambda _: perfil_page(page))
    )
    page.update()

def salvar_perfil(nome, email, faixa, page):
    # Lógica para salvar os dados alterados (a ser implementada)
    print(f"Salvando Nome: {nome}, Email: {email}, Faixa: {faixa}")
    perfil_page(page)

def perfil_page(page):
    page.controls.clear()
    
    # Dados do aluno
    aluno_nome = "João da Silva"
    aluno_email = "joao.silva@email.com"
    aluno_curso = "Faixa Amarela - Judô"
    
    # Layout da página de perfil
    page.add(
        ft.Text("Perfil do Aluno", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY),
        ft.Divider(height=1, color=ft.colors.GREY_300),
        ft.Column(
            [
                ft.Text(f"Nome: {aluno_nome}", size=16),
                ft.Text(f"E-mail: {aluno_email}", size=16),
                ft.Text(f"Faixa: {aluno_curso}", size=16),
            ],
            spacing=10,
        ),
        ft.ElevatedButton("Editar Perfil", on_click=lambda _: editar_perfil_page(page)),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()
def alterar_senha_page(page):
    page.controls.clear()
    
    # Campos de senha
    senha_atual_input = ft.TextField(label="Senha Atual", password=True, can_reveal_password=True)
    nova_senha_input = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True)
    confirmar_senha_input = ft.TextField(label="Confirmar Nova Senha", password=True, can_reveal_password=True)
    
    # Layout da página de alteração de senha
    page.add(
        ft.Text("Alterar Senha", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY),
        ft.Divider(height=1, color=ft.colors.GREY_300),
        ft.Column(
            [
                senha_atual_input,
                nova_senha_input,
                confirmar_senha_input,
            ],
            spacing=10
        ),
        ft.ElevatedButton("Salvar", on_click=lambda _: salvar_senha(senha_atual_input.value, nova_senha_input.value, confirmar_senha_input.value, page)),
        ft.ElevatedButton("Cancelar", on_click=lambda _: configuracoes_page(page))
    )
    page.update()

def salvar_senha(senha_atual, nova_senha, confirmar_senha, page):
    # Lógica de validação e salvamento da senha (a ser implementada)
    if nova_senha == confirmar_senha:
        print(f"Senha atual: {senha_atual}, Nova senha: {nova_senha}")
        configuracoes_page(page)
    else:
        print("As senhas não correspondem.")

def eventos_page(page):
    page.controls.clear()
    
    # Layout da página de eventos
    page.add(
        ft.Text("Próximos Eventos", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY),
        ft.Divider(height=1, color=ft.colors.GREY_300),
        ft.Column(
            [
                ft.Text("01/11/2024 - Torneio Regional de Judô", size=16),
                ft.Text("15/11/2024 - Exame de Faixa - Academia", size=16),
                ft.Text("25/12/2024 - Festa de Confraternização", size=16),
            ],
            spacing=10,
        ),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()
def configuracoes_page(page):
    page.controls.clear()
    
    # Layout da página de configurações
    page.add(
        ft.Text("Configurações", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY),
        ft.Divider(height=1, color=ft.colors.GREY_300),
        ft.Column(
            [
                ft.Switch(label="Notificações", value=True),
                ft.Switch(label="Modo Escuro", value=False),
                ft.ElevatedButton("Alterar Senha", on_click=lambda _: alterar_senha_page(page)),
            ],
            spacing=10
        ),
        ft.ElevatedButton("Voltar", on_click=lambda _: home_page(page))
    )
    page.update()

# Página inicial de home
def home_page(page):
    page.controls.clear()
    
    # Exemplo de dados do aluno
    aluno_nome = "João da Silva"
    aluno_foto_url = "C:/Users/fabfr/Desktop/,/documentos DETRAN/foto rosto.jpg"  # Substitua pela URL da foto do aluno
    cor_faixa = ft.colors.YELLOW  # Altere a cor conforme a faixa do aluno

        # Seção de ícones principais (menu)
    main_menu = ft.Column(
        [
            ft.Row([
                ft.IconButton(icon=ft.icons.NOTIFICATIONS, on_click=lambda _: avisos_page(page)),
                ft.Text("Avisos", color=ft.colors.BLUE_GREY),
            ]),
            ft.Row([
                ft.IconButton(icon=ft.icons.SCHEDULE, on_click=lambda _: horarios_treinos(page)),
                ft.Text("Treinos", color=ft.colors.BLUE_GREY),
            ]),
            ft.Row([
                ft.IconButton(icon=ft.icons.PAYMENTS, on_click=lambda _: contribuicao_page(page)),
                ft.Text("Mensalidade", color=ft.colors.BLUE_GREY),
            ]),
            ft.Row([
                ft.IconButton(icon=ft.icons.BOOK, on_click=lambda _: apostila_page(page)),
                ft.Text("Apostila", color=ft.colors.BLUE_GREY),
            ]),
        ],
        spacing=10,  # Espaçamento entre os itens do menu
        alignment=ft.MainAxisAlignment.CENTER, # Alinhamento dos itens
        horizontal_alignment=ft.CrossAxisAlignment.END
        
    )

    menu_container = ft.Container(
        content=main_menu,
        bgcolor=ft.colors.WHITE,
        opacity=0.0,  # Começa ofuscado
        padding=ft.padding.all(20),
        alignment=ft.alignment.center,
        border_radius=0,  # Remove bordas para ocupar a tela toda
        width=page.width,  # Ocupe a largura total da página
        height=page.height  # Ocupe a altura total da página
    )
    menu_container.visible = False
    def toggle_menu(e):
        # Alterna a visibilidade do menu
        menu_container.visible = not menu_container.visible
        menu_container.opacity = 1.0 if menu_container.visible else 0.0
        page.update()

    # Botão para abrir/fechar o menu
    menu_button = ft.IconButton(icon=ft.icons.MENU, on_click=toggle_menu, alignment=ft.alignment.top_left)
    # Cabeçalho com foto e nome do aluno
    header = ft.Container(
    content=ft.Row(
        [
            ft.Image(src=aluno_foto_url, width=80, height=80, border_radius=40),
            ft.Column(
                [
                    ft.Text(aluno_nome, size=18, color=ft.colors.BLACK),
                    faixa_widget(cor_faixa),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    ),
    padding=ft.padding.all(5),
    bgcolor=ft.colors.LIGHT_BLUE_50  # Aplica a cor de fundo no Container
)


    # Seção de notícias e vídeos
    conteudo = ft.Column(
        [
            ft.Text("Notícias do Judô e Academia", size=18, color=ft.colors.BLUE_GREY, weight=ft.FontWeight.BOLD),
            ft.Card(
    content=ft.Column(
        [
            ft.Text("Judô na Olimpíada: Destaques de 2024", size=14),
            ft.Container(
                content=ft.Text(
                    "Assista no YouTube"
                ),
                on_click=lambda _: page.launch_url("https://www.youtube.com/watch?v=video_id_exemplo"),
            )
        ],
        spacing=5
    )
)

        ],
        spacing=5
    )


    # Barra de navegação na parte inferior
    # navbar = ft.Container(
    #     content=ft.Row(
    #     [
    #         ft.Row([
    #             ft.IconButton(icon=ft.icons.HOME, selected=True),
    #             ft.Text("Início", color=ft.colors.BLUE_GREY),
    #         ]),
    #         ft.Row([
    #             ft.IconButton(icon=ft.icons.PERSON, on_click=lambda _: perfil_page(page)),
    #             ft.Text("Perfil", color=ft.colors.BLUE_GREY),
    #         ]),
    #         ft.Row([
    #             ft.IconButton(icon=ft.icons.EVENT, on_click=lambda _: eventos_page(page)),
    #             ft.Text("Eventos", color=ft.colors.BLUE_GREY),
    #         ]),
    #         ft.Row([
    #             ft.IconButton(icon=ft.icons.SETTINGS, on_click=lambda _: configuracoes_page(page)),
    #             ft.Text("Configurações", color=ft.colors.BLUE_GREY),
    #         ]),
    #     ],
    #     alignment=ft.MainAxisAlignment.SPACE_AROUND,
    #     ),
    #     padding=ft.padding.symmetric(vertical=10),  # Aplica padding ao container
    #     bgcolor=ft.colors.LIGHT_BLUE_100
    # )
    
    def mudar_aba(index):
        page.clean()  # Limpa a página atual
        if index == 0:
            page.add(
        menu_button, 
        menu_container,
        header,
        ft.Divider(height=1, color=ft.colors.GREY_300),
        conteudo,  # Seção de notícias e vídeos
        navbar # Navbar na parte inferior
    )
        elif index == 1:
            perfil_page(page)
        elif index == 2:
           eventos_page(page)
        elif index == 3:
            configuracoes_page(page)

    navbar =  ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Inicio", selected_icon=True),
            ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Perfil"),
            ft.NavigationBarDestination(icon=ft.icons.EVENT, label="Eventos"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Configurações"),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
        ),
        on_change=lambda e: mudar_aba(e.control.selected_index)
    )

    # Adicionando todos os componentes à página
    page.add(
        menu_button, 
        menu_container,
        header,
        ft.Divider(height=1, color=ft.colors.GREY_300),
        conteudo,  # Seção de notícias e vídeos
        navbar # Navbar na parte inferior
    )
    mudar_aba(0)
    page.update()



# Página de login
def login_page(page):
    def login(e):
        if user_input.value == "admin" and password_input.value == "123":
            home_page(page)
        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Login Inválido", color=ft.colors.BLUE_GREY),
                content=ft.Text("Usuário ou senha incorretos.", color=ft.colors.BLUE_GREY),
                actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
            )
            page.dialog.open = True
            page.update()

    user_input = ft.TextField(label="Usuário", color=ft.colors.BLUE_GREY)
    password_input = ft.TextField(label="Senha", password=True, color=ft.colors.BLUE_GREY)
    
    page.controls.clear()
    page.add(
        ft.Text("Login - Academia de Judô", size=24, color=ft.colors.BLUE_GREY, text_align=ft.TextAlign.CENTER),
        user_input,
        password_input,
        ft.ElevatedButton("Entrar", on_click=login)
    )
    page.update()

# Função principal do app Flet
def main(page: ft.Page):
    page.adaptive = True
    page.title = "Confirmação de Presença - Academia de Judô"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE  # Define o fundo como branco
    
    login_page(page)

# Executa o app Flet
ft.app(target=main)
