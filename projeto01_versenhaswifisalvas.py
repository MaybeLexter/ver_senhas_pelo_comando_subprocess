import PySimpleGUI as sg
import subprocess

def redes_info():
    try:
        comando_netsh = subprocess.check_output("netsh wlan show profiles", encoding="cp858", shell=True)
        redes = []
        for linha in comando_netsh.split('\\n'):
            if "Todos os Perfis de Usuários" in linha:
                posicao_referencia = linha.find(":")
                rede = linha[posicao_referencia + 2:]
                senha = informacao_da_rede(rede)
                redes.append(rede + " - " + senha)
        return redes
    except subprocess.CalledProcessError as E:
        return ["Erro ao obter informações"]

def informacao_da_rede(wifi):
    try:
        comando_netsh = subprocess.check_output(["netsh", "wlan", "show", "profile", wifi, "key", "=", "clear"],
                                                  encoding="cp858", shell=True)
        senha = ''
        for linha in comando_netsh.split('\n'):
            if "Conteúdo da Chave" in linha:
                posicao_referencia = linha.find(":")
                senha = linha[posicao_referencia + 2:]
                break
        return senha
    except subprocess.CalledProcessError as E:
        return "Confira o nome da rede"
sg.theme("Black")
layout =  [
    [sg.Text("Bem vindo! Qual senha você gostaria de saber?")],
    [sg.Input(key='-INPUT-', default_text='Nome da rede')],
    [sg.Text(size=(40,1), key='-OUTPUT-')],
    [sg.Button('Pesquisar'), sg.Button('Sair')],
    [sg.Button('Ver todas as redes')],
    [sg.Text('By Leo')]
]

window = sg.Window('Senha do Wifi', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    elif event == 'Ver todas as redes':
        resultado = redes_info()
        if resultado:
            sg.popup_scrolled('\n'.join(resultado), title='Todas as redes')
        else:
            sg.popup('Nenhuma rede Wi-Fi encontrada.', title='Todas as redes')
    elif event == 'Pesquisar':
        rede = values['-INPUT-']
        senha = informacao_da_rede(rede)
        window['-OUTPUT-'].update(f"Para a rede '{rede}' a senha é: {senha}")

window.close()
