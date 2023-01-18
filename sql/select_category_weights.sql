SELECT 
	Categories.CategoryID,
	Categories.Name,
	COALESCE(TemplateCategoryModifications.QuantityMultiplier,1) as Multiplier
FROM 
    Categories
LEFT JOIN(
    SELECT * 
    FROM TemplateCategoryModifications 
    WHERE RecipeID= :placeholder 
    ) as TemplateCategoryModifications
ON
    Categories.CategoryID = TemplateCategoryModifications.CategoryID
