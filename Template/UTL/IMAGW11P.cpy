      *----------------------------------------------------------------*
      * PROCEDURE COMUM A TODOS OS MODULOS FUNCIONAIS BASICOS PARA     *
      *                   TRATAMENTO DE ERROS                          *
      *----------------------------------------------------------------*
      *90900-ABEND-PROGRAM SECTION.
       90900-ABEND-PROGRAM SECTION.
           SET     ERRO-LIVRE TO TRUE.
           IF      WRK-ABCODE EQUAL TO SPACES
                   EXEC CICS ASSIGN ABCODE (WRK-ABCODE)
                   END-EXEC
                   IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
                      CONTINUE
                   END-IF
           END-IF.
           STRING WRK-PROGRAM
                , ' - ABEND PROGRAM '
                , ' - CODE = '
                , WRK-ABCODE
                DELIMITED BY SIZE
                INTO FRWKGLIV-PARAMETROS
           END-STRING.
           MOVE 16         TO IMAGW00C-COD-RETORNO  OF DFHCOMMAREA.
           MOVE 'ER99'     TO IMAGW00C-COD-ERRO     OF DFHCOMMAREA.
           MOVE 'IMAG9999' TO IMAGW00C-COD-MENSAGEM OF DFHCOMMAREA.
           PERFORM 91000-API-ERROR.
       90900-99-EXIT. EXIT.

       91000-API-ERROR SECTION.
           MOVE WRK-PARAGRAFO  TO FRWKGHEA-IDEN-PARAGRAFO.
           MOVE WRK-PROGRAM TO FRWKGHEA-NOME-PROGRAMA.
           EVALUATE TRUE
           WHEN ERRO-DB2
                MOVE FRWKGDB2-TAM-LAYOUT      TO FRWKGHEA-TAM-DADOS
                MOVE WRK-AREA-ERRO-DB2        TO WRK-BLOCO-INF-ERRO
           WHEN ERRO-CICS
                MOVE EIBFN                    TO FRWKGCIC-EIBFN
                MOVE EIBRCODE                 TO FRWKGCIC-EIBRCODE
                MOVE EIBRSRCE                 TO FRWKGCIC-EIBRSRCE
                MOVE EIBRESP                  TO FRWKGCIC-EIBRESP
                MOVE EIBRESP2                 TO FRWKGCIC-EIBRESP2
                MOVE EIBTASKN                 TO FRWKGCIC-EIBTASKN
                MOVE FRWKGCIC-TAM-LAYOUT      TO FRWKGHEA-TAM-DADOS
                MOVE WRK-AREA-ERRO-CICS       TO WRK-BLOCO-INF-ERRO
           WHEN ERRO-MODULO
                MOVE WRK-MODULO               TO FRWKGMOD-NOME-MODULO
                MOVE FRWKGMOD-TAM-LAYOUT      TO FRWKGHEA-TAM-DADOS
                MOVE WRK-AREA-ERRO-MOD        TO WRK-BLOCO-INF-ERRO
           WHEN ERRO-LIVRE
                MOVE FRWKGLIV-TAM-LAYOUT      TO FRWKGHEA-TAM-DADOS
                MOVE WRK-AREA-ERRO-LIV        TO WRK-BLOCO-INF-ERRO
           WHEN OTHER
                CONTINUE
           END-EVALUATE.
           EXEC CICS LINK PROGRAM  ('FRWK1999')
                          COMMAREA (WRK-AREA-ERRO)
                          LENGTH   (LENGTH OF WRK-AREA-ERRO)
                          NOHANDLE
           END-EXEC.
           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              CONTINUE
           END-IF.
           PERFORM 99990-RETURN.
       91000-99-EXIT. EXIT.

       99990-RETURN SECTION.
           EXEC CICS RETURN END-EXEC.
           IF EIBRESP EQUAL DFHRESP(NORMAL)
              CONTINUE
           END-IF.
       99990-99-EXIT. EXIT.
