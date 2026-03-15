CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority INTEGER DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Добавление тестовых данных
INSERT INTO tasks (title, description, priority) VALUES
    ('Изучить Docker', 'Понять основы контейнеризации', 5),
    ('Написать практическую работу', 'Создать todo-приложение с Docker', 4),
    ('Сдать проект', 'Подготовиться к защите', 3)
ON CONFLICT DO NOTHING;