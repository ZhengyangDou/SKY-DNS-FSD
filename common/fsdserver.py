import geoip2.database
from geopy.distance import geodesic

fsd_chengdu_location = (34.7732, 113.722)
fsd_hongkong_location = (22.308, 113.918)
fsd_quanzhou_location = (34.7732, 113.722)
fsd_Tokyo_location = (35.6895, 139.6917)
fsd_server = ({'name': '成都', 'location': fsd_chengdu_location}, {'name': '香港', 'location': fsd_hongkong_location}, {'name': '泉州', 'location': fsd_quanzhou_location}, {'name': '东京', 'location': fsd_Tokyo_location})

def get_ip_info(ip):
    reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
    response = reader.city(ip)
    # 解析出城市和经纬度
    city = response.city.name
    longitude = response.location.longitude
    latitude = response.location.latitude
    return city, longitude, latitude
# 计算两个经纬度之间的距离

def get_distance(location1, location2):
    # 判断出哪个服务器距离用户最近
    distance = geodesic(location1, location2).km
    return distance

def get_nearest_server(ip):
    # 获取用户所在城市
    city, longitude, latitude = get_ip_info(ip)
    # 计算用户所在城市和各个服务器的距离
    distance_list = []
    for server in fsd_server:
        distance = get_distance((latitude, longitude), server['location'])
        distance_list.append({'name': server['name'], 'distance': distance})
    # 找出距离最近的服务器
    nearest_server = sorted(distance_list, key=lambda x: x['distance'])[0]
    return nearest_server['name']
