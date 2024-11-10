# Experimental data
The experimental data used to train EPI Suite models are available [here](https://episuite.dev/EpiWebSuite/#/help/associated-databases). We provide an interface to access the data directly within the package. Here's a quote from the EPI Suite website:
> The EPIUnified database holds the combined values from: PhysProp and the available EPI Suite™ model Training and Validation sets.  
The data sets available are:  
**WSKOWWIN**: WSKOWWIN Program Methodology & Validation Documents (includes Training & Validation datasets)  
**WaterFragmentDataFiles**: WATERNT (Water Solubility Fragment) Program Methodology & Validation Documents (includes Training & Validation datasets) BioHCwin - estimates biodegradation of hydrocarbons  
**MP-BP-VP-TestSets**: MPBPWIN (Melting Pt, Boiling Pt, Vapor Pressure) Program Test Sets  
**Data_for_BCFBAF**: BCFBAF Excel spreadsheets of BCF and kM data used in training & validation (includes the Jon Arnot Source BCF DB with multiple BCF values)  
**HENRYWIN_Data_EPI**: HENRYWIN Data files used in training & validation (includes Meylan and Howard (1991) Data document)  

# Headers
CAS		-	Chemical Abstract Service Registry number (the few numbers below 000050-00-0 are not real CAS numbers, but used to designate compounds with no CAS number or an unknown CAS number; these designated numbers can be retrieved from the SRC SMILECAS database).  

CLASS	-	An arbitrary classification of compounds by structure.  Many compounds overlap individual classes.  In general, compounds that are drugs or pesticides are assigned to those classes.  Anilines were given precedence over phenols which were given precedence over nitrobenzenes, etc.  The class numbers are as follows:  
                1.  Alkanes				24.  Haloalcohols, aliphatic
                2.  Haloalkanes				25.  Nitriles
                3.  Alkenes				26.  Misc Nitrogens
                4.  Haloalkenes				27.  Pyridines
                5.  Alkynes				30.  Drugs
                6.  Ethers, aliphatic			31.  Dyes
                7.  Nitroso				32.  Steroids
                8.  Pesticides				34.  Amino acids
                9.  Biphenyls				35.  Misc Aromatics
                10.  PAHs				37.  Thioureas
                11.  Alkyl Benzenes			38.  Multiply aliphatic -OH
                12.  Halobenzenes			40.  Misc. Sulfur
                13.  Misc. Benzenes			41.  Phosphorus
                14.  Amines, aliphatic			42.  Naphthalenes
                15.  Anilines				43.  Cholic acids
                16.  Phenols				44.  Dioxins & Benzofurans
                17.  Acids, aliphatic			45.  Nitrobenzenes
                18.  Acids, aromatic			47.  Amides
                19.  Alcohols, aliphatic			48.  Ureas
                20.  Aldehydes				49.  Nitro, aliphatic
                21.  Esters				50.  Aromatic sulfonamides
                22.  Ketones				51.  Glycolamide esters
                23.  Epoxides

LOGP		-	measured log Kow value  
LOGMOLAR  -	logarithm of the measured water solubility in molar units  
ESTIMATE	-	water solubility estimate (in molar units) using equation 20  
ERROR		-	the difference between LOGMOLAR and ESTIMATE  
WSOL		-	the measured water solubility in units of mg/L  
MP			-	the melting point in oC;  "Liq" refers to liquids (MP < 25oC)  
MOLWT	-	the molecular weight of the compound  
