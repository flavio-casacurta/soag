      *================================================================*
      * IDENTIFICACAO:                                                 *
      * NOME DA AREA DE COMUNICACAO...: @PREFIX
      * OBJETIVO DA AREA DE TRABALHO..: TRAFEGAR DADOS ENTRE
      *                                 FUNCIONAL E BASICO             *
      * SERVICO.......................: @SERVICO
      *                                 @ENTIDADE1
      *                                 @ENTIDADE2
      * APLICACAO.....................: @APPLID
      *                                 @APPLNAME
      * TIPO DE REGISTRO..............: FIXO                           *
      * TAMANHO DO REGISTRO EM BYTES..: @LENGTH
      *                                                                *
      * DATA DE CRIACAO...............: @DATE
      * ANALISTA RESPONSAVEL..........: @ANALISTA
      * GRUPO.........................: @GRUPO
      * PROGRAMADOR...................: @AUTHOR
      *----------------------------------------------------------------*
      * ALTERACOES:                                                    *
      *                                                                *
      * DATA            NOME               DESCRICAO                   *
      * ==========  =================  ==============================  *
      * 99/99/9999  XXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  *
      *                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  *
      *----------------------------------------------------------------*
      * DESCRICAO DA AREA DE TRABALHO:                                 *
      *                                                                *
REMARKS
      *                                                                *
      *----------------------------------------------------------------*

           05  @PREFIX-HEADER.
            07     @PREFIX-COD-LAYOUT           PIC  X(08)
                                                      VALUE '@PREFIX'.
            07     @PREFIX-TAM-LAYOUT           PIC  9(05) VALUE @LENGTH.
           05  @PREFIX-REGISTRO.
>>>>>>>     07
            07     @PREFIX-BLOCO-ENTRADA.
            07     @PREFIX-BLOCO-SAIDA.
           05  @PREFIX-DADOS-SESSAO.
            07     @PREFIX-EMPRESA-OPER         PIC  9(005).
            07     @PREFIX-DEPENDENCIA-OPER     PIC  9(005).
            07     @PREFIX-CCANAL               PIC  9(003).
            07     @PREFIX-TIPO-USUAR           PIC  X(001).
            07     @PREFIX-CAUTEN-SEGRC         PIC  X(030).
            07     @PREFIX-TIPO-USUAR-AUTORIZ   PIC  X(001).
            07     @PREFIX-USUARIO-AUTORIZ      PIC  X(030).
            07     @PREFIX-NOPER-FLUXO          PIC  X(040).
            07     @PREFIX-SOLIC-MAIS-DADOS     PIC  X(001).
