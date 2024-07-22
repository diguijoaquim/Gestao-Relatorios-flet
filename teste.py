import flet as ft

def main(page: ft.Page):
    selected_file_paths = []

    def file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_paths
        if e.files:
            selected_file_paths = [file.path for file in e.files[:3]]  # Limita a 3 arquivos
            status_text.value = f"Arquivos selecionados: {', '.join(selected_file_paths)}"
        else:
            selected_file_paths = []
            status_text.value = "Nenhum arquivo selecionado"
        page.update()

    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    select_button = ft.ElevatedButton(text="Selecionar Fotos", on_click=lambda _: file_picker.pick_files(allow_multiple=True))

    status_text = ft.Text(value="Nenhum arquivo selecionado")

    page.add(select_button, status_text)

ft.app(target=main)
