import requests
from typing import Dict, Any
from pathlib import Path


class DingTalkRobot:
    def __init__(self, access_token: str):
        self.url = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"
        self.headers = {"Content-Type": "application/json"}

    def send_markdown(self, content: str) -> Dict[str, Any]:
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "Test日报",
                "text": content
            }
        }

        try:
            response = requests.post(url=self.url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"发送钉钉消息失败: {e}")
            return {"errcode": -1, "errmsg": str(e)}


def generate_test_report() -> str:
    report_json = Path(__file__).parent.parent / 'data' / 'report_related' / 'report.json'

    return f"""
#### Guardian测试报告
> - 用例总数: 1
> - 执行用例: 2
> - 通过用例: 3
> - 失败用例: 4

            """


if __name__ == '__main__':
    access_token = "894b86f84ed88794a5588b33f432047eb9354542e253f15b2208fb59e01c8c61"
    ding_notify = DingTalkRobot(access_token=access_token)
    response = ding_notify.send_markdown(generate_test_report())
    print(response)
