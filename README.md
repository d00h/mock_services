# Проблема 

При разработки в микросервисной парадигме неплохо бы иметь легкие "фейковые" копии внешних сервисов 
и задавать их поведение определяемое декларативно и имеющие осмысленное имя. 

Кроме того хорошо бы где то иметь документацию используемых методов. 

традиционные способы monkeypatch и мокировние через depenency injection не всегда удобны и никак 
не решают второе пожелание.

# Идея

Создать простой локальный сервер пути которого полностью повторяют api внешнего сервиса
и дать возможность задавать ответы api через yaml файл профиля.

профиль это общее осмысленное название для какого то поведения внешней среды.

например: google_auth_down, weak_connection, telegram_blocks

все методы не определенные в yaml файле возвращают ответ имитирующий нормальную работу сервиса. 

# Запуск

```shell 

make build up

```

открыть в браузере http://127.0.0.1:5400

посмотреть, как пример того, как сервис работает можно запустив:

```shell

# посылаем на 127.0.0.1:5400/mock_profile настройки профиля
python tools/mock-ctl.py put-profile profiles/easysms_123.yaml 

# эмитируем работу с внешним сервисом
python tools/example-easysms.py

```

где default, easysms_limit, easysms_weak, easysms_123 это профили из папки profiles

# Примеры

в justfile описанны примеры использования:


# Использование 

в разрабатываемом сервисе заменить host внешнего сервиса

например: 

```python

EASYSMS_URL=http://mock_services.develop/service/easysms

```

# Cтруктура проекта

* mock_services flask проект
* specs документация внешних сервисов 
* profiles профили состояния 
* tools дополнительные утилиты для разработки 

# Cтруктура api сервиса

* /apidocs документация внешних сервисов и тестер 
* /service/easysms точка для замены сервиса
* /mock_profile управления профилями
* /mock_logger получения логов мокированых запросов

# Профиль

это файл содержаций список ответов сервисов

```yaml

- endpoint: easysms.send_sms
  content_type: application/json
  body_template: |
      {
          "message": "sended",
          "sms_id": "1"
      }
  step: 0
  change: 50
  status: 200

- endpoint: easysms.send_sms
  content_type: application/json
  body_template: |
      {
          "message": "sended",
          "sms_id": "2"
      }
  step: 0
  change: 50
  status: 200

- endpoint: easysms.send_sms
  content_type: application/json
  body_template: |
      {
          "message": "sended",
          "sms_id": "3"
      }
  step: 1
  status: 200
```

описывает последовательность вызовов сервиса easysms

1 вызов с вероятностью 50/50 либо sms_id = 1 либо sms_id = 2

2 вызов sms_id = 3

название endpoint берется из swagger 

# generate-service-stub

простая и грязная утилита генерирует начальный файл для сервиса из swagger spec


```shell

python tools/generate-service-stub.py spec/cloudpayments.yaml
python tools/generate-service-stub.py spec/mailgun.yaml -o mailgun.py
python tools/generate-service-stub.py spec/easysms.yaml

```

чисто теоретически возможно генерировать более полную версию исходника или делать это прям на лету
, но на первом этапе этого достаточно.


# точки расширения

1. сделать генератор профиля из HAR архива.

для разбора прецедентов
