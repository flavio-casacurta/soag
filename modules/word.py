# coding: utf8

import sys, traceback, win32com.client as win32
                    
def main(argv1, argv2, argv3):
    
    keys = [[" EJECT",            ""],
            [" MOVE",             " MOVER"],
            [" TO",               " PARA"],
            [" CALL",             " CHAMAR"],
            [" PERFORM",          " EXECUTAR ROTINA"],
            [" IF",               " SE"],
            [" ELSE",             " SENAO"],
            [" END-IF",           " FIM-SE"],
            [" UNTIL",            " ATE QUE"],
            [" WHILE",            " ENQUANTO"],
            [" NOT EQUAL",        " DIFERENTE"],
            [" NOT",              " NAO"],
            [" LESS",             " MENOR QUE"],
            [" EQUAL",            " IGUAL A"],
            [" GREATER",          " MAIOR QUE"],
            [" TO",               " PARA"],
            [" COMPUTE",          " CALCULAR"],
            [" ADD",              " SOMAR"],
            [" FROM",             " DE"],
            [" OPEN",             " ABRIR"],
            [" CLOSE",            " FECHAR"],
            [" INPUT PROCEDURE",  " ROTINA DE ENTRADA :"],
            [" INPUT  PROCEDURE", " ROTINA DE ENTRADA :"],
            [" OUTPUT PROCEDURE", " ROTINA DE SAIDA   :"],
            [" INPUT",            " PARA LEITURA :"],
            [" OUTPUT",           " PARA GRAVACAO :"],
            [" AND",              " E"],
            [" OR",               " OU"],
            [" SELECT",           " SELECIONAR REGISTRO"],
            [" DELETE",           " DELETAR REGISTRO"],
            [" INSERT",           " INCLUIR REGISTRO"],
            [" UPDATE",           " ALTERAR REGISTRO"],
            [" SET",              " MUDANDO"],
            [" LIKE",             " CONTENHA"],
            [" INTO",             " NA AREA"],
            [" WHERE",            " AONDE"],
            [" GROUP BY",         " AGRUPADO POR"],
            [" ORDER BY",         " ORDENADO POR"],
            [" THRU",             " ATE"],
            [" READ",             " LER"],
            [" WRITE",            " GRAVAR"],
            [" RELEASE",          " GRAVAR (SD)"],
            [" RETURN",           " LER (SD)"],
            [" SPACE",            " ESPACO"],
            [" SPACES",           " ESPACOS"],
            [" OF",               " DA AREA"],
            [" DISPLAY",          " EXIBIR"],
            [" SUBTRACT",         " SUBTRAIR"],
            [" FETCH",            " LER CURSOR"],
            [" USING",            " USANDO"],
            [" VARYING",          " VARIANDO"],
            [" BY",               " EM"],
            [" GOBACK",           " ENCERRAR PROGRAMA"],
            [" STOP",             " ENCERRAR"], 
            [" RUN",              ""],
            [" GO",               " IR"],
            [" SORT",             " CLASSIFICAR"],
            [" ASCENDING KEY",    " CHAVE ASCENDENTE"],
            [" ASCENDING",        " ASCENDENTE"],
            [" DESCENDING",       " DESCENDENTE"],
            [" KEY",              " CHAVE"],
            [" UPON",             " AO"],
            [" CONSOLE",          " OPERADOR"], 
            [" ACCEPT",           " RECEBER DIGITACAO"],
            [" NEXT",             " PROXIMA"],
            [" SENTENCE",         " SENTENCA"],
            [" AT END",           " NO FIM DE ARQUIVO"],
            [" GIVING",           " OBTENDO"],
            [" STRING",           " FORMATAR"],
            [" DELIMITED BY",     ""],
            [" END-PERFORM",      " FIM-LOOP-EXECUCAO"],
            [" EXIT",             " FIM DE ROTINA"],
            [" INITIALIZE",       " INICIALIZAR AREA"],
            [" PROGRAM-ID",       " PROGRAMA"],
            [" SECTION",          ""],
            [" NOT",              " NAO"],
            [" NUMERIC",          " NUMERICO"],
            [" EXEC SQL",         " EXECUTAR COMANDO SQL"],
            [" EXEC  SQL",        " EXECUTAR COMANDO SQL"],
            [" EXEC   SQL",       " EXECUTAR COMANDO SQL"],
            [" END-EXEC",         " FIM DE EXECUCAO"],
            [" END-IF.",          " FIM-SE."],
            [" SECTION.",         ""],
            [" EVALUATE",         " VERIFICAR O VALOR DE"],
            [" WHEN",             " QUANDO FOR"],
            [" DIVIDE",           " DIVIDIR"],
            [" END-EVALUATE",     " FIM DE VERIFICACAO"]]

    proc  = False
    qtde  = 0
    procs = []

    try:
        
        with open(argv3) as f:
            
            for line in f:
                
                if 'PROCEDURE' in line and 'DIVISION.' in line:
                    proc = True
                    continue
                
                if  proc:
                    if  qtde > 1:
                        for key in keys:
                            line = line.replace(key[0], key[1])
                        procs.append(line)
                    else:
                        qtde += 1
    
        app               = win32.Dispatch('Word.Application')
        app.Visible       = False
        app.DisplayAlerts = False
        
        apd = app.Documents.Open(argv1)
        
        for tb in argv2:
            app.Selection.Find.Execute(tb[0], False, False, False, False, \
                                               False, True, 1, False, tb[1], 2)
        
        if  len(procs) > 0:
            app.Selection.Find.Execute('@PROCEDURE', False, False, False, \
                                           False, False, True, 1, False, '', 2)
            doc = apd.Range()
            for line in procs:
                doc.InsertAfter(line)
        else:
            app.Selection.Find.Execute('@PROCEDURE', False, False, False, \
                                           False, False, True, 1, False, '', 2)
        
        app.ActiveDocument.Close(SaveChanges=True)
        
        app.Quit()
        
    except:
        return traceback.format_exc()

if __name__=='__main__':
  main(sys.argv[1], sys.argv[2], sys.argv[3])