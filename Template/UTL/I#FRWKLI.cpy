      ******************************************************                    
      *                                                    *                    
      * NOME BOOK : FRWKGLIV                               *                    
      * DESCRICAO : COPY DE ERROS LIVRES                   *                    
      * DATA      : 29/08/2006                             *                    
      * AUTOR     : CARLA PARALS SENDIN                    *                    
      * EMPRESA   : CPM/GFT                                *                    
      * GRUPO     : TI MELHORIAS                           *                    
      * COMPONENTE: FRAMEWORK ONLINE                       *                    
      *                                                    *                    
      ******************************************************                    
      *                                                    *                    
      * FRWKGLIV-HEADER.                                   *                    
      *   FRWKGLIV-COD-LAYOUT       = CODIGO DE LAYOUT     *                    
      *   FRWKGLIV-TAM-LAYOUT       = TAMANHO DO LAYOUT    *                    
      * FRWKGLIV-REGISTRO.                                 *                    
      *   FRWKGLIV-COD-MENSAGEM     = CÛDIGO DA MENSAGEM   *                    
      *   FRWKGLIV-IDIOMA           = IDIOMA               *                    
      *   FRWKGLIV-PAR-MENSAGEM     = PARAMETROS MENSAGEM  *                    
      *                                                    *                    
      ******************************************************                    
      * DATA       AUTOR        MODIFICACAO                *                    
      * --------   ---------    -------------------------- *                    
      * DD/MM/AAAA JNNNNNN      XXXXXXXXXXXXXXXXXXXXXXXXXX *                    
      ******************************************************                    
       05 FRWKGLIV-HEADER.                                                      
          07 FRWKGLIV-COD-LAYOUT PIC X(008) VALUE 'FRWKGLIV'.                   
          07 FRWKGLIV-TAM-LAYOUT PIC 9(005) VALUE 526.                          
       05 FRWKGLIV-REGISTRO.                                                    
          07 FRWKGLIV-COD-MENSAGEM      PIC X(08).                              
          07 FRWKGLIV-IDIOMA            PIC 9(05).                              
          07 FRWKGLIV-PARAMETROS        PIC X(500).                             
