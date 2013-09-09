      *================================================================*
       IDENTIFICATION                  DIVISION.
      *================================================================*
       PROGRAM-ID. @APPLID1@SIGLAPGML.
       AUTHOR.     @AUTHOR.
      *================================================================*
      *@CONTRATANTE
      *----------------------------------------------------------------*
      *                                                                *
      *    APLICACAO       : @APPLID
      *                      @APPLNAME
      *    PROGRAMA        : @APPLID1@SIGLAPGML
      *    PROGRAMADOR     : @AUTHOR
      *    ANALISTA        : @ANALISTA
      *    GRUPO           : @GRUPO
      *    DATA DE CRIACAO : @DATE
      *                                                                *
      *----------------------------------------------------------------*
      *    OBJETIVO....: PROGRAMA COORDENADOR                          *
      *                  @SERVICO @ENTIDADE1
      *                  @ENTIDADE2
      *----------------------------------------------------------------*
      *    BOOKS FUNCIONAIS...:                                        *
      *    @APPLIDW@SIGLAPGME - BOOK ENTRADA DE DADOS DO FRAMEWORK
@REMBOOKSAIDA
      *    @APPLIDW00C - BOOK CONTROLE - COMUNICACAO ENTRE MODULOS
      *    @APPLIDW@SIGLAPGMI - BOOK COMUNICACAO COM FUNCIONAL @APPLID3@SIGLAPGML
@REMBOOKFUNCIONAIS
      *    @APPLIDW00W - BOOK DE WORK DO PROGRAMA
      *    @APPLIDW01W - BOOK DE WORK PARA TRATAMENTO DE ERROS
      *    @APPLIDW00P - BOOK DE PROCEDUR PARA ACESSOS AO GAM
      *    @APPLIDW01P - BOOK DE PROCEDUR PARA TRATAMENTO DE ERROS
      *----------------------------------------------------------------*
      *    BOOKS DA ARQUITETURA:                                       *
      *    I#FRWKAQ - COMMAREA ENTRE PROGRAMA/FRAMEWORK                *
      *    I#FRWK04 - COMMAREA ENTRE PROGRAMA/FRWK1200(GAM)            *
      *    FRWKWAAA - BLOCO DE INFORMACOES DA SESSAO                   *
      *    I#FRWK83 - BLOCO DE INFORMACOES DA SESSAO                   *
      *    I#FRWKGE - COMMAREA FRWK1999 - LOG DE ERRO                  *
      *    I#FRWKDB - AREA DO FRWK1999  - LOG DE ERROS DB2             *
      *    I#FRWKCI - AREA DO FRWK1999  - LOG DE ERROS CICS            *
      *    I#FRWKMD - AREA DO FRWK1999  - LOG DE ERROS MODULO          *
      *    I#FRWKLI - AREA DO FRWK1999  - LOG DE ERROS LIVRE           *
      *----------------------------------------------------------------*
      *    MODULOS.............:                                       *
      *    FRWK1200 - GERENCIADOR DO GAM  - BOOK I#FRWK04              *
      *    FRWK1999 - TRATAMENTO DE ERROS - BOOK I#FRWKGE              *
      *    @APPLID3@SIGLAPGML - MODULO FUNCIONAL
@REMMODLFUNCIONAIS
      *================================================================*

      *================================================================*
       ENVIRONMENT                     DIVISION.
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
           '* INICIO DA WORKING-STORAGE *'.
      *----------------------------------------------------------------*
       77  WRK-PROGRAM                 PIC  X(08) VALUE '@APPLID1@SIGLAPGML'.
       77  WRK-NREG-QTDE               PIC S9(09) COMP VALUE +0.
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREA DE ENTRADA *'.
      *----------------------------------------------------------------*
      *    WRK-@APPLIDW@SIGLAPGME
       01  FILLER.
           COPY @APPLIDW@SIGLAPGME.
@AREADESAIDA
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* BLOCO PERSISTENTE DO GAM *'.
      *----------------------------------------------------------------*
       01  WRK-@APPLIDW@SIGLAPGMP.
           05      @APPLIDW@SIGLAPGMP-HEADER.
            07     @APPLIDW@SIGLAPGMP-COD-LAYOUT           PIC  X(08)
                                                 VALUE '@APPLIDW@SIGLAPGMP'.
            07     @APPLIDW@SIGLAPGMP-TAM-LAYOUT           PIC  9(05) VALUE @LENBOOKP.
           05      @APPLIDW@SIGLAPGMP-BLOCO-PAGINACAO      PIC  X(@LENBLPAG).
      *----------------------------------------------------------------*
       01  FILLER                      PIC  X(050)         VALUE
           '* AREA DE ACESSO FUNCIONAL *'.
      *----------------------------------------------------------------*
       01  WRK-@APPLID3@SIGLAPGML.
           COPY @APPLIDW00C.
           COPY @APPLIDW@SIGLAPGMI.
      *----------------------------------------------------------------*
@WORKINGFUNCIONAIS
       01  FILLER                      PIC  X(050)         VALUE
           '* AREAS DE WORKING *'.
      *----------------------------------------------------------------*
       COPY @APPLIDW00W.
       COPY @APPLIDW01W.
      *----------------------------------------------------------------*
      *               L I N K A G E    S E C T I O N                   *
      *----------------------------------------------------------------*
       LINKAGE                         SECTION.
      *----------------------------------------------------------------*
      *----------------------------------------------------------------*
      *  I#FRWKAQ:  COMMAREA INTERFACE (I/O) COM O FRAMEWORK           *
      *----------------------------------------------------------------*
       01  DFHCOMMAREA.
           COPY 'I#FRWKAQ'.
      *----------------------------------------------------------------*
       PROCEDURE DIVISION.
      *----------------------------------------------------------------*
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
           PERFORM 90100-PROG-INIT.
           INITIALIZE  FRWKGHEA-REGISTRO
                       FRWKGCIC-REGISTRO
                       FRWKGMOD-REGISTRO
                       FRWKGLIV-REGISTRO
                       FRWKGLAQ-BLOCO-RETORNO
                       @APPLIDW@SIGLAPGMI-REGISTRO
           PERFORM 1100-RECUPERAR-DADOS-ENTRADA.
      *----------------------------------------------------------------*
       1000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       1100-RECUPERAR-DADOS-ENTRADA    SECTION.
      *----------------------------------------------------------------*
           MOVE '1100-RECUPERAR-DADOS-ENTRADA' TO WRK-PARAGRAFO.
           MOVE @APPLIDW@SIGLAPGME-HEADER TO @APPLID1200-HEADER.
           PERFORM 90300-CONS-LIBERAR-GAM.
           MOVE @APPLID1200-REGISTRO(1:LENGTH OF @APPLIDW@SIGLAPGME-REGISTRO)
             TO @APPLIDW@SIGLAPGME-REGISTRO.
      *----------------------------------------------------------------*
       1100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2000-PROCESSAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE    '2000-PROCESSAR' TO WRK-PARAGRAFO.
           PERFORM 2100-OBTER-DADOS-SESSAO.

           EVALUATE TRUE
               WHEN FRWKWAAA-PRIMEIRO-BLOCO
               WHEN FRWKWAAA-ULTIMO-BLOCO
               WHEN FRWKWAAA-CONSULTA-INICIAL
                    CONTINUE
               WHEN FRWKWAAA-BLOCO-SEGUINTE
               WHEN FRWKWAAA-BLOCO-ANTERIOR
                    PERFORM 2200-OBTER-DADOS-PERSISTENTE
               WHEN OTHER
                    MOVE 16             TO FRWKGLAQ-COD-RETORNO
                    MOVE '0013'         TO FRWKGLAQ-COD-ERRO
                    MOVE '@ERROCICS'     TO FRWKGLAQ-COD-MENSAGEM
                    MOVE FRWKGLAQ-COD-MENSAGEM
                                        TO FRWKGLIV-COD-MENSAGEM
                    SET  ERRO-LIVRE     TO TRUE
                    PERFORM 91000-API-ERROR
           END-EVALUATE.

           PERFORM 2300-ALIMENTAR-FUNCIONAL.
           PERFORM 2400-CHAMAR-FUNCIONAL.
           PERFORM 2500-BLOCO-PERSISTENTE.
           PERFORM 2600-GRAVAR-DADOS-SAIDA.
      *----------------------------------------------------------------*
       2000-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2100-OBTER-DADOS-SESSAO         SECTION.
      *----------------------------------------------------------------*
           MOVE '2100-OBTER-DADOS-SESSAO'  TO WRK-PARAGRAFO.
           MOVE FRWKWAAA-HEADER TO @APPLID1200-HEADER.
           MOVE FRWKEL83-COD-LAYOUT TO @APPLID1200-COD-LAYOUT.
           PERFORM 90200-CONSULTAR-GAM.
           MOVE @APPLID1200-REGISTRO(1:LENGTH OF FRWKWAAA-REGISTRO)
             TO FRWKWAAA-REGISTRO.
      *----------------------------------------------------------------*
       2100-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2200-OBTER-DADOS-PERSISTENTE    SECTION.
      *----------------------------------------------------------------*
           MOVE '2200-OBTER-DADOS-PERSISTENTE'  TO WRK-PARAGRAFO.
           MOVE @APPLIDW@SIGLAPGMP-HEADER TO @APPLID1200-HEADER.
           PERFORM 90600-CONSULTAR-GAM-PERSISTENT.
           MOVE @APPLID1200-REGISTRO(1:LENGTH OF WRK-@APPLIDW@SIGLAPGMP)
             TO WRK-@APPLIDW@SIGLAPGMP.
           MOVE @APPLIDW@SIGLAPGMP-BLOCO-PAGINACAO  TO @APPLIDW@SIGLAPGMI-BLOCO-PAGINACAO.
      *----------------------------------------------------------------*
       2200-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2300-ALIMENTAR-FUNCIONAL        SECTION.
      *----------------------------------------------------------------*
           MOVE '2300-ALIMENTAR-FUNCIONAL' TO WRK-PARAGRAFO.
           MOVE FRWKWAAA-SOLIC-MAIS-DADOS
             TO @APPLIDW@SIGLAPGMI-P-SENTIDO-PAGINACAO.
@ALIMENTARFUNCIONAL
           MOVE @APPLIDW@SIGLAPGME-REGISTRO TO @APPLIDW@SIGLAPGMI-BLOCO-ENTRADA.
      *----------------------------------------------------------------*
       2300-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2400-CHAMAR-FUNCIONAL           SECTION.
      *----------------------------------------------------------------*
           MOVE '2400-CHAMAR-FUNCIONAL' TO WRK-PARAGRAFO.
           INITIALIZE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID3@SIGLAPGML.
           MOVE '@APPLID3@SIGLAPGML'             TO WRK-MODULO.
           EXEC CICS LINK              PROGRAM (WRK-MODULO)
                                       COMMAREA(WRK-@APPLID3@SIGLAPGML)
                                       LENGTH  (LENGTH OF WRK-@APPLID3@SIGLAPGML)
                                       NOHANDLE
           END-EXEC.

           IF EIBRESP NOT EQUAL DFHRESP(NORMAL)
              MOVE 16                     TO FRWKGLAQ-COD-RETORNO
              MOVE '0014'                 TO FRWKGLAQ-COD-ERRO
              MOVE '@ERROCICS'             TO FRWKGLAQ-COD-MENSAGEM
              SET ERRO-CICS TO TRUE
              PERFORM 91000-API-ERROR
           END-IF.

           MOVE @APPLIDW00C-BLOCO-RETORNO OF WRK-@APPLID3@SIGLAPGML
             TO FRWKGLAQ-BLOCO-RETORNO.
           IF FRWKGLAQ-COD-RETORNO GREATER THAN 1
              IF FRWKGLAQ-COD-RETORNO GREATER THAN 8
                 SET ERRO-MODULO TO TRUE
                 PERFORM 91000-API-ERROR
               ELSE
                 PERFORM 3000-FINALIZAR
              END-IF
           END-IF.
      *----------------------------------------------------------------*
       2400-99-EXIT. EXIT.
      *----------------------------------------------------------------*

      *----------------------------------------------------------------*
       2500-BLOCO-PERSISTENTE          SECTION.
      *----------------------------------------------------------------*
           MOVE '2500-BLOCO-PERSISTENTE'  TO WRK-PARAGRAFO.
           MOVE @APPLIDW@SIGLAPGMI-BLOCO-PAGINACAO TO @APPLIDW@SIGLAPGMP-BLOCO-PAGINACAO.
           MOVE @APPLIDW@SIGLAPGMP-HEADER TO @APPLID1200-HEADER.
           MOVE @APPLIDW@SIGLAPGMP-BLOCO-PAGINACAO TO @APPLID1200-REGISTRO.

           EVALUATE TRUE
               WHEN FRWKWAAA-PRIMEIRO-BLOCO
               WHEN FRWKWAAA-ULTIMO-BLOCO
               WHEN FRWKWAAA-CONSULTA-INICIAL
                    PERFORM 90500-CRIAR-GAM-PERSISTENTE
               WHEN FRWKWAAA-BLOCO-SEGUINTE
               WHEN FRWKWAAA-BLOCO-ANTERIOR
                    PERFORM 90700-ATUALIZAR-GAM-PERSISTENT
               WHEN OTHER
                    CONTINUE
           END-EVALUATE.
      *----------------------------------------------------------------*
       2500-99-EXIT. EXIT.
      *----------------------------------------------------------------*
@GRAVARDADOSSAIDA
@MODULOSFUNCIONAIS

      *----------------------------------------------------------------*
       3000-FINALIZAR                  SECTION.
      *----------------------------------------------------------------*
           MOVE '3000-FINALIZAR' TO WRK-PARAGRAFO.
           PERFORM 99990-RETURN.
      *----------------------------------------------------------------*
       3000-99-EXIT. EXIT.
      *----------------------------------------------------------------*
       COPY @APPLIDW00P.
       COPY @APPLIDW01P.
      *----------------------------------------------------------------*
       END PROGRAM @APPLID1@SIGLAPGML.
