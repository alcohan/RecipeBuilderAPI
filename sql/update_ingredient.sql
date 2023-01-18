UPDATE 
    Ingredients 
SET 
    Name = :name, 
    Unit = :unit,
    PortionVolume = :portionvol,
    CasePrice = :caseprice,
    CaseSize = :casesize,
    PortionSize = :portionsize,
    PortionUtensil = :utensil,
    YieldPercent = :yield,
    Calories = :calories,
    TTLFatGrams = :ttlfat,
    SatFatGrams = :satfat,
    CholesterolMiligrams = :choles,
    SodiumMiligrams = :sodium,
    CarbohydratesGrams = :carbs,
    FiberGrams = :fiber,
    SugarGrams = :sugar,
    ProteinGrams = :protein
WHERE 
    IngredientID = :id