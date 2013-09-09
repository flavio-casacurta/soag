      *================================================================*
      *@CONTRATANTE
      *================================================================*
      * IDENTIFICACAO:                                                 *
      * NOME DA AREA DE COMUNICACAO...: @PREFIX
      * OBJETIVO DA AREA DE TRABALHO..: SAIDA DO COORDENADOR           *
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
      *--------------------------------------------------------------- *
      * ALTERACOES:                                                    *
      *                                                                *
      * DATA            NOME               DESCRICAO                   *
      * ==========  =================  ==============================  *
      * 99/99/9999  XXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  *
      *                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  *
      *--------------------------------------------------------------- *
      * DESCRICAO DA AREA DE TRABALHO:                                 *
      *                                                                *
@REMARKS
      *                                                                *
      *--------------------------------------------------------------- *
           05  @PREFIX-HEADER.
            07     @PREFIX-COD-LAYOUT           PIC  X(08)
                                                 VALUE '@PREFIX'.
            07     @PREFIX-TAM-LAYOUT           PIC  9(05) VALUE @LENGTH.
           05  @PREFIX-REGISTRO.
@FIELDS
