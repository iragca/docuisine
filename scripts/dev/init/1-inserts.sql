BEGIN;

-- =====================
-- USERS
-- =====================
INSERT INTO users (id, username, email, password, role, preview_img, img)
VALUES
    (1, 'alice', 'alice@example.com', 'hashed_password_1P!', 'user', NULL, NULL),
    (2, 'bob', 'bob@example.com', 'hashed_password_2P!', 'admin', NULL, NULL);

-- =====================
-- INGREDIENTS
-- =====================
INSERT INTO ingredients (id, name, preview_img, img)
VALUES
    (1, 'Salt', NULL, NULL),
    (2, 'Sugar', NULL, NULL),
    (3, 'Flour', NULL, NULL),
    (4, 'Butter', NULL, NULL),
    (5, 'Egg', NULL, NULL);

-- =====================
-- CATEGORIES
-- =====================
INSERT INTO categories (id, name, preview_img, img)
VALUES
    (1, 'Dessert', NULL, NULL),
    (2, 'Breakfast', NULL, NULL),
    (3, 'Quick Meals', NULL, NULL);

-- =====================
-- RECIPES
-- =====================
INSERT INTO recipes (
    id,
    user_id,
    name,
    cook_time_sec,
    prep_time_sec,
    non_blocking_time_sec,
    servings,
    preview_img,
    img
)
VALUES
    (1, 1, 'Pancakes', 600, 300, 0, 4, NULL, NULL),
    (2, 2, 'Scrambled Eggs', 300, 120, 0, 2, NULL, NULL);

-- =====================
-- RECIPE STEPS
-- =====================
INSERT INTO recipe_steps (recipe_id, step_number, description)
VALUES
    (1, 1, 'Mix all dry ingredients together.'),
    (1, 2, 'Add wet ingredients and stir until smooth.'),
    (1, 3, 'Cook on a hot pan until golden brown.'),

    (2, 1, 'Crack eggs into a bowl and whisk.'),
    (2, 2, 'Cook eggs in a pan over low heat while stirring.');

-- =====================
-- RECIPE INGREDIENTS
-- =====================
INSERT INTO recipe_ingredients (
    recipe_id,
    ingredient_id,
    amount_grams,
    amount_readable
)
VALUES
    (1, 1, 5, '1 tsp salt'),
    (1, 2, 20, '2 tbsp sugar'),
    (1, 3, 200, '2 cups flour'),
    (1, 4, 30, '2 tbsp butter'),
    (1, 5, 100, '2 eggs'),

    (2, 1, 2, 'A pinch of salt'),
    (2, 4, 15, '1 tbsp butter'),
    (2, 5, 150, '3 eggs');

-- =====================
-- RECIPE CATEGORIES
-- =====================
INSERT INTO recipe_categories (recipe_id, category_id)
VALUES
    (1, 1), -- Pancakes → Dessert
    (1, 2), -- Pancakes → Breakfast
    (2, 2), -- Scrambled Eggs → Breakfast
    (2, 3); -- Scrambled Eggs → Quick Meals

-- =====================
-- STORES
-- =====================
INSERT INTO stores (
    id,
    name,
    longitude,
    latitude,
    address,
    phone,
    website,
    preview_img,
    img
)
VALUES
    (1, 'Fresh Market', 121.0437, 14.6760, '123 Main St, City', '555-1234', 'https://freshmarket.example', NULL, NULL),
    (2, 'Daily Grocer', 121.0500, 14.6800, '456 Side St, City', NULL, NULL, NULL, NULL);

-- =====================
-- SHELF (STORE INVENTORY)
-- =====================
INSERT INTO shelf (
    store_id,
    ingredient_id,
    quantity
)
VALUES
    (1, 1, 100), -- Salt
    (1, 2, 50),  -- Sugar
    (1, 3, 200), -- Flour
    (1, 4, 40),  -- Butter
    (2, 5, 60);  -- Eggs

COMMIT;
