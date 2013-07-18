from django.db import models

disease_list = ["breast_cancer", "lung_cancer", "prostate_cancer", "type_2_diabetes", "gastric_cancer", "hypertension", "stroke", "colon_cancer", "rheumatoid_arthritis", "chronic_kidney_disease", "chronic_obstructive_pulmonary_disease", "ovarian_cancer", "thyroid_cancer", "bladder_cancer", "uterus_cancer", "chronic_liver_disease", "nephritis", "coronary_heart_disease"]### Specify disease_list
#disease_list = ["breast_cancer", "lung_cancer"]
add_list = ["atrial_fibrillation", "scleroderma", "psoriasis", "alzheimer", "macular_degeneration", "restless_leg_syndrome", "crohn_disease", "esophageal_squamous_cell_carcinoma", "melanoma", "multiple_sclerosis", "exfoliation_glaucoma", "type_1_diabetes", "celiac_disease", "obesity", "venous_thromboembolism", "gallstones", "parkinson_disease", "ulcerative_colitis", "bipolar_disorder", "primary_biliary_cirrhosis", "systemic_lupus_erythematosus"]
disease_list.extend(add_list)


for di in disease_list:
	if di.find("_")!= -1:
		temp_dn = di.split("_")
		dn = " ".join(temp_dn).title()
	else:
		temp_dn = di.title()
	d = Disease(disease_id=di, disease_name=dn)
	d.save()
 
