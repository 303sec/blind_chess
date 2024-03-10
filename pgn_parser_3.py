import re

def pgn_to_spoken_language(pgn_text):
    # Remove comments and variations
    pgn_text = re.sub(r"\{[^}]*\}", "", pgn_text)  # Remove comments
    pgn_text = re.sub(r"\([^)]*\)", "", pgn_text)  # Remove variations

    # Splitting moves
    moves = pgn_text.strip().split()

    spoken_moves = []
    color = "White"

    # Dictionary for piece abbreviations
    pieces_dict = {"N": "Knight", "B": "Bishop", "Q": "Queen", "K": "King", "R": "Rook"}

    # Process each move
    for move in moves:
        if move[0].isdigit():  # Skip move numbers
            continue

        # Handle annotations and special characters
        move = move.replace('??', '').replace('?!', '')
        move = move.replace('+', ' check').replace('#', ' checkmate')
        move = move.replace('!!', '').replace('!', ' ')

        spoke_move_prefix = color
        disambiguation = ""

        if 'x' in move:
            move = move.replace('x', ' captures on ')
        
        if move.startswith(('O-O', '0-0')):
            spoke_move_prefix += " castles"
            if 'O-O-O' in move or '0-0-0' in move:
                spoke_move_prefix += " queenside"
            else:
                spoke_move_prefix += " kingside"
            spoken_moves.append(spoke_move_prefix)
            color = "Black" if color == "White" else "White"
            continue
        
        # Extract any disambiguation (file, rank, or file and rank)
        match = re.match(r"([NBRQK])([a-h1-8]?)([a-h][1-8])", move)
        if match:
            piece, disambiguation_data, target_square = match.groups()
            piece_name = pieces_dict[piece]

            # If the disambiguation data is numeric, it's specifying a rank, otherwise it's a file
            if disambiguation_data.isnumeric():
                disambiguation = f" on rank {disambiguation_data}"
            elif disambiguation_data.isalpha():
                disambiguation = f" on file {disambiguation_data}"
            
            target_square = re.sub(r"[+#=!?]+$", "", target_square)  # Remove annotations from the target square
            move_description = f" {piece_name}{disambiguation} to {target_square}"
            if " to  captures" in move_description:
                move_description = move_description.replace(" to  captures", " captures")
            spoke_move_prefix += move_description
        else:  # This block is for pawns or unclear piece moves
            # Your existing handling for non-disambiguation moves (e.g., pawn moves, unclear piece moves)
            piece = "Pawn"
            for p in pieces_dict:
                if p in move:
                    piece = pieces_dict[p]
                    move = move.replace(p, '', 1)  # Remove piece symbol once
                    break
            target_square = re.sub(r"[+#=!?]+$", "", move)  # Remove annotations from target square
            spoke_move_prefix += f" {piece} to {target_square}"
            if " to  captures" in spoke_move_prefix:
                spoke_move_prefix = spoke_move_prefix.replace(" to  captures", " captures")
            # Regex to change 'Pawn to {} captures' to 'Pawn on {} captures'
            # spoke_move_prefix = re.sub(r"Pawn to ([a-h][1-8]) captures", r"Pawn on \1 captures", spoke_move_prefix)
        
        spoken_moves.append(spoke_move_prefix)

        # Change color for next move
        color = "Black" if color == "White" else "White"

    return spoken_moves


# Example PGN (shortened for brevity)
pgn_text = """
1. e4 { The game starts with the pirc defense. This game was played in 1999 and it is known as Kasparovs immortal game! } (1. c4) 1... d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6! 6. f3 b5 7. Nge2!? Nbd7 8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3! e5 11. O-O-O Qe7 12. Kb1 a6 13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 16. Rd1 Nb6 17. g3 Kb8 18. Na5 Ba8 19. Bh3 d5 20. Qf4+ Ka7 21. Rhe1 d4 22. Nd5! Nbxd5 23. exd5 Qd6 24. Rxd4!! cxd4?? (24... Kb6 25. b4 Qxf4 26. Rxf4 Nxd5 27. Rxf7 cxb4 28. axb4 Nxb4 29. Nb3) 25. Re7+! { This is a double rook sacrifice but blacks king is weak. How does kasparov make the most out of the situation? } 25... Kb6 (25... Qxe7 26. Qxd4+ Kb8 27. Qb6+ Bb7 28. Nc6+ Ka8 29. Qa7#) 26. Qxd4+ Kxa5 27. b4+ Ka4 28. Qc3! { Threatening mate on b3 } 28... Qxd5 29. Ra7 Bb7 30. Rxb7! Qc4 31. Qxf6 Kxa3 32. Qxa6+ Kxb4 33. c3+!! Kxc3 34. Qa1+ Kd2 35. Qb2+ Kd1 36. Bf1!! { Only winning move! } 36... Rd2 (36... Qxf1 37. Qc2+ Ke1 38. Re7+) 37. Rd7!! Rxd7 38. Bxc4 bxc4 39. Qxh8 Rd3 40. Qa8 c3 41. Qa4+ Ke1 42. f4 f5 43. Kc1 Rd2 44. Qa7 { Kasparov, Garry - Topalov, Veselin, 1-0, Hoogovens, 1999, https://lichess.org/9gFZXLl5 } *
"""

# Convert PGN to spoken language
spoken_moves = pgn_to_spoken_language(pgn_text)

# Output the spoken language format
for move in spoken_moves:
    print(move, '...')
