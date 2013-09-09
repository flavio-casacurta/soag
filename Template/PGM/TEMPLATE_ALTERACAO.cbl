      *----------------------------------------------------------------*
       2050-VALIDAR-UNICIDADE SECTION.
      *----------------------------------------------------------------*
           MOVE @BOOK-@PK    TO @PK    OF @DCLGEM
           MOVE @BOOK-@UNICO TO @UNICO OF @DCLGEM

           EXEC SQL SELECT COUNT(*)
                      INTO :WRK-COUNT
                      FROM  @TABELA
                     WHERE  @PK <> :DCLGEN.@PK
                       AND          @UNICO
                         = :@DCLGEN.@UNICO
           END-EXEC.

           IF SQLCODE NOT EQUAL ZEROS
              MOVE 16                  TO SACLW000-COD-RETORNO
              MOVE 'ER03'              TO SACLW000-COD-ERRO
              MOVE '@ERRODB2'          TO SACLW000-COD-MENSAGEM
              SET  ERRO-DB2            TO TRUE
              MOVE '@TABELA'
                                       TO FRWKGDB2-NOME-TABELA
              SET  DB2-SELECT          TO TRUE
              MOVE SPACES              TO FRWKGDB2-STORED-PROC
              MOVE SPACES              TO FRWKGDB2-LOCAL
              MOVE SQLCA               TO FRWKGDB2-SQLCA
              MOVE SQLCODE             TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

           IF WRK-COUNT GREATER THAN ZEROS
              MOVE 08                  TO SACLW000-COD-RETORNO
              MOVE 'ER02'              TO SACLW000-COD-ERRO
              MOVE '@MESSAGE'          TO SACLW000-COD-MENSAGEM
              PERFORM 3000-FINALIZAR
           END-IF.
      *----------------------------------------------------------------*
       2050-99-EXIT. EXIT.
      *----------------------------------------------------------------*
