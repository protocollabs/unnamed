tips:
	@echo
	@echo "now install and setup configuration files, prefered in /etc/unnamed/"
	@echo "Edit /lib/systemd/system/unnamed.service and point to the configuration file(s)"
	@echo "now call sudo systemctl daemon-reload"
	@echo ".. enable service via: sudo systemctl enable ohnld@FOO.service"
	@echo ".. start service via:  sudo systemctl start ohnld@FOO.service"
	@echo ".. status via:         sudo systemctl status ohnld@FOO.service"
	@echo ".. log info via:       sudo journalctl -u ohnld@FOO.service"

install_deps:
	sudo -H pip3 install -r requirements.txt

install:
	install -m 755 -T unnamed.py /usr/bin/unnamed
	install -m 644 assets/unnamed.service /lib/systemd/system/
	mkdir -p /etc/unnamed
	make tips

uninstall:
	rm -rf /usr/bin/unnamed
	rm -rf /lib/systemd/system/unnamed.service

