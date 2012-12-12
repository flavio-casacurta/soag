      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID3@PGMIDI.
       AUTHOR.     @AUTHOR
      *================================================================*
      *                 @CONTRATANTE
      *----------------------------------------------------------------*
      *                                                                *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID3@PGMIDI
      *    PROGRAMADOR     : @AUTHOR
      *    ANALISTA        : @ANALISTA
      *    GRUPO           : @GRUPO
      *    DATA DE CRIACAO : @DATE
      *                                                                *
      *----------------------------------------------------------------*
      *    OBJETIVO....: MODULO FUNCIONAL                              *
      *                  @SERVICO @ENTIDADE1
      *                  @ENTIDADE2
      *----------------------------------------------------------------*
      *    BOOKS FUNCIONAIS...:                                        *
      *    @APPLIDW00C - BOOK CONTROLE - COMUNICACAO ENTRE MODULOS
      *    @BOOKI - BOOK COMUNICACAO DESTE MODULO
      *    @BOOKC - BOOK COMUNICACAO COM A PERSISTENCIA @APPLID4@PGMIDI
      *    @APPLIDW10W - BOOK DE WORK DO PROGRAMA
      *    @APPLIDW01W - BOOK DE WORK PARA TRATAMENTO DE ERROS
      *    @APPLIDW11P - BOOK DE PROCEDUR PARA TRATAMENTO DE ERROS
      *----------------------------------------------------------------*
      *    BOOKS DA ARQUITETURA:                                       *
      *    I#FRWKGE - COMMAREA FRWK1999 - LOG DE ERRO                  *
      *    I#FRWKDB - AREA DO FRWK1999  - LOG DE ERROS DB2             *
      *    I#FRWKCI - AREA DO FRWK1999  - LOG DE ERROS CICS            *
      *    I#FRWKMD - AREA DO FRWK1999  - LOG DE ERROS MODULO          *
      *    I#FRWKLI - AREA DO FRWK1999  - LOG DE ERROS LIVRE           *
      *----------------------------------------------------------------*
      *    MODULOS.............:                                       *
      *    @APPLID4@PGMIDI - MODULO PERSISTENCIA
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
       77  WRK-PROGRAM                 PIC  X(008) VALUE '@APPLID3@PGMIDI'.
       77  WRK-INVOKINGPROG            PIC  X(008) VALUE SPACES.
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREA DE ACESSO PERSISTENCIA *'.
      *----------------------------------------------------------------*
       01  WRK-@APPLID4@PGMIDI.
           COPY @APPLIDW00C.
           COPY @BOOKC.
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREAS DE WORKING GENERICAS*'.
      *----------------------------------------------------------------*
       COPY @APPLIDW10W.
       COPY @APPLIDW01W.
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           02  LNK-@APPLID3@PGMIDI.
           COPY @APPLIDW00C.
           COPY @BOOKI.
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
           INITIALIZE  FRWKGHEA-REGISTRO
                       FRWKGCIC-REGISTRO
                       FRWKGMOD-REGISTRO
                       FRWKGLIV-REGISTRO
                       @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDI.

           IF EIBCALEN EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '0031'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           EXEC CICS ASSIGN INVOKINGPROG (WRK-INVOKINGPROG)
                     NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '0032'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS           TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           IF WRK-INVOKINGPROG(1:4) NOT EQUAL TO '@APPLID'
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@PGMIDI
              MOVE '0033'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROLIV'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-LIVRE          TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

      *----------------------------------------------------------------*
       1000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE    '2000-PROCESSAR' TO WRK-PARAGRAFO.
           PERFORM 2100-CONSISTIR-DADOS.
           PERFORM 2200-ALIMENTAR-PERSISTENCIA.
           PERFORM 2300-CHAMAR-PERSISTENCIA.
           PERFORM 2900-DEVOLVER-DADOS.
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-CONSISTIR-DADOS            SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-CONSISTIR-DADOS'     TO WRK-PARAGRAFO.
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-ALIMENTAR-PERSISTENCIA     SECTION.
      *----------------------------------------------------------------*
           MOVE '2200-ALIMENTAR-PERSISTENCIA' TO WRK-PARAGRAFO.
           MOVE @BOOKI-REGISTRO TO @BOOKC-REGISTRO.
      *----------------------------------------------------------------*
      *    DADOS DA SESSAO
      *----------------------------------------------------------------*
           MOVE @BOOKI-EMPRESA-OPER       TO @BOOKC-EMPRESA-OPER.
           MOVE @BOOKI-DEPENDENCIA-OPER   TO @BOOKC-DEPENDENCIA-OPER
           MOVE @BOOKI-CCANAL             TO @BOOKC-CCANAL.
           MOVE @BOOKI-TIPO-USUAR         TO @BOOKC-TIPO-USUAR.
           MOVE @BOOKI-CAUTEN-SEGRC       TO @BOOKC-CAUTEN-SEGRC.
           MOVE @BOOKI-TIPO-USUAR-AUTORIZ TO
                                            @BOOKC-TIPO-USUAR-AUTORIZ.
           MOVE @BOOKI-USUARIO-AUTORIZ    TO @BOOKC-USUARIO-AUTORIZ.
           MOVE @BOOKI-NOPER-FLUXO        TO @BOOKC-NOPER-FLUXO.
      *----------------------------------------------------------------*
       2200-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-CHAMAR-PERSISTENCIA        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-CHAMAR-PERSISTENCIA' TO WRK-PARAGRAFO.
           INITIALIZE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@PGMIDI
           MOVE '@APPLID4@PGMIDI'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@APPLID4@PGMIDI)
                                       LENGTH  (LENGTH OF WRK-@APPLID4@PGMIDI)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI
              MOVE 'ER34'     TO @APPLIDW00C-COD-ERRO OF LNK-@APPLID3@PGMIDI
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           IF @APPLIDW00C-COD-RETORNO OF WRK-@APPLID4@PGMIDI NOT EQUAL TO ZEROS
              MOVE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@PGMIDI
                TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDI
              MOVE @APPLIDW00C-COD-RETORNO   OF LNK-@APPLID3@PGMIDI
                TO FRWKGMOD-COD-RETORNO
              SET ERRO-MODULO TO TRUE

              PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2300-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2900-DEVOLVER-DADOS             SECTION.
      *----------------------------------------------------------------*
           MOVE '2900-DEVOLVER-DADOS' TO WRK-PARAGRAFO.
           MOVE '@MSGSUCESSO' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDI.
           MOVE @BOOKC-REGISTRO TO @BOOKI-REGISTRO.
      *----------------------------------------------------------------*
       2900-99-EXIT. EXIT.
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
       END PROGRAM @APPLID3@PGMIDI.
