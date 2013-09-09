      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID3@PGMIDL.
       AUTHOR.     @AUTHOR
      *================================================================*
      *                 @CONTRATANTE
      *----------------------------------------------------------------*
      *                                                                *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID3@PGMIDL
      *    PROGRAMADOR     : @AUTHOR
      *    ANALISTA        : @ANALISTA
      *    DATA DE CRIACAO : @DATE
      *                                                                *
      *----------------------------------------------------------------*
      *    OBJETIVO....: MODULO FUNCIONAL                              *
      *                  @SERVICO @ENTIDADE
      *----------------------------------------------------------------*
      *    BOOKS FUNCIONAIS...:                                        *
      *    @APPLIDW00C - BOOK CONTROLE - COMUNICACAO ENTRE MODULOS
      *    @BOOKI - BOOK COMUNICACAO DESTE MODULO
      *    @BOOKC - BOOK COMUNICACAO COM A PERSISTENCIA @APPLID4@PGMIDS
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
      *    @APPLID4@PGMIDS - MODULO PERSISTENCIA
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
       77  WRK-PROGRAM                 PIC  X(008) VALUE '@APPLID3@PGMIDL'.
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREA DE ACESSO PERSISTENCIA *'.
      *----------------------------------------------------------------*
       01  WRK-@APPLID4@PGMIDS.
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
           02  LNK-@APPLID3@PGMIDL.
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
                       @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDL.

           IF EIBCALEN EQUAL TO ZEROS
              MOVE 16         TO @APPLIDW00C-COD-RETORNO
              MOVE 'ER01'     TO @APPLIDW00C-COD-ERRO
              MOVE '@APPLID9999' TO @APPLIDW00C-COD-MENSAGEM
              SET ERRO-CICS TO TRUE
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
           PERFORM 2400-DEVOLVER-DADOS.
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
           MOVE @BOOKI-REGISTRO     TO @BOOKC-REGISTRO.
 >>>>>>    IF @BOOKI-P-BLOCO-ANTERIOR
           ELSE
           END-IF.
       2200-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-CHAMAR-PERSISTENCIA        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-CHAMAR-PERSISTENCIA' TO WRK-PARAGRAFO.
           INITIALIZE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@PGMIDS.
           MOVE '@APPLID4@PGMIDS'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@APPLID4@PGMIDS)
                                       LENGTH  (LENGTH OF WRK-@APPLID4@PGMIDS)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDL
              MOVE 'ER01'     TO @APPLIDW00C-COD-ERRO OF LNK-@APPLID3@PGMIDL
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@PGMIDL
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@PGMIDS
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@PGMIDL.
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDL GREATER THAN 1
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDL GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@PGMIDI
                   TO FRWKGMOD-COD-RETORNO
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
              ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------*
       2300-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2400-DEVOLVER-DADOS             SECTION.
      *----------------------------------------------------------------*
           MOVE '2400-DEVOLVER-DADOS' TO WRK-PARAGRAFO.
           MOVE @BOOKC-REGISTRO TO @BOOKI-REGISTRO.
      *----------------------------------------------------------------*
       2400-99-EXIT. EXIT.
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
       END PROGRAM @APPLID3@PGMIDL.
