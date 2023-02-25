from pull_simulator import PullSimulator, ALREADY_MAXED
from time import time


class PlayerSimulator:
    def __init__(self, sample_size: int=10000, star_goal: int=6, existing_pity: int=0, num_a6_standard: int=0):
        self.sample_size = sample_size
        
        # pull simulator parameters
        self.star_goal = star_goal
        self.existing_pity = existing_pity
        self.num_a6_standard = num_a6_standard
        
        # statistics results
        self.players = []
        self.num_players = 0
        self.total_pulls = 0
        self.luckiest = 0
        self.average = 0
        self.unluckiest = 0

    def run(self):
        start = time()
        print(f"Running {self.sample_size} simulations with {self.star_goal} star goal, {self.existing_pity} existing pity, and {self.num_a6_standard} A6 standards")        
        
        for _ in range(self.sample_size):
            # create a pull simulator
            cur_player = PullSimulator(star_goal=self.star_goal, existing_pity=self.existing_pity, num_a6_standard=self.num_a6_standard)
            for _ in range(1000):
                obtained_char = cur_player.single_pull()    
                if obtained_char == ALREADY_MAXED:
                    break

            # calculate statistics
            self.num_players += 1
            self.total_pulls += cur_player.num_pulls
            
            if self.luckiest == 0 or cur_player.num_pulls < self.luckiest.num_pulls:
                self.luckiest = cur_player
            
            if self.unluckiest == 0 or cur_player.num_pulls > self.unluckiest.num_pulls:
                self.unluckiest = cur_player
        
        self.average = self.total_pulls / self.num_players
        
        print(f"Finished in {time() - start:.3f} seconds")


    def print_results(self):
        # luckiest player
        self.luckiest.print_stats()
        
        # unluckiest player
        self.unluckiest.print_stats()
        
        print(f"Average number of pulls to A6: {self.average}")


if __name__ == '__main__':
    player = PlayerSimulator(sample_size=100000, star_goal=6, existing_pity=10, num_a6_standard=4)
    player.run()
    player.print_results()