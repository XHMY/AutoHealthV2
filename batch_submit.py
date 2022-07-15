import requests
import json
import datetime
import argparse


def submit(payloads, headers):
    url = "https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"
    r = requests.post(url, headers=headers, data=payloads.encode("utf-8"))
    print("ID:", r.json()["resultEntity"]["id"], "提交成功!")


def date_range_submit(last_card, headers, start_date_string="2022-07-15", end_date_string="2022-08-26"):
    start_date = datetime.datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_string, "%Y-%m-%d")
    date_range = (end_date - start_date).days + 1

    last_card['result']['BZ'] = ''
    del last_card['result']['ID']

    for i in range(date_range):
        date_string = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")

        health_card_data = {
            "entity": {
                "cn": ["本人承诺登记后、到校前不再前往其他地区"],
                "_ext": "{}",
                "__type": "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
            }
        }

        last_card["result"].update({
            "TBRQ": date_string,
            "TJSJ": f"{date_string} 09:05",
            "BT": date_string + last_card["result"]["BT"][10:]
        })
        health_card_data["entity"].update({k.lower(): v for k, v in last_card['result'].items()})
        submit(json.dumps(health_card_data, ensure_ascii=False))
        print(f'已提交 {date_string} 健康卡')



def main():
    parser = argparse.ArgumentParser(description='提交健康卡')
    parser.add_argument('-s', '--start-date', type=str, required=True, help='提交开始日期: %Y-%m-%d')
    parser.add_argument('-e', '--end-date', type=str, required=True, help='提交结束日期: %Y-%m-%d')
    parser.add_argument('-jsid', '--JSESSIONID', type=str, required=True, help='JSESSIONID')
    args = parser.parse_args()

    headers = {
        'authority': 'work.zcst.edu.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'accept': '*/*',
        'content-type': 'text/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://work.zcst.edu.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/jkxxcj.jsp?ticket=ST-750274-AgriFzKd1Rbfe3MMQHfj-authserver.zcst.edu.cn',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'cookie': f'JSESSIONID={args.jsid}',
    }

    last_card_data = requests.post('https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryYear.biz.ext',
                                headers=headers, data={}).json()
    date_range_submit(last_card_data, headers, args.s, args.e)


