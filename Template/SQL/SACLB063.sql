CREATE TABLE DB2PRD.TTPO_MANIF_SERVC                                            
(                                                                               
 CTPO_MANIF_SERVC      DECIMAL(2) NOT NULL,                                     
 ITPO_MANIF_SERVC      CHAR(50) NOT NULL,                                       
 CSIT_REG              DECIMAL(1) NOT NULL,                                     
 CUSUAR_INCL           CHAR(9) NOT NULL,                                        
 HINCL_REG             TIMESTAMP NOT NULL,                                      
 CUSUAR_MANUT          CHAR(9),                                                 
 HMANUT_REG            TIMESTAMP,                                               
 CONSTRAINT SACLX630  PRIMARY KEY (CTPO_MANIF_SERVC)                            
)                                                                               
 IN SACLD000.SACLS063;                                                          
