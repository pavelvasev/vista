==== Что это

Скрипт для Питон 3.8+, который визуализирует заданные сущности согласно описанию.
Для графики используется библиотека https://docs.pyvista.org

===== Подготовка скрипта

Установить библиотеки необходимые для работы:

pip install pyvista[all] imageio[ffmpeg] numpy

====== Запуск скрипта

`python vista.py [data]`
где data каталог данных.

====== План
- вернуть поверхность версия 1
- посмотреть, мб окажется полезно некая матрица слоев или что-то такое
- мб вынести слой управления камерами - как отдельный плагин,
итого плагин возвращает не 1 визуальный объект а набор: а) визуальных объектов, 
б) слоев для камер и т.п.
- подумать как удобно добавить а) полет камеры, б) запись видео.
мб загрузка проекта это должна определять вещи. в т.ч. что идет режим видео.
но мб и ортогонально сделать кстати - тогда запуск программы это запуск набора
разных штук, в т.ч. например плагинов с командой на запись мультика. хотя
с другой стороны эти вещи хотелось бы делать и из гуи.

====== Новая идея
каталог данных
загрузчики - каждый кто может тот загружает (tryload) (т.е. мб не 1 а несколько)
проходчик по подкаталогам.
выполнение питон-скрипта есть частный случай.
если надо указать параметры пишите json-записку для загрузчика например. param.json.
либо модификаторы подумать но тогда нужна ортогональность. плюс нужен доступ к последним загруженным данным.

далее. загрузчик сам добавляет визуальные процессы в plotter а наружу выдает список каналов а точнее
имя, тип, указатель на функцию записи. пока тип это галочка потом еще цвет добавим.
ну а мб цвет альтерантивно будет (подумать - ибо хочется ортогональности)
  хотя это мб и событие. но это версия 2.
и далее интерфейс просто отображает все эти каналы. причем если имена совпадают то показывает 1 имя.

далее модификаторы.. например norm=false. или еще какой. или задание цвета.
мб совместить это с params как-то. типа json значит модификатор. или собрать всех в 1 json но это неудобно.
либо в подпапке собрать json-ки. я к тому что params.json это тоже мб модификатор такой.

+ действия - создать поверхность по..

======
2024 (c) ИММ УрО РАН, г. Екатеринбург
