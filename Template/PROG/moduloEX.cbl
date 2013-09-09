
      *----------------------------------------------------------------
       @LABEL-CHAMAR-@MODULO                    SECTION.
      *----------------------------------------------------------------
           MOVE '@LABEL-CHAMAR-@MODULO' TO WRK-PARAGRAFO.
           INITIALIZE @CONTROLE-BLOCO-RETORNO OF WRK-@MODULO.
@MOVEKEYS
           MOVE '@MODULO'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@MODULO)
                                       LENGTH  (LENGTH OF WRK-@MODULO)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '@ERRLOCAL1'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @CONTROLE-BLOCO-RETORNO OF WRK-@MODULO
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM NOT EQUAL TO ZEROS
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
                   TO FRWKGMOD-COD-RETORNO
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------
       @LABEL-99-EXIT. EXIT.
      *----------------------------------------------------------------
