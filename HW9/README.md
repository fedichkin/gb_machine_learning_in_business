# STARS PREDICT
Итоговый проект (пример) курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/deepu1109/star-dataset

Задача: Предсказать тип звезды по её характеристикам

Используемые признаки:

- **Temperature** - температура в кельвинах
- **Luminosity** - светимость звезды в единицах светимости Солнца
- **Radius** - радиус звезды расчитанный относительно радиуса Солнца
- **Absolute magnitude** - абсолютная звездная величина
- **Star colo**r - цвет здезды ('Red', 'Blue White', 'White', 'Yellowish White', 'Blue white',
       'Pale yellow orange', 'Blue', 'Blue-white', 'Whitish',
       'yellow-white', 'Orange', 'White-Yellow', 'white', 'Blue ',
       'yellowish', 'Yellowish', 'Orange-Red', 'Blue white ',
       'Blue-White')
- **Spectral Class** - класс спектра ('M', 'B', 'A', 'F', 'O', 'K', 'G')
- **Star type** - тип звезды (целевой признак который будем предсказывать)

Тип зведы включает в себя 6 классов, от 0 до 5

- 0 - Коричневый карлик
- 1 - Красный карлик
- 2 - Белый карлик
- 3 - Главная последовательность
- 4 - Супер гигант
- 5 - Гипер гигант

Модель: RandomForestClassifier

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/fedichkin/gb_machine_learning_in_business.git
$ cd gb_machine_learning_in_business/HW9
$ docker build -t fedichkin/gb_starts_predict .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -v <your_local_path_to_pretrained_models>:/app/app/models fedichkin/gb_starts_predict
```

### Переходим на localhost:8180