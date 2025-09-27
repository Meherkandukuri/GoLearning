-- 002_seed.sql: seed common vegetables
INSERT INTO vegetables (name, unit, category) VALUES
 ('Tomato','kg','Vegetable') ON CONFLICT DO NOTHING,
 ('Potato','kg','Vegetable') ON CONFLICT DO NOTHING,
 ('Onion','kg','Vegetable') ON CONFLICT DO NOTHING,
 ('Carrot','kg','Vegetable') ON CONFLICT DO NOTHING;