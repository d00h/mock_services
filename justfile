_all:
    @just --list


set-profile FILENAME SERVER='http://127.0.0.1:5400':
    curl -X POST  -o /dev/null --data-binary "@{{ FILENAME }}" "{{ SERVER }}/mock_profile"    

   
get-profile SERVER='http://127.0.0.1:5400':
    curl -X GET "{{ SERVER }}/mock_profile"

   
delete-profile SERVER='http://127.0.0.1:5400':
    curl -X delete "{{ SERVER }}/mock_profile"

   
get-logs SERVER='http://127.0.0.1:5400':
    curl -X get "{{ SERVER }}/mock_logger"
    
delete-logs SERVER='http://127.0.0.1:5400':
    curl -X delete "{{ SERVER }}/mock_logger"

easysms COUNT='3':
    python tools/example-easysms.py --count={{ COUNT }}

