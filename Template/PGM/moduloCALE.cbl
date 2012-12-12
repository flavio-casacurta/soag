
      *----------------------------------------------------------------
       2800-CHAMAR-CALE1000                    SECTION.
      *----------------------------------------------------------------
           MOVE '2800-CHAMAR-CALE1000' TO WRK-PARAGRAFO.
           INITIALIZE CALEWAAC-BLOCO-RETORNO OF CALEWAAC.
           MOVE 'CALE1000'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(CALEWAAC)
                                       LENGTH  (LENGTH OF CALEWAAC)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '@ERR_LOCAL'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE CALEWAAC-BLOCO-RETORNO OF CALEWAAC
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDI
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI NOT EQUAL TO ZEROS
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI
                   TO FRWKGMOD-COD-RETORNO
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------
       2800-99-EXIT. EXIT.
      *----------------------------------------------------------------
