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


def get_person_article_count(person_id: str) -> int:
    """发表论文数"""
    sql = text(f"""
                SELECT COUNT(1)
                FROM t_md_person_article
                WHERE is_deleted = 0 AND person_id = '{person_id}'
    """)
    count = execute_query(sql)
    print(f"发表论文数量: {count}")
    return count


def get_person_article_count_last_years(person_id: str, years: int) -> int:
    """近n年发表论文数量"""
    sql = text(f"""
                SELECT COUNT(1)
                FROM mdm_master_play.t_md_person_article tmpa
                JOIN mdm_master_play.t_md_article tma ON tmpa.article_id = tma.id
                WHERE tmpa.person_id = '{person_id}'
                AND publish_date BETWEEN DATE_SUB(CURDATE(), INTERVAL {years} YEAR) AND CURDATE()
                AND tmpa.is_deleted = 0 AND tma.is_deleted = 0
    """)
    count = execute_query(sql)
    print(f"近{years}年发表论文数量: {count}")
    return count


def get_person_article_count_by_type(person_id: str, person_type: str = "first") -> int:
    """根据类型查询医生论文数量"""
    sql = text(f"""
                SELECT COUNT(1)
                FROM mdm_master_play.t_md_person_article tmpa
                JOIN mdm_master_play.t_md_article tma ON tmpa.article_id = tma.id
                WHERE tmpa.person_id = '{person_id}' AND tmpa.person_type = '{person_type}'
                AND tmpa.is_deleted = 0 AND tma.is_deleted = 0
    """)
    count = execute_query(sql)
    print(f"{person_type}论文数量: {count}")
    return count


def get_person_trial_count(person_id: str) -> int:
    sql = text(f"""
        SELECT COUNT(1)
        FROM mdm_master_play.t_md_clinical_trial_researcher tmctr
        JOIN mdm_master_play.t_md_clinical_trial tmct ON tmctr.clinical_trial_id = tmct.id
        WHERE tmctr.is_deleted = 0 AND tmct.is_deleted = 0
        AND tmctr.person_id = '{person_id}'
    """)
    count = execute_query(sql)
    print(f"参与临床试验数量: {count}")
    return count


def get_person_conference_count(person_id: str) -> int:
    sql = text(f"""
        SELECT COUNT(1)
        FROM mdm_master_play.t_md_person_conference tmpc
        JOIN mdm_master_play.t_md_conference tmc ON tmpc.conference_id = tmc.id
        WHERE tmpc.is_deleted = 0
        AND tmc.is_deleted = 0
        AND tmpc.person_id = '{person_id}'
    """)
    count = execute_query(sql)
    print(f"参与会议数量: {count}")
    return count


def get_person_science_article_count(person_id: str) -> int:
    sql = text(
        f"""
        select count(1)
        from mdm_master_play.t_md_person_pop_science_article tmppsa
        join mdm_master_play.t_md_pop_science_article tmpsa
        on tmppsa.pop_science_article_id = tmpsa.id 
        where tmppsa.is_deleted = 0
        and tmpsa.is_deleted = 0 
        and tmppsa.person_id = '{person_id}'
        """
    )
    count = execute_query(sql)
    print(f"发布科普文章数量: {count}")
    return count


def get_person_article_partner_id(person_id: str) -> List[str]:
    sql = text(f"""
        SELECT DISTINCT tmpa2.person_id
        FROM t_md_person_article tmpa
        JOIN t_md_person_article tmpa2 ON tmpa.article_id = tmpa2.article_id
        WHERE tmpa.person_id = '{person_id}' AND tmpa2.person_id != '{person_id}'
    """)
    origin_result = execute_query(sql, scalar=False)
    print(f"论文合作者人数：{len(origin_result)}")
    return [item[0] for item in origin_result]


def get_person_trial_partner_count(person_id: str) -> List[str]:
    sql = text(f"""
        SELECT DISTINCT tmctr2.person_id
        FROM t_md_clinical_trial_researcher tmctr
        JOIN t_md_clinical_trial_researcher tmctr2 ON tmctr.clinical_trial_id = tmctr2.clinical_trial_id
        WHERE tmctr.person_id = '{person_id}' AND tmctr2.person_id != '{person_id}'
    """)
    origin_result = execute_query(sql, scalar=False)
    print(f"临床试验合作者人数：{len(origin_result)}")
    return [item[0] for item in origin_result]


def get_person_conference_partner_count(person_id: str) -> List[str]:
    sql = text(f"""
        SELECT DISTINCT tmpc2.person_id
        FROM t_md_person_conference tmpc
        JOIN t_md_person_conference tmpc2 ON tmpc.conference_id = tmpc2.conference_id
        WHERE tmpc.person_id = '{person_id}' AND tmpc2.person_id != '{person_id}'
    """)

    origin_result = execute_query(sql, scalar=False)
    print(f"会议合作者人数：{len(origin_result)}")
    return [item[0] for item in origin_result]


def get_person_science_article_partner_count(person_id: str) -> List[str]:
    sql = text(f"""
        select distinct tmi2.person_id
        from mdm_master_play.t_md_person_pop_science_article tmi
        join mdm_master_play.t_md_person_pop_science_article tmi2
        on tmi.pop_science_article_id = tmi2.pop_science_article_id 
        where tmi.person_id = '{person_id}'
        and tmi2.person_id <> '{person_id}'
        and tmi.is_deleted = 0
        and tmi2.is_deleted = 0
    """)

    origin_result = execute_query(sql, scalar=False)
    print(f"文章合作者人数：{len(origin_result)}")
    return [item[0] for item in origin_result]


def get_person_society_partner_count(person_id: str) -> List[str]:
    sql = text(f"""
            select distinct tmps2.person_id
            from t_md_person_society tmps
            join t_md_person_society tmps2
            on tmps.society_id = tmps2.society_id
            where tmps.person_id = '{person_id}'
            and tmps2.person_id <> '{person_id}'
            and tmps2.is_deleted = 0
            and tmps.is_deleted = 0
    """)

    origin_result = execute_query(sql, scalar=False)
    print(f"协会合作者人数：{len(origin_result)}")
    return [item[0] for item in origin_result]


def get_person_institution(person_list: List[str]) -> int:
    person_ids_str = ', '.join(f'"{id_}"' for id_ in person_list)
    sql = text(f"""
        SELECT COUNT(DISTINCT institution_id)
        FROM t_md_person_ref_standard
        WHERE is_default = 1 
        AND is_deleted = 0
        AND person_id IN ({person_ids_str})
    """)
    if person_list:
        count = execute_query(sql)
        print(f"去重后合作机构数：{count}")
        return count
    return 0


def get_person_indicator(person_id: str) -> None:
    get_person_article_count(person_id)
    get_person_article_count_last_years(person_id, 3)
    get_person_article_count_last_years(person_id, 5)
    get_person_article_count_by_type(person_id)
    get_person_article_count_by_type(person_id, "correspond")
    get_person_trial_count(person_id)
    get_person_conference_count(person_id)
    get_person_science_article_count(person_id)
    print("x" * 30)

    article_partner_list = get_person_article_partner_id(person_id)
    trial_partner_list = get_person_trial_partner_count(person_id)
    conference_partner_list = get_person_conference_partner_count(person_id)
    cience_article_partner_list = get_person_science_article_partner_count(person_id)
    society_partner_list = get_person_society_partner_count(person_id)

    origin_result = (article_partner_list + trial_partner_list + conference_partner_list + cience_article_partner_list +
                     society_partner_list)
    result = {item for item in origin_result}
    print(f"去重后合作者数量：{len(result)}")
    print(f"去重后合作人：{result}")
    get_person_institution(list(result))
    print("x" * 30)


if __name__ == '__main__':
    get_person_indicator("7d9890d0070d11ecb68200163e1f7c71")
