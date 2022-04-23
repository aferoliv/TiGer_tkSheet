import tkinter as tk
import pandas as pd
from tkinter import ttk
import tksheet
import Bronsted as Br


#######
# selecionadoAD: sistemas escolhidos para AD até 10 sistemas
# selecionadoNT: sistemas escolhidos para NT até 3 sistemas
#
selecionadoAD=[0,0,0,0,0,0,0,0]
selecionadoAD[0]=0
#
selecionadoNT=[0,0,0]
selecionadoNT[0]=0
#
######
class Tela:
    def __init__(self,master,lista_biblioteca, lista_especies):
        #
        self.master=master
        self.title = "TiGer - Simulation of Acid-Base Curve Titration for mixture of mono/poliprotic systems"
        self.lista_especies = lista_especies
        self.lista_biblioteca = lista_biblioteca
        self.biblioteca="Titger.xlxs"
        self.numero_especieAD = 0
        self.numero_especieNT = 0
        #
        # define tamanho da janela
        #
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (w, h))
        #
        #
        self.caixa1(master, lista_especies)
        self.TabelaAD(master)
        self.TabelaNT(master)
        #
        # Botões e Texto no MasterFrame
        #
        self.botaoSair = tk.Button(master, text='     Sair    ', command=master.destroy)
        self.botaoSair.grid(column=10, row=12)
        self.botaoCalc = tk.Button(master, text='  Calcular   ', command=self.Calcular)
        self.botaoCalc.grid(column=4, row=12)
        #
        #
        self.master.mainloop()


    def on_biblioteca(self,event):
        #
        # Le a biblioteca selecionada na tela e atualiza a lista de espécies.
        #
        bib=self.combo.current()
        if bib==0:                      # 'Geral':
            self.tipo_bib="Geral"
            self.biblioteca = 'Titger.xlsx'
            self.dados_pKa = pd.read_excel(self.biblioteca)
            lista = self.dados_pKa.iloc[:, 0]
            self.lista_sistemas = lista.values.tolist()
            self.lista_especies  = self.lista_sistemas     #dados_pKa.iloc[1]

        elif bib==1:                    #'Medicamentos':
            #self.lista_especies = ['Ma', 'Mb', 'Mc', 'Md', 'Me']
            self.tipo_bib = "Medicamentos"
            self.biblioteca = 'titger.xlsx'
            self.dados_pKa = pd.read_excel(self.biblioteca)
            lista = self.dados_pKa.iloc[:, 0]
            self.lista_sistemas = lista.values.tolist()
            self.lista_especies = self.lista_sistemas  # dados_pKa.iloc[1]
        elif bib==2:                    #'Bioquímicos':
            self.lista_especies = ['Ba', 'Bb', 'Bc', 'Bd', 'Be']
        self.comboE['values'] = self.lista_especies

    def on_especies(self,event):
        pass

    def caixa1(self,master, lista):
        #
        # Cria os textos, botões e ComboBox da Caixa Principal
        #
        self.caixa1 = tk.Frame(master, borderwidth=2, relief='raised')
        self.caixa1.grid(column=0, row=10)
        #
        self.texto1 = tk.Label(self.caixa1, text='selecione a Base de Dados')
        self.texto2 = tk.Label(self.caixa1, text='selecione o Sistema ')



        self.botaoAD = tk.Button(self.caixa1, text='   Inserir como titulado   ', command=self.InsereAD)
        self.botaoNT = tk.Button(self.caixa1, text='   Inserir como Titulante   ', command=self.InsereNT)
        self.pH_escrita = tk.Entry(self.caixa1)
        self.texto1.grid(column=0, row=1, padx=10, pady=10)
        self.texto2.grid(column=0, row=2, padx=10, pady=10)
        self.pH_escrita.grid(column=1, row=2, padx=10, pady=10)

        self.botaoAD.grid(column=1, row=4)
        self.botaoNT.grid(column=0, row=4)
        #
        # Combo Biblioteca
        #
        n = tk.StringVar()
        self.combo = ttk.Combobox(self.caixa1, width=27, textvariable=n, state='readonly')
        self.combo['values'] = self.lista_biblioteca
        self.combo['state'] = 'readonly'
        self.combo.current(0)
        self.combo.bind('<<ComboboxSelected>>', self.on_biblioteca)
        self.combo.current(0)
        self.combo.grid(column=1, row=1, padx=10, pady=10)
        #
        #
        #
        n = tk.StringVar()
        self.comboE = ttk.Combobox(self.caixa1, width=27, textvariable=n, state='readonly')
        self.comboE['values'] = self.lista_especies
        self.comboE['state'] = 'readonly'
        self.comboE.bind('<<ComboboxSelected>>', self.on_especies)
        self.comboE.current(1)
        self.comboE.grid(column=1, row=2, padx=10, pady=10)
        #
    def InsereAD (self):
        self.tipo_bib = lista_biblioteca[self.combo.current()]
        selecao = self.comboE.current()
        self.numero_especieAD = self.numero_especieAD + 1
        biblioteca=self.biblioteca
        intermediario = Br.BronstedDados(biblioteca,selecao)
        print('numero especie', self.numero_especieAD)
        ######################
        #
        # imprime a linha na tabela AD
        ################
        if self.numero_especieAD < 8:
            selecionadoAD[self.numero_especieAD] = [biblioteca, selecao]
            linha = intermediario.valores.tolist()
            print('selecao AD: ', selecao, 'biblioteca: ',self.tipo_bib, linha)
            self.selecao_tabela.set_row_data(linha, values = linha)

    def InsereNT(self):
        self.tipo_bib = lista_biblioteca[self.combo.current()]
        selecao = self.comboE.current()
        self.numero_especieNT = self.numero_especieNT + 1
        biblioteca=self.biblioteca
        intermediario = Br.BronstedDados(biblioteca, selecao)
        print('numero especie', self.numero_especieNT)
        if self.numero_especieNT<3:
            selecionadoNT[self.numero_especieNT]=[biblioteca,selecao]
            linha = intermediario.valores.tolist()
            print('selecao AD: ', selecao, 'biblioteca: ',self.tipo_bib, linha)
            #self.selecao_tabelaNT.insert_row()

    def TabelaAD(self,master):

        self.selecao_frameAD= tk.Frame(master, borderwidth=2, relief='raised')
        self.selecao_frameAD.grid(column=0, row=14)
        self.textoAD = tk.Label(self.selecao_frameAD, text='Titulado')
        self.textoAD.grid(column=1, row=10,  padx=10, pady=10)
        legenda = ['sistema AD', 'nNH2', 'carga', 'nCOO(-)', 'pK1', 'pK2', 'pK3', 'pK4', 'pK5', 'pK6', 'pK7', 'pK8', 'fim']
        self.selecao_tabela= tksheet.Sheet(self.selecao_frameAD,
                                           height=100,
                                           width=500,
                                           page_up_down_select_row=True,
                                           expand_sheet_if_paste_too_big=True,
                                           # empty_vertical = 0,
                                           column_width=30,
                                           startup_select=(0, 1, "rows"))
        self.selecao_tabela.headers(legenda)
        self.selecao_tabela.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                    "drag_select",  # enables shift click selection as well
                                    "select_all",
                                    "column_drag_and_drop",
                                    "row_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "row_width_resize",
                                    "column_height_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row",
                                    "copy",
                                    "cut",
                                    "paste",
                                    "delete",
                                    "undo",
                                    "edit_cell"
                                    ))

        self.selecao_tabela.grid()

    def TabelaNT(self,master):

        self.selecao_frameNT = tk.Frame(master, borderwidth=2, relief='raised')
        self.selecao_frameNT.grid(column=0, row=13)
        self.textoNT = tk.Label(self.selecao_frameNT, text='Titulante')
        self.textoNT.grid(column=1, row=1, padx=10, pady=10)

        legenda = ['sistema NT', 'nNH2', 'carga', 'nCOO(-)', 'pK1', 'pK2', 'pK3', 'pK4', 'pK5', 'pK6', 'pK7', 'pK8', 'fim']
        self.selecao_tabelaNT= tksheet.Sheet(self.selecao_frameNT,
                                             height=100,
                                             width=500,
                                           page_up_down_select_row=True,
                                           expand_sheet_if_paste_too_big=True,
                                           # empty_vertical = 0,
                                           column_width=30,
                                           startup_select=(0, 1, "rows"))
        self.selecao_tabelaNT.headers(legenda)
        self.selecao_tabelaNT.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                    "drag_select",  # enables shift click selection as well
                                    "select_all",
                                    "column_drag_and_drop",
                                    "row_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "row_width_resize",
                                    "column_height_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row",
                                    "copy",
                                    "cut",
                                    "paste",
                                    "delete",
                                    "undo",
                                    "edit_cell"
                                    ))

        self.selecao_tabelaNT.grid()
    def Calcular(self):
        sistemaAD=[]
        sistemaNT=[]
        print('Dados AD: ',selecionadoAD[1],'número AD',self.numero_especieAD, 'Dados NT', selecionadoNT, 'numero NT',self.numero_especieNT)
    def ButtonSair(self):
        #
        master.destroy
        #

if __name__ == '__main__':
    window = tk.Tk()
    lista_biblioteca = ['Geral', 'Medicamentos', 'Bioquímicos']
    lista_especies=['','']
    app = Tela(window,lista_biblioteca, lista_especies)
