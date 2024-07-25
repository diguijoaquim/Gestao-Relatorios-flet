import flet as ft
from control import getCartas
def main(page: ft.Page):
    page.theme_mode = 'light'
    page.title = 'Sistema de Control de Relatorios'
    selected_file_paths = []


    def change_mode(e):
        if page.theme_mode=="light":
            page.theme_mode="dark"
        else:
            page.theme_mode="light"
        page.update()


    page.appbar=ft.AppBar(leading=ft.Icon(ft.icons.COMPUTER),
                          title=ft.Text('Sistema de Control de Relatorios'),
                          actions=[
                              ft.IconButton(icon=ft.icons.LIGHT_MODE,on_click=change_mode)
                          ],
                          bgcolor=ft.colors.GREEN_700,
                          color='white'
                          )

    # Aqui ficam as três imagens
    imagens = ft.Column(width=100)

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

    home=ft.Container(content=ft.Column(controls=[
        ft.Text("Lançamento de Carta", weight="bold", size=30),
        tabela
       
    ]))
    database=ft.Container(content=ft.Text("DataBase"))
    setting=ft.Container(content=ft.Text("Setting"))

    body=ft.Container()
    body.content=home
    
    def change(e):
        id=e.control.selected_index
        if id==0:
            body.content=home
            page.update()
        elif id==1:
            body.content=database
            page.update()
        elif id==2:
            body.content=setting
            page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HOME_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.HOME),
                label="Inicio",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.COMPUTER_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.COMPUTER),
                label="Dados",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Definicoes"),
            ),
        ],
        on_change=change
    )
    def cancer(e):
        form.open=False
        imagens.controls.clear()
        page.update()
        
    form=ft.AlertDialog(title=ft.Text("Lancamento de Carta"),
                        content=ft.Container(width=600,content=ft.Card(content=ft.Container(padding=20, content=ft.Row(controls=[
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
        ])))),
                        actions=[
                            ft.ElevatedButton("Cancelar",on_click=cancer),
                            ft.ElevatedButton("Lancar",color=ft.colors.GREEN_700)
                        ])
    def open_dialog(e):
        page.dialog=form
        form.open=True
        page.update()

    page.floating_action_button=ft.FloatingActionButton(icon=ft.icons.ADD,on_click=open_dialog)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ body], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )
    page.update()

ft.app(target=main)