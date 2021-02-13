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

посмотреть как работает можно запустив

```shell

python tools/example-easysms.py default
python tools/example-easysms.py easysms_limit
python tools/example-easysms.py easysms_weak
python tools/example-easysms.py easysms_123

```

где default, easysms_limit, easysms_weak, easysms_123 это профили из папки profiles

# Использование 

в разрабатываемом сервисе заменить host внешнего сервиса

например: EASYSMS_URL=http://mock_services.develop/easysms_weak

# Cтруктура проекта

* mock_services flask проект
* specs документация внешних сервисов 
* profiles профили состояния 
* tools дополнительные утилиты для разработки 

# Cтруктура api сервиса

* /apidocs документация внешних сервисов и тестор 
* /service/easysms/profile/ точка для замены сервиса
* /profile/название управления профилями (планируется)

# genarate-service-stub

простая и грязная утилита генерирует начальный файл для сервиса из swagger spec


'''shell
python tools/generate-service-stub.py spec/cloudpayments.yaml
python tools/generate-service-stub.py spec/mailgun.yaml -o mailgun.py
python tools/generate-service-stub.py spec/easysms.yaml
'''

чисто теоретически возможно генерировать более полную версию исходника или делать это прям на лету
, но на первом этапе этого достаточно.
