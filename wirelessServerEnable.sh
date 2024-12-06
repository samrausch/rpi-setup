cp /etc/dhcpcd.conf.static /etc/dhcpcd.conf
systemctl enable hostapd
systemctl enable dnsmasq
reboot
