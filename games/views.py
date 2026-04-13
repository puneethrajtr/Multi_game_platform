from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import chess

from .forms import RegisterForm, LoginForm, FizzBuzzForm, TicTacToeForm, ChessMoveForm
from .models import PlayerProfile, GameScore
from . import services


def home(request):
    """
    Home page view.
    """
    return render(request, 'home.html')


def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def fizzbuzz_game(request):
    """
    FizzBuzz game view.
    """
    mode = request.GET.get('mode') or request.session.get('fizzbuzz_mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'

    # Reinitialize if mode changed or game not in session.
    if request.session.get('fizzbuzz_mode') != mode or 'fizzbuzz_number' not in request.session:
        request.session['fizzbuzz_mode'] = mode
        request.session['fizzbuzz_number'] = 1
        request.session['fizzbuzz_player1_score'] = 0
        request.session['fizzbuzz_player2_score'] = 0
        request.session['fizzbuzz_turn'] = 'player1'
        request.session['fizzbuzz_game_over'] = False
        request.session['fizzbuzz_winner'] = None
        request.session['fizzbuzz_scored'] = False

    current_number = request.session['fizzbuzz_number']
    player1_score = request.session['fizzbuzz_player1_score']
    player2_score = request.session['fizzbuzz_player2_score']
    turn = request.session.get('fizzbuzz_turn', 'player1')
    game_over = request.session.get('fizzbuzz_game_over', False)
    winner = request.session.get('fizzbuzz_winner')
    game_over_popup = request.session.pop('fizzbuzz_game_over_popup', None)

    def finalize_game(final_winner):
        request.session['fizzbuzz_game_over'] = True
        request.session['fizzbuzz_winner'] = final_winner

        if request.session.get('fizzbuzz_scored'):
            return

        if mode == 'cpu':
            awarded_score = request.session['fizzbuzz_player1_score']
        else:
            awarded_score = max(
                request.session['fizzbuzz_player1_score'],
                request.session['fizzbuzz_player2_score']
            )

        GameScore.objects.create(
            user=request.user,
            game_name='fizzbuzz',
            score=awarded_score
        )

        profile = request.user.profile
        profile.total_score += awarded_score
        profile.games_played += 1
        profile.save()

        request.session['fizzbuzz_scored'] = True

    if request.method == 'POST' and not game_over:
        form = FizzBuzzForm(request.POST)
        if form.is_valid():
            posted_mode = form.cleaned_data.get('mode') or mode
            if posted_mode in ('cpu', 'pvp') and posted_mode != mode:
                return redirect(f'/games/fizzbuzz/?mode={posted_mode}')

            user_answer = form.cleaned_data['answer']
            is_correct = services.validate_fizzbuzz_answer(current_number, user_answer)

            if is_correct:
                if turn == 'player1':
                    request.session['fizzbuzz_player1_score'] += 10
                else:
                    request.session['fizzbuzz_player2_score'] += 10
                request.session['fizzbuzz_number'] += 1

                if mode == 'cpu':
                    request.session['fizzbuzz_turn'] = 'player2'
                    computer_number = request.session['fizzbuzz_number']
                    computer_answer = services.fizzbuzz_computer_answer(computer_number)
                    if services.validate_fizzbuzz_answer(computer_number, computer_answer):
                        request.session['fizzbuzz_player2_score'] += 10
                        request.session['fizzbuzz_number'] += 1
                        request.session['fizzbuzz_turn'] = 'player1'
                        messages.info(request, f'Computer answered {computer_answer} correctly.')
                    else:
                        finalize_game('Player 1')
                        request.session['fizzbuzz_game_over_popup'] = (
                            'Computer made a mistake. You win!'
                        )
                else:
                    request.session['fizzbuzz_turn'] = 'player2' if turn == 'player1' else 'player1'
            else:
                if mode == 'cpu':
                    finalize_game('Computer')
                    player_score = request.session['fizzbuzz_player1_score']
                    request.session['fizzbuzz_game_over_popup'] = (
                        f'Wrong answer. Computer wins! Your score: {player_score}'
                    )
                else:
                    final_winner = 'Player 2' if turn == 'player1' else 'Player 1'
                    finalize_game(final_winner)
                    request.session['fizzbuzz_game_over_popup'] = (
                        f'Wrong answer. {final_winner} wins!'
                    )

            return redirect('fizzbuzz_game')
    else:
        form = FizzBuzzForm(initial={'mode': mode})

    turn_label = 'Player 1' if turn == 'player1' else ('Computer' if mode == 'cpu' else 'Player 2')

    context = {
        'form': form,
        'current_number': current_number,
        'current_score': player1_score,
        'player1_score': player1_score,
        'player2_score': player2_score,
        'mode': mode,
        'turn_label': turn_label,
        'game_over': game_over,
        'winner': winner,
        'game_over_popup': game_over_popup,
    }
    return render(request, 'fizzbuzz.html', context)


@login_required
def fizzbuzz_reset(request):
    """
    Reset FizzBuzz game.
    """
    for key in [
        'fizzbuzz_mode',
        'fizzbuzz_number',
        'fizzbuzz_player1_score',
        'fizzbuzz_player2_score',
        'fizzbuzz_turn',
        'fizzbuzz_game_over',
        'fizzbuzz_winner',
        'fizzbuzz_scored',
        'fizzbuzz_game_over_popup',
    ]:
        if key in request.session:
            del request.session[key]

    mode = request.GET.get('mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'
    return redirect(f'/games/fizzbuzz/?mode={mode}')


@login_required
def tictactoe_game(request):
    """
    TicTacToe game view.
    """
    mode = request.GET.get('mode') or request.session.get('tictactoe_mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'

    # Initialize or reinitialize session state when mode changes.
    if request.session.get('tictactoe_mode') != mode or 'tictactoe_board' not in request.session:
        request.session['tictactoe_mode'] = mode
        request.session['tictactoe_board'] = services.initialize_tictactoe_board()
        request.session['tictactoe_game_over'] = False
        request.session['tictactoe_winner'] = None
        request.session['tictactoe_turn'] = 'X'
        request.session['tictactoe_scored'] = False

    board = request.session['tictactoe_board']
    game_over = request.session.get('tictactoe_game_over', False)
    winner = request.session.get('tictactoe_winner', None)
    current_turn = request.session.get('tictactoe_turn', 'X')

    def finalize_game(result):
        request.session['tictactoe_game_over'] = True
        request.session['tictactoe_winner'] = result

        if request.session.get('tictactoe_scored'):
            return

        score = 0
        if mode == 'cpu':
            if result == 'X':
                score = 50
                messages.success(request, 'You Win! +50 points')
            elif result == 'Draw':
                score = 10
                messages.info(request, 'Draw! +10 points')
            else:
                messages.error(request, 'Computer Wins!')
        else:
            if result == 'Draw':
                score = 10
                messages.info(request, 'Draw! +10 points')
            else:
                score = 30
                messages.success(request, f'{services.get_tictactoe_player_label(result)} wins! +30 points')

        GameScore.objects.create(
            user=request.user,
            game_name='tictactoe',
            score=score
        )

        profile = request.user.profile
        profile.total_score += score
        profile.games_played += 1
        profile.save()

        request.session['tictactoe_scored'] = True
    
    if request.method == 'POST' and not game_over:
        form = TicTacToeForm(request.POST)
        if form.is_valid():
            posted_mode = form.cleaned_data.get('mode') or mode
            if posted_mode in ('cpu', 'pvp') and posted_mode != mode:
                return redirect(f'/games/tictactoe/?mode={posted_mode}')

            position = form.cleaned_data['position']
            
            symbol = current_turn

            if services.is_valid_move(board, position):
                board[position] = symbol
                request.session['tictactoe_board'] = board
                
                result = services.check_winner(board)
                if result:
                    finalize_game(result)
                else:
                    if mode == 'cpu':
                        comp_position = services.tictactoe_move(board)
                        if comp_position is not None:
                            board[comp_position] = 'O'
                            request.session['tictactoe_board'] = board
                            result = services.check_winner(board)
                            if result:
                                finalize_game(result)
                            else:
                                request.session['tictactoe_turn'] = 'X'
                    else:
                        request.session['tictactoe_turn'] = 'O' if symbol == 'X' else 'X'
                
                return redirect('tictactoe_game')
    else:
        form = TicTacToeForm(initial={'mode': mode})
    
    board_with_index = list(enumerate(board))
    board_rows = [board_with_index[i:i+3] for i in range(0, 9, 3)]
    turn_label = services.get_tictactoe_player_label(current_turn)
    if mode == 'cpu' and current_turn == 'O':
        turn_label = 'Computer (O)'
    
    context = {
        'board_rows': board_rows,
        'game_over': game_over,
        'winner': winner,
        'mode': mode,
        'turn_label': turn_label,
        'form': form,
    }
    return render(request, 'tictactoe.html', context)


@login_required
def tictactoe_reset(request):
    """
    Reset TicTacToe game.
    """
    for key in [
        'tictactoe_mode',
        'tictactoe_board',
        'tictactoe_game_over',
        'tictactoe_winner',
        'tictactoe_turn',
        'tictactoe_scored',
    ]:
        if key in request.session:
            del request.session[key]

    mode = request.GET.get('mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'
    return redirect(f'/games/tictactoe/?mode={mode}')


@login_required
def chess_game(request):
    """
    Chess game view.
    """
    mode = request.GET.get('mode') or request.session.get('chess_mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'

    if request.session.get('chess_mode') != mode or 'chess_fen' not in request.session:
        board = services.initialize_chess_board()
        request.session['chess_mode'] = mode
        request.session['chess_fen'] = board.fen()
        request.session['chess_game_over'] = False
        request.session['chess_result'] = None
        request.session['chess_scored'] = False

    board = chess.Board(request.session['chess_fen'])
    game_over = request.session.get('chess_game_over', False)
    result_label = request.session.get('chess_result')

    def finalize_game(current_board):
        request.session['chess_game_over'] = True
        game_result = services.get_chess_result_label(current_board)
        request.session['chess_result'] = game_result

        if request.session.get('chess_scored'):
            return

        score = 0
        if mode == 'cpu':
            if game_result == 'White wins':
                score = 100
                messages.success(request, 'You win! +100 points')
            elif game_result == 'Draw':
                score = 30
                messages.info(request, 'Draw! +30 points')
            else:
                messages.error(request, 'Computer wins!')
        else:
            if game_result == 'Draw':
                score = 30
                messages.info(request, 'Draw! +30 points')
            else:
                score = 70
                messages.success(request, f'{game_result}! +70 points')

        GameScore.objects.create(
            user=request.user,
            game_name='chess',
            score=score,
        )

        profile = request.user.profile
        profile.total_score += score
        profile.games_played += 1
        profile.save()

        request.session['chess_scored'] = True

    if request.method == 'POST' and not game_over:
        form = ChessMoveForm(request.POST)
        if form.is_valid():
            posted_mode = form.cleaned_data.get('mode') or mode
            if posted_mode in ('cpu', 'pvp') and posted_mode != mode:
                return redirect(f'/games/chess/?mode={posted_mode}')

            if mode == 'cpu' and board.turn == chess.BLACK:
                return redirect('chess_game')

            move_text = form.cleaned_data['move']
            move = services.parse_chess_move(board, move_text)

            if move is None:
                messages.error(request, 'Invalid move. Use SAN (e4, Nf3) or UCI (e2e4).')
            else:
                board.push(move)

                if board.is_game_over(claim_draw=True):
                    finalize_game(board)
                elif mode == 'cpu' and board.turn == chess.BLACK:
                    computer_move = services.get_chess_computer_move(board)
                    if computer_move is not None:
                        computer_move_label = board.san(computer_move)
                        board.push(computer_move)
                        messages.info(request, f'Computer move: {computer_move_label}')
                        if board.is_game_over(claim_draw=True):
                            finalize_game(board)

                request.session['chess_fen'] = board.fen()
                return redirect('chess_game')
    else:
        form = ChessMoveForm(initial={'mode': mode})

    piece_glyphs = {
        'K': '♔',
        'Q': '♕',
        'R': '♖',
        'B': '♗',
        'N': '♘',
        'P': '♙',
        'k': '♚',
        'q': '♛',
        'r': '♜',
        'b': '♝',
        'n': '♞',
        'p': '♟',
    }
    piece_names = {
        'K': 'King',
        'Q': 'Queen',
        'R': 'Rook (Elephant)',
        'B': 'Bishop (Camel)',
        'N': 'Knight',
        'P': 'Pawn',
        'k': 'King',
        'q': 'Queen',
        'r': 'Rook (Elephant)',
        'b': 'Bishop (Camel)',
        'n': 'Knight',
        'p': 'Pawn',
    }

    board_rows = []
    for rank in range(7, -1, -1):
        row = []
        for file_index in range(8):
            square = chess.square(file_index, rank)
            piece = board.piece_at(square)
            symbol = piece.symbol() if piece else ''
            row.append(
                {
                    'square': chess.square_name(square),
                    'symbol': symbol,
                    'glyph': piece_glyphs.get(symbol, ''),
                    'name': piece_names.get(symbol, ''),
                    'is_light': (rank + file_index) % 2 == 1,
                }
            )
        board_rows.append(row)

    turn_label = 'White'
    if board.turn == chess.BLACK:
        turn_label = 'Black' if mode == 'pvp' else 'Computer (Black)'

    context = {
        'form': form,
        'mode': mode,
        'board_rows': board_rows,
        'game_over': game_over,
        'result_label': result_label,
        'turn_label': turn_label,
        'turn_color': 'white' if board.turn == chess.WHITE else 'black',
        'can_user_move': (not game_over) and (mode == 'pvp' or board.turn == chess.WHITE),
    }
    return render(request, 'chess.html', context)


@login_required
def chess_reset(request):
    """
    Reset Chess game.
    """
    for key in [
        'chess_mode',
        'chess_fen',
        'chess_game_over',
        'chess_result',
        'chess_scored',
    ]:
        if key in request.session:
            del request.session[key]

    mode = request.GET.get('mode', 'cpu')
    if mode not in ('cpu', 'pvp'):
        mode = 'cpu'
    return redirect(f'/games/chess/?mode={mode}')


def leaderboard(request):
    """
    Leaderboard view showing top players.
    """
    players = PlayerProfile.objects.select_related('user').order_by('-total_score')[:20]
    
    context = {
        'players': players
    }
    return render(request, 'leaderboard.html', context)
