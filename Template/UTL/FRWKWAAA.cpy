      ******************************************************************
      *                                                                *
      * NOME BOOK : FRWKWAAA                                           *
      * DESCRICAO : LAYOUT DA AREA DE MEMORIA COM OS DADOS DA SESSAO   *
      *             VERSAO 2 - SUBSTITUI O COPYBOOK I#FRWK83           *
      * DATA      : 13/11/2008                                         *
      * AUTOR     : CARLOS ROBERTO DE MORAES                           *
      * EMPRESA   : CPM/GFT                                            *
      * GRUPO     : TI MELHORIAS                                       *
      * COMPONENTE: FRAMEWORK ONLINE                                   *
      *                                                                *
      ******************************************************************
      *                                                                *
      * FRWKWAAA-REGISTRO.                                             *
      *  FRWKWAAA-CSESS-FRWK         = CODIGO DA SESSAO                *
      *  FRWKWAAA-NOPER-FLUXO        = NUMERO DA OPERACAO              *
      *  FRWKWAAA-CULT-FLUXO-EXTER   = CODIGO FLUXO EXTERNO            *
      *  FRWKWAAA-EMPRESA-OPER       = EMPRESA                         *
      *  FRWKWAAA-DEPENDENCIA-OPER   = DEPENDENCIA                     *
      *  FRWKWAAA-CCANAL             = CANAL                           *
      *  FRWKWAAA-WINFO-DADOS-IDIOM  = IDIOMA                          *
      *  FRWKWAAA-DT-LOCAL           = DATA LOCAL                      *
      *  FRWKWAAA-HR-LOCAL           = HORA LOCAL                      *
      *  FRWKWAAA-FLAG-MONETARIO     = FLAG MONETARIO                  *
      *  FRWKWAAA-SOLIC-MAIS-DADOS   = SOLIC MAIS DADO                 *
      *  FRWKWAAA-TIPO-USUAR         = TIPO USUARIO                    *
      *  FRWKWAAA-CAUTEN-SEGRC       = USUARIO                         *
      *  FRWKWAAA-TIPO-USUAR-AUTORIZ = TIPO USUARIO AUTORIZANTE        *
      *  FRWKWAAA-USUARIO-AUTORIZ    = USUARIO AUTORIZANTE             *
      *  FRWKWAAA-PERFIL-USU-AUTORIZ = PERFIL USUARIO AUTORIZANTE      *
      *  FRWKWAAA-WINFO-DADOS-EMPRE  = DADOS EMPRESA                   *
      *  FRWKWAAA-CODIGO-DEPENDENCIA = DEPENDENCIA EMPRESA             *
      *  FRWKWAAA-WINFO-DADOS-DTSIST = DATA SISTEMA                    *
      *  FRWKWAAA-WINFO-DADOS-DTOPER = DATA OPERACAO                   *
      *  FRWKWAAA-TAM-DISP-BLK-SAIDA = TAMANHO DISPONIVEL              *
      *  FRWKWAAA-FLAG-ASSINATURA    = INDICADOR DE VALIDACAO DA ASSI- *
      *                                NATURA                          *
      *  FRWKWAAA-FLAG-ALCADA        = INDICADOR DE VALIDACAO DA ALCA- *
      *                                DA                              *
      *  FRWKWAAA-EMPR-USUAR-TRAB    = EMPRESA DE TRABALHO DO USUARIO  *
      *  FRWKWAAA-DEPEND-USUAR-TRAB  = DEPENDDENCIA DE TRABALHO USUARIO*
      *  FRWKWAAA-EMPR-OPERANTE      = EMPRESA OPERANTE DO USUARIO     *
      *  FRWKWAAA-DEPEND-OPERANTE    = DEPENDENCIA OPERANTE DO USUARIO *
      *  FRWKWAAA-NIVEL-SEGUR        = NIVEL DE SEGURANCAO DO LOGON    *
      ******************************************************************
      * DATA       AUTOR        MODIFICACAO                            *
      * --------   ---------    -------------------------------------- *
      * DD/MM/AAAA JNNNNNN      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX *
      ******************************************************************
      *
          07 FRWKWAAA-HEADER.
             09  FRWKWAAA-COD-LAYOUT          PIC  X(08)
                 VALUE 'FRWKWAAA'.
             09  FRWKWAAA-TAM-LAYOUT          PIC  9(05)
                 VALUE 263.
      *
          07 FRWKWAAA-REGISTRO.
             09  FRWKWAAA-CSESS-FRWK          PIC  X(32).
             09  FRWKWAAA-NOPER-FLUXO         PIC  X(40).
             09  FRWKWAAA-CULT-FLUXO-EXTER    PIC  X(08).
             09  FRWKWAAA-EMPRESA-OPER        PIC  9(05).
             09  FRWKWAAA-DEPENDENCIA-OPER    PIC  9(05).
             09  FRWKWAAA-CCANAL              PIC  9(03).
             09  FRWKWAAA-WINFO-DADOS-IDIOM   PIC  9(02).
             09  FRWKWAAA-DT-LOCAL            PIC  X(08).
             09  FRWKWAAA-HR-LOCAL            PIC  X(06).
             09  FRWKWAAA-FLAG-MONETARIO      PIC  X(01).
             09  FRWKWAAA-SOLIC-MAIS-DADOS    PIC  X(01).
                88 FRWKWAAA-IDADOS-VALIDOS   VALUES
                                 'N' 'P' 'S' 'A' 'U' 'I'.
                88 FRWKWAAA-SEM-PAGINACAO     VALUE 'N'.
                88 FRWKWAAA-PRIMEIRO-BLOCO    VALUE 'P'.
                88 FRWKWAAA-BLOCO-SEGUINTE    VALUE 'S'.
                88 FRWKWAAA-BLOCO-ANTERIOR    VALUE 'A'.
                88 FRWKWAAA-ULTIMO-BLOCO      VALUE 'U'.
                88 FRWKWAAA-CONSULTA-INICIAL  VALUE 'I'.
             09  FRWKWAAA-TIPO-USUAR          PIC  X(01).
             09  FRWKWAAA-CAUTEN-SEGRC        PIC  X(30).
             09  FRWKWAAA-TIPO-USUAR-AUTORIZ  PIC  X(01).
             09  FRWKWAAA-USUARIO-AUTORIZ     PIC  X(30).
             09  FRWKWAAA-PERFIL-USU-AUTORIZ  PIC  X(08).
             09  FRWKWAAA-WINFO-DADOS-EMPRE   PIC  9(05).
             09  FRWKWAAA-CODIGO-DEPENDENCIA  PIC  9(05).
             09  FRWKWAAA-WINFO-DADOS-DTSIST  PIC  9(08).
             09  FRWKWAAA-WINFO-DADOS-DTOPER  PIC  9(08).
             09  FRWKWAAA-TAM-DISP-BLK-SAIDA  PIC S9(05) COMP-3.
             09  FRWKWAAA-FLAG-ASSINATURA     PIC  X(01).
             09  FRWKWAAA-FLAG-ALCADA         PIC  X(01).
             09  FRWKWAAA-EMPR-USUAR-TRAB     PIC  9(10).
             09  FRWKWAAA-DEPEND-USUAR-TRAB   PIC  9(08).
             09  FRWKWAAA-EMPR-OPERANTE       PIC  9(10).
             09  FRWKWAAA-DEPEND-OPERANTE     PIC  9(08).
             09  FRWKWAAA-NIVEL-SEGUR         PIC  9(02).
      *
      *----------------------------------------------------------------*
