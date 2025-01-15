import requests
url = "https://test.pharmaos.com/gw/api/hcp-api-svc/admin/tag/save"
payload = {
    "name": f"医学标签52",
    "code": f"Material_Tag_yixue52",
    "categoryId": 1813,
    "type": "ARTIFICIAL",
    "valueSelectMode": "SINGLE",
    "relationDictType": "CUSTOMIZED",
    "tagValues": [
        {
            "value": "AAA",
            "isHovered": False,
            "sort": 1
        }
    ],
    "valueUpdateType": "MANUAL",
    "entityCode": "MATERIAL"
}
headers = {
    "content-type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh",
    "Connection": "keep-alive",
    "Cookie": "gr_user_id=b974c697-fe87-40ac-b27e-4c5b1cb7725b; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226231643135623133646131303266643439366434663061396130656339366235222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; jXcKXPxOebJgfTXq=ZjVmMGU2NzUtNTI0NC00OGE1LTkxMGMtM2Q1N2E1ZmU1Y2Rl; acw_tc=0a472f8e17369300557832711e00f9645afe3f313e5fcb131d40ed276c0e4b; JSESSIONID=31B7A4C4018071A43DC9688190D954A5; gw-history-redirect-url=https://test.pharmaos.com/static/paas-configcenter-static/?1736930517107; token=4568c52e2d50455cb4993146164231c0",
    "Origin": "https://test.pharmaos.com",
    "Referer": "https://test.pharmaos.com/static/paas-configcenter-static/sfl-config/tag-manage/data-center-tag/createTag?type=2&entityCode=MATERIAL&dataType=materialLabel&sourceTabIndex=5",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TM-Header-AppId": "configuration-center",
    "TM-Header-TenantId": "802bee57456646baab00807f4df59250",
    "TM-Header-Token": "8ac2749491741df80194692068cb411e",
    "TM-Header-UserId": "8ac274657d0425b3017d35ed4eec0074",
    "TM-Header-UserName": "%E9%82%93%E8%B6%85%E8%8B%B1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
