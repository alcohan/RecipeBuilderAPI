SELECT 
	[Template].Template as Template
	,[Template].TemplateID -- just used for sorting in the order they were created	
	,SUM([Template].Multiplier * (COALESCE([Target].Price,0) + [Template].Price)) as Price
	,SUM([Template].Multiplier * (COALESCE([Target].Calories,0) + [Template].Calories)) as Calories
	,SUM([Template].Multiplier * (COALESCE([Target].TTLFat,0) + [Template].TTLFat)) as TTLFat
	,SUM([Template].Multiplier * (COALESCE([Target].SatFat,0) + [Template].SatFat)) as SatFat
	,SUM([Template].Multiplier * (COALESCE([Target].Cholesterol,0) + [Template].Cholesterol)) as Cholesterol
	,SUM([Template].Multiplier * (COALESCE([Target].Sodium,0) + [Template].Sodium)) as Sodium
	,SUM([Template].Multiplier * (COALESCE([Target].Carbohydrates,0) + [Template].Carbohydrates)) as Carbohydrates
	,SUM([Template].Multiplier * (COALESCE([Target].Fiber,0) + [Template].Fiber)) as Fiber
	,SUM([Template].Multiplier * (COALESCE([Target].Sugar,0) + [Template].Sugar)) as Sugar
	,SUM([Template].Multiplier * (COALESCE([Target].Protein,0) + [Template].Protein)) as Protein
FROM 
	(
	SELECT --Get all templates with nutrition broken down by category & multiplier as a column
		a.* 
		,COALESCE(TemplateCategoryModifications.QuantityMultiplier,1) as Multiplier
	from 
		( --One row for each Template Category, with associated nutrition by category or NULL if none
			SELECT 
				Recipes.Name as Template
				,Recipes.RecipeID as TemplateID
				,Categories.Name as Category
				,Categories.CategoryID
				,COALESCE([TemplateNutrition].Price,0) as Price
				,COALESCE([TemplateNutrition].Calories,0) as Calories
				,COALESCE([TemplateNutrition].TTLFat,0) as TTLFat
				,COALESCE([TemplateNutrition].SatFat,0) as SatFat
				,COALESCE([TemplateNutrition].Cholesterol,0) as Cholesterol
				,COALESCE([TemplateNutrition].Sodium,0) as Sodium
				,COALESCE([TemplateNutrition].Carbohydrates,0) as Carbohydrates
				,COALESCE([TemplateNutrition].Fiber,0) as Fiber
				,COALESCE([TemplateNutrition].Sugar,0) as Sugar
				,COALESCE([TemplateNutrition].Protein,0) as Protein
			FROM 
				Recipes
				CROSS JOIN Categories
				LEFT JOIN 
					( 
                    --  One row for each Template Category that has some nutrition. 
                    --  Template Categories without nutrition have NULL CategoryID but still appear here
                    --  This is basically the same query as selecting a normal recipe nutrition
					SELECT 
						Recipes.Name as Template
						,Recipes.RecipeID as TemplateID
						,Ingredients.CategoryID
						,COALESCE(SUM(Ingredients.PortionCost * RecipeIngredients.Quantity),0) as Price
						,COALESCE(SUM(Ingredients.Calories * RecipeIngredients.Quantity),0) as Calories
						,COALESCE(SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity),0) as TTLFat
						,COALESCE(SUM(Ingredients.SatFatGrams * RecipeIngredients.Quantity),0) as SatFat
						,COALESCE(SUM(Ingredients.CholesterolMiligrams * RecipeIngredients.Quantity),0) as Cholesterol
						,COALESCE(SUM(Ingredients.SodiumMiligrams * RecipeIngredients.Quantity),0) as Sodium
						,COALESCE(SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity),0) as Carbohydrates
						,COALESCE(SUM(Ingredients.FiberGrams * RecipeIngredients.Quantity),0) as Fiber
						,COALESCE(SUM(Ingredients.SugarGrams * RecipeIngredients.Quantity),0) as Sugar
						,COALESCE(SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity),0) as Protein
					FROM 
						Recipes
						LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    					LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
						LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
					WHERE Recipes.IsTemplate=1
					GROUP BY
						Recipes.Name
						,Recipes.RecipeID
						,Ingredients.CategoryID
					)as [TemplateNutrition]
				ON Categories.CategoryID = [TemplateNutrition].CategoryID
				AND Recipes.RecipeID = [TemplateNutrition].TemplateID
			WHERE IsTemplate=1
			GROUP BY
				Recipes.Name
				,Recipes.RecipeID
				,Categories.Name
				,Categories.CategoryID
				,[TemplateNutrition].Price
				,[TemplateNutrition].Calories
				,[TemplateNutrition].TTLFat
				,[TemplateNutrition].SatFat
				,[TemplateNutrition].Cholesterol
				,[TemplateNutrition].Sodium
				,[TemplateNutrition].Carbohydrates
				,[TemplateNutrition].Fiber
				,[TemplateNutrition].Sugar
				,[TemplateNutrition].Protein
				) as a
	LEFT JOIN TemplateCategoryModifications 
		ON TemplateCategoryModifications.CategoryID = a.CategoryID 
		AND TemplateCategoryModifications.RecipeID = a.TemplateID
	
	) as [Template]

LEFT JOIN

(
	SELECT 
		Recipes.Name
		,Recipes.RecipeID
		,Categories.Name as Category
		,Categories.CategoryID
		,COALESCE(SUM(Ingredients.PortionCost * RecipeIngredients.Quantity) ,0) as Price
		,COALESCE(SUM(Ingredients.Calories * RecipeIngredients.Quantity),0) as Calories
		,COALESCE(SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity),0) as TTLFat
		,COALESCE(SUM(Ingredients.SatFatGrams * RecipeIngredients.Quantity),0) as SatFat
		,COALESCE(SUM(Ingredients.CholesterolMiligrams * RecipeIngredients.Quantity),0) as Cholesterol
		,COALESCE(SUM(Ingredients.SodiumMiligrams * RecipeIngredients.Quantity),0) as Sodium
		,COALESCE(SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity),0) as Carbohydrates
		,COALESCE(SUM(Ingredients.FiberGrams * RecipeIngredients.Quantity),0) as Fiber
		,COALESCE(SUM(Ingredients.SugarGrams * RecipeIngredients.Quantity),0) as Sugar
		,COALESCE(SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity),0) as Protein
	FROM 
		Recipes
		LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
		LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
		LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID
	WHERE 
		Recipes.RecipeID = :placeholder
	GROUP BY
		Recipes.Name
		,Recipes.RecipeID
		,Categories.Name
		,Categories.CategoryID
	) as [Target]

on [Template].CategoryID = [Target].CategoryID
GROUP BY
	[Template].Template
	,[Template].TemplateID
