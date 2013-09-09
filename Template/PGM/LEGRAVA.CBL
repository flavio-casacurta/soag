      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*

       PROGRAM-ID. @PGMID.
       AUTHOR.     @AUTHOR.

      *================================================================*
      *                 @EMPRESADESCRICAO
      *----------------------------------------------------------------*
      *    PROGRAMA....:  @PGMID
      *    SISTEMA.....:  @SISTEMA
      *    PROGRAMADOR.:  @AUTHOR
      *    ANALISTA....:  @ANALISTA
      *    GRUPO.......:  @GRUPO
      *    DATA........:  @DATE
      *----------------------------------------------------------------*
      *    OBJETIVO....:  @OBJETIVO
      *                   LER    ARQUIVO:
      *                          @DFILEIN
      *                   GRAVAR ARQUIVO
      *                          @DFILEOUT
      *----------------------------------------------------------------*
      *    ARQUIVOS....:                                               *
      *                DDNAME           I/O        INCLUDE/BOOK
      *                @FILEIN          I         @INCIN
      *                @FILEOUT          O         @INCOUT
      *----------------------------------------------------------------*
      *    BOOK'S......:                                               *
      *    @INCIN - BOOK DE ENTRADA
      *    @INCOUT - BOOK DE SAIDA
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

           SELECT @FILEIN ASSIGN      TO   UT-S-@FILEIN
                      FILE STATUS      IS   WRK-FS-@FILEIN.

           SELECT @FILEOUT ASSIGN      TO   UT-S-@FILEOUT
                      FILE STATUS      IS   WRK-FS-@FILEOUT.

      *================================================================*
       DATA                            DIVISION.
      *================================================================*

      *----------------------------------------------------------------*
       FILE                            SECTION.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE ENTRADA - @DFILEIN
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHIN
      *----------------------------------------------------------------*
       FD  @FILEIN
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-@FILEIN                 PIC  X(@LENGTHIN).

      *----------------------------------------------------------------*
      *   INPUT:   ARQUIVO DE SAIDA   - @DFILEOUT
      *            ORG. SEQUENCIAL    - LRECL   = @LENGTHOUT
      *----------------------------------------------------------------*
       FD  @FILEOUT
           RECORDING MODE IS F
           LABEL RECORD IS STANDARD
           BLOCK CONTAINS 0 RECORDS.

       01  FD-@FILEOUT                 PIC  X(@LENGTHOUT).

      *----------------------------------------------------------------*
       WORKING-STORAGE                 SECTION.
      *----------------------------------------------------------------*

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)        VALUE
           '*** INICIO DA WORKING-STORAGE SECTION         ****'.

>>>WORKING
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       77  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ACUMULADORES                       ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-ACUMULADORES.

           03 WRK-LIDOS-@FILEIN       PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-GRAVADOS-@FILEOUT    PIC  9(009) COMP-3  VALUE ZEROS.
           03 WRK-DISPLAY              PIC +Z(017)9        VALUE ZEROS.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE TESTE DE FILE-STATUS               ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

       01  WRK-FS-@FILEIN             PIC  X(002)         VALUE SPACES.
       01  WRK-FS-@FILEOUT             PIC  X(002)         VALUE SPACES.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE ENTRADA @FILEIN                   ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

>>>AREABOOKIN
       COPY @BOOKIN.

      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
       01  FILLER                      PIC  X(050)         VALUE
           '*** AREA DE SADA @FILEOUT                      ***'.
      *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

>>>AREABOOKOUT
       COPY @BOOKOUT.

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

           PERFORM 3000-PROCESSAR UNTIL WRK-FS-@FILEIN EQUAL '10'.

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

           OPEN INPUT   @FILEIN
                OUTPUT  @FILEOUT.

           PERFORM 1100-TESTAR-FILE-STATUS.

      *----------------------------------------------------------------*
       1000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-TESTAR-FILE-STATUS         SECTION.
      *----------------------------------------------------------------*

           MOVE '1100-TESTAR-FILE-STATUS' TO   FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 1110-TESTAR-FS-@FILEIN .

           PERFORM 1120-TESTAR-FS-@FILEOUT.

      *----------------------------------------------------------------*
       1100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1110-TESTAR-FS-@FILEIN          SECTION.
      *----------------------------------------------------------------*

           MOVE '1110-TESTAR-FS-@FILEIN' TO   FRWKGHEA-IDEN-PARAGRAFO.

           IF  WRK-FS-@FILEIN         NOT EQUAL  '00'
               MOVE '@FILEIN'         TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN    TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1110-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1120-TESTAR-FS-@FILEOUT         SECTION.
      *----------------------------------------------------------------*

           MOVE '1120-TESTAR-FS-@FILEOUT' TO   FRWKGHEA-IDEN-PARAGRAFO.

           IF  WRK-FS-@FILEOUT         NOT EQUAL  '00'
               MOVE '@FILEOUT'         TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEOUT    TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
           END-IF.

      *----------------------------------------------------------------*
       1120-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-VERIFICAR-VAZIO            SECTION.
      *----------------------------------------------------------------*

           MOVE '2000-VERIFICAR-VAZIO' TO   FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 2100-LER-@FILEIN .

           IF (WRK-LIDOS-@FILEIN      EQUAL     ZEROS)
               DISPLAY '************ @PGMID ************'
               DISPLAY '*                                *'
               DISPLAY '*     ARQUIVO @FILEIN VAZIO     *'
               DISPLAY '*       PROGRAMA ENCERRADO       *'
               DISPLAY '*                                *'
               DISPLAY '************ @PGMID ************'
               MOVE '@FILEIN'         TO FRWKGARQ-NOME-ARQUIVO
               MOVE WRK-FS-@FILEIN    TO FRWKGARQ-FILE-STATUS
               PERFORM 9100-FORMATAR-ERRO-ARQUIVO
               PERFORM 9000-FINALIZAR
           END-IF.

      *----------------------------------------------------------------*
       2000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-LER-@FILEIN               SECTION.
      *----------------------------------------------------------------*

           MOVE '2100-LER-@FILEIN '   TO   FRWKGHEA-IDEN-PARAGRAFO.

           READ @FILEIN               INTO @BOOK@INREG.

           IF WRK-FS-@FILEIN          EQUAL     '10'
               GO TO 2100-99-FIM
           END-IF.

           PERFORM 1110-TESTAR-FS-@FILEIN.
           ADD  1  TO   WRK-LIDOS-@FILEIN.

      *----------------------------------------------------------------*
       2100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*

           MOVE '3000-PROCESSAR' TO FRWKGHEA-IDEN-PARAGRAFO.

           PERFORM 3100-FORMATAR-@FILEOUT.
           PERFORM 3200-GRAVAR-@FILEOUT.
           PERFORM 2100-LER-@FILEIN.

      *----------------------------------------------------------------*
       3000-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3100-FORMATAR-@FILEOUT          SECTION.
      *----------------------------------------------------------------*

           MOVE '3100-FORMATAR-@FILEOUT' TO FRWKGHEA-IDEN-PARAGRAFO.

           INITIALIZE @BOOK@OUTREG
            REPLACING ALPHANUMERIC DATA BY SPACES
             NUMERIC DATA BY ZEROS.

>>>FORMATOUT

      *----------------------------------------------------------------*
       3100-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       3200-GRAVAR-@FILEOUT            SECTION.
      *----------------------------------------------------------------*

           MOVE '3200-GRAVAR-@FILEOUT' TO FRWKGHEA-IDEN-PARAGRAFO.

           WRITE FD-@FILEOUT           FROM    @BOOK@OUTREG.

           PERFORM 1120-TESTAR-FS-@FILEOUT.

           ADD 1                       TO  WRK-GRAVADOS-@FILEOUT.

      *----------------------------------------------------------------*
       3200-99-FIM.                    EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       9000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
      *
           MOVE '9000-FINALIZAR'       TO FRWKGHEA-IDEN-PARAGRAFO.

           DISPLAY '*********** @PGMID ***********'
           DISPLAY '*                              *'
           DISPLAY '*     RESUMO PROCESSAMENTO     *'
           DISPLAY '* ---------------------------- *'
           MOVE    WRK-LIDOS-@FILEIN   TO WRK-DISPLAY
           DISPLAY '* LIDOS    @FILEIN : ' WRK-DISPLAY
           DISPLAY '*                              *'
           MOVE    WRK-GRAVADOS-@FILEOUT  TO WRK-DISPLAY
           DISPLAY '* GRAVADOS @FILEOUT : ' WRK-DISPLAY
           DISPLAY '*                              *'
           DISPLAY '*********** @PGMID ***********'

           CLOSE @FILEIN
                 @FILEOUT.

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
