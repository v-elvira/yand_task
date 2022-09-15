# Запуск #
<code>sudo gunicorn -b 0.0.0.0:80 yand_rest.wsgi</code>

или:

<code>~/start_yand.sh</code> (там та же команда)



С Docker-ом у меня не получилось, поэтому автоматический перезапуск при рестарте контейнера пыталась сделать через 

<code>crontab -e</code> добавлением туда <code>@reboot ~/start_yand.sh</code>



# Тест #
<code>python3 unit_t.py</code> -  прилагавшийся к заданию тест (на порт 80).

Дополнительные задачи не делала.
