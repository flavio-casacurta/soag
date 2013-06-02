      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID4@SIGLAPGM@PERSISTENCIA.
       AUTHOR.     @AUTHOR.
      *================================================================*
      *@CONTRATANTE
      *----------------------------------------------------------------*
      *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID4@SIGLAPGM@PERSISTENCIA
      *    PROGRAMADOR     : @AUTHOR
      *    ANALISTA        : @ANALISTA
      *    GRUPO           : @GRUPO
      *    DATA DE CRIACAO : @DATE
      *
      *----------------------------------------------------------------*
      *    OBJETIVO....: MODULO PERSISTENCIA
      *                  @SERVICO @ENTIDADE1
      *                  @ENTIDADE2
      *----------------------------------------------------------------*
      *    BOOKS FUNCIONAIS...:                                        *
      *    @APPLIDW00C - BOOK CONTROLE - COMUNICACAO ENTRE MODULOS
      *    @APPLIDW@SIGLAPGMC - BOOK COMUNICACAO DESTE MODULO
      *    @APPLIDW10W - BOOK DE WORK DO PROGRAMA
      *    @APPLIDW01W - BOOK DE WORK PARA TRATAMENTO DE ERROS
      *    @APPLIDW11P - BOOK DE PROCEDUR PARA TRATAMENTO DE ERROS
      *    @DCLGEN - DCLGEN DA TABELA @ENTIDADE3
      *                                @ENTIDADE4
      *----------------------------------------------------------------*
      *    BOOKS DA ARQUITETURA:                                       *
      *    I#FRWKGE - COMMAREA FRWK1999 - LOG DE ERRO                  *
      *    I#FRWKDB - AREA DO FRWK1999  - LOG DE ERROS DB2             *
      *    I#FRWKCI - AREA DO FRWK1999  - LOG DE ERROS CICS            *
      *    I#FRWKMD - AREA DO FRWK1999  - LOG DE ERROS MODULO          *
      *    I#FRWKLI - AREA DO FRWK1999  - LOG DE ERROS LIVRE           *
      *----------------------------------------------------------------*
      *================================================================*

      *================================================================*
        ENVIRONMENT                    DIVISION.
      *================================================================*
      *----------------------------------------------------------------*
       CONFIGURATION                   SECTION.
      *----------------------------------------------------------------*
       SPECIAL-NAMES.
           DECIMAL-POINT               IS COMMA.
      *================================================================*
       DATA                            DIVISION.
      *================================================================*
      *----------------------------------------------------------------*
       WORKING-STORAGE                 SECTION.
      *----------------------------------------------------------------*
       77  FILLER                      PIC  X(050)         VALUE
           '* INICIO DA AREA DE WORKING *'.
      *----------------------------------------------------------------*
       77  WRK-INVOKINGPROG            PIC  X(008) VALUES SPACES.
       77  WRK-PROGRAM                 PIC  X(008) VALUE '@APPLID4@SIGLAPGM@PERSISTENCIA'.
       77  WRK-TABELA                  PIC  X(018) VALUE
                                                   '@TABLENAME'.
      *----------------------------------------------------------------*
      * AREAS DE WORKING GENERICAS*
      *----------------------------------------------------------------*
       COPY @APPLIDW10W.
       COPY @APPLIDW01W.
      *----------------------------------------------------------------*
      * AREA PARA DB2
      *----------------------------------------------------------------*
           EXEC SQL  INCLUDE SQLCA     END-EXEC.
           EXEC SQL  INCLUDE @DCLGEN  END-EXEC.
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           02  LNK-@APPLID4@SIGLAPGM@PERSISTENCIA.
           COPY @APPLIDW00C.
           COPY @APPLIDW@SIGLAPGMC.
      *================================================================*
       PROCEDURE DIVISION.
      *================================================================*
      *----------------------------------------------------------------*
       0000-MAIN                       SECTION.
      *----------------------------------------------------------------*
           PERFORM 1000-INICIAR.
           PERFORM 2000-PROCESSAR.
           PERFORM 3000-FINALIZAR.
      *----------------------------------------------------------------*
       0000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1000-INICIAR                    SECTION.
      *----------------------------------------------------------------*
           MOVE '1000-INICIAR'   TO WRK-PARAGRAFO.
           INITIALIZE  FRWKGHEA-REGISTRO
                       FRWKGCIC-REGISTRO
                       FRWKGMOD-REGISTRO
                       FRWKGLIV-REGISTRO
                       @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
                       @DCLGEN.

           IF EIBCALEN EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '0041'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           EXEC CICS ASSIGN INVOKINGPROG (WRK-INVOKINGPROG)
                     NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '0042'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              SET ERRO-CICS           TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           IF WRK-INVOKINGPROG NOT EQUAL TO '@APPLID3@SIGLAPGM@TYPEPGM'
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '0043'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '@ERROLIV'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              SET ERRO-LIVRE          TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       1000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '2000-PROCESSAR'   TO WRK-PARAGRAFO.
           PERFORM 2100-@COMANDOSQL-@ENTIDADELABEL.
@PERFORMLABEL
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-@COMANDOSQL-@ENTIDADELABEL     SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-@COMANDOSQL-@ENTIDADELABEL' TO WRK-PARAGRAFO.
@SQLSELECTMAX
@VALORIZARDCLGEN
@INSTRUCAOSQL

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE '16'        TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '0045'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@SIGLAPGM@PERSISTENCIA
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-@COMANDOSQL  TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

@MOVEDCLGEN
      *----------------------------------------------------------------*
       3000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '3000-FINALIZAR' TO WRK-PARAGRAFO.
           PERFORM 99990-RETURN.
      *----------------------------------------------------------------*
       3000-99-EXIT. EXIT.
      *----------------------------------------------------------------*
       COPY @APPLIDW11P.
      *----------------------------------------------------------------*
       END PROGRAM @APPLID4@SIGLAPGM@PERSISTENCIA.
