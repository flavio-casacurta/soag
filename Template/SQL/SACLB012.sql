CREATE TABLE DB2PRD.TFAML_MANIF_SERVC                                           
(                                                                               
 CFAML_MANIF_SERVC     DECIMAL(4) NOT NULL,                                     
 IFAML_MANIF_SERVC     CHAR(50) NOT NULL,                                       
 CSIT_REG              DECIMAL(1) NOT NULL,                                     
 CUSUAR_INCL           CHAR(9) NOT NULL,                                        
 HINCL_REG             TIMESTAMP NOT NULL,                                      
 CUSUAR_MANUT          CHAR(9),                                                 
 HMANUT_REG            TIMESTAMP,                                               
 CONSTRAINT SACLX120  PRIMARY KEY (CFAML_MANIF_SERVC)                           
)                                                                               
 IN SACLD000.SACLS012;                                                          
