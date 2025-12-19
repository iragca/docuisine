# Database

## Entity Relation Diagram

```mermaid
erDiagram

    USER {
        int id PK
        text username
        text email
        text password
        text role
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    STORE {
        int id PK
        text name
        geojson location
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    INGREDIENT {
        int id PK
        int type_id
        text name
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    RECIPE {
        int id PK
        int user_id FK
        int category_id FK
        text title
        int cook_time_sec
        int prep_time_sec
        int non_blocking_sec
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    CATEGORY {
        int id PK
        text name
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    SHELF {
        int id PK
        int store_id FK
        int ingredient_id FK
        int quantity
        timestamp created_at
        timestamp updated_at
    }

    RECIPE_INGREDIENT {
        int id PK
        int recipe_id FK
        int ingredient_id FK
        int amount_grams
        text amount_readable
        timestamp created_at
        timestamp updated_at
    }

    RECIPE_STEP {
        int id PK
        int recipe_id FK
        text description
        int step_num
        text preview_img
        text img
        timestamp created_at
        timestamp updated_at
    }

    %% Relationships

    USER ||--o{ RECIPE : creates
    CATEGORY ||--o{ RECIPE : categorizes

    RECIPE ||--o{ RECIPE_STEP : has
    RECIPE ||--o{ RECIPE_INGREDIENT : uses
    INGREDIENT ||--o{ RECIPE_INGREDIENT : included_in

    STORE ||--o{ SHELF : has
    INGREDIENT ||--o{ SHELF : stored_in
```

Columns `preview_img`, `img`, `created_at`, `updated_at` should be implemented as a superclass `Entity` that should be inherited from when implementing `user`, `store`, `ingredient`, etc.
