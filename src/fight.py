from typing import List, Optional

from enums.fight_results import FightResult


class Fight:
    def __init__(self):
        self.result: List[Optional[int]] = [None, None]
        self.fight_result: FightResult = FightResult.tie

    def take_fight_result(self) -> None:
        if self.result[0] > self.result[1]:
            self.fight_result = FightResult.first_player
        if self.result[0] < self.result[1]:
            self.fight_result = FightResult.second_player

    def player_win(self, player_number: int) -> bool:
        if player_number == 0 and self.fight_result == FightResult.first_player:
            return True
        elif player_number == 1 and self.fight_result == FightResult.second_player:
            return True
        else:
            return False

    def text_to_user(self, winner: bool) -> str:
        if self.fight_result == FightResult.tie:
            return "Tie!"
        elif winner:
            return "You won!!!"
        else:
            return "You lose :("



