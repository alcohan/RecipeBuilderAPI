SELECT
    Recipes.Name
    ,Recipes.RecipeID
    ,Recipes.ImageURL
    ,CAST( CAST(COALESCE(SUM(Ingredients.PortionCost * RecipeIngredients.Quantity),0) as Decimal(5,2)) as float) as Price
    ,CAST( CAST(COALESCE(SUM(Ingredients.Calories * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Calories
    ,CAST( CAST(COALESCE(SUM(Ingredients.TTLFatGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as TTLFat
    ,CAST( CAST(COALESCE(SUM(Ingredients.SatFatGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as SatFat
    ,CAST( CAST(COALESCE(SUM(Ingredients.CholesterolMiligrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Cholesterol
    ,CAST( CAST(COALESCE(SUM(Ingredients.SodiumMiligrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Sodium
    ,CAST( CAST(COALESCE(SUM(Ingredients.CarbohydratesGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Carbohydrates
    ,CAST( CAST(COALESCE(SUM(Ingredients.FiberGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Fiber
    ,CAST( CAST(COALESCE(SUM(Ingredients.SugarGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Sugar
    ,CAST( CAST(COALESCE(SUM(Ingredients.ProteinGrams * RecipeIngredients.Quantity),0) as Decimal(5,1)) as float) as Protein
    ,COALESCE(COUNT(RecipeIngredients.Quantity),0) as IngredientQty
FROM
    Recipes
    LEFT JOIN RecipeIngredients ON Recipes.RecipeID = RecipeIngredients.RecipeID
    LEFT JOIN Ingredients ON RecipeIngredients.IngredientID = Ingredients.IngredientID
WHERE
    IsTemplate = :placeholder
GROUP BY
    Recipes.Name
    ,Recipes.RecipeID
    ,Recipes.ImageURL