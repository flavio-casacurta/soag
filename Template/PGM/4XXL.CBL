      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID4@PGMIDI.
       AUTHOR.     @AUTHOR.
      *================================================================*
      *                 @CONTRATANTE
      *----------------------------------------------------------------*
      *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID4@PGMIDI
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
      *    @BOOKC - BOOK COMUNICACAO DESTE MODULO
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
      *    MODULOS.............:                                       *
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
       77  WRK-PROGRAM                 PIC  X(008) VALUE '@APPLID4@PGMIDI'.
       77  WRK-TABELA                  PIC  X(016) VALUE
                                                   '@TABLENAME'.
       77  WRK-NREG-QTDE               PIC S9(009) COMP-3 VALUE ZEROS.
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
      * AREA DE DECLARACAO DOS CURSORES
      *----------------------------------------------------------------*
           EXEC SQL DECLARE CSR01-@DCLGEN CURSOR FOR
                       FROM DB2PRD.@TABLENAME
                FETCH FIRST @OPTIMIZE ROWS ONLY
           END-EXEC.

           EXEC SQL DECLARE CSR02-@DCLGEN CURSOR FOR
                       FROM DB2PRD.@TABLENAME
                FETCH FIRST @OPTIMIZE ROWS ONLY
           END-EXEC.

           EXEC SQL DECLARE CSR03-@DCLGEN CURSOR FOR
                       FROM DB2PRD.@TABLENAME
                FETCH FIRST @OPTIMIZE ROWS ONLY
           END-EXEC.

           EXEC SQL DECLARE CSR04-@DCLGEN CURSOR FOR
                       FROM DB2PRD.@TABLENAME
                FETCH FIRST @OPTIMIZE ROWS ONLY
           END-EXEC.
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           02  LNK-@APPLID4@PGMIDI.
           COPY @APPLIDW00C.
           COPY @BOOKC.
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
           MOVE '1000-INICIAR' TO WRK-PARAGRAFO.

           INITIALIZE  FRWKGHEA-REGISTRO
                       FRWKGCIC-REGISTRO
                       FRWKGMOD-REGISTRO
                       FRWKGLIV-REGISTRO
                       @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID4@PGMIDI
                       @DCLGEN.

           IF EIBCALEN EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0041'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           EXEC CICS ASSIGN INVOKINGPROG (WRK-INVOKINGPROG)
                     NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0042'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET ERRO-CICS           TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           IF WRK-INVOKINGPROG NOT EQUAL TO '@APPLID3@PGMIDI'
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0043'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERROLIV'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET ERRO-LIVRE          TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       1000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '2000-PROCESSAR' TO WRK-PARAGRAFO.

           PERFORM 2100-OPEN-CURSOR.

           PERFORM 2200-FETCH-CURSOR.

           EVALUATE TRUE
               WHEN @PREFIX-P-BLOCO-ANTERIOR
               WHEN @PREFIX-P-ULTIMO-BLOCO
                    PERFORM VARYING WRK-IDX FROM @QOCC BY -1
                      UNTIL WRK-IDX EQUAL ZEROS
                         OR SQLCODE = +100
                         COMPUTE WRK-NREG-QTDE = WRK-NREG-QTDE + 1
                         PERFORM 2300-MOVE-@DCLGEN-TO-@BOOKC
                         PERFORM 2200-FETCH-CURSOR
                    END-PERFORM
               WHEN OTHER
                    PERFORM VARYING WRK-IDX FROM 1 BY 1
                      UNTIL WRK-IDX GREATER @QOCC
                         OR SQLCODE = +100
                         COMPUTE WRK-NREG-QTDE = WRK-NREG-QTDE + 1
                         PERFORM 2300-MOVE-@DCLGEN-TO-@BOOKC
                         PERFORM 2200-FETCH-CURSOR
                    END-PERFORM
           END-IF.

           IF  SQLCODE   EQUAL TO ZEROS
               MOVE 01         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
           END-IF.

           MOVE WRK-NREG-QTDE TO SACLW0FC-NREG-QTDE.

           PERFORM 2400-CLOSE-CURSOR.
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-OPEN-CURSOR                SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-OPEN-CURSOR' TO WRK-PARAGRAFO.

           IF @PREFIX-P-ULTIMO-BLOCO
              PERFORM 2105-SELECT-MAX-ULTIMO-BLOCO
           ELSE
              @MOVE-ULTIMA-KEY
           END-IF.

           EVALUATE TRUE
               WHEN @PREFIX-P-CONSULTA-INICIAL
               WHEN @PREFIX-P-PRIMEIRO-BLOCO
                    PERFORM 2110-OPEN-CURSOR-MAIOR-IGUAL
               WHEN @PREFIX-P-BLOCO-SEGUINTE
                    PERFORM 2120-OPEN-CURSOR-MAIOR
               WHEN @PREFIX-P-BLOCO-ANTERIOR
                    PERFORM 2130-OPEN-CURSOR-MENOR
               WHEN @PREFIX-P-ULTIMO-BLOCO
                    PERFORM 2140-OPEN-CURSOR-MENOR-IGUAL
               WHEN OTHER
                   MOVE 16      TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
                   MOVE '0044'  TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
                   MOVE '@ERROLIV'
                                TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
                   SET  ERRO-LIVRE     TO TRUE
                   PERFORM 91000-API-ERROR
           END-EVALUATE.
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2105-SELECT-MAX-ULTIMO-BLOCO    SECTION.
      *----------------------------------------------------------------*
           MOVE '2105-SELECT-MAX-ULTIMO-BLOCO' TO WRK-PARAGRAFO.

           EXEC SQL SELECT VALUE(MAX(@COLPK), 0)
                      INTO :@DCLGEN.@COLPKCBL
                      FROM DB2PRD.@TABLENAME
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0045'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-SELECT  TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2105-99-EXIT. EXIT.
      *----------------------------------------------------------------*


      *----------------------------------------------------------------*
       2110-OPEN-CURSOR-MAIOR-IGUAL    SECTION.
      *----------------------------------------------------------------*
           MOVE '2110-OPEN-CURSOR-MAIOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL OPEN CSR01-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0046'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-OPEN    TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2110-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2120-OPEN-CURSOR-MAIOR          SECTION.
      *----------------------------------------------------------------*
           MOVE '2120-OPEN-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL OPEN CSR02-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0047'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-OPEN    TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2120-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2130-OPEN-CURSOR-MENOR          SECTION.
      *----------------------------------------------------------------*
           MOVE '2130-OPEN-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL OPEN CSR03-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0048'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-OPEN    TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2130-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2140-OPEN-CURSOR-MENOR-IGUAL    SECTION.
      *----------------------------------------------------------------*
           MOVE '2140-OPEN-CURSOR-MENOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL OPEN CSR04-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0049'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-OPEN    TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2140-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-FETCH-CURSOR               SECTION.
      *----------------------------------------------------------------*
           MOVE '2200-FETCH-CURSOR' TO WRK-PARAGRAFO.

           EVALUATE TRUE
               WHEN @PREFIX-P-CONSULTA-INICIAL
               WHEN @PREFIX-P-PRIMEIRO-BLOCO
                   PERFORM 2210-FETCH-CURSOR-MAIOR-IGUAL
               WHEN @PREFIX-P-BLOCO-SEGUINTE
                   PERFORM 2220-FETCH-CURSOR-MAIOR
               WHEN @PREFIX-P-BLOCO-ANTERIOR
                   PERFORM 2230-FETCH-CURSOR-MENOR
               WHEN @PREFIX-P-ULTIMO-BLOCO
                   PERFORM 2240-FETCH-CURSOR-MENOR-IGUAL
               WHEN OTHER
                   MOVE 16      TO IMAGW00C-COD-RETORNO  OF LNK-IMAG4XXC
                   MOVE 16      TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
                   MOVE '0050'  TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
                   MOVE '@ERROLIV'
                                TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
                   SET  ERRO-LIVRE     TO TRUE
                   PERFORM 91000-API-ERROR
           END-EVALUATE.
      *----------------------------------------------------------------*
       2200-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2210-FETCH-CURSOR-MAIOR-IGUAL   SECTION.
      *----------------------------------------------------------------*
           MOVE '2210-FETCH-CURSOR-MAIOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL FETCH CSR01-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0051'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-FETCH   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2210-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2220-FETCH-CURSOR-MAIOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2220-FETCH-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL FETCH CSR02-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0052'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-FETCH   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2220-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2230-FETCH-CURSOR-MENOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2230-FETCH-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL FETCH CSR03-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0053'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-FETCH   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2230-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2240-FETCH-CURSOR-MENOR-IGUAL   SECTION.
      *----------------------------------------------------------------*
           MOVE '2240-FETCH-CURSOR-MENOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL FETCH CSR04-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0054'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-FETCH   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2240-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-MOVE-@DCLGEN-TO-@BOOKC        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-MOVE-@DCLGEN-TO-@BOOKC' TO WRK-PARAGRAFO.

           @VALORIZAR-BOOK

      *----------------------------------------------------------------*
       2300-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2400-CLOSE-CURSOR               SECTION.
      *----------------------------------------------------------------*
           MOVE '2400-CLOSE-CURSOR' TO WRK-PARAGRAFO.

           EVALUATE TRUE
               WHEN @PREFIX-P-CONSULTA-INICIAL
               WHEN @PREFIX-P-PRIMEIRO-BLOCO
                   PERFORM 2410-CLOSE-CURSOR-MAIOR-IGUAL
               WHEN @PREFIX-P-BLOCO-SEGUINTE
                   PERFORM 2420-CLOSE-CURSOR-MAIOR
               WHEN @PREFIX-P-BLOCO-ANTERIOR
                   PERFORM 2430-CLOSE-CURSOR-MENOR
               WHEN @PREFIX-P-ULTIMO-BLOCO
                   PERFORM 2440-CLOSE-CURSOR-MENOR-IGUAL
               WHEN OTHER
                   MOVE 16      TO IMAGW00C-COD-RETORNO  OF LNK-IMAG4XXC
                   MOVE 16      TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
                   MOVE '0055'  TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
                   MOVE '@ERROLIV'
                                TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
                   SET  ERRO-LIVRE     TO TRUE
                   PERFORM 91000-API-ERROR
           END-EVALUATE.

      *----------------------------------------------------------------*
       2400-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2410-CLOSE-CURSOR-MAIOR-IGUAL   SECTION.
      *----------------------------------------------------------------*
           MOVE '2410-CLOSE-CURSOR-MAIOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL CLOSE CSR01-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0056'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-CLOSE   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2410-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2420-CLOSE-CURSOR-MAIOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2420-CLOSE-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL CLOSE CSR02-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0057'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-CLOSE   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2420-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2430-CLOSE-CURSOR-MENOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2430-CLOSE-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL CLOSE CSR03-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0058'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-CLOSE   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2430-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2440-CLOSE-CURSOR-MENOR-IGUAL   SECTION.
      *----------------------------------------------------------------*
           MOVE '2440-CLOSE-CURSOR-MENOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL CLOSE CSR04-@DCLGEN
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0059'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-CLOSE   TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       2440-99-EXIT. EXIT.
      *----------------------------------------------------------------*

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
       END PROGRAM @APPLID4@PGMIDI.
