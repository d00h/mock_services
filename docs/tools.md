# genarate-service-stub

простая и грязная утилита генерирует начальный файл для сервиса из swagger spec


'''shell
python tools/generate-service-stub.py spec/cloudpayments.yaml
python tools/generate-service-stub.py spec/mailgun.yaml -o mailgun.py
python tools/generate-service-stub.py spec/easysms.yaml
'''

чисто теоретически возможно генерировать более полную версию исходника или делать это прям на лету
, но на первом этапе этого достаточно.
