from flaskr.celery_conf import celery_app
from flaskr.api.services import PPPData, ExchangeRateData, CurrencyData, GenerateData
from celery import chain


@celery_app.task
def work_PPP_gen(*args) -> bool:
    """Celery task to generate the PPP data asynchronously

    Returns:
        bool: True if the task was successfull else False
    """
    
    serve_api = PPPData()
    flag = serve_api.get_ppp_data()
    
    return flag

@celery_app.task
def work_ExchRate_gen(*args) -> bool:
    """Celery task to generate the Exchange rate data asynchronously

    Returns:
        bool: True if the task was successfull else False
    """
    serve_api = ExchangeRateData()
    flag = serve_api.get_exch_rate_data()

    return flag

@celery_app.task
def work_Currency_gen(*args) -> bool:
    """Celery task to generate the Currency data asynchronously

    Returns:
        bool: True if the task was successfull else False
    """
    serve_api = CurrencyData()
    flag = serve_api.get_currency_data()

    return flag

@celery_app.task
def work_MergedData_gen(*args) -> bool:
    """Celery task to generate the Final data after merging required ones
    asynchronously

    Returns:
        bool: True if the task waas successfull else False
    """
    serve_api = GenerateData()
    flag = serve_api.generate_merged_final_data()

    return flag

@celery_app.task
def task_flow_ConversionModuleData(*args):
    """Task flow for generation of data required by the salary value
    conversion module __ to be run at a particular interval of time __
    """
    # Tasks to be executed in group
    task_sign_ppp = work_PPP_gen.s()
    task_sign_exch_rate = work_ExchRate_gen.s()
    task_sign_currency = work_Currency_gen.s()
    final_merge_task = work_MergedData_gen.s()
    # Creating a chain to sequentially execute tasks
    task_chain = chain(task_sign_ppp, task_sign_exch_rate, task_sign_currency, final_merge_task)
    # Starting async execution
    task_result = task_chain.apply_async()

    return None








    