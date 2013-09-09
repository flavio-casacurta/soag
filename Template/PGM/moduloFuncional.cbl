
      *----------------------------------------------------------------
       @LABEL-CHAMAR-@MODULO                    SECTION.
      *----------------------------------------------------------------
           MOVE '@LABEL-CHAMAR-@MODULO' TO WRK-PARAGRAFO.
           INITIALIZE @FCTRL-BLOCO-RETORNO OF WRK-@MODULO.
           MOVE '@MODULO'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@MODULO)
                                       LENGTH  (LENGTH OF WRK-@MODULO)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO FRWKGLAQ-COD-RETORNO
              MOVE '@ERR_LOCAL'     TO FRWKGLAQ-COD-ERRO
              MOVE '@ERROCICS' TO FRWKGLAQ-COD-MENSAGEM
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @FCTRL-BLOCO-RETORNO OF WRK-@MODULO
             TO FRWKGLAQ-BLOCO-RETORNO.
           IF FRWKGLAQ-COD-RETORNO GREATER THAN 1
              IF FRWKGLAQ-COD-RETORNO GREATER THAN 8
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------
       @LABEL-99-EXIT. EXIT.
      *----------------------------------------------------------------
