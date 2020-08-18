import requests


headers = {
    'authority': 'api.cafebazaar.ir',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
}


def convert_number(number):
    final_number = ''
    for num in number:
        if num.isnumeric():
            final_number += str(int(num))
        else:
            final_number += num
    return final_number


def get_download_link(package_name):
    data = """
        {"properties": {
            "androidClientInfo": {
                "sdkVersion": 22,
                "cpu": "x86,armeabi-v7a,armeabi"}
            },
        "singleRequest": {
            "appDownloadInfoRequest": {
                "downloadStatus": 1,
                "packageName": "%s"}
            }
        }""" % package_name
    url = 'https://api.cafebazaar.ir/rest-v1/process/AppDownloadInfoRequest'
    response = requests.get(
        url, headers=headers, data=data
    )
    if response.ok:
        response_data = response.json()['singleReply']['appDownloadInfoReply']
        token = response_data['token']
        cdn_prefix = response_data['cdnPrefix'][0]
        download_link = f'{cdn_prefix}apks/{token}.apk'
        return download_link
    else:
        return {'error': 'Bad request'}


def get_details(package_name):
    data = """
        {"properties": {
            "language": 2,
            "clientID": "7ouolt3ifuwghtn3mwlv5sd44pe5wmyc",
            "deviceID": "7ouolt3ifuwghtn3mwlv5sd44pe5wmyc",
            "clientVersion": "web"},
        "singleRequest": {
            "appDetailsRequest": {
                "language": "fa",
                "packageName": "%s"}
            }
        }""" % package_name
    url = 'https://api.cafebazaar.ir/rest-v1/process/AppDetailsRequest'
    developer_page_url = 'https://cafebazaar.ir/developer/'
    response = requests.post(
        url, headers=headers, data=data)
    if response.ok:
        response_data = response.json()['singleReply']['appDetailsReply']
        if response_data['price']['price'] == 0:
            name = response_data['name']
            icon = f'https://s.cafebazaar.ir/1/icons/{package_name}_512x512.png'
            short_description = response_data['shortDescription']
            description = response_data['description']
            author_name = response_data['authorName']
            author_url = developer_page_url + response_data['authorSlug']
            install_count_range = response_data['stats']['installCountRange']
            install_count_range = install_count_range.replace('،', ',')
            review_count = response_data['stats']['reviewCount']
            version_name = response_data['package']['versionName']
            version_code = response_data['package']['versionCode']
            last_updated = response_data['package']['lastUpdated']
            return {
                'name': name,
                'icon': icon,
                'short_description': short_description,
                'description': description,
                'author_name': author_name,
                'author_url': author_url,
                'install_count_range': convert_number(install_count_range),
                'review_count': review_count,
                'version_name': convert_number(version_name),
                'version_code': version_code,
                'last_updated': convert_number(last_updated)
            }
        else:
            return {'error': 'Price of this app is over than 0 toman'}
