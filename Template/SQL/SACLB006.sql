CREATE TABLE DB2PRD.TCATEG_MANIF_PSSOA                                          
(                                                                               
 CCATEG_MANIF          DECIMAL(4) NOT NULL,                                     
 CTPO_MANIF_SERVC      DECIMAL(2) NOT NULL,                                     
 CFAML_MANIF_SERVC     DECIMAL(4) NOT NULL,                                     
 CPRODT_MANIF_SERVC    DECIMAL(4) NOT NULL,                                     
 CASSNT_MANIF_SERVC    DECIMAL(4) NOT NULL,                                     
 CSIT_REG              DECIMAL(1) NOT NULL,                                     
 CUSUAR_INCL           CHAR(9) NOT NULL,                                        
 HINCL_REG             TIMESTAMP NOT NULL,                                      
 CUSUAR_MANUT          CHAR(9),                                                 
 HMANUT_REG            TIMESTAMP,                                               
 CONSTRAINT SACLX060  PRIMARY KEY (CCATEG_MANIF),                               
 CONSTRAINT SACLX061  UNIQUE (CTPO_MANIF_SERVC, CFAML_MANIF_SERVC, CPRODT_MANIF_
SERVC, CASSNT_MANIF_SERVC),                                                     
 CONSTRAINT SACL6301  FOREIGN KEY (CTPO_MANIF_SERVC)                            
  REFERENCES DB2PRD.TTPO_MANIF_SERVC  (CTPO_MANIF_SERVC)                        
  ON DELETE RESTRICT,                                                           
 CONSTRAINT SACL1201  FOREIGN KEY (CFAML_MANIF_SERVC)                           
  REFERENCES DB2PRD.TFAML_MANIF_SERVC  (CFAML_MANIF_SERVC)                      
  ON DELETE RESTRICT,                                                           
 CONSTRAINT SACL4801  FOREIGN KEY (CPRODT_MANIF_SERVC)                          
  REFERENCES DB2PRD.TPRODT_MANIF_SERVC  (CPRODT_MANIF_SERVC)                    
  ON DELETE RESTRICT,                                                           
 CONSTRAINT SACL0201  FOREIGN KEY (CASSNT_MANIF_SERVC)                          
  REFERENCES DB2PRD.TASSNT_MANIF_SERVC  (CASSNT_MANIF_SERVC)                    
  ON DELETE RESTRICT                                                            
)                                                                               
 IN SACLD000.SACLS006;                                                          
