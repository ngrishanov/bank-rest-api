from sanic import response, Sanic
from asyncpg import exceptions

from server.storage.db import db
from server.utils import validate_account_num, validate_account_amount

app = Sanic()


@app.listener('before_server_start')
async def before_server_start(app, loop):
    await db.start()


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    await db.close()


@app.route('/accounts', methods=['POST'])
@validate_account_num('num')
@validate_account_amount('amount')
async def create_account(request):
    num = request.json.get('num')
    amount = request.json.get('amount')

    try:
        await db.execute(
            'INSERT INTO accounts(num, amount) VALUES($1, $2)',
            num,
            amount,
        )
    except exceptions.UniqueViolationError as e:
        return response.json({
            'success': False,
            'error': 'account_already_exists',
        }, status=400)

    return response.json({
        'success': True,
    })


@app.route('/accounts/<num>', methods=['GET'])
async def get_account(request, num):
    try:
        num = int(num)
    except ValueError:
        return response.json({
            'success': False,
            'error': 'invalid_num'
        }, status=400)

    if num <= 0:
        return response.json({
            'success': False,
            'error': 'invalid_num'
        }, status=400)

    account = await db.fetchrow(
        'SELECT num, amount FROM accounts WHERE num = $1',
        num,
    )

    if not account:
        return response.json({
            'success': False,
            'error': 'account_not_found',
        }, status=400)

    return response.json({
        'success': True,
        'result': {
            'num': account['num'],
            'amount': account['amount'],
        },
    })


@app.route('/transfer', methods=['POST'])
@validate_account_num('num_from')
@validate_account_num('num_to')
@validate_account_amount('amount')
async def transfer_amount(request):
    num_from = request.json.get('num_from')
    num_to = request.json.get('num_to')
    amount = request.json.get('amount')

    if num_from == num_to:
        return response.json({
            'success': False,
            'error': 'account_nums_should_be_different',
        }, status=400)

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            account_from = await db.fetchrow(
                'SELECT num, amount FROM accounts WHERE num = $1 FOR UPDATE',
                num_from,
                conn=conn,
            )

            if not account_from:
                return response.json({
                    'success': False,
                    'error': 'account_from_not_found',
                }, status=400)

            if account_from['amount'] - amount < 0:
                return response.json({
                    'success': False,
                    'error': 'not_enough_funds',
                }, status=400)

            account_to = await db.fetchrow(
                'SELECT num, amount FROM accounts WHERE num = $1 FOR UPDATE',
                num_to,
                conn=conn,
            )

            if not account_to:
                return response.json({
                    'success': False,
                    'error': 'account_to_not_found',
                }, status=400)

            amount_from = await db.fetchrow(
                'UPDATE accounts SET amount = amount - $1 WHERE num = $2 RETURNING amount',
                amount,
                num_from,
                conn=conn,
            )

            amount_to = await db.fetchrow(
                'UPDATE accounts SET amount = amount + $1 WHERE num = $2 RETURNING amount',
                amount,
                num_to,
                conn=conn,
            )

    return response.json({
        'success': True,
        'result': {
            'amount_from': amount_from['amount'],
            'amount_to': amount_to['amount'],
        }
    })
