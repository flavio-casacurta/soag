CREATE TABLE DB2PRD.TASSNT_MANIF_SERVC                                          
(                                                                               
 CASSNT_MANIF_SERVC    DECIMAL(4) NOT NULL,                                     
 IASSNT_MANIF_SERVC    CHAR(100) NOT NULL,                                      
 CSIT_REG              DECIMAL(1) NOT NULL,                                     
 CUSUAR_INCL           CHAR(9) NOT NULL,                                        
 HINCL_REG             TIMESTAMP NOT NULL,                                      
 CUSUAR_MANUT          CHAR(9),                                                 
 HMANUT_REG            TIMESTAMP,                                               
 CONSTRAINT SACLX020  PRIMARY KEY (CASSNT_MANIF_SERVC)                          
)                                                                               
 IN SACLD000.SACLS002;                                                          
