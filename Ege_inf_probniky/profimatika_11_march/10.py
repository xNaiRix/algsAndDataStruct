#7
bits = 16
pixels = 1920*1080
info_in_picture = bits*pixels
packet_info = 300 * info_in_picture
v = 1474560 
sec = packet_info/v
print(sec, "секунд")
print(sec/60, "минут")