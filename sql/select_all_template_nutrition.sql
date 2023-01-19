SELECT 
	b.Template as Template,
	b.TemplateID,
	SUM(b.Multiplier * c.Price) as Price,
	SUM(b.Multiplier * c.Calories) as Calories,
	SUM(b.Multiplier * c.TTLFat) as TTLFat,
	SUM(b.Multiplier * c.SatFat) as SatFat,
	SUM(b.Multiplier * c.Cholesterol) as Cholesterol,
	SUM(b.Multiplier * c.Sodium) as Sodium,
	SUM(b.Multiplier * c.Carbohydrates) as Carbohydrates,
	SUM(b.Multiplier * c.Fiber) as Fiber,
	SUM(b.Multiplier * c.Sugar) as Sugar,
	SUM(b.Multiplier * c.Protein) as Protein,
	SUM(b.Multiplier * c.IngredientQty) as IngredientQty
FROM 
(
SELECT 
	a.Template, 
	a.TemplateID,
	a.Category, 
	a.CategoryID, 
	COALESCE(TemplateCategoryModifications.QuantityMultiplier,1) as Multiplier
from 
(
	SELECT 
		Recipes.Name as Template,
		Recipes.RecipeID as TemplateID,
		Categories.Name as Category,
		Categories.CategoryID
	FROM 
		Recipes
		CROSS JOIN Categories
	WHERE IsTemplate=1
) as a
LEFT JOIN TemplateCategoryModifications 
	ON TemplateCategoryModifications.CategoryID = a.CategoryID 
	AND TemplateCategoryModifications.RecipeID = a.TemplateID
) as b
INNER JOIN (
SELECT 
    Recipes.Name,
    Recipes.RecipeID,
	Categories.Name as Category,
	Categories.CategoryID,
    COALESCE(SUM(Ingredients.PortionCost * RecipeIngredients.Quantity),0) as Price,
    COALESCE(SUM(Ingredients.Calories * RecipeIngredients.Quantity),0) as Calories,
    COALESCE(SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity),0) as TTLFat,
    COALESCE(SUM(Ingredients.SatFatGrams * RecipeIngredients.Quantity),0) as SatFat,
    COALESCE(SUM(Ingredients.CholesterolMiligrams * RecipeIngredients.Quantity),0) as Cholesterol,
    COALESCE(SUM(Ingredients.SodiumMiligrams * RecipeIngredients.Quantity),0) as Sodium,
    COALESCE(SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity),0) as Carbohydrates,
    COALESCE(SUM(Ingredients.FiberGrams * RecipeIngredients.Quantity),0) as Fiber,
    COALESCE(SUM(Ingredients.SugarGrams * RecipeIngredients.Quantity),0) as Sugar,
    COALESCE(SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity),0) as Protein,
    COALESCE(SUM(RecipeIngredients.Quantity),0) as IngredientQty
FROM 
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
	LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
WHERE 
    Recipes.RecipeID = :placeholder
GROUP BY
    Recipes.Name,
    Recipes.RecipeID,
	Categories.Name,
	Categories.CategoryID
) as c
on b.CategoryID = c.CategoryID
GROUP BY
	b.Template,
	b.TemplateID
