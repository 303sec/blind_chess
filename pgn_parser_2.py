
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

        # Handle annotations
        move = move.replace('??', ' dubious').replace('?!', ' question mark')
        move = move.replace('+', ' check').replace('#', ' checkmate')
        
        if 'x' in move:
            move = move.replace('x', ' captures on ')

        spoken_move = color

        # Handle exclamations
        move = move.replace('!!', ' double exclam').replace('!', ' exclam')

        if move.startswith(('O-O', '0-0')):
            spoken_move += " castles"
            if 'O-O-O' in move or '0-0-0' in move:
                spoken_move += " queenside"
            else:
                spoken_move += " kingside"
        else:
            piece = "Pawn"  # Default piece is pawn
            for p in pieces_dict:
                if p in move:
                    piece = pieces_dict[p]
                    move = move.replace(p, '', 1)  # Remove piece symbol once
                    break
            target_square = re.sub(r"[+#=!?]+$", "", move)  # Remove annotations from target square
            spoken_move += f" {piece} to {target_square}"
        if "to  captures" in spoken_move:
            spoken_move = spoken_move.replace("to  captures", "captures")
        spoken_moves.append(spoken_move)

        # Change color for next move
        color = "Black" if color == "White" else "White"

    return spoken_moves

# Example PGN (shortened for brevity)
pgn_text = """
1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6! 6. f3 b5 
7. Nge2!? Nbd7 8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3! e5 11. O-O-O Qe7 
12. Kb1 a6 13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 16. Rd1 Nb6 
24. Rxd4!! cxd4?? 25. Re7+! Kb6 
38. Bxc4 bxc4 39. Qxh8 Rd3 $18 40. Qa8 c3 
41. Qa4+ Ke1 42. f4 f5 43. Kc1 Rd2 44. Qa7 *
"""

# Convert PGN to spoken language
spoken_moves = pgn_to_spoken_language(pgn_text)

# Output the spoken language format
for move in spoken_moves:
    print(move)
    print('<break time="3s" />')
