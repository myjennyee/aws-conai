truncate table Table_DataSet
DECLARE @JsonData NVARCHAR(MAX) = N'';
INSERT INTO Table_DataSet (Prompt, Response, DeleteFlg, CreatedDateTime, UpdatedDateTime)
SELECT 
    JSON_VALUE(j.value, '$.prompt') AS Prompt,
    JSON_VALUE(j.value, '$.response') AS Response,
    0 AS DeleteFlg,
    GETDATE() AS CreatedDateTime,
    GETDATE() AS UpdatedDateTime
FROM OPENJSON(@JsonData) AS j;
insert into Table_DataSet (Prompt, Response, DeleteFlg) 
select Prompt,Max( response), 3 from Table_DataSet group by Prompt