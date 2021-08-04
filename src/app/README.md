# FastAPI-miniapp
API and UI for convert image to negative

- /negative_image (POST) - получает на входе .png/.jpeg картинку в формате base64. В ответе - json с негативом изображения, закодированном в формат base64. При удачном ответе изображение сохраняется в базу данных;
- /get_last_images (GET) - Отдает json с 3 последними изображениями (в оригинале и негативе) в формате base64, загруженные ранее методом /negative_image. Причем у каждой пары изображений уникальные идентификаторы.
Помимо rest api, реализован UI сервиса с возможностью загрузки изображения из файла и просмотра последних 3х загруженных фотографий.


### Start application
Get latest docker & docker-compose:  
https://www.docker.com/  
https://docs.docker.com/compose/  
Run in terminal:  
`docker-compose up -d --build`  
`docker-compose up`  
Wait for docker to set up container, then open [http://0.0.0.0](http://0.0.0.0)

Documentation is accessible via [http://0.0.0.0/docs/](http://0.0.0.0/docs/)
and [http://0.0.0.0/redoc/](http://0.0.0.0/redoc/)

API resources:  
- [http://0.0.0.0/api/v1/negative_image](http://0.0.0.0/api/v1/negative_image)
- [http://0.0.0.0/api/v1/get_last_images](http://0.0.0.0/api/v1/get_last_images)

### Run tests
Run in terminal:  
`docker-compose up`  
And another terminal window:  
`docker-compose exec web pytest tests/`