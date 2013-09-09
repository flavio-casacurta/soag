      ******************************************************                    
      *                                                    *                    
      * NOME BOOK : FRWKGL83                               *                    
      * DESCRICAO : LAYOUT DA AREA DE MEMORIA COM OS DADOS *                    
      *             DA SESSAO                              *                    
      * DATA      : 10/07/2006                             *                    
      * AUTOR     : ALEXANDRE CITRIN ENK                   *                    
      * EMPRESA   : CPM/GFT                                *                    
      * GRUPO     : TI MELHORIAS                           *                    
      * COMPONENTE: FRAMEWORK ONLINE                       *                    
      *                                                    *                    
      ******************************************************                    
      *                                                    *                    
      * FRWKEL83-REGISTRO.                                 *                    
      *  FRWKEL83-CSESS-FRWK         = CODIGO DA SESSAO    *                    
      *  FRWKEL83-NOPER-FLUXO        = NUMERO DA OPERACAO  *                    
      *  FRWKEL83-CULT-FLUXO-EXTER   = CODIGO FLUXO EXTERNO*                    
      *  FRWKEL83-EMPRESA-OPER       = EMPRESA             *                    
      *  FRWKEL83-DEPENDENCIA-OPER   = DEPENDENCIA         *                    
      *  FRWKEL83-CCANAL             = CANAL               *                    
      *  FRWKEL83-WINFO-DADOS-IDIOM  = IDIOMA              *                    
      *  FRWKEL83-DT-LOCAL           = DATA LOCAL          *                    
      *  FRWKEL83-HR-LOCAL           = HORA LOCAL          *                    
      *  FRWKEL83-FLAG-MONETARIO     = FLAG MONETARIO      *                    
      *  FRWKEL83-SOLIC-MAIS-DADOS   = SOLIC MAIS DADO     *                    
      *  FRWKEL83-TIPO-USUAR         = TIPO USUARIO        *                    
      *  FRWKEL83-CAUTEN-SEGRC       = USUARIO             *                    
      *  FRWKEL83-TIPO-USUAR-AUTORIZ = TIPO USUARIO AUTORIZ*                    
      *  FRWKEL83-USUARIO-AUTORIZ    = USUARIO AUTORIZ     *                    
      *  FRWKEL83-PERFIL-USU-AUTORIZ = PERFIL USUARIO AUTOR*                    
      *  FRWKEL83-WINFO-DADOS-EMPRE  = DADOS EMPRESA       *                    
      *  FRWKEL83-CODIGO-DEPENDENCIA = DEPENDENCIA EMPRESA *                    
      *  FRWKEL83-WINFO-DADOS-DTSIST = DATA SISTEMA        *                    
      *  FRWKEL83-WINFO-DADOS-DTOPER = DATA OPERACAO       *                    
      *  FRWKEL83-TAM-DISP-BLK-SAIDA = TAMANHO DISPONIVEL  *                    
      ******************************************************                    
      * DATA       AUTOR        MODIFICACAO                *                    
      * --------   ---------    -------------------------- *                    
      * DD/MM/AAAA JNNNNNN      XXXXXXXXXXXXXXXXXXXXXXXXXX *                    
      ******************************************************                    
          07 FRWKEL83-HEADER.                                                   
             09  FRWKEL83-COD-LAYOUT          PIC  X(08)                        
                 VALUE 'FRWKEL83'.                                              
             09  FRWKEL83-TAM-LAYOUT          PIC  9(05)                        
                 VALUE 225.                                                     
          07 FRWKEL83-REGISTRO.                                                 
             09  FRWKEL83-CSESS-FRWK          PIC  X(32).                       
             09  FRWKEL83-NOPER-FLUXO         PIC  X(40).                       
             09  FRWKEL83-CULT-FLUXO-EXTER    PIC  X(08).                       
             09  FRWKEL83-EMPRESA-OPER        PIC  9(05).                       
             09  FRWKEL83-DEPENDENCIA-OPER    PIC  9(05).                       
             09  FRWKEL83-CCANAL              PIC  9(03).                       
             09  FRWKEL83-WINFO-DADOS-IDIOM   PIC  9(02).                       
             09  FRWKEL83-DT-LOCAL            PIC  X(08).                       
             09  FRWKEL83-HR-LOCAL            PIC  X(06).                       
             09  FRWKEL83-FLAG-MONETARIO      PIC  X(01).                       
             09  FRWKEL83-SOLIC-MAIS-DADOS    PIC  X(01).                       
                88 FRWKEL83-IDADOS-VALIDOS   VALUES                             
                                 'N' 'P' 'S' 'A' 'U' 'I'.                       
                88 FRWKEL83-SEM-PAGINACAO     VALUE 'N'.                        
                88 FRWKEL83-PRIMEIRO-BLOCO    VALUE 'P'.                        
                88 FRWKEL83-BLOCO-SEGUINTE    VALUE 'S'.                        
                88 FRWKEL83-BLOCO-ANTERIOR    VALUE 'A'.                        
                88 FRWKEL83-ULTIMO-BLOCO      VALUE 'U'.                        
                88 FRWKEL83-CONSULTA-INICIAL  VALUE 'I'.                        
             09  FRWKEL83-TIPO-USUAR          PIC  X(01).                       
             09  FRWKEL83-CAUTEN-SEGRC        PIC  X(30).                       
             09  FRWKEL83-TIPO-USUAR-AUTORIZ  PIC  X(01).                       
             09  FRWKEL83-USUARIO-AUTORIZ     PIC  X(30).                       
             09  FRWKEL83-PERFIL-USU-AUTORIZ  PIC  X(08).                       
             09  FRWKEL83-WINFO-DADOS-EMPRE   PIC  9(05).                       
             09  FRWKEL83-CODIGO-DEPENDENCIA  PIC  9(05).                       
             09  FRWKEL83-WINFO-DADOS-DTSIST  PIC  9(08).                       
             09  FRWKEL83-WINFO-DADOS-DTOPER  PIC  9(08).                       
             09  FRWKEL83-TAM-DISP-BLK-SAIDA  PIC S9(05) COMP-3.                
             09  FRWKEL83-FLAG-ASSINATURA     PIC  X(01).                       
             09  FRWKEL83-FLAG-ALCADA         PIC  X(01).                       
