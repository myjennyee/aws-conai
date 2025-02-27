The 3 Tables and Columns

table_structure = """
Table_Clash: clashId, clashTestId, clashName, clashIssue, clashDistance, clashGrid, clashLevel, clashPointX, clashPointY, clashPointZ, item1, item2, image, deleteFlg, description, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_ClashTest: clashTestId, clashTestTimeStamp, orgFile, clashTestZone, clashTestName, tolerance, totalClashes, new, active, reviewed, approved, resolved, type, deleteFlg, comment, createdBy, createdDateTime, updatedBy, updatedDateTime
Table_Element: elementId, clashId, clashName, ClashTestId, orgFile, elementItemType, elementCategory, elementFamily, elementType, elementPhase, deleteFlg, comment, createBy, createdDateTime, updatedBy, updatedDateTime
""" 
Table_Element
elementId	clashId	clashName	ClashTestId	orgFile	elementItemType	elementCategory	elementFamily	elementType	elementPhase	deleteFlg	comment	createBy	createdDateTime	updatedBy	updatedDateTime
2385302	f5c0cf8b-e4d9-4546-8a66-f854bf387fc7	Clash2	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-H-0000.nwc	Item2	Pipes	Pipe Types	AWS_Pipe_Carbon Steel	Carbon Steel Pipes For Ordinary Piping(KS D 3507)	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570
2406205	e1f7dfd3-b910-4922-8898-d1797e0eb081	Clash1	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-H-0000.nwc	Item2	Pipes	Pipe Types	AWS_Pipe_Carbon Steel	Carbon Steel Pipes For Ordinary Piping(KS D 3507)	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570
2453697	8f73711b-4d09-4ae9-ac8c-5c3dad10654f	Clash3	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-H-0000.nwc	Item2	Pipes	Pipe Types	AWS_Pipe_Copper	Copper	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570
2521577	8f73711b-4d09-4ae9-ac8c-5c3dad10654f	Clash3	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-M-0000.nwc	Item1	Mechanical Equipment	AWS_MUA_ENCLOSURE	AWS_MUA_ENCLOSURE	Phase - Exist	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570
2521577	e1f7dfd3-b910-4922-8898-d1797e0eb081	Clash1	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-M-0000.nwc	Item1	Mechanical Equipment	AWS_MUA_ENCLOSURE	AWS_MUA_ENCLOSURE	Phase - Exist	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570
2521577	f5c0cf8b-e4d9-4546-8a66-f854bf387fc7	Clash2	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	ICN062-HME-30-XX-M3-M-0000.nwc	Item1	Mechanical Equipment	AWS_MUA_ENCLOSURE	AWS_MUA_ENCLOSURE	Phase - Exist	0	NULL	NULL	2025-02-22 05:20:48.570	NULL	2025-02-22 05:20:48.570

Table_Clash
clashId	clashTestId	clashName	clashIssue	clashDistance	clashGrid	clashLevel	clashPointX	clashPointY	clashPointZ	item1	item2	image	deleteFlg	description	createdBy	createdDateTime	updatedBy	updatedDateTime
8f73711b-4d09-4ae9-ac8c-5c3dad10654f	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash3	N/A	-0.0360	V.A-V.2	V RF	170547.5150	543084.2990	18.8920	2521577	2453697	..\UploadedFiles\Test 1_files\cd000003.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813
e1f7dfd3-b910-4922-8898-d1797e0eb081	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash1	Open	-0.0690	V.A-V.2	V RF	170550.7470	543084.1680	19.0360	2521577	2406205	..\UploadedFiles\Test 1_files\cd000001.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813
f5c0cf8b-e4d9-4546-8a66-f854bf387fc7	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash2	Close	-0.0690	V.A-V.2	V RF	170547.9510	543084.3190	19.0360	2521577	2385302	..\UploadedFiles\Test 1_files\cd000002.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813

Table_ClashTest
clashTestId	clashTestTimeStamp	orgFile	clashTestZone	clashTestName	tolerance	totalClashes	new	active	reviewed	approved	resolved	type	 	deleteFlg	comment	createdBy	createdDateTime	updatedBy	updatedDateTime
b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	2025:02:22 05:20:46	File	SHELL-1	Test 1	0.001m	3	3	0	0	0	0	Hard	0	NULL	NULL	2025-02-22 05:20:48.767	NULL	2025-02-22 05:20:48.767

Please consider those column names and tables and also sample data.
Neglect CreatedDate and UpdatedDate columns, description, deleteFlg columns they are almost useless.
Read Json file and check query from Json with those provided table structure as some columns are mismatched and meaningless columns, not containing columns in tables.
If need please do join conditions Innerjoin, OuterJoins, Leftjoins, Union and others from these 3 related table.
And release me downloadable link to download the prepare Json.


