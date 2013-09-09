      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*

       PROGRAM-ID. GOTF2DSS.
       AUTHOR.     HOMI.

      *================================================================*
      *                 S O N D A - P R O C W O R K                    *
      *----------------------------------------------------------------*
      *    PROGRAMA....:  GOTF2DSS                                     *
      *    PROGRAMADOR.:  HOMI                              -  SONDA   *
      *    ANALISTA....:  XXXXXXXXXXXXXXXX                  -  SONDA   *
      *    DATA........:  MAIO/2012                                    *
      *----------------------------------------------------------------*
      *    ARQUIVOS....:                                               *
      *                DDNAME           I/O           INCLUDE/BOOK     *
      *                GOTF001E          I              GOTFW00S       *
      *----------------------------------------------------------------*
      *    BOOK'S......:                                               *
      *    GOTFW00S - BOOK DE ENTRADA - DADOS PARA AGENDAMENTO EVENTO  *
      *    I#FRWKGE - GRAVAR LOG DE ERRO P/ BATCH                      *
      *    I#FRWKAR - BOOK PARA TRATAMENTO DE ERROS DE ARQUIVOS        *
      *    I#FRWKLI - AREA PARA FORMATACAO DE ERRO LIVRE               *
      *    I#FRWKMD - AREA PARA FORMATACAO DE ERRO DE MODULO           *
      *    I#CKRS04 - BOOK DE CONEXAO DB2                              *
      *----------------------------------------------------------------*
      *    BCO DE DADOS:                                               *
      *                TABLE                          INCLUDE/BOOK     *
      *                DB2PRD.TCTRL_RECPC_TARIF         GOTFB072       *
      *                DB2PRD.TREGRA_EVNTO_TARIF        GOTFB0B1       *
      *----------------------------------------------------------------*
      *    MODULOS.....:                                               *
      *    CKRS1000 - MODULO PARA INDICAR PROCESSAMWENTO               *
      *    CKRS0105 - MODULO PARA INICIAR E FINALIZAR CONEXAO DB2      *
      *    CKRS0100 - REALIZAR CONEXAO DB2 E TRATAMENTO COMMIT/RESTART *
      *    FRWK2999 - GRAVAR LOG DE ERRO P/ BATCH                      *
      *    BRAD0450 - ROTINA DE ABEND                                  *
      *================================================================*

      *================================================================*
       ENVIRONMENT                     DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       CONFIGURATION                   SECTION.
      *----------------------------------------------------------------*

       SPECIAL-NAMES.
           DECIMAL-POINT               IS   COMMA.

      *----------------------------------------------------------------*
       INPUT-OUTPUT                    SECTION.
      *----------------------------------------------------------------*

       FILE-CONTROL.

           SELECT GOTF001E ASSIGN      TO   UT-S-GOTF001E
                      FILE STATUS      IS   WRK-FS-GOTF001E.

      *================================================================*
       DATA                            DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       FILE                            SECTION.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
      *   INPUT: GOTF001E - DADOS PARA INSERIR TABELA GOTFB0B7         *
      *            ORG. SEQUENCIAL     -   LRECL   =  355              *
      *----------------------------------------------------------------*
       FD  GOTF001E
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-GOTF001E                 PIC  X(355).

      *----------------------------------------------------------------*
       WORKING-STORAGE                 SECTION.
      *----------------------------------------------------------------*

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(50)  VALUE
           '*** INICIO DA WORKING-STORAGE SECTION         ****'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE COMUNICACAO COM CKRS0105           ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       77  WRK-CKRS0105                PIC  X(08)  VALUE  'CKRS0105'.

           COPY 'I#CKRS04'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE COMUNICACAO COM CKRS0100 ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-CKRS0100                PIC  X(08)  VALUE 'CKRS0100'.
       COPY 'I#CKRS01'.

       01  WRK-AREA-RESTART.
           05  WRK-RST-LIDOS-GOTF001E  PIC  9(009)         VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE AUXILIARES                         ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-VALOR-COBR-TARIF        PIC S9(15)V99 COMP-3 VALUE ZEROS.
       01  FILLER      REDEFINES       WRK-VALOR-COBR-TARIF.
         05  WRK-VAL-COBR-TARIF        PIC  9(02).
         05  WRK-VCALCD-COBR-TARIF     PIC  9(13)V99.

       01  WRK-SQLCODE-AUX             PIC S9(09)  VALUE ZEROS.
       01  FILLER                      REDEFINES   WRK-SQLCODE-AUX.
         05  FILLER                    PIC  9(06).
         05  WRK-SQLCODE-9-3           PIC S9(03).

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)         VALUE
           '*** AREA DE CHAVES                             ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE ACUMULADORES                       ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-ACUMULADORES.
         05  WRK-LIDOS-GOTF001E        PIC  9(09)  COMP-3  VALUE ZEROS.
         05  WRK-INSER-GOTFB0B7        PIC  9(09)  COMP-3  VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE TESTE DE FILE-STATUS               ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FS-GOTF001E             PIC  X(02)  VALUE SPACES.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DE ENTRADA GOTF001E                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       COPY GOTFW00S.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DO FRWK2999                           ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FRWK2999                PIC  X(08)  VALUE
           'FRWK2999'.

       01  WRK-AREA-ERRO.
           COPY 'I#FRWKGE'.
           05  WRK-BLOCO-INFO-ERRO.
             10 WRK-CHAR-INFO-ERRO     PIC  X(01) OCCURS 0 TO 30000
                                       TIMES DEPENDING ON
                                       FRWKGHEA-TAM-DADOS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA P/ FORMATACAO DE ERRO DE ARQUIVO      ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-ERRO-ARQUIVO.
           COPY 'I#FRWKAR'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA P/ FORMATACAO DE ERRO DE LIVRE        ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-ERRO-LIVRE.
           COPY 'I#FRWKLI'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA P/ FORMATACAO DE ERRO DE DB2          ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-ERRO-DB2.
           COPY 'I#FRWKDB'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA P/ FORMATACAO DE ERRO DE MODULO       ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-ERRO-MODULO.
           COPY 'I#FRWKMD'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DA BRAD0450                           ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-BRAD0450.
         05  WRK-0450-ABEND-BAT        PIC S9(04)  COMP    VALUE +1111.
         05  WRK-0450-DUMP-BAT         PIC  X(01)  VALUE 'S'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** AREA DA TABELA DB2                         ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

           EXEC SQL
               INCLUDE SQLCA
           END-EXEC.

           EXEC SQL
               INCLUDE GOTFB0B7
           END-EXEC.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(50)  VALUE
           '*** FIM DA WORKING-STORAGE SECTION             ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

      *================================================================*
       PROCEDURE                       DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       0000-ROTINA-PRINCIPAL           SECTION.
      *----------------------------------------------------------------*

           MOVE '0000-ROTINA-PRINCIPAL' TO      FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 1000-INICIAR.

           PERFORM 2000-VERIFICAR-VAZIO.

           PERFORM 3000-PROCESSAR
             UNTIL WRK-FS-GOTF001E      EQUAL   '10'

           PERFORM 9000-FINALIZAR.

      *----------------------------------------------------------------*
       0000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1000-INICIAR                    SECTION.
      *----------------------------------------------------------------*

           MOVE '1000-INICIAR'          TO      FRWKGHEA-IDEN-PARAGRAFO.

           CALL 'CKRS1000'.

           PERFORM 7000-INICIAR-CKRS0105.

           INITIALIZE FRWKGHEA-REGISTRO
                      FRWKGARQ-REGISTRO
                      FRWKGDB2-REGISTRO.

           OPEN INPUT   GOTF001E.

           PERFORM 1100-TESTAR-FILE-STATUS.

      *----------------------------------------------------------------*
       1000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-TESTAR-FILE-STATUS         SECTION.
      *----------------------------------------------------------------*

           MOVE '1100-TESTAR-FILE-STATUS' TO    FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 1110-TESTAR-FS-GOTF001E.

      *----------------------------------------------------------------*
       1100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1110-TESTAR-FS-GOTF001E         SECTION.
      *----------------------------------------------------------------*

           MOVE '1110-TESTAR-FS-GOTF001E' TO    FRWKGHEA-IDEN-PARAGRAFO.

           IF WRK-FS-GOTF001E       NOT EQUAL   '00'
              MOVE 'GOTF001E'           TO      FRWKGARQ-NOME-ARQUIVO
              MOVE WRK-FS-GOTF001E      TO      FRWKGARQ-FILE-STATUS
              PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-VERIFICAR-VAZIO            SECTION.
      *----------------------------------------------------------------*

           MOVE '2000-VERIFICAR-VAZIO'  TO      FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 2100-LER-GOTF001E.

           IF (WRK-LIDOS-GOTF001E       EQUAL   ZEROS)
              DISPLAY '************ GOTF2DSS ************'
              DISPLAY '*                                *'
              DISPLAY '*     ARQUIVO GOTF001E VAZIO     *'
              DISPLAY '*       PROGRAMA ENCERRADO       *'
              DISPLAY '*                                *'
              DISPLAY '************ GOTF2DSS ************'
              PERFORM 9000-FINALIZAR
           END-IF.

      *----------------------------------------------------------------*
       2000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-LER-GOTF001E               SECTION.
      *----------------------------------------------------------------*

           MOVE '2100-LER-GOTF001E'     TO      FRWKGHEA-IDEN-PARAGRAFO.

           READ GOTF001E                INTO    GOTFW00S-REGISTRO.

           IF WRK-FS-GOTF001E           EQUAL   '10'
              NEXT SENTENCE
           ELSE
              PERFORM 1110-TESTAR-FS-GOTF001E
              ADD     1              TO      WRK-LIDOS-GOTF001E
           END-IF.

      *----------------------------------------------------------------*
       2100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*

           MOVE '3000-PROCESSAR-SALARIO'
                                        TO      FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 5000-INSERIR-GOTFB0B7.

           PERFORM 2100-LER-GOTF001E.

      *----------------------------------------------------------------*
       3000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       5000-INSERIR-GOTFB0B7           SECTION.
      *----------------------------------------------------------------*

           MOVE '5000-INSERIR-GOTFB0B7' TO      FRWKGHEA-IDEN-PARAGRAFO.

           INITIALIZE            GOTFB0B7.

           MOVE CSIST-ORIGE-TARIF
                                        TO
                                        CSIST-ORIGE-TARIF  OF GOTFB0B7.
           MOVE DRECEB-MOVTO-TARIF
                                        TO
                                        DRECEB-MOVTO-TARIF OF GOTFB0B7.
           MOVE NMOVTO-EVNTO-TARIF
                                        TO
                                        NMOVTO-EVNTO-TARIF OF GOTFB0B7.

           MOVE HSIT-OPER-REALZ         TO
                                        HSIT-OPER-REALZ    OF GOTFB0B7.

           MOVE CSIT-OPER-REALZ         TO
                                        CSIT-OPER-REALZ    OF GOTFB0B7.

           MOVE CUSUAR-MOVTO-EVNTO      TO
                                        CUSUAR-MOVTO-EVNTO OF GOTFB0B7

           MOVE RJUSTF-EVNTO-TARIF      TO
                                        RJUSTF-EVNTO-TARIF OF GOTFB0B7.

           EXEC SQL
             INSERT INTO DB2PRD.TSIT_MOVTO_TARIF
                   (CSIST_ORIGE_TARIF  ,
                    DRECEB_MOVTO_TARIF ,
                    NMOVTO_EVNTO_TARIF ,
                    HSIT_OPER_REALZ    ,
                    CSIT_OPER_REALZ    ,
                    CUSUAR_MOVTO_EVNTO ,
                    RJUSTF_EVNTO_TARIF)
               VALUES
                   (:GOTFB0B7.CSIST-ORIGE-TARIF  ,
                    :GOTFB0B7.DRECEB-MOVTO-TARIF ,
                    :GOTFB0B7.NMOVTO-EVNTO-TARIF ,
                    :GOTFB0B7.HSIT-OPER-REALZ    ,
                    :GOTFB0B7.CSIT-OPER-REALZ    ,
                    :GOTFB0B7.CUSUAR-MOVTO-EVNTO ,
                    :GOTFB0B7.RJUSTF-EVNTO-TARIF)
           END-EXEC.

           IF (SQLCODE              NOT EQUAL   ZEROS)  OR
              (SQLWARN0                 EQUAL   'W')
              MOVE 'TSIT_MOVTO_TARIF'   TO      FRWKGDB2-NOME-TABELA
              SET DB2-UPDATE            TO      TRUE
              MOVE '0020'               TO      FRWKGDB2-LOCAL
              PERFORM 9200-TRATAR-ERRO-DB2
           END-IF.

           ADD 1                        TO      WRK-INSER-GOTFB0B7.

      *----------------------------------------------------------------*
       5000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       7000-INICIAR-CKRS0105           SECTION.
      *----------------------------------------------------------------*

           MOVE '7000-INICIAR-CKRS0105' TO FRWKGHEA-IDEN-PARAGRAFO.

           MOVE 'C'                    TO PARM-OP.
           MOVE 'DB2'                  TO PARM-SSID.
           MOVE SPACES                 TO PARM-PLAN.

           CALL WRK-CKRS0105           USING PARM-CKRS0105.

      *----------------------------------------------------------------*
       7000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       7100-ENCERRAR-CKRS0105          SECTION.
      *----------------------------------------------------------------*

           MOVE '7100-ENCERRAR-CKRS0105' TO FRWKGHEA-IDEN-PARAGRAFO.

           MOVE 'D'                    TO PARM-OP.
           MOVE SPACES                 TO PARM-PLAN.

           CALL WRK-CKRS0105           USING PARM-CKRS0105.

      *----------------------------------------------------------------*
       7100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
      *
           MOVE '9000-FINALIZAR'        TO      FRWKGHEA-IDEN-PARAGRAFO.
      *
           DISPLAY '*********** GOTF2DSS ***********'
           DISPLAY '*                              *'
           DISPLAY '*     RESUMO PROCESSAMENTO     *'
           DISPLAY '* ---------------------------- *'
           DISPLAY '* LIDOS    GOTF001E : ' WRK-LIDOS-GOTF001E
           DISPLAY '*                              *'
           DISPLAY '* INSERE   GOTFB0B7 : ' WRK-INSER-GOTFB0B7
           DISPLAY '*                              *'
           DISPLAY '*********** GOTF2DSS ***********'

           PERFORM  7100-ENCERRAR-CKRS0105.

           CLOSE GOTF001E.

           PERFORM 1100-TESTAR-FILE-STATUS.

           STOP RUN.

      *----------------------------------------------------------------*
       9000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9100-FORMATAR-ERRO-ARQUIVO      SECTION.
      *----------------------------------------------------------------*

           SET  ERRO-ARQUIVO            TO      TRUE.

           MOVE FRWKGARQ-TAM-LAYOUT     TO      FRWKGHEA-TAM-DADOS.
           MOVE WRK-AREA-ERRO-ARQUIVO   TO      WRK-BLOCO-INFO-ERRO
                                                (1:FRWKGHEA-TAM-DADOS).

           PERFORM 9900-TRATAR-ERRO.

      *----------------------------------------------------------------*
       9100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9200-TRATAR-ERRO-DB2            SECTION.
      *----------------------------------------------------------------*

           SET  ERRO-DB2                TO      TRUE.

           MOVE FRWKGDB2-TAM-LAYOUT     TO      FRWKGHEA-TAM-DADOS.
           MOVE FRWKGHEA-IDEN-PARAGRAFO(1:16)
                                        TO      FRWKGDB2-LOCAL.
           MOVE SQLSTATE                TO      FRWKGDB2-SQLSTATE.
           MOVE SQLCA                   TO      FRWKGDB2-SQLCA.
           MOVE SQLCODE                 TO      WRK-SQLCODE-AUX.
           MOVE WRK-SQLCODE-9-3         TO      FRWKGDB2-SQLCODE2.
           MOVE WRK-AREA-ERRO-DB2       TO      WRK-BLOCO-INFO-ERRO
                                                (1:FRWKGHEA-TAM-DADOS).

           PERFORM 9900-TRATAR-ERRO.

      *----------------------------------------------------------------
       9200-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9300-TRATAR-ERRO-MODULO         SECTION.
      *----------------------------------------------------------------*

           SET ERRO-MODULO              TO      TRUE.

           MOVE FRWKGMOD-TAM-LAYOUT     TO      FRWKGHEA-TAM-DADOS.
           MOVE WRK-AREA-ERRO-MODULO    TO      WRK-BLOCO-INFO-ERRO
                                                (1:FRWKGHEA-TAM-DADOS).

           DISPLAY ' '.
           DISPLAY 'FRWKGMOD-NOME-MODULO   = ' FRWKGMOD-NOME-MODULO.
           DISPLAY 'FRWKGMOD-COD-RETORNO   = ' FRWKGMOD-COD-RETORNO.
           DISPLAY 'FRWKGMOD-COD-ERRO      = ' FRWKGMOD-COD-ERRO.
           DISPLAY 'FRWKGMOD-COD-MENSAGEM  = ' FRWKGMOD-COD-MENSAGEM.

           PERFORM 9900-TRATAR-ERRO.

      *----------------------------------------------------------------*
       9300-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9900-TRATAR-ERRO                SECTION.
      *----------------------------------------------------------------*

           MOVE 'GOTF2DSS'              TO      FRWKGHEA-NOME-PROGRAMA.

           PERFORM 9990-GRAVAR-LOG-ERRO.

           PERFORM 9999-ABENDAR-PROGRAMA.

           GOBACK.

      *----------------------------------------------------------------*
       9900-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9990-GRAVAR-LOG-ERRO            SECTION.
      *----------------------------------------------------------------*

           CALL WRK-FRWK2999            USING   WRK-AREA-ERRO.

      *----------------------------------------------------------------*
       9990-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9999-ABENDAR-PROGRAMA           SECTION.
      *----------------------------------------------------------------*

           DISPLAY '*** BRAD0450 CHAMADO PARA ABENDAR O PROGRAMA ***'.
           DISPLAY ' '.

           CALL 'BRAD0450'             USING    WRK-0450-ABEND-BAT
                                                WRK-0450-DUMP-BAT.

      *----------------------------------------------------------------*
       9999-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
      *================================================================*
