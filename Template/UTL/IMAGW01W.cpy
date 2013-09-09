      *---------------------------------------------------------------*         
      * AREAS PARA TRATAMENTO DE ERROS E ACIONAMENTO DA API 'FRWK1999'*         
      *---------------------------------------------------------------*         
       01  WRK-PARAGRAFO               PIC X(30) VALUE SPACES.                  
       01  WRK-AREA-ERRO.                                                       
           COPY 'I#FRWKGE'.                                                     
           03  WRK-BLOCO-INF-ERRO.                                              
            05 WRK-CHAR-INFO-ERRO      PIC X(01) OCCURS 0 TO 30000 TIMES        
                                       DEPENDING ON FRWKGHEA-TAM-DADOS.         
                                                                                
       01  WRK-COPY-DB2.                                                        
           03  WRK-AREA-ERRO-DB2.                                               
            COPY 'I#FRWKDB'.                                                    
                                                                                
       01  WRK-COPY-CICS.                                                       
           03 WRK-AREA-ERRO-CICS.                                               
           COPY 'I#FRWKCI'.                                                     
                                                                                
       01  WRK-COPY-MOD.                                                        
           03  WRK-AREA-ERRO-MOD.                                               
           COPY 'I#FRWKMD'.                                                     
                                                                                
       01  WRK-COPY-LIV.                                                        
           03  WRK-AREA-ERRO-LIV.                                               
           COPY 'I#FRWKLI'.                                                     
