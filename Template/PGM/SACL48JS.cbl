       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. SACL48JS.
       AUTHOR.     ADERBAL MACHADO RIBEIRO - JAPI.
      *================================================================*
      *                 SCOPUS TECNOLOGIA                              *
      *----------------------------------------------------------------*
      *                                                                *
      *    APLICACAO       : SACL                                      *
      *    PROGRAMA        : SACL48JS                                  *
      *    PROGRAMADOR     : ADERBAL MACHADO RIBEIRO - JAPI            *
      *    ANALISTA        : SCOPUS                                    *
      *    DATA DE CRIACAO : 2011 JUN 12 23:25:54                      *
      *                                                                *
      *----------------------------------------------------------------*
      *    OBJETIVO....: MODULO PERSISTENCIA                           *
      *                  CONSULTALISTA INFORMACAO COMPLEMENT           *
      *----------------------------------------------------------------*
      *    BOOKS FUNCIONAIS...:                                        *
      *    SACLW000 - BOOK CONTROLE - COMUNICACAO ENTRE MODULOS        *
      *    SACLW8JC - BOOK COMUNICACAO DESTE MODULO                    *
      *    SACLW1W0 - BOOK DE WORK DO PROGRAMA                         *
      *    SACLW0W1 - BOOK DE WORK DO FRWK1999                         *
      *    SACLW1P1 - BOOK DE PROCEDUR PARA TRATAMENTO DE ERROS        *
      *    SACLB032 - DCLGEN DA TABELA INFORMACAO COMPLEMENT           *
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
      *    GLOG1001 - GERENCIADOR DO GAM  - BOOK I#GLOG01              *
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
       77  WRK-PROGRAM                 PIC  X(008) VALUE 'SACL48JS'.
       77  WRK-INVOKINGPROG            PIC  X(008) VALUE SPACES.

       01  WRK-NREG-QTDE               PIC S9(009) COMP-3 VALUE ZEROS.
      *----------------------------------------------------------------*
      * AREAS DE WORKING GENERICAS*
      *----------------------------------------------------------------*
       COPY SACLW1W0.
       COPY SACLW0W1.
      *----------------------------------------------------------------*
      * AREA PARA DB2
      *----------------------------------------------------------------*
           EXEC SQL  INCLUDE SQLCA     END-EXEC.
           EXEC SQL  INCLUDE SACLB032  END-EXEC.
      *----------------------------------------------------------------*
           EXEC SQL
                DECLARE CSR01-SACLB032 CURSOR FOR
                SELECT
                             NPROT_MANIF
                           , NSEQ_MANIF
                           , NORD_COMPL_ABERT
                           , CPTCAO_TBELA
                           , RCOMPL_ABERT_MANIF
                FROM
                             DB2PRD.TMANIF_PSSOA_COMPL
                WHERE
                             NPROT_MANIF             >=
                   :SACLB032.NPROT-MANIF
                AND        NSEQ_MANIF              >=
                   :SACLB032.NSEQ-MANIF
                AND        NORD_COMPL_ABERT        >=
                   :SACLB032.NORD-COMPL-ABERT
             ORDER BY
                             NPROT_MANIF
                    ,        NSEQ_MANIF
                    ,        NORD_COMPL_ABERT
           END-EXEC.
           EXEC SQL
                DECLARE CSR02-SACLB032 CURSOR FOR
                SELECT
                             NPROT_MANIF
                           , NSEQ_MANIF
                           , NORD_COMPL_ABERT
                           , CPTCAO_TBELA
                           , RCOMPL_ABERT_MANIF
                FROM
                             DB2PRD.TMANIF_PSSOA_COMPL
                WHERE
                             NPROT_MANIF             >
                   :SACLB032.NPROT-MANIF
                AND        NSEQ_MANIF              >
                   :SACLB032.NSEQ-MANIF
                AND        NORD_COMPL_ABERT        >
                   :SACLB032.NORD-COMPL-ABERT
             ORDER BY
                             NPROT_MANIF
                    ,        NSEQ_MANIF
                    ,        NORD_COMPL_ABERT
           END-EXEC.
           EXEC SQL
                DECLARE CSR03-SACLB032 CURSOR FOR
                SELECT
                             NPROT_MANIF
                           , NSEQ_MANIF
                           , NORD_COMPL_ABERT
                           , CPTCAO_TBELA
                           , RCOMPL_ABERT_MANIF
                FROM
                             DB2PRD.TMANIF_PSSOA_COMPL
                WHERE
                             NPROT_MANIF             <
                   :SACLB032.NPROT-MANIF
                AND        NSEQ_MANIF              <
                   :SACLB032.NSEQ-MANIF
                AND        NORD_COMPL_ABERT        <
                   :SACLB032.NORD-COMPL-ABERT
             ORDER BY
                             NPROT_MANIF             DESC
                    ,        NSEQ_MANIF              DESC
                    ,        NORD_COMPL_ABERT        DESC
           END-EXEC.
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           02  LNK-SACL48JS.
           COPY SACLW000.
           COPY SACLW8JC.
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
                       SACLW000-BLOCO-RETORNO
                       SACLB032.

           IF  EIBCALEN   EQUAL TO ZEROS
               MOVE 16          TO SACLW000-COD-RETORNO
               MOVE 'ER02'      TO SACLW000-COD-ERRO
               MOVE 'SACL9999'  TO SACLW000-COD-MENSAGEM
               SET ERRO-CICS    TO TRUE
               PERFORM 91000-API-ERROR
           END-IF.

           EXEC CICS ASSIGN INVOKINGPROG (WRK-INVOKINGPROG)
                     NOHANDLE
           END-EXEC.

           IF  EIBRESP NOT EQUAL DFHRESP(NORMAL)
               MOVE 16                 TO SACLW000-COD-RETORNO
               MOVE 'ER02'             TO SACLW000-COD-ERRO
               MOVE 'SACL9999'         TO SACLW000-COD-MENSAGEM
               SET ERRO-CICS           TO TRUE
               PERFORM 91000-API-ERROR
           END-IF.

           IF  WRK-INVOKINGPROG NOT EQUAL TO 'SACL38JL'
               MOVE 16                 TO SACLW000-COD-RETORNO
               MOVE 'ER03'             TO SACLW000-COD-ERRO
               MOVE 'SACL9999'         TO SACLW000-COD-MENSAGEM
               SET ERRO-LIVRE          TO TRUE
               PERFORM 91000-API-ERROR
           END-IF.

           MOVE SACLW8JC-NREG-QTDE TO WRK-NREG-QTDE.
      *----------------------------------------------------------------*
       1000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '2000-PROCESSAR' TO WRK-PARAGRAFO.

           PERFORM 2100-OPEN-CURSOR.

           PERFORM 2200-FETCH-CURSOR.

           IF  SQLCODE EQUAL +100
               MOVE 08         TO SACLW000-COD-RETORNO
               MOVE 'ER03'     TO SACLW000-COD-ERRO
               MOVE 'SACL0563' TO SACLW000-COD-MENSAGEM
               PERFORM 3000-FINALIZAR
           END-IF.

           PERFORM VARYING WRK-IDX FROM 1 BY 1
             UNTIL SQLCODE EQUAL TO +100
                OR WRK-IDX GREATER WRK-NREG-QTDE
                PERFORM 2300-ALIMENTAR-INFORMACAO-COMP
                PERFORM 2200-FETCH-CURSOR
           END-PERFORM.

           IF  SQLCODE   EQUAL TO ZEROS
               MOVE 01         TO SACLW000-COD-RETORNO
           END-IF.

           COMPUTE WRK-NREG-QTDE = WRK-IDX - 1.

           MOVE WRK-NREG-QTDE TO SACLW8JC-NREG-QTDE.

           PERFORM 2400-CLOSE-CURSOR.
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-OPEN-CURSOR                SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-OPEN-CURSOR' TO WRK-PARAGRAFO.

           MOVE SACLW8JC-NPROT-MANIF
             TO NPROT-MANIF OF SACLB032.
           MOVE SACLW8JC-NSEQ-MANIF
             TO NSEQ-MANIF OF SACLB032.
           MOVE SACLW8JC-NORD-COMPL-ABERT
             TO NORD-COMPL-ABERT OF SACLB032.

           EVALUATE SACLW8JC-SOLIC-MAIS-DADOS
               WHEN 'I'
               WHEN 'P'
               WHEN 'U'
                   PERFORM 2110-OPEN-CURSOR-MAIOR-IGUAL
               WHEN 'S'
                   PERFORM 2120-OPEN-CURSOR-MAIOR
               WHEN 'A'
                   PERFORM 2130-OPEN-CURSOR-MENOR
               WHEN OTHER
                   MOVE 16             TO SACLW000-COD-RETORNO
                   MOVE 'ER04'         TO SACLW000-COD-ERRO
                   MOVE 'SACL9999'     TO SACLW000-COD-MENSAGEM
                   SET  ERRO-LIVRE     TO TRUE
                   PERFORM 91000-API-ERROR
           END-EVALUATE.
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2110-OPEN-CURSOR-MAIOR-IGUAL    SECTION.
      *----------------------------------------------------------------*
           MOVE '2110-OPEN-CURSOR-MAIOR-IGUAL' TO WRK-PARAGRAFO.

           EXEC SQL
                OPEN CSR01-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER05'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-OPEN    TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2110-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2120-OPEN-CURSOR-MAIOR          SECTION.
      *----------------------------------------------------------------*
           MOVE '2120-OPEN-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL
                OPEN CSR02-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER06'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-OPEN    TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2120-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2130-OPEN-CURSOR-MENOR          SECTION.
      *----------------------------------------------------------------*
           MOVE '2130-OPEN-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL
                OPEN CSR03-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER07'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-OPEN    TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2130-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-FETCH-CURSOR               SECTION.
      *----------------------------------------------------------------*
           MOVE '2200-FETCH-CURSOR' TO WRK-PARAGRAFO.

           EVALUATE SACLW8JC-SOLIC-MAIS-DADOS
               WHEN 'I'
               WHEN 'P'
               WHEN 'U'
                   PERFORM 2210-FETCH-CURSOR-MAIOR-IGUAL
               WHEN 'S'
                   PERFORM 2220-FETCH-CURSOR-MAIOR
               WHEN 'A'
                   PERFORM 2230-FETCH-CURSOR-MENOR
               WHEN OTHER
                   MOVE 16             TO SACLW000-COD-RETORNO
                   MOVE 'ER08'         TO SACLW000-COD-ERRO
                   MOVE 'SACL9999'     TO SACLW000-COD-MENSAGEM
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

           EXEC SQL
                FETCH CSR01-SACLB032 INTO
                   :SACLB032.NPROT-MANIF
                 , :SACLB032.NSEQ-MANIF
                 , :SACLB032.NORD-COMPL-ABERT
                 , :SACLB032.CPTCAO-TBELA
                 , :SACLB032.RCOMPL-ABERT-MANIF
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS AND +100
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER09'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-FETCH   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2210-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2220-FETCH-CURSOR-MAIOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2220-FETCH-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL
                FETCH CSR02-SACLB032 INTO
                   :SACLB032.NPROT-MANIF
                 , :SACLB032.NSEQ-MANIF
                 , :SACLB032.NORD-COMPL-ABERT
                 , :SACLB032.CPTCAO-TBELA
                 , :SACLB032.RCOMPL-ABERT-MANIF
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS AND +100
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER10'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-FETCH   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2220-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2230-FETCH-CURSOR-MENOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2230-FETCH-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL
                FETCH CSR03-SACLB032 INTO
                   :SACLB032.NPROT-MANIF
                 , :SACLB032.NSEQ-MANIF
                 , :SACLB032.NORD-COMPL-ABERT
                 , :SACLB032.CPTCAO-TBELA
                 , :SACLB032.RCOMPL-ABERT-MANIF
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS AND +100
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER11'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-FETCH   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2230-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-ALIMENTAR-INFORMACAO-COMP        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-ALIMENTAR-INFORMACAO-COMP' TO WRK-PARAGRAFO.

           MOVE          NPROT-MANIF                        OF SACLB032
             TO SACLW8JC-NPROT-MANIF-L(WRK-IDX).
           MOVE          NSEQ-MANIF                         OF SACLB032
             TO SACLW8JC-NSEQ-MANIF-L(WRK-IDX).
           MOVE          NORD-COMPL-ABERT                   OF SACLB032
             TO SACLW8JC-NORD-COMPL-ABERT-L(WRK-IDX).
           MOVE          CPTCAO-TBELA                       OF SACLB032
             TO SACLW8JC-CPTCAO-TBELA-L(WRK-IDX).
           MOVE          RCOMPL-ABERT-MANIF-TEXT            OF SACLB032
             TO SACLW8JC-RCOMPL-ABERT-MANIF-L(WRK-IDX).
      *----------------------------------------------------------------*
       2300-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2400-CLOSE-CURSOR               SECTION.
      *----------------------------------------------------------------*
           MOVE '2400-CLOSE-CURSOR' TO WRK-PARAGRAFO.

           EVALUATE SACLW8JC-SOLIC-MAIS-DADOS
               WHEN 'I'
               WHEN 'P'
               WHEN 'U'
                   PERFORM 2410-CLOSE-CURSOR-MAIOR-IGUAL
               WHEN 'S'
                   PERFORM 2420-CLOSE-CURSOR-MAIOR
               WHEN 'A'
                   PERFORM 2430-CLOSE-CURSOR-MENOR
               WHEN OTHER
                   MOVE 16             TO SACLW000-COD-RETORNO
                   MOVE 'ER12'         TO SACLW000-COD-ERRO
                   MOVE 'SACL9999'     TO SACLW000-COD-MENSAGEM
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

           EXEC SQL
                CLOSE CSR01-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER13'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-CLOSE   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2410-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2420-CLOSE-CURSOR-MAIOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2420-CLOSE-CURSOR-MAIOR' TO WRK-PARAGRAFO.

           EXEC SQL
                CLOSE CSR02-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER14'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-CLOSE   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2420-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2430-CLOSE-CURSOR-MENOR         SECTION.
      *----------------------------------------------------------------*
           MOVE '2430-CLOSE-CURSOR-MENOR' TO WRK-PARAGRAFO.

           EXEC SQL
                CLOSE CSR03-SACLB032
           END-EXEC.

           IF  SQLCODE NOT EQUAL TO ZEROS
               MOVE 16         TO SACLW000-COD-RETORNO
               MOVE 'ER15'     TO SACLW000-COD-ERRO
               MOVE 'SACL9999' TO SACLW000-COD-MENSAGEM
               SET ERRO-DB2    TO TRUE
               MOVE 'TMANIF_PSSOA_COM'
                               TO FRWKGDB2-NOME-TABELA
               SET DB2-CLOSE   TO TRUE
               MOVE SPACES     TO FRWKGDB2-STORED-PROC
               MOVE SPACES     TO FRWKGDB2-LOCAL
               MOVE SQLCA      TO FRWKGDB2-SQLCA
               MOVE SQLCODE    TO FRWKGDB2-SQLCODE
               PERFORM 91000-API-ERROR
           END-IF.
      *----------------------------------------------------------------*
       2430-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '3000-FINALIZAR' TO WRK-PARAGRAFO.

           PERFORM 99990-RETURN.
      *----------------------------------------------------------------*
       3000-99-EXIT. EXIT.
      *----------------------------------------------------------------*
       COPY SACLW1P1.
      *----------------------------------------------------------------*
       END PROGRAM SACL48JS.
