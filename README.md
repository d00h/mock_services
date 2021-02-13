# Проблема 

При разработки в микросервисной парадигме неплохо бы иметь легкие "фейковые" копии внешних сервисов 
и задавать их поведение определяемое декларативно и имеющие осмысленное имя. 

Кроме того хорошо бы где то иметь документацию испольуемых методов. 

традиционные способы monkeypatch и мокировние через depenency injection не всегда удобны и никак 
не решают второе пожелание.

# Идея

Создать простой локальный сервер пути которого полностью повторяют api внешнего сервиса
и дать возможность задавать ответы api через yaml файл.

все методы не определенные в yaml файле имеют имитирующий нормальную работу сервиса. 

# Запуск

```shell 

make build up

```

открыть в браузере http://127.0.0.1:5000

# Cтруктура проекта

mock_services
specs 
profiles 
tools 

# Cтруктура api сервиса

# Внутренности

создает 

   endpoint service/**profile**/external_service/.....

где:

   * profile [ sms_limit, default, bill_down ]_
