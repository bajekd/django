import asyncio
import json

import discord
import requests

client = discord.Client()


def update_score(user, points):
    url = "https://drf-discord-quiz.herokuapp.com/api/score/update/"
    new_score = {"name": user, "points": points}
    requests.post(url, data=new_score)


def get_score():
    leaderboard = f"{'Place':^10} | {'Name':^10} | {'Points':^10} | \n"
    response = requests.get("https://drf-discord-quiz.herokuapp.com/api/score/leaderboard/")
    json_data = json.loads(response.text)
    leaderboard += f"{45 * '-'} \n"

    for index, elem in enumerate(json_data, start=1):
        leaderboard += f"{index:^10} | {elem['name']:^10} | {elem['points']:^10} | \n"

    leaderboard += f"{45 * '-'} \n"

    return leaderboard


def get_question():
    question = ""
    correct_answers = []
    response = requests.get("https://drf-discord-quiz.herokuapp.com/api/random/")
    json_data = json.loads(response.text)

    question += "Question: \n"
    question += f"{json_data['title']} \n"
    points = json_data["points"]

    for index, answer in enumerate(json_data["answers"], start=1):
        question += f"{index}) {answer['answer']} \n"

        if answer["is_correct"]:
            correct_answers.append(index)

    return (question, correct_answers, points)


@client.event
async def on_message(message):
    POSSIBLE_ANSWERS = ["1", "2", "3", "4"]

    if message.author == client.user:
        return

    if message.content.startswith("$leaderboard"):
        leaderboard = get_score()
        await message.channel.send(leaderboard)

    if message.content.startswith("$question"):
        question, correct_answers, points = get_question()
        await message.channel.send(question)

        def check(msg):
            # only person who request question can answer on it
            return (msg.author == message.author) and (msg.content in POSSIBLE_ANSWERS)
            # return msg.content in POSSIBLE_ANSWERS # (first come, first served)

        try:
            user_answer = await client.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            return await message.channel.send("Sorry, you take to long to answer. Go back to the shadow!")

        if int(user_answer.content) in correct_answers:
            user = user_answer.author
            await message.channel.send(f"Congraturations! {user.name} got it right! +{points}.")
            update_score(user, points)
        else:
            await message.channel.send("Ops... You SHALL NOT PASS!")


client.run("ODQxNjA4Mjk0NDM0NjAzMDE4.YJpOzQ.aF0Z4-0y6xK93PG5Xl7BW4Xs-Qs")
