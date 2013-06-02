      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID3@SIGLAPGM@TYPEPGM.
       AUTHOR.     @AUTHOR
      *================================================================*
      *@CONTRATANTE
      *----------------------------------------------------------------*
      *                                                                *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID3@SIGLAPGM@TYPEPGM
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
      *    @APPLIDW@SIGLAPGMI - BOOK COMUNICACAO DESTE MODULO
      *    @APPLIDW@SIGLAPGMC - BOOK COMUNICACAO COM A PERSISTENCIA @APPLID4@SIGLAPGM@PERSISTENCIA
@REMBOOKFUNCIONAIS
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
@REMBOOKARQUITETUR
      *----------------------------------------------------------------*
      *    MODULOS.............:                                       *
      *    @APPLID4@SIGLAPGM@PERSISTENCIA - MODULO PERSISTENCIA
@REMMODLFUNCIONAIS
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
       77  WRK-PROGRAM                 PIC  X(008) VALUE '@APPLID3@SIGLAPGM@TYPEPGM'.
@WRKINVOKINGPROG
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREA DE ACESSO PERSISTENCIA *'.
      *----------------------------------------------------------------*
       01  WRK-@APPLID4@SIGLAPGM@PERSISTENCIA.
           COPY @APPLIDW00C.
           COPY @APPLIDW@SIGLAPGMC.
      *----------------------------------------------------------------*
@WORKINGFUNCIONAIS
       01  FILLER                      PIC  X(050)         VALUE
           '* AREAS DE WORKING GENERICAS*'.
      *----------------------------------------------------------------*
       COPY @APPLIDW10W.
       COPY @APPLIDW01W.
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           02  LNK-@APPLID3@SIGLAPGM@TYPEPGM.
           COPY @APPLIDW00C.
           COPY @APPLIDW@SIGLAPGMI.
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
                       @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM.

           IF EIBCALEN EQUAL TO ZEROS
              MOVE 16          TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '0031'      TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '@ERROCICS'  TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.
@INVOKINGPROG

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
@CONSISTIRDADOS
@CHAMARFUNCIONAIS
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-ALIMENTAR-PERSISTENCIA     SECTION.
      *----------------------------------------------------------------*
           MOVE '2200-ALIMENTAR-PERSISTENCIA' TO WRK-PARAGRAFO.
           MOVE @APPLIDW@SIGLAPGMI-REGISTRO TO @APPLIDW@SIGLAPGMC-REGISTRO.
@GLOG
      *----------------------------------------------------------------*
       2200-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-CHAMAR-PERSISTENCIA        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-CHAMAR-PERSISTENCIA' TO WRK-PARAGRAFO.
           INITIALIZE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@SIGLAPGM@PERSISTENCIA
           MOVE '@APPLID4@SIGLAPGM@PERSISTENCIA'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@APPLID4@SIGLAPGM@PERSISTENCIA)
                                       LENGTH  (LENGTH OF WRK-@APPLID4@SIGLAPGM@PERSISTENCIA)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16         TO @APPLIDW00C-COD-RETORNO  OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '0034'     TO @APPLIDW00C-COD-ERRO     OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              MOVE '@ERROCICS' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID4@SIGLAPGM@PERSISTENCIA
             TO @APPLIDW00C-BLOCO-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM.
           IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM GREATER THAN 1
              IF @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM GREATER THAN 8
                 MOVE @APPLIDW00C-COD-RETORNO OF LNK-@APPLID3@SIGLAPGM@TYPEPGM
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
@MODULOSFUNCIONAIS

      *----------------------------------------------------------------*
       2900-DEVOLVER-DADOS             SECTION.
      *----------------------------------------------------------------*
           MOVE '2900-DEVOLVER-DADOS' TO WRK-PARAGRAFO.
           MOVE '@MSGSUCESSO' TO @APPLIDW00C-COD-MENSAGEM OF LNK-@APPLID3@SIGLAPGM@TYPEPGM.
           MOVE @APPLIDW@SIGLAPGMC-REGISTRO TO @APPLIDW@SIGLAPGMI-REGISTRO.
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
       END PROGRAM @APPLID3@SIGLAPGM@TYPEPGM.
