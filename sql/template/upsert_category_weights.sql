MERGE TemplateCategoryModifications AS [Target]
	USING (
		SELECT RecipeID=:recipeid,
		CategoryID=:categoryid, 
		QuantityMultiplier=:multiplier
		) AS [Source]
ON [Target].CategoryID = [Source].CategoryID
	AND [Target].RecipeID = [Source].RecipeID
WHEN MATCHED THEN
UPDATE SET 
	[Target].QuantityMultiplier = [Source].QuantityMultiplier
WHEN NOT MATCHED THEN
	INSERT (RecipeID, CategoryID, QuantityMultiplier) 
	VALUES ([Source].RecipeID, [Source].CategoryID, [Source].QuantityMultiplier) ;