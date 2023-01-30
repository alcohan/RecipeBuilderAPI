SELECT 
    Ingredients.Calories
    ,Ingredients.CarbohydratesGrams
    ,Ingredients.CasePrice
    ,Ingredients.CaseSize
    ,Ingredients.CategoryID
    ,Categories.Name as Category
    ,Ingredients.CholesterolMiligrams
    ,Ingredients.FiberGrams
    ,Ingredients.ImageURL
    ,Ingredients.IngredientID
    ,Ingredients.Name
    ,Ingredients.PortionCost
    ,Ingredients.PortionSize
    ,Ingredients.PortionUtensil
    ,Ingredients.PortionVolume
    ,Ingredients.PortionWeight
    ,Ingredients.ProteinGrams
    ,Ingredients.SatFatGrams
    ,Ingredients.SodiumMiligrams
    ,Ingredients.SugarGrams
    ,Ingredients.TTLFatGrams
    ,Ingredients.Unit
    ,Ingredients.YieldPercent
    ,Ingredients.PortionsPerCase
FROM 
    Ingredients
LEFT JOIN
    Categories
ON
    Ingredients.CategoryID = Categories.CategoryID
WHERE 
    IngredientID = :placeholder
ORDER BY
    Ingredients.CategoryID