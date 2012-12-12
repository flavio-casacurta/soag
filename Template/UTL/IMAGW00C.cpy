      *****************************************************************
      * NOME BOOK : IMAGW00C - BLOCO DE CONTROLE DE PROCESSAMENTO     *
      *                                                               *
      * DESCRICAO : AREA DE USO COMUM PARA RECEBIMENTO DE DADOS DO    *
      *             FRAMEWORK E PASSAGEM DO CONTROLE PARA PROGRAMA    *
      *             CORRESPONDENTE, BEM COMO O RETORNO PARA A ORI-    *
      *             GEM.                                              *
      * DATA      : 09/2011                                           *
      * AUTOR     : HOMI INFORMATICA                                  *
      * EMPRESA   : XXXXXXXXXXX                                       *
      * GRUPO     : XXXXXXXXXXXXX                                     *
      * COMPONENTE: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX          *
      * TAMANHO   : 27 BYTES                                          *
      *****************************************************************
      * IMAGW00C-COD-LAYOUT     = CODIGO DESTE LAYOUT                 *
      * IMAGW00C-TAM-LAYOUT     = TAMANHO DO REGISTRO                 *
      *                                                               *
      * IMAGW00C-COD-RETORNO    = CODIGO DE RETORNO PARA ORIGEM       *
      * IMAGW00C-COD-ERRO       = CODIGO DE ERRO PARA ORIGEM          *
      * IMAGW00C-COD-MENSAGEM   = CODIGO DE MENSAGEM PARA ORIGEM      *
      *                                                               *
      *****************************************************************
      * DATA       AUTOR             DESCRICAO / MANUTENCAO           *
      *****************************************************************
      * XX/XX/XXXX XXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX *
      *****************************************************************
           05  IMAGW00C-HEADER.
               10  IMAGW00C-COD-LAYOUT     PIC X(008) VALUE 'IMAGW00C'.
               10  IMAGW00C-TAM-LAYOUT     PIC 9(005) VALUE 27.
           05  IMAGW00C-BLOCO-RETORNO.
               10  IMAGW00C-COD-RETORNO    PIC 9(002).
               10  IMAGW00C-COD-ERRO       PIC X(004).
               10  IMAGW00C-COD-MENSAGEM   PIC X(008).
