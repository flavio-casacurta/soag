      ******************************************************************        
      *                                                                *        
      * NOME BOOK : I#FRWK04                                           *        
      * DESCRICAO : COPY DO GESTOR DAS AREAS DE MEMORIA                *        
      * DATA      : 01/06/2006                                         *        
      * AUTOR     : ALEXANDRE CITRIN ENK                               *        
      * EMPRESA   : CPM/GFT                                            *        
      * GRUPO     : TI MELHORIAS                                       *        
      * COMPONENTE: FRAMEWORK ONLINE                                   *        
      *                                                                *        
      ******************************************************************        
      *                                                                *        
      * FRWKGL04-HEADER                = CODIGO DO LAYOUT              *        
      *  FRWKGL04-COD-LAYOUT           = IDENTIFICADOR LAYOUT FRAMEWORK*        
      *  FRWKGL04-TAM-LAYOUT           = TAMANHO LAYOUT FRAMEWORK      *        
      * FRWKGL04-REGISTRO.                                             *        
      *  FRWKGL04-BLOCO-RETORNO.                                       *        
      *    FRWKEL04-COD-RETORNO        = CODIGO DE RETORNO             *        
      *    FRWKEL04-COD-ERRO           = CODIGO DE ERRO                *        
      *    FRWKEL04-MENSAGEM           = MENSAGEM DE ERRO              *        
      *  FRWKGL04-BLOCO-ENTRADA.                                       *        
      *    FRWKEL04-COD-LAYOUT           = IDENTIFICADOR DO BLOCO      *        
      *    FRWKEL04-TAM-LAYOUT           = TAMANHO DO BLOCO            *        
      *    FRWKEL04-IDENT-AREA-GLOBAL    = POINTER DA AREA GLOBAL OU   *        
      *                                    NOME DO CHANNEL             *        
      *    FRWKEL04-FUNCAO               = FUNCAO QUE SERA EXECUTADA   *        
      *                                    'CO' - CONSULTA             *        
      *                                    'CL' - CONSULTAR E LIBERAR  *        
      *                                    'CR' - CRIAR                *        
      *                                    'AT' - ATUALIZAR            *        
      *                                    'LI' - LIBERAR MEMORIA      *        
      *    FRWKEL04-PERM-ACESSO          = PERMISSAO DE ACESSO.        *        
      *                                    'C' CONSULTAR               *        
      *                                    'A' ATUALIZAR               *        
      *                                    'R' RESTRITO                *        
      *    FRWKEL04-IND-BLOCO            = INDICADOR BLOCO SAIDA       *        
      *                                    '1' - BLOCO DE SAIDA        *        
      *                                    '2' - BLOCO DE MENSAGENS    *        
      *                                    '3' - BLOCO PERSISTENTE     *        
      *                                    '4' - BLOCO POS-TRANSACAO   *        
      *                                    '5' - BLOCO RASTREABILIDADE *        
      *                                    '6' - BLOCO AUTORIZACAO     *        
      *                                    '9' - OUTROS                *        
      *    FRWKEL04-ID-BLOCO             = IDENT BLOCO DA FUNCAO       *        
      *  FRWKEL04-BLOCO-SAIDA.                                         *        
      *    FRWKEL04-TAM-BLOCO            = TAMANHO BLOCO SOLICITADO    *        
      *    FRWKEL04-BUFFER               = CONTEUDO DO BLOCO           *        
      ******************************************************************        
      * DATA       AUTOR        MODIFICACAO                            *        
      * --------   ---------    --------------------------             *        
      * DD/MM/AAAA JNNNNNN      XXXXXXXXXXXXXXXXXXXXXXXXXX             *        
      ******************************************************************        
         05  FRWKEL04-BLOCOS-FIXOS.                                             
           07  FRWKEL04-HEADER.                                                 
              09  FRWKEL04-COD-LAYOUT              PIC X(008)                   
                  VALUE 'FRWKEL04'.                                             
              09  FRWKEL04-TAM-LAYOUT              PIC 9(005)                   
                  VALUE 60.                                                     
           07  FRWKEL04-REGISTRO.                                               
              09  FRWKEL04-BLOCO-RETORNO.                                       
                  11  FRWKEL04-COD-RETORNO         PIC 9(002).                  
                  11  FRWKEL04-COD-ERRO            PIC X(004).                  
                  11  FRWKEL04-COD-MENSAGEM        PIC X(008).                  
              09  FRWKEL04-BLOCO-ENTRADA.                                       
                  11  FRWKEL04-IDENT-AREA-GLOBAL   PIC X(016).                  
                  11  FRWKEL04-FUNCAO              PIC X(002).                  
                      88 FRWKEL04-FUNCAO-VALIDA    VALUES                       
                                     'CO' 'CL' 'CR' 'AT' 'LI'.                  
                      88 FRWKEL04-FUN-CONSULTAR    VALUE 'CO'.                  
                      88 FRWKEL04-FUN-CONS-LIBERAR VALUE 'CL'.                  
                      88 FRWKEL04-FUN-CRIAR        VALUE 'CR'.                  
                      88 FRWKEL04-FUN-ATUALIZAR    VALUE 'AT'.                  
                      88 FRWKEL04-FUN-LIBERAR      VALUE 'LI'.                  
                  11  FRWKEL04-PERM-ACESSO         PIC X(001).                  
                      88 FRWKEL04-PERM-VALIDA      VALUES                       
                                                  'C' 'A' 'R'.                  
                      88 FRWKEL04-PERM-CONSULTAR   VALUE  'C'.                  
                      88 FRWKEL04-PERM-ATUALIZAR   VALUE  'A'.                  
                      88 FRWKEL04-PERM-RESTRITO    VALUE  'R'.                  
                  11  FRWKEL04-IND-BLOCO           PIC X(001).                  
                      88 FRWKEL04-IND-BL-VALIDO    VALUE                        
                                  '1' '2' '3' '4' '5' '6' '9'.                  
                      88 FRWKEL04-IND-BL-SAIDA     VALUE  '1'.                  
                      88 FRWKEL04-IND-BL-MENS      VALUE  '2'.                  
                      88 FRWKEL04-IND-BL-PERS      VALUE  '3'.                  
                      88 FRWKEL04-IND-BL-POS       VALUE  '4'.                  
                      88 FRWKEL04-IND-BL-RASTRE    VALUE  '5'.                  
                      88 FRWKEL04-IND-BL-AUTORIZ   VALUE  '6'.                  
                      88 FRWKEL04-IND-BL-OUTRO     VALUE  '9'.                  
                  11  FRWKEL04-ID-BLOCO            PIC X(008).                  
              09  FRWKEL04-BLOCO-ENTRADA-SAIDA.                                 
                  11  FRWKEL04-TAM-BLOCO           PIC 9(005).                  
         05  FRWKEL04-BLOCO-VARIAVEL.                                           
           07  FRWKEL04-BLOCO-SAIDA.                                            
              09  FRWKEL04-BUFFER.                                              
                  13 FRWKEL04-FILLER  PIC X(001)                                
                                          OCCURS 0 TO 32707 TIMES               
                                       DEPENDING ON FRWKEL04-TAM-BLOCO.         
