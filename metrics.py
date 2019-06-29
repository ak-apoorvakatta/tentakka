import numpy as np
import random
from dbmanager import *

def log_transform(track):
    return (np.log(track) - np.log(track.shift(1))).dropna()


def generate_mean(track):
    return (log_transform(track).describe().T[['mean']] * 100).mean().item()


def generate_std(track):
    return (log_transform(track).describe().T[['std']] * 100).mean().item()


def generate_sharpe(track):
    return generate_mean(track) / generate_std(track)


def generate_sortino(track):
    target = 0.0
    logged = log_transform(track)
    logged['downside_returns'] = 0

    logged.loc[logged[logged.columns[0]] < target, 'downside_returns'] = logged[logged.columns[0]] ** 2
    expected_return = logged[logged.columns[0]].mean()
    down_stdev = np.sqrt(logged['downside_returns'].mean())
    sortino_ratio = expected_return / down_stdev

    return sortino_ratio


def generate_win_count(track):
    logged = log_transform(track)
    return logged[logged > 0.0].count().sum()


def generate_avg_win(track):
    logged = log_transform(track)
    return logged[logged > 0.0].mean().mean()


def generate_loss_count(track):
    logged = log_transform(track)
    return logged[logged < 0.0].count().sum()


def generate_avg_loss(track):
    logged = log_transform(track)
    return logged[logged < 0.0].mean().mean()


def maxDD(xs):
    i = np.argmax(np.maximum.accumulate(xs) - xs)  # end of the period
    j = np.argmax(xs[:i])
    return xs[i] - xs[j]


def generate_maxDD(track):
    logged = log_transform(track)
    track = logged.values.flatten()
    return maxDD(track)


def generate_expectancy(track):
    return generate_avg_win(track) * (
            generate_win_count(track) / (generate_win_count(track) +
                                         generate_loss_count(track))
    ) - generate_avg_loss(track) * (
                       generate_loss_count(track) / (generate_win_count(track) + generate_loss_count(track)))


def generate_metrics(track):
    return {'mean': generate_mean(track),
            'std': generate_std(track),
            'expectancy': generate_expectancy(track),
            'maxDD': 1 / generate_maxDD(track),
            'sharpe': generate_sharpe(track),
            'sortino': generate_sortino(track)}


def generate_odd(room):
    sum_of_returns = np.sum([abs(strat['predicted_return']) for strat in room])
    return [1 / (0.5 + (strat['predicted_return'] / sum_of_returns)) for strat in room]


def generate_trader_strategy_metrics():
    predicted_returns = []
    traders = select_all('public', 'trader_tracks').traderid.unique().tolist()
    for t in traders:
        t_tracks = select_where('public', 'trader_tracks', 'traderid', '=', t)
        strategies = t_tracks.strategyid.unique().tolist()
        for s in strategies:
            t_track = t_tracks.query('strategyid == @s', engine='python')[['dateindex', 'value']].set_index('dateindex')
            metrics_test = generate_metrics(t_track)
            predicted_returns.append(
                {'traderid': t,
                 'strategyid': s,
                 'strategy_metrics': metrics_test,
                 'predicted_return': getcoeff.dot(
                     [metrics_test['expectancy'], metrics_test['maxDD'], metrics_test['sharpe']])})

    return predicted_returns

def generate_traders_for_room(metrics_for_traders):

    room = [metrics_for_traders.pop(metrics_for_traders.index(random.choice(metrics_for_traders)))for i in range(0,10)]
    [i.update({'odds_of_win': j}) for i, j in list(zip(room, generate_odd(room)))]

    return room