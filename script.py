#!/usr/bin/python3

import discord
import secrets
import random
import re
import numpy as np
import math

# TODO:
# Better user input
# Visible opening position

# 99 mines max

client = discord.Client()


status = "Minesweeper"

message_regex = re.compile(r"minesweep(er)?( ([12]\d|[5-9]))?")
num_regex = re.compile(r"\d?\d")


def generate_board(rows, columns, num_mines):
    board = [[0 for i in range(0, columns)] for j in range(0, rows)]

    board_coordinates = [(x, y) for x in range(0, rows)
                         for y in range(0, columns)]
    mine_coordinates = random.sample(board_coordinates, num_mines)

    for mine in mine_coordinates:
        x, y = mine
        board[x][y] = 9
        neighbors = [(x - 1, y), (x - 1, y + 1), (x, y - 1), (x + 1, y - 1),
                     (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y - 1)]
        for n in neighbors:
            if 0 <= n[0] < rows and 0 <= n[1] < columns and n not in mine_coordinates:
                board[n[0]][n[1]] += 1

    return board


def convert(board, zero_emote="zero", bomb_emote="a"):
    message = ""
    emotes = [zero_emote, "one", "two", "three", "four",
              "five", "six", "seven", "eight", bomb_emote]

    for row in board:
        for square in row:
            message += f"||:{emotes[square]}:||"
        message += "\n"

    return message


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(status))


rows = 9
columns = 11

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel

    message_content = message.clean_content.lower()

    if message_regex.match(message_content):
        num_input = num_regex.search(message_content)
        num_squares = rows * columns
        num_mines = 15
        if num_input:
            num_mines = int(num_input.group(0))
        await channel.send(f"creating {rows}x{columns} board with {num_mines} mines")
        if num_squares < 100:
            await channel.send(convert(generate_board(rows, columns, num_mines)))
        else:
            board = generate_board(rows, columns, num_mines)
            parts = np.array_split(board, math.ceil(num_squares / 99))
            for part in parts:
                await channel.send(convert(list(part)))

client.run(secrets.token)
