      ******************************************************                    
      *                                                    *                    
      * NOME BOOK : FRWKGLAQ                               *                    
      * DESCRICAO : COMMAREA DE COMPONENTES TECNICOS E     *                    
      *             MODULOS FUNCIONAIS                     *                    
      * DATA      : 29/08/2006                             *                    
      * AUTOR     : CARLA PARALS SENDIN                    *                    
      * EMPRESA   : CPM/GFT                                *                    
      * GRUPO     : TI MELHORIAS                           *                    
      * COMPONENTE: FRAMEWORK ONLINE                       *                    
      *                                                    *                    
      ******************************************************                    
      *                                                    *                    
      * FRWKGLAQ-HEADER.                                   *                    
      *   FRWKGLAQ-COD-LAYOUT       = CODIGO DE LAYOUT     *                    
      *   FRWKGLAQ-TAM-LAYOUT       = TAMANHO DO LAYOUT    *                    
      * FRWKGLAQ-REGISTRO.                                 *                    
      *  FRWKGLAQ-BLOCO-ENTRADA.                           *                    
      *   FRWKGLAQ-IDENT-AREA-GLOBAL=POINTER DA AREA GLOBAL*                    
      *  FRWKGLAQ-BLOCO-SAIDA.                             *                    
      *   FRWKGLAQ-PROTOCOLO       = PROTOCOLO             *                    
      *  FRWKGLAQ-BLOCO-RETORNO.                           *                    
      *   FRWKGLAQ-COD-RETORNO     = CÛDIGO DE RETORNO     *                    
      *   FRWKGLAQ-COD-ERRO        = CÛDIGO DE ERRO        *                    
      *   FRWKGLAQ-COD-MENSAGEM    = CÛDIGO DA MENSAGEM    *                    
      *                                                    *                    
      ******************************************************                    
      * DATA       AUTOR        MODIFICACAO                *                    
      * --------   ---------    -------------------------- *                    
      * DD/MM/AAAA JNNNNNN      XXXXXXXXXXXXXXXXXXXXXXXXXX *                    
      ******************************************************                    
       05 FRWKGLAQ-HEADER.                                                      
          07 FRWKGLAQ-COD-LAYOUT PIC X(008) VALUE 'FRWKGLAQ'.                   
          07 FRWKGLAQ-TAM-LAYOUT PIC 9(005) VALUE 61.                           
       05 FRWKGLAQ-REGISTRO.                                                    
          07 FRWKGLAQ-BLOCO-RETORNO.                                            
             09 FRWKGLAQ-COD-RETORNO         PIC 9(002).                        
             09 FRWKGLAQ-COD-ERRO            PIC X(004).                        
             09 FRWKGLAQ-COD-MENSAGEM        PIC X(008).                        
          07 FRWKGLAQ-BLOCO-ENTRADA.                                            
             09 FRWKGLAQ-IDENT-AREA-GLOBAL   PIC X(016).                        
          07 FRWKGLAQ-BLOCO-SAIDA.                                              
             09 FRWKGLAQ-PROTOCOLO           PIC 9(018).                        
