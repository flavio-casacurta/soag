      *----------------------------------------------------------
       IDENTIFICATION  DIVISION.
      *----------------------------------------------------------
       PROGRAM-ID. PSVP1095.
      ************************************************************
      * SISTEMA     : BRADESCO VIDA E PREVIDENCIA                *
      * SUBSISTEMA  : PSVP                                       *
      * ANALISTA    : DEBORA CORREA    - ALTRAN                  *
      * DATA        : 22/11/2006                                 *
      * OBJETIVO    : ATUALIZAR SALDO BLOQUEADO NO PRIMEIRO DIA  *
      *               DO ANO, ANTES DA NET PSVP0000              *
      *               - ZERAR VALOR DE ANO ATUAL - 2             *
      ************************************************************
ALTR  *       ANALISTA: THIAGO S RIBEIRO  -  ALTRAN              *
      *       DATA....: 13/04/2007                               *
      *       OBJETIVO: ATUALIZAR VALORES DE SALDO DISPONIVEL E  *
      *                 BLOQUEADO.                               *
      *----------------------------------------------------------*
DE0609*       ANALISTA: DEBORA            - PRIME                *
      *       DATA....: 09/06/2009                               *
      *       OBJETIVO: ACERTO NOS VALORES DE SDO DISPONIVEL E   *
      *                 BLOQUEADO.                               *
      *----------------------------------------------------------*
PR0609*       ANALISTA: THIAGO S RIBEIRO  -  PRIME               *
      *       DATA....: 22/06/2009                               *
      *       OBJETIVO: ATUALIZAR VALORES DE SALDO DISPONIVEL E  *
      *                 BLOQUEADO PARA A PECQB027.               *
      *----------------------------------------------------------*
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT               IS COMMA.

       INPUT-OUTPUT                    SECTION.
       FILE-CONTROL.

       DATA DIVISION.
       FILE SECTION.

      *---------------------------------------------------------------*
       WORKING-STORAGE SECTION.
      *---------------------------------------------------------------*

       01  WRK-FIM                    PIC  X(001) VALUE 'N'.
PR0609 01  WRK-FIM-PECQB027           PIC  X(001) VALUE 'N'.
PR0609 01  WRK-PULAR-MOV-QUOTA        PIC  X(001) VALUE 'N'.
       01  WRK-BATCH                  PIC  X(008) VALUE 'BATCH'.
       01  WRK-CKRS0100               PIC  X(008) VALUE 'CKRS0100'.
       01  WRK-AREA-RESTART.
           05  WRK-LIDOS              PIC  9(009) COMP-3
                                                  VALUE ZEROS.
           05  WRK-CONT               PIC  9(009) COMP-3
                                                  VALUE ZEROS.
           05  WRK-MVQT-NR-MOV-QTA    PIC S9(10)V COMP-3
                                                  VALUE ZEROS.
PR0609     05  WRK-TABELA             PIC  X(008) VALUE SPACES.

      *----------------------------------------------------------------*
       01  FILLER                     PIC  X(050) VALUE
                      '*** AREA PARA BRAD7100 ***'.
      *----------------------------------------------------------------*

       COPY I#BRAD7C.
       COPY I#CKRS01.

      *---------------------------------------------------------------*
      *          DEFINICAO DAS AREAS DE COMUNICACAO DO COBOL X DB2    *
      *---------------------------------------------------------------*

           EXEC SQL INCLUDE SQLCA    END-EXEC.
           EXEC SQL INCLUDE PECQB007 END-EXEC.
PR0609     EXEC SQL INCLUDE PECQB027 END-EXEC.

      *---------------------------------------------------------------*
      *          DEFINICAO DAS AREAS DE 'DECLARE CURSOR'               *
      *---------------------------------------------------------------*

           EXEC SQL DECLARE C1 CURSOR WITH HOLD FOR
                SELECT QBLOQ_MOVTO_ATUAL,
                       QBLOQ_MOVTO_ANTER,
                       QRENTB_ATUAL_EMPR,
                       QRENTB_ANTER_EMPR,
                       MVQT_NR_MOV_QTA
                  FROM DB2PRD.PECQ_MOV_QUOTA
                 WHERE ( QBLOQ_MOVTO_ATUAL > 0 OR
DE0609                   QBLOQ_MOVTO_ANTER > 0 )
                   AND MVQT_NR_MOV_QTA     >= :PECQB007.MVQT-NR-MOV-QTA
DE0609             AND YEAR(MVQT_DT_OCORR) >=  YEAR(CURRENT DATE) - 2
                   FOR UPDATE OF QRENTB_ANTER_EMPR,
                                 QRENTB_ATUAL_EMPR,
                                 QBLOQ_MOVTO_ATUAL,
                                 QBLOQ_MOVTO_ANTER
           END-EXEC.

PR0609     EXEC SQL DECLARE CSR01-PECQB027 CURSOR WITH HOLD FOR
"               SELECT QBLOQ_MOVTO_ATUAL,
"                      QBLOQ_MOVTO_ANTER,
"                      QRENTB_ATUAL_EMPR,
"                      QRENTB_ANTER_EMPR,
"                      NREG_TBELA_ASSOC
"                 FROM DB2PRD.TMOVTC_TRNSF_ASSOC
"                WHERE ( QBLOQ_MOVTO_ATUAL > 0 OR
"                        QBLOQ_MOVTO_ANTER > 0 )
"                  AND NREG_TBELA_ASSOC    >= :PECQB027.NREG-TBELA-ASSOC
"                  AND YEAR(DORIGN_CREDT_CONTB)
"                                          >=  YEAR(CURRENT DATE) - 2
"                  FOR UPDATE OF QRENTB_ANTER_EMPR,
"                                QRENTB_ATUAL_EMPR,
"                                QBLOQ_MOVTO_ATUAL,
"                                QBLOQ_MOVTO_ANTER
PR0609     END-EXEC.

      *===============================================================*
       PROCEDURE DIVISION.
      *===============================================================*
      *----------------------------------------------------------------*
       0000-INICIAR               SECTION.
      *----------------------------------------------------------------*

           PERFORM 1000-INICIO
PR0609     PERFORM 2000-ROTINA-PRINCIPAL
           PERFORM 3000-FINALIZA
           GOBACK.

      *----------------------------------------------------------------*
       0000-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA INICIO                                               *
      ******************************************************************
      *----------------------------------------------------------------*
       1000-INICIO                SECTION.
      *----------------------------------------------------------------*

           INITIALIZE CKRS01-INTERFACE

           MOVE ' '                   TO CK01-PLAN
           MOVE 'DB2'                 TO CK01-ID-DB2
           MOVE 'I'                   TO CK01-FUNCAO
           MOVE WRK-AREA-RESTART      TO CK01-AREA-RESTART

           MOVE  LENGTH OF WRK-AREA-RESTART
                                      TO CK01-TAM-AREA-RESTART

           PERFORM 5000-CHAMADA-CKRS0100

           DISPLAY 'CK01-STATUS  ' CK01-STATUS

           IF CK01-STATUS EQUAL 'REST'
              MOVE CK01-AREA-RESTART(1:CK01-TAM-AREA-RESTART)
                                      TO WRK-AREA-RESTART

PR0609        IF WRK-TABELA EQUAL 'PECQB007'
"                MOVE WRK-MVQT-NR-MOV-QTA
"                                     TO MVQT-NR-MOV-QTA  OF PECQB007
"                MOVE ZEROS           TO NREG-TBELA-ASSOC OF PECQB027
"                MOVE 'N'             TO WRK-PULAR-MOV-QUOTA
"             ELSE
"                MOVE WRK-MVQT-NR-MOV-QTA
"                                     TO NREG-TBELA-ASSOC OF PECQB027
"                MOVE 'S'             TO WRK-PULAR-MOV-QUOTA
"             END-IF
"          ELSE
"             MOVE ZEROS              TO MVQT-NR-MOV-QTA  OF PECQB007
"                                        NREG-TBELA-ASSOC OF PECQB027
PR0609        MOVE 'N'                TO WRK-PULAR-MOV-QUOTA
           END-IF

PR0609*    MOVER WRK-MVQT-NR-MOV-QTA   TO MVQT-NR-MOV-QTA OF PECQB007

PR0609     IF WRK-PULAR-MOV-QUOTA EQUAL 'N'
              PERFORM 1100-OPEN-CURSOR-PECQB007
              PERFORM 2100-FETCH-PECQB007
PR0609     END-IF.

      *----------------------------------------------------------------*
       1000-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA OPEN CURSOR PECQB007                                 *
      ******************************************************************
      *----------------------------------------------------------------*
       1100-OPEN-CURSOR-PECQB007  SECTION.
      *----------------------------------------------------------------*

           EXEC SQL
                OPEN C1
           END-EXEC

           IF (SQLCODE NOT EQUAL ZEROS) OR
              (SQLWARN0    EQUAL 'W')
               MOVE 'DB2'             TO ERR-TIPO-ACESSO
               MOVE ' OPEN '          TO ERR-DBD-TAB
               MOVE 'CURSOR '         TO ERR-FUN-COMANDO
               MOVE SQLCODE           TO ERR-SQL-CODE
               MOVE '0010'            TO ERR-LOCAL
               MOVE SPACES            TO ERR-SEGM
               PERFORM 999-ROTINA-ERRO
           END-IF.

      *----------------------------------------------------------------*
       1100-99-FIM. EXIT.
      *----------------------------------------------------------------*

PR0609******************************************************************
"     *    ROTINA ABRIR CURSOR PECQB027                                *
"     ******************************************************************
"     *----------------------------------------------------------------*
PR0609 1200-OPEN-CURSOR-PECQB027  SECTION.
"     *----------------------------------------------------------------*
"
"          EXEC SQL
"               OPEN CSR01-PECQB027
"          END-EXEC
"
"          IF (SQLCODE NOT EQUAL ZEROS) OR
"             (SQLWARN0    EQUAL 'W')
"              MOVE 'DB2'             TO ERR-TIPO-ACESSO
"              MOVE ' OPEN '          TO ERR-DBD-TAB
"              MOVE 'PECQB027'        TO ERR-FUN-COMANDO
"              MOVE SQLCODE           TO ERR-SQL-CODE
"              MOVE '1200'            TO ERR-LOCAL
"              MOVE SPACES            TO ERR-SEGM
"              PERFORM 999-ROTINA-ERRO
"          END-IF.
"
"     *----------------------------------------------------------------*
PR0609 1200-99-FIM. EXIT.
PR0609*----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA PRINCIPAL                                            *
      ******************************************************************
      *----------------------------------------------------------------*
       2000-ROTINA-PRINCIPAL      SECTION.
      *----------------------------------------------------------------*

PR0609     IF WRK-PULAR-MOV-QUOTA EQUAL 'N'
PR0609      PERFORM UNTIL WRK-FIM EQUAL 'S'
             MOVE MVQT-NR-MOV-QTA OF PECQB007
                                      TO WRK-MVQT-NR-MOV-QTA

             PERFORM 2150-UPDATE-TAB11

             MOVE 'P'                 TO CK01-FUNCAO
             MOVE 'DB2'               TO CK01-ID-DB2
PR0609       MOVE 'PECQB007'          TO WRK-TABELA
             MOVE WRK-AREA-RESTART    TO CK01-AREA-RESTART
             MOVE LENGTH OF WRK-AREA-RESTART
                                      TO CK01-TAM-AREA-RESTART
             PERFORM 5000-CHAMADA-CKRS0100

             PERFORM 2100-FETCH-PECQB007
PR0609      END-PERFORM
"          END-IF
"
PR0609     MOVE ZEROS                 TO WRK-CONT
PR0609                                   WRK-LIDOS

PR0609     PERFORM 1200-OPEN-CURSOR-PECQB027
PR0609     PERFORM 2200-FETCH-PECQB027

PR0609     PERFORM UNTIL WRK-FIM-PECQB027 EQUAL 'S'
"             MOVE NREG-TBELA-ASSOC OF PECQB027
"                                     TO WRK-MVQT-NR-MOV-QTA
"
"             PERFORM 2160-UPDATE-PECQB027
"
"             MOVE 'P'                TO CK01-FUNCAO
"             MOVE 'DB2'              TO CK01-ID-DB2
"             MOVE 'PECQB027'         TO WRK-TABELA
"             MOVE WRK-AREA-RESTART   TO CK01-AREA-RESTART
"             MOVE LENGTH OF WRK-AREA-RESTART
"                                     TO CK01-TAM-AREA-RESTART
"             PERFORM 5000-CHAMADA-CKRS0100
"
"             PERFORM 2200-FETCH-PECQB027
PR0609     END-PERFORM.

      *----------------------------------------------------------------*
       2000-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA FETCH PECQB007                                       *
      ******************************************************************
      *----------------------------------------------------------------*
       2100-FETCH-PECQB007        SECTION.
      *----------------------------------------------------------------*

           EXEC SQL
                FETCH C1
                 INTO :PECQB007.QBLOQ-MOVTO-ATUAL,
                      :PECQB007.QBLOQ-MOVTO-ANTER,
                      :PECQB007.QRENTB-ATUAL-EMPR,
                      :PECQB007.QRENTB-ANTER-EMPR,
                      :PECQB007.MVQT-NR-MOV-QTA
           END-EXEC

           IF (SQLCODE NOT EQUAL ZEROS AND + 100) OR
              (SQLWARN0    EQUAL 'W')
              MOVE 'DB2'              TO ERR-TIPO-ACESSO
              MOVE 'FETCH '           TO ERR-DBD-TAB
              MOVE 'CURSOR '          TO ERR-FUN-COMANDO
              MOVE SQLCODE            TO ERR-SQL-CODE
              MOVE '0020'             TO ERR-LOCAL
              MOVE SPACES             TO ERR-SEGM
              PERFORM 999-ROTINA-ERRO
           END-IF

           IF SQLCODE EQUAL +100
              MOVE 'S'                TO WRK-FIM
           ELSE
              ADD 1                   TO WRK-LIDOS
                                         WRK-CONT
           END-IF.

      *----------------------------------------------------------------*
       2100-99-FIM. EXIT.
      *----------------------------------------------------------------*

PR0609******************************************************************
"     *    ROTINA ATUALIZAR TABELA PECQB027                            *
"     ******************************************************************
"     *----------------------------------------------------------------*
PR0609 2160-UPDATE-PECQB027       SECTION.
"     *----------------------------------------------------------------*
"
"          EXEC SQL
"               UPDATE DB2PRD.TMOVTC_TRNSF_ASSOC
"                  SET QRENTB_ATUAL_EMPR = QRENTB_ATUAL_EMPR +
"                                          QBLOQ_MOVTO_ANTER,
"                      QRENTB_ANTER_EMPR = QRENTB_ATUAL_EMPR,
"                      QBLOQ_MOVTO_ANTER = QBLOQ_MOVTO_ATUAL,
"                      QBLOQ_MOVTO_ATUAL = 0
"                WHERE CURRENT OF CSR01-PECQB027
"          END-EXEC
"
"          IF (SQLCODE NOT EQUAL ZEROS) OR
"             (SQLWARN0    EQUAL 'W')
"             MOVE 'DB2'              TO ERR-TIPO-ACESSO
"             MOVE 'UPDATE'           TO ERR-DBD-TAB
"             MOVE 'PECQB027'         TO ERR-FUN-COMANDO
"             MOVE SQLCODE            TO ERR-SQL-CODE
"             MOVE '2160'             TO ERR-LOCAL
"             MOVE SPACES             TO ERR-SEGM
"             PERFORM 999-ROTINA-ERRO
"          END-IF.
"
"     *----------------------------------------------------------------*
PR0609 2160-99-FIM. EXIT.
"     *----------------------------------------------------------------*

PR0609******************************************************************
"     *    ROTINA SELECIONAR CURSOR PECQB027                           *
"     ******************************************************************
"     *----------------------------------------------------------------*
PR0609 2200-FETCH-PECQB027        SECTION.
"     *----------------------------------------------------------------*
"
"          EXEC SQL
"               FETCH CSR01-PECQB027
"                INTO :PECQB027.QBLOQ-MOVTO-ATUAL,
"                     :PECQB027.QBLOQ-MOVTO-ANTER,
"                     :PECQB027.QRENTB-ATUAL-EMPR,
"                     :PECQB027.QRENTB-ANTER-EMPR,
"                     :PECQB027.NREG-TBELA-ASSOC
"          END-EXEC
"
"          IF (SQLCODE NOT EQUAL ZEROS AND + 100) OR
"             (SQLWARN0    EQUAL 'W')
"             MOVE 'DB2'              TO ERR-TIPO-ACESSO
"             MOVE 'FETCH '           TO ERR-DBD-TAB
"             MOVE 'PECQB027'         TO ERR-FUN-COMANDO
"             MOVE SQLCODE            TO ERR-SQL-CODE
"             MOVE '2200'             TO ERR-LOCAL
"             MOVE SPACES             TO ERR-SEGM
"             PERFORM 999-ROTINA-ERRO
"          END-IF
"
"          IF SQLCODE EQUAL +100
"             MOVE 'S'                TO WRK-FIM-PECQB027
"          ELSE
"             ADD 1                   TO WRK-LIDOS
"                                        WRK-CONT
"          END-IF.
"
"     *----------------------------------------------------------------*
PR0609 2200-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA UPDATE TABELA PECQB007                               *
      ******************************************************************
      *----------------------------------------------------------------*
       2150-UPDATE-TAB11          SECTION.
      *----------------------------------------------------------------*

           EXEC SQL
                UPDATE DB2PRD.PECQ_MOV_QUOTA
                   SET QRENTB_ATUAL_EMPR = QRENTB_ATUAL_EMPR +
                                           QBLOQ_MOVTO_ANTER,
                       QRENTB_ANTER_EMPR = QRENTB_ATUAL_EMPR,
                       QBLOQ_MOVTO_ANTER = QBLOQ_MOVTO_ATUAL,
                       QBLOQ_MOVTO_ATUAL = 0
                 WHERE CURRENT OF C1
           END-EXEC

           IF (SQLCODE NOT EQUAL ZEROS) OR
              (SQLWARN0    EQUAL 'W')
              MOVE 'DB2'              TO ERR-TIPO-ACESSO
              MOVE 'UPDATE'           TO ERR-DBD-TAB
              MOVE 'CURSOR '          TO ERR-FUN-COMANDO
              MOVE SQLCODE            TO ERR-SQL-CODE
              MOVE '0030'             TO ERR-LOCAL
              MOVE SPACES             TO ERR-SEGM
              PERFORM 999-ROTINA-ERRO
           END-IF.

      *----------------------------------------------------------------*
       2100-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA FINALIZA                                             *
      ******************************************************************
      *----------------------------------------------------------------*
       3000-FINALIZA              SECTION.
      *----------------------------------------------------------------*

PR0609     IF WRK-PULAR-MOV-QUOTA EQUAL 'N'
              PERFORM 3100-CLOSE-CURSOR-PECQB007
PR0609     END-IF

           PERFORM 3200-CLOSE-CURSOR-PECQB027

           MOVE 'F'                   TO CK01-FUNCAO
           MOVE 'DB2'                 TO CK01-ID-DB2
           PERFORM 5000-CHAMADA-CKRS0100.

      *----------------------------------------------------------------*
       3000-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA CLOSE CURSOR PECQB007                                *
      ******************************************************************
      *----------------------------------------------------------------*
       3100-CLOSE-CURSOR-PECQB007 SECTION.
      *----------------------------------------------------------------*

           EXEC SQL
                CLOSE C1
           END-EXEC

           IF (SQLCODE NOT EQUAL ZEROS) OR
              (SQLWARN0    EQUAL 'W')
              MOVE 'DB2'              TO ERR-TIPO-ACESSO
              MOVE 'CLOSE '           TO ERR-DBD-TAB
              MOVE 'CURSOR '          TO ERR-FUN-COMANDO
              MOVE SQLCODE            TO ERR-SQL-CODE
              MOVE '0040'             TO ERR-LOCAL
              MOVE SPACES             TO ERR-SEGM
              PERFORM 999-ROTINA-ERRO
           END-IF.

      *----------------------------------------------------------------*
       3100-99-FIM. EXIT.
      *----------------------------------------------------------------*

PR0609******************************************************************
"     *    ROTINA FECHAR CURSOR PECQB027                               *
"     ******************************************************************
"     *----------------------------------------------------------------*
PR0609 3200-CLOSE-CURSOR-PECQB027 SECTION.
"     *----------------------------------------------------------------*
"
"          EXEC SQL
"               CLOSE CSR01-PECQB027
"          END-EXEC
"
"          IF (SQLCODE NOT EQUAL ZEROS) OR
"             (SQLWARN0    EQUAL 'W')
"             MOVE 'DB2'              TO ERR-TIPO-ACESSO
"             MOVE 'CLOSE '           TO ERR-DBD-TAB
"             MOVE 'PECQB027'         TO ERR-FUN-COMANDO
"             MOVE SQLCODE            TO ERR-SQL-CODE
"             MOVE '3200'             TO ERR-LOCAL
"             MOVE SPACES             TO ERR-SEGM
"             PERFORM 999-ROTINA-ERRO
"          END-IF.
"
"     *----------------------------------------------------------------*
PR0609 3200-99-FIM. EXIT.
"     *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA CHAMADA CKRS0100                                     *
      ******************************************************************
      *----------------------------------------------------------------*
       5000-CHAMADA-CKRS0100      SECTION.
      *----------------------------------------------------------------*

            CALL WRK-CKRS0100 USING CKRS01-INTERFACE

            IF CK01-CODIGO-RETORNO NOT EQUAL ZEROS
               PERFORM 999-ROTINA-ERRO
            END-IF.

      *----------------------------------------------------------------*
       5000-99-FIM. EXIT.
      *----------------------------------------------------------------*

      ******************************************************************
      *    ROTINA ERRO                                                 *
      ******************************************************************
      *----------------------------------------------------------------*
       999-ROTINA-ERRO            SECTION.
      *----------------------------------------------------------------*

           MOVE 'PSVP1095'            TO ERR-PGM

           CALL 'BRAD7100'         USING WRK-BATCH
                                         ERRO-AREA
                                         SQLCA
           GOBACK.

      *----------------------------------------------------------------*
       999-99-FIM.  EXIT.
      *----------------------------------------------------------------*
