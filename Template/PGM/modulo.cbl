
      *----------------------------------------------------------------
       @LABEL-CHAMAR-@MODULO                    SECTION.
      *----------------------------------------------------------------
           MOVE '@LABEL-CHAMAR-@MODULO' TO WRK-PARAGRAFO.
           INITIALIZE @APPLIDW000-BLOCO-RETORNO OF WRK-@MODULO.
           MOVE '@MODULO'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@MODULO)
                                       LENGTH  (LENGTH OF WRK-@MODULO)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW000-COD-RETORNO OF LNK-@APPLID3@PGMIDI
              MOVE '@ERR_LOCAL'     TO @APPLIDW000-COD-ERRO OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS' TO @APPLIDW000-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           IF @APPLIDW000-COD-RETORNO OF WRK-@MODULO NOT EQUAL TO ZEROS
              MOVE @APPLIDW000-BLOCO-RETORNO OF WRK-@MODULO
                TO @APPLIDW000-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDI
              IF @APPLIDW000-COD-RETORNO GREATER THAN 8
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------
       @LABEL-99-EXIT. EXIT.
      *----------------------------------------------------------------
