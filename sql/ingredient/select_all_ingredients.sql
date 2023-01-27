SELECT 
    Ingredients.Name
    ,Ingredients.IngredientID
    ,Ingredients.ImageURL
    ,Categories.Name as Category
    ,Ingredients.CategoryID

    ,Ingredients.Calories
    ,Ingredients.CarbohydratesGrams
    ,Ingredients.CholesterolMiligrams
    ,Ingredients.FiberGrams
    ,Ingredients.ProteinGrams
    ,Ingredients.SatFatGrams
    ,Ingredients.SodiumMiligrams
    ,Ingredients.SugarGrams
    ,Ingredients.TTLFatGrams

    ,Ingredients.Unit
    ,Ingredients.CasePrice
    ,Ingredients.CaseSize
    ,Ingredients.YieldPercent
    ,Ingredients.PortionSize

    ,Ingredients.PortionCost
    ,Ingredients.PortionsPerCase

    ,Ingredients.PortionVolume
    ,Ingredients.PortionWeight
    ,Ingredients.PortionUtensil
FROM 
    Ingredients 
LEFT JOIN Categories ON Ingredients.CategoryID = Categories.CategoryID

ORDER BY
    Ingredients.CategoryID