# -*- coding: utf-8 -*-

import traceback

def WordHtml(argv1, argv2, argv3, argv4):

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
            [" RETURN",           " RETORNAR"],
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
            [" END-EVALUATE",     " FIM DE VERIFICACAO"],
            [" VALUES",           " VALORES"],
            [" VALUE",            " VALOR"]]

    proc  = False
    qtde  = 0
    htmls = ''

    try:

        with open(argv4) as f1:

            for line in f1:

                if 'PROCEDURE' in line and 'DIVISION.' in line:
                    proc = True
                    continue

                if  proc:
                    if  qtde > 1:
                        for key in keys:
                            line = line.replace(key[0], key[1])
                        htmls += line.replace(' ', '&nbsp;') + '<br/>'
                    else:
                        qtde += 1

        with open(argv2, 'w') as f2:

            with open(argv1)  as f3:

                for line in f3:
                    if  '@PROCEDURE' in line:
                        f2.write(line.replace('@PROCEDURE', \
                                                          '<br/>' + htmls))
                    else:
                        for tb in argv3:
                            line = line.replace(tb[0], tb[1])
                        f2.write(line)

    except:
        return traceback.format_exc()
