
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
              MOVE 16         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '@ERR_LOCAL'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @FCTRL-BLOCO-RETORNO OF WRK-@MODULO
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDI
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI NOT EQUAL TO ZEROS
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI
                   TO FRWKGMOD-COD-RETORNO
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              END-IF
           ELSE
              MOVE 8          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '@ERR_LOCAL'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@MSGERROR' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              PERFORM 3000-FINALIZAR
           END-IF.
      *----------------------------------------------------------------
       @LABEL-99-EXIT. EXIT.
      *----------------------------------------------------------------
