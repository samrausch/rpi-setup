cp /etc/dhcpcd.conf.dynamic /etc/dhcpcd.conf
systemctl disable hostapd
systemctl disable dnsmasq
reboot
