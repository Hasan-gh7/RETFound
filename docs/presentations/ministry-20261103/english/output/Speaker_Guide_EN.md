# Diabetic Retinopathy Screening in Syria

## 1. Diabetic Retinopathy Screening in Syria

Present the existing system as a research platform. The meeting seeks a clinical protocol and a local validation partnership, not approval for autonomous diagnosis.



## 2. What we need from this meeting

The platform currently produces one prediction per image. Patient-level workflow, multi-image eye grading and referral policy remain proposed. Local validation must precede claims of Syrian clinical readiness.



## 3. Can the two eyes have different DR grades?

Asymmetric severity is documented. Browning et al. describe a selected case series; it does not estimate prevalence in Syria. The clinical referral rule must be locally agreed and validated.

- R2: Browning et al. · Asymmetric retinopathy, 1988 — https://pubmed.ncbi.nlm.nih.gov/3377038/

## 4. Can DR be present in one eye and absent in the other?

Cases with proliferative retinopathy in one eye and no retinopathy in the fellow eye have been reported. The model result alone cannot explain the cause of asymmetry. This slide concerns diabetic retinopathy, not absence of every possible eye disease.

- R2: Browning et al. · Asymmetric retinopathy, 1988 — https://pubmed.ncbi.nlm.nih.gov/3377038/

## 5. Is one fundus image per eye enough to grade DR?

Adequacy depends on the field, quality and intended task. NHS guidance uses two nominal 45-degree fields for routine digital screening, centred on the fovea and disc; this is an example, not a prescribed Syrian protocol. Distinguish detecting a lesion from excluding DR or determining maximum severity. The current classifier does not independently assess diabetic macular oedema; ask when OCT or further clinical examination is needed.

- R3: NHS · Fundus image quality, updated 2026 — https://www.gov.uk/government/publications/diabetic-eye-screening-pathway-for-images-and-where-images-cannot-be-taken/diabetic-eye-screening-guidance-when-adequate-images-cannot-be-taken

## 6. What if two specialists disagree on the grade?

NHS grading pathways include secondary grading and arbitration. Proposed reference design: independent readers blinded to the AI prediction, with a third specialist resolving disagreements where feasible. Record disagreement on image quality separately from disagreement on disease severity.

- R4: NHS · Grading and arbitration pathways — https://assets.publishing.service.gov.uk/media/668423b903469096e184059d/20230725_Diabetic_eye_screening_pathways_-_patient_grading_referral_surveillance_.pdf

## 7. The minimum dataset

Collect only justified clinical variables; age, diabetes duration/type and available glycaemic control can support subgroup analysis. The model itself uses the image, not these variables. Keep both eyes and repeat visits of a patient within one dataset partition. Check corruption, duplicates and conflicting labels. Size the study statistically; do not invent a fixed image target. Test data must be locked before selecting improvements.



## 8. From local data to a clinical decision

This is a proposed clinical workflow. Existing code checks file integrity, uses Jev for fundus modality admission, then applies RETFound. Jev admission is not validated medical image-quality assessment. Combining multiple images into an eye-level result requires an agreed and tested rule. Preserve original images; retain model and preprocessing versions. A clinician-approved referral protocol is required.



## 9. What is required to start?

No budget, duration or study size is approved. The current API is local. Multi-user access, longitudinal records and referral tracking require additional implementation. Separate training is not required to begin external evaluation of the frozen model.



## 10. Three issues we must resolve

The original RETFound study discusses generalisation limits across cohorts and devices. No project evidence establishes a Syrian genetic cause of model performance differences. Jev runs through OpenRouter and its provider; retention and contractual requirements must be assessed. Current provider failure blocks DR inference; no validated offline replacement is claimed.

- R1: RETFound · Nature, 2023 — https://www.nature.com/articles/s41586-023-06555-x
- R3: NHS · Fundus image quality, updated 2026 — https://www.gov.uk/government/publications/diabetic-eye-screening-pathway-for-images-and-where-images-cannot-be-taken/diabetic-eye-screening-guidance-when-adequate-images-cannot-be-taken

## 11. Every disagreement should lead to action

Review false negatives, under-grading, false rejection, quality failures and a sample of apparent agreements. Keep the original prediction, reader labels, final decision, cause, owner and closure status. Do not automatically retrain on physician corrections. Any model change needs a separate version and independent evaluation.



## 12. Four decisions to close the meeting

Predefine sensitivity, specificity, severity errors, ungradable/rejected images, system failures, referral burden and confidence intervals. Count the entire workflow, not only successfully accepted images. The saved 1000-image APTOS run is RETFound-only: 84.70% exact-grade accuracy, 98.95% any-DR sensitivity and 97.71% specificity; these are not Syrian clinical performance estimates. Patient independence and checkpoint training independence remain unverified. No new inference was performed for this deck.



## 13. Evidence supporting the discussion

R1 supports the need to study generalisation; R2 documents asymmetry without establishing local frequency; R3 is an English screening protocol example; R4 supports documented secondary reading and arbitration. Saved project results are historical research evidence, not a fresh clinical validation.

- R1: RETFound · Nature, 2023 — https://www.nature.com/articles/s41586-023-06555-x
- R2: Browning et al. · Asymmetric retinopathy, 1988 — https://pubmed.ncbi.nlm.nih.gov/3377038/
- R3: NHS · Fundus image quality, updated 2026 — https://www.gov.uk/government/publications/diabetic-eye-screening-pathway-for-images-and-where-images-cannot-be-taken/diabetic-eye-screening-guidance-when-adequate-images-cannot-be-taken
- R4: NHS · Grading and arbitration pathways — https://assets.publishing.service.gov.uk/media/668423b903469096e184059d/20230725_Diabetic_eye_screening_pathways_-_patient_grading_referral_surveillance_.pdf
- P1: Saved project evaluation · 29 October 2026 — results/runs/aptos1000-20261029/predictions.json