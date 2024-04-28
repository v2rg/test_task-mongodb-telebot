import datetime

from dateutil.relativedelta import relativedelta

from mongo import get_documents


def get_date_steps(request):
    start = datetime.datetime.fromisoformat(request['dt_from'])
    end = datetime.datetime.fromisoformat(request['dt_upto'])
    step = None

    if request['group_type'] == 'hour':
        step = datetime.timedelta(hours=1)  # шаг в 1 час
    elif request['group_type'] == 'day':
        step = datetime.timedelta(days=1)  # шаг в 1 день
    elif request['group_type'] == 'month':
        step = relativedelta(months=1)  # шаг в 1 месяц

    if step:
        date = start

        if request['group_type'] == 'month':
            new_date = datetime.datetime.strftime(date, '%Y, %m')
            date = datetime.datetime.strptime(new_date, '%Y, %m')

            while date <= end:
                yield date
                date += step
        else:
            while date <= end:
                yield date
                date += step


async def get_response(request):
    dates = list(get_documents(
        datetime.datetime.fromisoformat(request['dt_from']),
        datetime.datetime.fromisoformat(request['dt_upto'])
    ))

    result = {
        'dataset': [],
        'labels': []
    }

    group_type = request['group_type']

    if group_type == 'hour':
        date_format = '%Y, %m, %d, %H'
    elif group_type == 'day':
        date_format = '%Y, %m, %d'
    else:
        date_format = '%Y, %m'

    for step in get_date_steps(request):  # генератор get_date_steps
        step_date = datetime.datetime.strftime(step, date_format)

        result['dataset'].append(sum([date['value'] for date in dates if
                                      step_date == datetime.datetime.strftime(date['dt'], date_format)]))
        result['labels'].append(datetime.datetime.isoformat(step))

    return result

# start = time.time()
# print(get_result(request))
# print(round(time.time() - start, 2))
