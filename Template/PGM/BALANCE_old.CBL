      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*

       PROGRAM-ID. @PGMID.
       AUTHOR.     @AUTHOR.

      *================================================================*
      *                 S O N D A - P R O C W O R K                    *
      *----------------------------------------------------------------*
      *    PROGRAMA....:  @PGMID
      *    PROGRAMADOR.:  @AUTHOR
      *    ANALISTA....:  @ANALISTA
      *    DATA........:  @DATE
      *----------------------------------------------------------------*
      *    OBJETIVO....:  BALANCE LINE ENTRE:
      *                   @DFILEIN1
      *                   @DFILEIN2
      *----------------------------------------------------------------*
      *    ARQUIVOS....:                                               *
      *                DDNAME           I/O        INCLUDE/BOOK
      *                @FILEIN1          I         @INCIN1
      *                @FILEIN2          I         @INCIN2
>>>FILEOUTS
      *----------------------------------------------------------------*
      *    BOOK'S......:                                               *
      *    @INCIN1 - BOOK DE ENTRADA1
      *    @INCIN2 - BOOK DE ENTRADA2
>>>BOOKSOUT
      *    I#FRWKGE - GRAVAR LOG DE ERRO P/ BATCH
      *    I#FRWKAR - BOOK PARA TRATAMENTO DE ERROS DE ARQUIVOS        *
      *----------------------------------------------------------------*
      *    MODULOS.....:                                               *
      *    CKRS1000 - MODULO PARA INDICAR PROCESSAMWENTO               *
      *    FRWK2999 - GRAVAR LOG DE ERRO P/ BATCH                      *
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

           SELECT @FILEIN1 ASSIGN      TO   UT-S-@FILEIN1
                      FILE STATUS      IS   WRK-FS-@FILEIN1.

           SELECT @FILEIN2 ASSIGN      TO   UT-S-@FILEIN2
                      FILE STATUS      IS   WRK-FS-@FILEIN2.
>>>SELECTOUT

      *================================================================*
       DATA                            DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       FILE                            SECTION.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE ENTRADA - @DFILEIN1
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHIN1
      *----------------------------------------------------------------*
       FD  @FILEIN1
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-@FILEIN1                 PIC  X(@LENGTHIN1).

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE ENTRADA - @DFILEIN2
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHIN2
      *----------------------------------------------------------------*
       FD  @FILEIN2
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-@FILEIN2                 PIC  X(@LENGTHIN2).
>>>FDOUTPUT

      *----------------------------------------------------------------*
       WORKING-STORAGE                 SECTION.
      *----------------------------------------------------------------*

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)        VALUE
           '*** INICIO DA WORKING-STORAGE SECTION         ****'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ACUMULADORES                       ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-ACUMULADORES.

           03 WRK-LIDOS-@FILEIN1       PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-LIDOS-@FILEIN2       PIC  9(009) COMP-3  VALUE ZEROS.
>>>GRAVADOSOUT
           03 WRK-DISPLAY              PIC +Z(017)9        VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TESTE DE FILE-STATUS               ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FS-@FILEIN1             PIC  X(002)         VALUE SPACES.
       01  WRK-FS-@FILEIN2             PIC  X(002)         VALUE SPACES.
>>>FILESTATUSOUT

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE CHAVES                             ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-CHAVE-@FILEIN1.

       01  WRK-CHAVE-@FILEIN2.

       01  WRK-CHAVE-@FILEIN1-ANT.

       01  WRK-CHAVE-@FILEIN2-ANT.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ENTRADA @FILEIN1                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

>>>AREABOOKIN1
       COPY @BOOKIN1.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ENTRADA @FILEIN2                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

>>>AREABOOKIN2
       COPY @BOOKIN2.
>>>AREASAIDA

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DO FRWK2999                           ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FRWK2999                PIC  X(008)         VALUE
           'FRWK2999'.

       01  WRK-AREA-ERRO.
           COPY 'I#FRWKGE'.
           05 WRK-BLOCO-INFO-ERRO.
              10 WRK-CHAR-INFO-ERRO    PIC  X(001) OCCURS 0 TO 30000
                                       TIMES DEPENDING ON
                                       FRWKGHEA-TAM-DADOS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA P/ FORMATACAO DE ERRO DE ARQUIVO      ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-ERRO-ARQUIVO.
           COPY 'I#FRWKAR'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DA BRAD0450                           ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-AREA-BRAD0450.
           05 WRK-0450-ABEND-BAT       PIC S9(004) COMP    VALUE +1111.
           05 WRK-0450-DUMP-BAT        PIC  X(001)         VALUE 'S'.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** FIM DA WORKING-STORAGE SECTION             ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

      *================================================================*
       PROCEDURE                       DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       0000-ROTINA-PRINCIPAL           SECTION.
      *----------------------------------------------------------------*

           MOVE '0000-ROTINA-PRINCIPAL'   TO   FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 1000-INICIAR.

           PERFORM 2000-VERIFICAR-VAZIO.

           PERFORM 3000-PROCESSAR

           PERFORM 9000-FINALIZAR.

      *----------------------------------------------------------------*
       0000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1000-INICIAR                    SECTION.
      *----------------------------------------------------------------*

           MOVE '1000-INICIAR'         TO FRWKGHEA-IDEN-PARAGRAFO.

           CALL 'CKRS1000'.

           INITIALIZE FRWKGHEA-REGISTRO
                      FRWKGARQ-REGISTRO.

           OPEN INPUT   @FILEIN1
                        @FILEIN2
>>>OPENOUTPUT

           PERFORM 1100-TESTAR-FILE-STATUS.

      *----------------------------------------------------------------*
       1000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-TESTAR-FILE-STATUS         SECTION.
      *----------------------------------------------------------------*

           MOVE '1100-TESTAR-FILE-STATUS' TO   FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 1110-TESTAR-FS-@FILEIN1.

           PERFORM 1120-TESTAR-FS-@FILEIN2.
>>>PERFORMTESTARFS

      *----------------------------------------------------------------*
       1100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1110-TESTAR-FS-@FILEIN1         SECTION.
      *----------------------------------------------------------------*

           MOVE '1110-TESTAR-FS-@FILEIN1' TO   FRWKGHEA-IDEN-PARAGRAFO.

           IF  WRK-FS-@FILEIN1         NOT EQUAL  '00'
               MOVE '@FILEIN1'         TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN1    TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1120-TESTAR-FS-@FILEIN2         SECTION.
      *----------------------------------------------------------------*

           MOVE '1120-TESTAR-FS-@FILEIN2' TO   FRWKGHEA-IDEN-PARAGRAFO.

           IF  WRK-FS-@FILEIN2         NOT EQUAL  '00'
               MOVE '@FILEIN2'         TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN2    TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1120-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
>>>TESTARFS

      *----------------------------------------------------------------*
       2000-VERIFICAR-VAZIO            SECTION.
      *----------------------------------------------------------------*

           MOVE '2000-VERIFICAR-VAZIO' TO   FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 2100-LER-@FILEIN1.

           IF (WRK-LIDOS-@FILEIN1      EQUAL     ZEROS)
               DISPLAY '************ @PGMID ************'
               DISPLAY '*                                *'
               DISPLAY '*     ARQUIVO @FILEIN1 VAZIO     *'
               DISPLAY '*       PROGRAMA ENCERRADO       *'
               DISPLAY '*                                *'
               DISPLAY '************ @PGMID ************'
               MOVE '@FILEIN1'        TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN1   TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
               PERFORM 9000-FINALIZAR
           END-IF.

           PERFORM 2200-LER-@FILEIN2.

           IF (WRK-LIDOS-@FILEIN2      EQUAL     ZEROS)
               DISPLAY '************ @PGMID ************'
               DISPLAY '*                                *'
               DISPLAY '*     ARQUIVO @FILEIN2 VAZIO     *'
               DISPLAY '*       PROGRAMA ENCERRADO       *'
               DISPLAY '*                                *'
               DISPLAY '************ @PGMID ************'
               MOVE '@FILEIN2'        TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN2   TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
               PERFORM 9000-FINALIZAR
           END-IF.

      *----------------------------------------------------------------*
       2000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-LER-@FILEIN1               SECTION.
      *----------------------------------------------------------------*

           MOVE '2100-LER-@FILEIN1'    TO   FRWKGHEA-IDEN-PARAGRAFO.

           READ @FILEIN1               INTO @BOOKIN@1REG.

           IF WRK-FS-@FILEIN1          EQUAL     '10'
               MOVE HIGH-VALUES        TO   WRK-CHAVE-@FILEIN1
               GO TO 2100-99-FIM
           END-IF.

           PERFORM 1110-TESTAR-FS-@FILEIN1.
           ADD  1  TO   WRK-LIDOS-@FILEIN1.
           PERFORM 2110-MONTAR-CHAVE-@FILEIN1.

>>>CLASS1

      *----------------------------------------------------------------*
       2100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2110-MONTAR-CHAVE-@FILEIN1      SECTION.
      *----------------------------------------------------------------*

           MOVE '2110-MONTAR-CHAVE-@FILEIN1' TO FRWKGHEA-IDEN-PARAGRAFO.

           MOVE WRK-CHAVE-@FILEIN1 TO WRK-CHAVE-@FILEIN1-ANT.

      *----------------------------------------------------------------*
       2110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-LER-@FILEIN2               SECTION.
      *----------------------------------------------------------------*

           MOVE '2200-LER-@FILEIN2'    TO   FRWKGHEA-IDEN-PARAGRAFO.

           READ @FILEIN2               INTO @BOOKIN@2REG.

           IF WRK-FS-@FILEIN2          EQUAL     '10'
               MOVE HIGH-VALUES        TO   WRK-CHAVE-@FILEIN2
               GO TO 2200-99-FIM
           END-IF.

           PERFORM 1120-TESTAR-FS-@FILEIN2.
           ADD  1  TO   WRK-LIDOS-@FILEIN2.
           PERFORM 2210-MONTAR-CHAVE-@FILEIN2.

>>>CLASS2

      *----------------------------------------------------------------*
       2200-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2210-MONTAR-CHAVE-@FILEIN2      SECTION.
      *----------------------------------------------------------------*

           MOVE '2210-MONTAR-CHAVE-@FILEIN2' TO FRWKGHEA-IDEN-PARAGRAFO.

           MOVE WRK-CHAVE-@FILEIN2 TO WRK-CHAVE-@FILEIN2-ANT.

      *----------------------------------------------------------------*
       2210-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*

           MOVE '3000-PROCESSAR' TO FRWKGHEA-IDEN-PARAGRAFO.

           IF      WRK-CHAVE-@FILEIN1  LESS THAN WRK-CHAVE-@FILEIN2
                   PERFORM 3100-@FILEIN1-MENOR-Q-@FILEIN2
           ELSE
             IF    WRK-CHAVE-@FILEIN1  EQUAL TO  WRK-CHAVE-@FILEIN2
                   PERFORM 3200-@FILEIN1-IGUAL-A-@FILEIN2
               ELSE
                   PERFORM 3300-@FILEIN1-MAIOR-Q-@FILEIN2
               END-IF
           END-IF.

      *----------------------------------------------------------------*
       3000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3100-@FILEIN1-MENOR-Q-@FILEIN2  SECTION.
      *----------------------------------------------------------------*

           MOVE '3100-@FILEIN1-MENOR-Q-@FILEIN2'
                                             TO FRWKGHEA-IDEN-PARAGRAFO.
>>>3100-@FILEIN1-MENOR-Q-@FILEIN2

           PERFORM 2100-LER-@FILEIN1.
           PERFORM 2200-LER-@FILEIN2.

      *----------------------------------------------------------------*
       3100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3200-@FILEIN1-IGUAL-A-@FILEIN2  SECTION.
      *----------------------------------------------------------------*

           MOVE  '3200-@FILEIN1-IGUAL-A-@FILEIN2'
                                           TO   FRWKGHEA-IDEN-PARAGRAFO.
>>>3200-@FILEIN1-IGUAL-A-@FILEIN2

           PERFORM 2100-LER-@FILEIN1.
           PERFORM 2200-LER-@FILEIN2.

      *----------------------------------------------------------------*
       3200-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3300-@FILEIN1-MAIOR-Q-@FILEIN2  SECTION.
      *----------------------------------------------------------------*

           MOVE  '3300-@FILEIN1-MAIOR-Q-@FILEIN2'
                                           TO   FRWKGHEA-IDEN-PARAGRAFO.
>>>3300-@FILEIN1-MAIOR-Q-@FILEIN2

           PERFORM 2100-LER-@FILEIN1.
           PERFORM 2200-LER-@FILEIN2.

      *----------------------------------------------------------------*
       3300-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
>>>FORMATOUT
>>>GRAVAROUT

      *----------------------------------------------------------------*
       9000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
      *
           MOVE '9000-FINALIZAR'       TO FRWKGHEA-IDEN-PARAGRAFO.
      *
           DISPLAY '*********** @PGMID ***********'
           DISPLAY '*                              *'
           DISPLAY '*     RESUMO PROCESSAMENTO     *'
           DISPLAY '* ---------------------------- *'
           MOVE    WRK-LIDOS-@FILEIN1  TO WRK-DISPLAY
           DISPLAY '* LIDOS    @FILEIN1 : ' WRK-DISPLAY
           DISPLAY '*                              *'
           MOVE    WRK-LIDOS-@FILEIN2  TO WRK-DISPLAY
           DISPLAY '* LIDOS    @FILEIN2 : ' WRK-DISPLAY
>>>DISPLAYOUT
           DISPLAY '*                              *'
           DISPLAY '*********** @PGMID ***********'

           CLOSE @FILEIN1
                 @FILEIN2
>>>CLOSEOUT

           PERFORM 1100-TESTAR-FILE-STATUS.

           STOP RUN.

      *----------------------------------------------------------------*
       9000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9100-FORMATAR-ERRO-ARQUIVO      SECTION.
      *----------------------------------------------------------------*

           SET ERRO-ARQUIVO            TO TRUE.

           MOVE FRWKGARQ-TAM-LAYOUT    TO FRWKGHEA-TAM-DADOS.
           MOVE WRK-AREA-ERRO-ARQUIVO  TO WRK-BLOCO-INFO-ERRO
                                          (1:FRWKGHEA-TAM-DADOS).

           PERFORM 9900-TRATAR-ERRO.

      *----------------------------------------------------------------*
       9100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9900-TRATAR-ERRO                SECTION.
      *----------------------------------------------------------------*

           MOVE '@PGMID'             TO FRWKGHEA-NOME-PROGRAMA.

           PERFORM 9990-GRAVAR-LOG-ERRO.

           PERFORM 9999-ABENDAR-PROGRAMA.

           GOBACK.

      *----------------------------------------------------------------*
       9900-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9990-GRAVAR-LOG-ERRO            SECTION.
      *----------------------------------------------------------------*

           CALL WRK-FRWK2999           USING WRK-AREA-ERRO.

      *----------------------------------------------------------------*
       9990-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9999-ABENDAR-PROGRAMA           SECTION.
      *----------------------------------------------------------------*

           DISPLAY '*** BRAD0450 CHAMADO PARA ABENDAR O PROGRAMA ***'.
           DISPLAY ' '.

           CALL 'BRAD0450'             USING WRK-0450-ABEND-BAT
                                             WRK-0450-DUMP-BAT.

      *----------------------------------------------------------------*
       9999-99-FIM.                    EXIT.
      *----------------------------------------------------------------*
      *================================================================*
