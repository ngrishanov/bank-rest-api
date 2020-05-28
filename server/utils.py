from functools import wraps

from sanic import response


def validate_account_num(key):
    def decorator(func):
        @wraps(func)
        async def func_wrapper(request, *args, **kwargs):
            num = request.json.get(key)

            if num is None:
                return response.json({
                    'success': False,
                    'error': 'invalid_num',
                }, status=400)

            if not isinstance(num, int):
                return response.json({
                    'success': False,
                    'error': 'invalid_num',
                }, status=400)

            if num <= 0:
                return response.json({
                    'success': False,
                    'error': 'invalid_num',
                }, status=400)

            return await func(request, *args, **kwargs)

        return func_wrapper

    return decorator


def validate_account_amount(key):
    def decorator(func):
        @wraps(func)
        async def func_wrapper(request, *args, **kwargs):
            amount = request.json.get(key)

            if amount is None:
                return response.json({
                    'success': False,
                    'error': 'invalid_amount',
                }, status=400)

            if not isinstance(amount, int):
                return response.json({
                    'success': False,
                    'error': 'invalid_amount',
                }, status=400)

            if amount < 0:
                return response.json({
                    'success': False,
                    'error': 'invalid_amount',
                }, status=400)

            return await func(request, *args, **kwargs)

        return func_wrapper

    return decorator
