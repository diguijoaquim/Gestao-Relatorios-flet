import flet as ft
from control import getCartas

def main(page: ft.Page):
    page.theme_mode = 'light'
    page.title = 'Sistema de Control de Relatorios'
    selected_file_paths = []

    # Aqui ficam as três imagens
    imagens = ft.Column(width=100)

    def change(e):
        if e.control.selected_index==0:
            print(e.control.selected_index)
            body.content=lancamento
        elif e.control.selected_index==1:
            print(1)
        elif e.control.selected_index==2:
            body.content=tabela
            print(2)
        page.update()

    # Tabela
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Cidade")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Número")),
            ft.DataColumn(ft.Text("Texto")),
            ft.DataColumn(ft.Text("Imagem")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        border_radius=10,
        border=ft.border.all(1, ft.colors.GREY_300),
    )

    # Recebe o evento de file_picker
    def file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_paths
        if e.files:
            selected_file_paths = [file.path for file in e.files[:3]]  # Limita a 3 arquivos
            
            imagens.controls.clear()
            for i in selected_file_paths:
                imagens.controls.append(
                    ft.Image(src=i)
                )
            page.update()
        else:
            selected_file_paths = []
            imagens.controls.clear()
            page.update()

    # File Picker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Botão para selecionar as imagens
    select_button = ft.ElevatedButton(text="Selecionar Fotos", on_click=lambda _: file_picker.pick_files(allow_multiple=True))

    # Cria a AppBar do app
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.CODE),
        title=ft.Text("Sistema de Control de Relatorios"),
        actions=[
            ft.IconButton(icon=ft.icons.HEART_BROKEN)
        ],
        bgcolor=ft.colors.GREEN_600,
        color=ft.colors.WHITE
    )

    # Rail 
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME, selected_icon=ft.icons.HOME, label="Lançamento de Carta"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.DATA_OBJECT),
                selected_icon_content=ft.Icon(ft.icons.DATA_OBJECT),
                label="Base de Dados",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Definições"),
            ),
        ],
        on_change=lambda e: change(e)
    )

    # Card de lançamento de carta
    lancamento = ft.Container(content=ft.Column(controls=[
        ft.Text("Lançamento de Carta", weight="bold", size=30),
        ft.Card(content=ft.Container(padding=20, content=ft.Row(controls=[
            ft.Column(controls=[
                ft.TextField(label='Nome'),
                ft.TextField(label='Rua'),
                ft.TextField(label='Cidade'),
                ft.TextField(label='Estado'),
                ft.TextField(label='Número'),
            ]),
            ft.Column(controls=[
                select_button,
                imagens,
                ft.CupertinoButton("Guardar", bgcolor=ft.colors.GREEN_600),
                file_picker
            ])
        ])))
    ]))

    # Adiciona os dados à tabela
    def update_tabela():
        tabela.rows.clear()
        for carta in getCartas():
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(carta['nome'])),
                        ft.DataCell(ft.Text(carta['cidade'])),
                        ft.DataCell(ft.Text(carta['estado'])),
                        ft.DataCell(ft.Text(carta['numero'])),
                        ft.DataCell(ft.Text(carta['texto'])),
                        ft.DataCell(ft.Image(src=carta['imagem'], width=100)),  # Exibindo imagem
                        ft.DataCell(ft.Row(controls=[
                            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.GREEN_700, key=f"{carta['id']}"),
                            ft.IconButton(ft.icons.VISIBILITY, icon_color=ft.colors.BLUE_700, key=f"{carta['id']}"),
                            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, key=f"{carta['id']}"),
                        ])),
                    ]
                )
            )

    update_tabela()

    # Corpo vazio
    body = ft.Container(content=lancamento)

    # Adicionar o rail e o body na page
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                body
            ],
            expand=True,
        )
    )

    # Alert Dialog
    alerta = ft.AlertDialog(
        title=ft.Text("Alerta"),
        content=ft.Text("Inscreva-se no canal este tutorial será muito importante para a sua prática de flet"),
        actions=[
            ft.ElevatedButton("Cancelar", bgcolor="red", color="white"),
            ft.ElevatedButton("Subscrever-se", bgcolor="green", color="white")
        ]
    )

    # Função abre o dialog
    def openalert(e):
        page.dialog = alerta
        alerta.open = True
        page.update()

    # Floating Action Button (FAB)
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=openalert)

    # Atualizar a página
    page.update()

ft.app(target=main)
