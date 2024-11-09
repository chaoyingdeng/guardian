from sqlalchemy import create_engine, text
from typing import List, Tuple, Union

engine = create_engine(
    'mysql+pymysql://crm_user:RScrm_pwd.1234@test-polarm-devmgr-01-sh2e.taimei.com/mdm_master_play',
    pool_size=5,
    max_overflow=10
)


def execute_query(sql: Union[str, text]):
    """执行 SQL 查询并返回结果"""
    with engine.connect() as connection:
        result = connection.execute(sql).fetchall()
        return [item[0] for item in result]


def get_article_field(field_name, person_id, ):
    """ 获取论文信息 """
    sql = text(
        f"""
        select tma.{field_name}
        from t_md_article tma
        join t_md_person_article tmpa
        where tma.id = tmpa.article_id
        and tmpa.person_id = '{person_id}'
        """
    )
    result = execute_query(sql)
    return result


def get_clinical_trial_field(field_name, person_id, ):
    """ 获取临床试验信息 """
    sql = text(
        f"""
        select tmct.{field_name}
        from t_md_clinical_trial tmct
        join t_md_clinical_trial_researcher tmctr
        on tmct.id = tmctr.clinical_trial_id
        where tmct.is_deleted = 0
        and tmctr.is_deleted = 0
        and tmctr.person_id = '{person_id}'
        """
    )
    result = execute_query(sql)
    return result


def get_conference_field(field_name, person_id):
    """ 获取会议相关信息 """
    sql = text(
        f"""
        select tmc.{field_name}
        from mdm_master_play.t_md_person_conference tmpc
        join mdm_master_play.t_md_conference tmc
        on tmpc.conference_id = tmc.id
        where tmpc.is_deleted = 0
        and tmc.is_deleted = 0
        and tmpc.person_id = '{person_id}'
        """
    )
    result = execute_query(sql)
    return result


def get_person_preferences_institution(person_id):
    get_article_field("id", person_id)
    get_clinical_trial_field("id", person_id)

    return


if __name__ == '__main__':
    print(get_conference_field("id", "8b42ba41070d11ecb68200163e1f7c71"))
