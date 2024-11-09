from sqlalchemy import create_engine, text
from typing import List, Tuple, Union

engine = create_engine(
    'mysql+pymysql://crm_user:RScrm_pwd.1234@test-polarm-devmgr-01-sh2e.taimei.com/mdm_master_play',
    pool_size=5,
    max_overflow=10
)


def execute_query(sql: Union[str, text], scalar: bool = True) -> Union[int, List[Tuple]]:
    """执行 SQL 查询并返回结果"""
    with engine.connect() as connection:
        result = connection.execute(sql)
        return result.scalar() if scalar else result.fetchall()
