SELECT 
	Categories.CategoryID
	,Categories.Name
	,Categories.ColorHex
	,Count(Ingredients.IngredientID) as ItemsQty
FROM Categories
	LEFT JOIN Ingredients
	ON Ingredients.CategoryID = Categories.CategoryID
GROUP BY
	Categories.CategoryID
	,Categories.Name
	,Categories.SortOrder
	,Categories.ColorHex
ORDER BY
	SortOrder