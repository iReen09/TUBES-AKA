import time
from time import perf_counter
from dataclasses import dataclass
from typing import List
import math

@dataclass
class PlayerStats:
    name: str
    shooting: float
    speed: float
    passing: float
    dribbling: float
    defense: float
    strength: float

@dataclass
class Team:
    name: str
    players: List[PlayerStats]
    formation: str
    team_spirit: float

@dataclass
class PredictionResult:
    team1_name: str
    team2_name: str
    team1_strength: float
    team2_strength: float
    team1_win_prob: float
    predicted_score: str
    execution_time: float
    iterations: int

class MatchPredictor:
    def init(self):
        self.iteration_count = 0

    def calculate_team_strength_iterative(self, team: Team) -> tuple[float, float]:
        start_time = perf_counter()
        total_strength = 0.0
        self.iteration_count = 0

        for player in team.players:
            player_contribution = (
                player.shooting * 0.2 +
                player.speed * 0.15 +
                player.passing * 0.15 +
                player.dribbling * 0.15 +
                player.defense * 0.2 +
                player.strength * 0.15
            )
            total_strength += player_contribution
            self.iteration_count += 1

        formation_bonus = {
            "4-3-3": 1.1,
            "4-4-2": 1.0,
            "5-3-2": 0.9,
            "3-5-2": 1.05,
        }

        bonus = formation_bonus.get(team.formation, 1.0)
        final_strength = (total_strength / len(team.players)) * bonus * (team.team_spirit / 100)
        execution_time = perf_counter() - start_time

        return final_strength, execution_time

    def calculate_team_strength_recursive(self, team: Team, player_index: int, total_strength: float) -> tuple[float, float]:
        if player_index == 0:
            self.start_time = perf_counter()

        if player_index >= len(team.players):
            formation_bonus = {
                "4-3-3": 1.1,
                "4-4-2": 1.0,
                "5-3-2": 0.9,
                "3-5-2": 1.05,
            }

            bonus = formation_bonus.get(team.formation, 1.0)
            final_strength = (total_strength / len(team.players)) * bonus * (team.team_spirit / 100)
            return final_strength, perf_counter() - self.start_time

        player = team.players[player_index]
        player_contribution = (
            player.shooting * 0.2 +
            player.speed * 0.15 +
            player.passing * 0.15 +
            player.dribbling * 0.15 +
            player.defense * 0.2 +
            player.strength * 0.15
        )

        self.iteration_count += 1

        return self.calculate_team_strength_recursive(
            team, player_index + 1, total_strength + player_contribution
        )

    def predict_match_result(self, team1: Team, team2: Team, algorithm: str) -> PredictionResult:
        self.iteration_count = 0

        if algorithm == "iterative":
            team1_strength, time1 = self.calculate_team_strength_iterative(team1)
            team2_strength, time2 = self.calculate_team_strength_iterative(team2)
        else:
            self.start_time = time.time()
            team1_strength, time1 = self.calculate_team_strength_recursive(team1, 0, 0)
            self.start_time = time.time()
            team2_strength, time2 = self.calculate_team_strength_recursive(team2, 0, 0)

        total_strength = team1_strength + team2_strength
        team1_win_prob = team1_strength / total_strength

        team1_goals = round(team1_strength / 20)
        team2_goals = round(team2_strength / 20)

        return PredictionResult(
            team1_name=team1.name,
            team2_name=team2.name,
            team1_strength=team1_strength,
            team2_strength=team2_strength,
            team1_win_prob=team1_win_prob * 100,
            predicted_score=f"{team1_goals}-{team2_goals}",
            execution_time=round(time1 + time2, 8),  # Round total execution time to 6 decimal places
            iterations=self.iteration_count
        )

def get_valid_float_input(prompt: str, min_val: float, max_val: float) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Masukkan angka antara {min_val} dan {max_val}")
        except ValueError:
            print("Masukkan angka yang valid")

def input_player_stats(player_number: int) -> PlayerStats:
    print(f"\nMasukkan statistik untuk Pemain {player_number}:")
    name = input("Nama pemain: ")

    return PlayerStats(
        name=name,
        shooting=get_valid_float_input("Shooting rating (0-100): ", 0, 100),
        speed=get_valid_float_input("Speed rating (0-100): ", 0, 100),
        passing=get_valid_float_input("Passing rating (0-100): ", 0, 100),
        dribbling=get_valid_float_input("Dribbling rating (0-100): ", 0, 100),
        defense=get_valid_float_input("Defense rating (0-100): ", 0, 100),
        strength=get_valid_float_input("Strength rating (0-100): ", 0, 100)
    )

def input_team_data() -> Team:
    print("\n=== Input Data Tim ===")
    team_name = input("Nama tim: ")

    while True:
        formation = input("Formasi (4-3-3/4-4-2/5-3-2/3-5-2): ")
        if formation in ["4-3-3", "4-4-2", "5-3-2", "3-5-2"]:
            break
        print("Formasi tidak valid. Pilih dari opsi yang tersedia.")

    team_spirit = get_valid_float_input("Team Spirit (0-100): ", 0, 100)

    print("\nMasukkan statistik untuk 5 pemain:")
    players = [input_player_stats(i + 1) for i in range(11)]

    return Team(
        name=team_name,
        players=players,
        formation=formation,
        team_spirit=team_spirit
    )

def display_prediction_result(result_iterative: PredictionResult, result_recursive: PredictionResult):
    print("+--------+----------------+------------+------------------------+------------------------+------------------------+------------------------+")
    print("| Nomor  | Nama Tim       | Kekuatan   | Prob. Menang (Iteratif)| Prob. Menang (Rekursif)| Waktu (Iteratif/Detik) | Waktu (Rekursif/Detik) |")
    print("+--------+----------------+------------+------------------------+------------------------+------------------------+------------------------+")

    print(f"| {'1':<6} | {result_iterative.team1_name:<14} | {result_iterative.team1_strength:<10.2f} | "
          f"{result_iterative.team1_win_prob:<22.2f}%| {result_recursive.team1_win_prob:<22.2f}%| "
          f"{result_iterative.execution_time:<22.8f} | {result_recursive.execution_time:<22.8f} |")

    print(f"| {'2':<6} | {result_iterative.team2_name:<14} | {result_iterative.team2_strength:<10.2f} | "
          f"{(100 - result_iterative.team1_win_prob):<22.2f}%| {(100 - result_recursive.team1_win_prob):<22.2f}%| "
          f"{result_iterative.execution_time:<22.8f} | {result_recursive.execution_time:<22.8f} |")

    print("+--------+----------------+------------+------------------------+------------------------+------------------------+------------------------+")

    print("\nPrediksi Skor (Iteratif):", result_iterative.predicted_score)
    print("Prediksi Skor (Rekursif):", result_recursive.predicted_score)


def main():
    while True:
        print("=== Program Prediksi Pertandingan PES ===")
        print("Silakan masukkan data untuk kedua tim.")

        print("\nData Tim 1:")
        team1 = input_team_data()
        print("\nData Tim 2:")
        team2 = input_team_data()

        predictor = MatchPredictor()

        print("\n=== Hasil Analisis ===")

        result_iterative = predictor.predict_match_result(team1, team2, "iterative")
        result_recursive = predictor.predict_match_result(team1, team2, "recursive")

        display_prediction_result(result_iterative, result_recursive)

        if input("\nIngin melakukan prediksi lagi? (y/n): ").lower() != 'y':
            print("Terima kasih telah menggunakan program prediksi PES!")
            break

if __name__ == "__main__":
    main()