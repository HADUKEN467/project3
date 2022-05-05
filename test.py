import random
from config import settings, variants, num_v, answers
from discord.ext import commands

bot = commands.Bot(command_prefix=settings['prefix'])


@bot.event
async def on_ready():
    print('Бот запущен!')


@bot.command()
async def helpme(ctx1):
    await ctx1.send('!exam - начать решение варианта')
    await ctx1.send('Если после команды !exam поступило сообщение другого рода, то ответ сбрасывается и команду нужно '
                    'прописать снова')
    await ctx1.send('После того как бот выдаст вариант будут записываться следующие 18 сообщений (т.к. 18 заданий)')
    await ctx1.send('Ответы записывать без пробелов. Также в десятичных числах использовать запятую, а не точку ('
                    'Пример:-0,89)')
    await ctx1.send('В заданиях 12, 14, 17 корни и промежутки записывать через пробел, а также в порядке по '
                    'возрастанию (Пример: "-9/6π -3π -3/2π -π" или "(-∞;-2] {0} (64;∞)"')
    await ctx1.send('Корень записывается , как sqrt() и со степенью так (Пример: корень из 225 - sqrt(255)), '
                    'кубический корень из 255 - sqrt3(255)')
    await ctx1.send('В задании 18 нужно будет написать 3 сообщения (1 - a, 2 - b, 3 - c)')
    await ctx1.send('Если в одном из сообщений в ответе будет несколько чисел нужно написать как в примере(Пример: 56 '
                    'и 67)')
    await ctx1.send('В задании 18 в букве b нужно писать ответ с маленькой буквы (Пример: "нет")')
    await ctx1.send('Логарифм пишется так (Пример: log3(2) - логарифм двух по основанию трёх)')
    await ctx1.send('Степень пишется так (Пример: 2**3 - два в третьей степени)')


@bot.command()
async def exam(ctx):
    def check(m):
        return m.author.id == ctx.author.id
    await ctx.send('Напишите номер варианта от 165 до 174 включительно')
    await ctx.send('Либо напишите команду !random')
    await ctx.send('Символы для ответов - ∞, π')
    answer = await bot.wait_for("message", check=check, timeout=30)
    answer = answer.content
    flag = True
    # выдача варианта
    for i in num_v:
        if answer == i:
            flag = False
            await ctx.send('Максимальное кол-во баллов 31')
            await ctx.send('Чтобы сбросить решение варианта нужно написать слово "отмена"')
            await ctx.send(variants[answer])
            num = str(i)
            break
    random_var = ''
    if answer == '!random':
        await ctx.send('Максимальное кол-во баллов 31')
        await ctx.send('Чтобы сбросить решение варианта нужно написать слово "отмена"')
        random_var = variants[random.choice(num_v)]
        await ctx.send(random_var)
    # запись ответов в переменную res
    res = []
    for i in range(1, 19):
        answer1 = await bot.wait_for("message", check=check, timeout=999999)
        answer1 = answer1.content
        if answer1.capitalize() == 'Отмена':
            await ctx.send('Решение варианта сброшено')
            break
        if i == 12 or i == 14 or i == 17:
            res.append(answer1.split())
            await ctx.send('Ответ записан!')
            continue
        elif i == 18:
            res1 = {}
            res1['a'] = answer1
            answer1 = await bot.wait_for("message", check=check, timeout=999999)
            answer1 = answer1.content
            res1['b'] = answer1
            answer1 = await bot.wait_for("message", check=check, timeout=999999)
            answer1 = answer1.content
            res1['c'] = answer1
            res.append(res1)
            await ctx.send('Ответ записан!')
            continue
        res.append(answer1)
        await ctx.send('Ответ записан!')
    # проверка ответов
    count = 0   # баллы
    if flag:
        for i in range(18):
            if res[i] == answers[random_var][i]:
                if 1 <= i <= 11:
                    count += 1
                elif i == 13 or i == 16:
                    count += 3
                elif i == 17 or i == 18:
                    count += 4
                else:
                    count += 2
    else:
        for i in range(18):
            if res[i] == answers[answer][i]:
                if 1 <= i <= 11:
                    count += 1
                elif i == 13 or i == 16:
                    count += 3
                elif i == 17 or i == 18:
                    count += 4
                else:
                    count += 2
    await ctx.send(str(count))


bot.run(settings['token'])
