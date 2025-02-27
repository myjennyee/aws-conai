Create datasets under the following scopes

• Table Reports
Summary of clashes per day/week/month
Clash details with filters (date, type, status, location)
New vs. resolved clashes
Breakdown by item type
Clashes involving specific items or layers

• Risk Reports
High-risk clashes (frequency, location)
Longest unresolved clashes
Clashes in critical areas, locations
Frequent clash components

• Clash Trend Reports
Trend of new vs. resolved clashes
Heatmap or Overview of frequent clash locations
Trend by clash type

• Estimation & Forecasting
Impact of unresolved clashes
Future clash estimation

• Static Data Summary with links
Overview of today's clashes
Status report per project phase

Sample User Queries
Summary of today's clashes
Most frequent clash components
New vs. resolved clashes in last month
Risk report for unresolved clashes
Clash frequency trends (1,2,3 months…).


My Core Tables and Columns

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

Table_ClashTest
clashId	clashTestId	clashName	clashIssue	clashDistance	clashGrid	clashLevel	clashPointX	clashPointY	clashPointZ	item1	item2	image	deleteFlg	description	createdBy	createdDateTime	updatedBy	updatedDateTime
8f73711b-4d09-4ae9-ac8c-5c3dad10654f	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash3	N/A	-0.0360	V.A-V.2	V RF	170547.5150	543084.2990	18.8920	2521577	2453697	..\UploadedFiles\Test 1_files\cd000003.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813
e1f7dfd3-b910-4922-8898-d1797e0eb081	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash1	N/A	-0.0690	V.A-V.2	V RF	170550.7470	543084.1680	19.0360	2521577	2406205	..\UploadedFiles\Test 1_files\cd000001.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813
f5c0cf8b-e4d9-4546-8a66-f854bf387fc7	b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	Clash2	N/A	-0.0690	V.A-V.2	V RF	170547.9510	543084.3190	19.0360	2521577	2385302	..\UploadedFiles\Test 1_files\cd000002.jpg	0	NULL	NULL	2025-02-22 05:20:48.813	NULL	2025-02-22 05:20:48.813

Table_Clash
clashTestId	clashTestTimeStamp	orgFile	clashTestZone	clashTestName	tolerance	totalClashes	new	active	reviewed	approved	resolved	type	 	deleteFlg	comment	createdBy	createdDateTime	updatedBy	updatedDateTime
b4c15dde-5e2e-4ce6-abf1-f52d9c939fbc	2025:02:22 05:20:46	File	SHELL-1	Test 1	0.001m	3	3	0	0	0	0	Hard	0	NULL	NULL	2025-02-22 05:20:48.767	NULL	2025-02-22 05:20:48.767

Structure it into input-output pairs (e.g., NL user query → SQL
query). Must cover all the Category I explained and should be
10000 pairs at least.
{"prompt": "Show me unresolved clashes in Zone A", "response": "SELECT * FROM Table_Clash WHERE
Status='Unresolved' AND Location='Zone A'"}
{"prompt": "List high-risk clashes found today", "response": "SELECT * FROM Table_Clash WHERE Risk_Level='High'
AND Date=GETDATE()"}
{"prompt": "How many clashes were resolved this week?", "response": "SELECT COUNT(*) FROM Table_Clash
WHERE Status='Resolved' AND Date >= DATEADD(DAY, -7, GETDATE())"}

I wanna create those dataset upto 1000Lines.
if too much to generate in once, create 100 Lines first.

The user requests might start under those following words ,
Calculate
Include
Write
Persist
Summarize
Progress
Skim
Scan
Load
Make
Do
Get
Show
Retrieve
Estimate
Predict
Forecast
Gain
Mention
List up
Simulate
Make Chart
Show a Pie Chart
Make a table
Make graph
Compare with Table 
Show with Table
Show with Pie Chart
Show with graph
Do a Table
Do a Pie chart 
So a Table 


Fetch
Obtain
Acquire
Collect
Gather
Access
Pull
Load
Extract
Capture
Recover
Fetch
Procure
Reclaim
Snag (informal)
Derive
Receive