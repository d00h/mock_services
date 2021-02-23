_all:
    @just --list

# get current config of server   
profile SERVER='http://127.0.0.1:5400':
    curl -X GET "{{ SERVER }}/mock_profile"
   
# install profile to server
install FILENAME SERVER='http://127.0.0.1:5400':
    curl -X POST  -o /dev/null --data-binary "@{{ FILENAME }}" "{{ SERVER }}/mock_profile"

# get mock logs
logs SERVER='http://127.0.0.1:5400':
    curl -X get "{{ SERVER }}/mock_logger"

# delete profile and logs
clean SERVER='http://127.0.0.1:5400':
    curl -X delete "{{ SERVER }}/mock_logger"
    curl -X delete "{{ SERVER }}/mock_profile"


run-easysms COUNT='3':
    python tools/example-easysms.py --count={{ COUNT }}

