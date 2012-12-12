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
      *    I#GLOG01 - AREA DO GLOG1001                                 *
      *----------------------------------------------------------------*
      *    MODULOS.............:                                       *
      *    GLOG1001 - AREA COMUNICACAO API GLOG - BOOK I#GLOG01        *
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
       77  WRK-INVOKINGPROG            PIC  X(008) VALUE SPACES.
       77  WRK-CURRENT-TIMESTAMP       PIC  X(026) VALUE SPACES.
       01  WRK-RASTREABILIDADE.
           03  WRK-PROGRAM             PIC  X(008) VALUE '@APPLID4@PGMIDI'.
           03  WRK-TABELA              PIC  X(018) VALUE
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
           MOVE '1000-INICIAR'   TO WRK-PARAGRAFO.
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
           MOVE '2000-PROCESSAR'   TO WRK-PARAGRAFO.
           PERFORM 2100-INSERIR-@ENTIDADE.
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-INSERIR-@ENTIDADE          SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-INSERIR-@ENTIDADE' TO WRK-PARAGRAFO.

           EXEC SQL SELECT VALUE(MAX(@COLPK), 0) + 1
                      INTO :@DCLGEN.@COLPKCBL
                      FROM DB2PRD.@TABLENAME
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0044'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
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

           EXEC SQL SET :WRK-CURRENT-TIMESTAMP = CURRENT_TIMESTAMP
           END-EXEC.

           @VALORIZAR-DCLGEN

           EXEC SQL INSERT INTO DB2PRD.@TABLENAME
                     )
           END-EXEC.

           IF SQLCODE NOT EQUAL TO ZEROS
              MOVE '16'        TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID4@PGMIDI
              MOVE '0045'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID4@PGMIDI
              MOVE '@ERRODB2'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI
              SET  ERRO-DB2    TO TRUE
              MOVE WRK-TABELA  TO FRWKGDB2-NOME-TABELA
              SET  DB2-INSERT  TO TRUE
              MOVE SPACES      TO FRWKGDB2-STORED-PROC
              MOVE SPACES      TO FRWKGDB2-LOCAL
              MOVE SQLCA       TO FRWKGDB2-SQLCA
              MOVE SQLCODE     TO FRWKGDB2-SQLCODE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE '@MSGSUCESSO'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID4@PGMIDI.
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
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
