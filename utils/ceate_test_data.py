from enum import Enum


class DataType(Enum):
    CALL = 'call process'
    COACH = 'coach process'
    CURRENT_MONTH_FLOW = 'current month flow process'


def get_data(data_type: DataType):
    match data_type:
        case DataType.CURRENT_MONTH_FLOW:
            CreatTestData.month_flow_process()
        case DataType.CALL:
            CreatTestData.call_process()
        case _:
            return


class CreatTestData:

    @classmethod
    def month_flow_process(cls):

        pass

    @classmethod
    def call_process(cls):
        pass
