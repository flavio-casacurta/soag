
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
              MOVE 16         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@SIGLAPGMI
              MOVE '@ERRLOCAL'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@SIGLAPGMI
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@SIGLAPGMI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE CALEWAAC-BLOCO-RETORNO OF CALEWAAC
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@SIGLAPGMI
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGMI NOT EQUAL TO ZEROS
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGMI GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGMI
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
