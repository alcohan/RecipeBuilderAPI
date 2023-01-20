DELETE FROM TemplateCategoryModifications
WHERE  
    RecipeID = :recipeid
AND
    CategoryID = :categoryid