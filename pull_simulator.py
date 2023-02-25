from random import uniform, randint

"""
base prob SSR   -> 0.75/100 -> 0.0075
base prob SR    ->    1/100 -> 0.01

every 80        -> 1 SSR
every 10        -> 1 SR

assumption      -> if alr get SR in 10, no guarantee for SSR
"""
PURCHASE_COST = 120
HARD_PITY = 80
SOFT_PITY = 10

ALREADY_MAXED = 69420
GET_TRASH = -1
GET_LIMITED = 0


SSR_CHARS = 9   # 1 - 9
SR_CHARS = 5    # 10 - 14
CHAR_DICT = {-1: 'Trash', 0: 'Limited', 1: 'King', 
             2: 'Huma', 3: 'Zero', 4: 'Samir', 
             5: 'Crow', 6: 'Tsubasa', 7: 'Cocoritter', 
             8: 'Meryl', 9: 'Shiro', 10: 'Ene', 11: 'Echo', 
             12: 'Pepper', 13: 'Hilda', 14: 'Bai Ling'}

is_print = False


class PullSimulator:
    def __init__(self, star_goal: int=6, existing_pity: int=0, num_a6_standard: int=0,
                 num_chips: int=0, limited_name: str='Limited'):
        # pull counts
        self.num_pulls = 0
        self.num_ssr = 0
        self.num_sr = 0
        self.num_limited = 0
        self.num_bought = 0
        self.limited_stars = -1
        self.pull_history = []
        
        self.ssr_pity = existing_pity
        self.sr_pity = 0
        self.num_ssr_off_pity = 0
        
        self.num_chips = num_chips
        self.num_a6_standard = num_a6_standard
        self.limited_name = limited_name
        
        self.star_goal = star_goal
        
        CHAR_DICT[0] = limited_name
        
        self.COPIES_DICT = {'Trash': 0, limited_name: 0, 'King': 0, 
                            'Huma': 0, 'Zero': 0, 'Samir': 0, 
                            'Crow': 0, 'Tsubasa': 0, 'Cocoritter': 0, 
                            'Meryl': 0, 'Shiro': 0, 'Ene': 0, 'Echo': 0, 
                            'Pepper': 0, 'Hilda': 0, 'Bai Ling': 0}
        
        self.is_print = False
    
    
    def print_stats(self):
        # 50/50s won
        won = (self.num_limited / self.num_ssr)
        
        print("=====================================")
        print(f"Pull stats ({self.num_pulls} pulls):")
        print(f"Total SR Pulled: {self.num_sr}")
        print(f"Total SSR Pulled: {self.num_ssr}")
        print(f"    of which off pity: {self.num_ssr_off_pity}")
        print(f"    of which limited: {self.num_limited} [{won:.2%}]")
        print(f"Remaining chips left: {self.num_chips}")
        print("=====================================")

        # print limited stats
        if self.limited_stars == -1:
            print(f"You did not pull {self.limited_name}")
        else:
            print(f"{self.limited_name} is at {self.limited_stars} stars with {self.num_pulls} pulls")
        print(f"Pulled: {self.num_limited}, Bought: {self.num_bought}")
        print("=====================================")
    
    
    def print_pull_history(self):
        for item in self.pull_history:
            print(item)
    
    
    def print_char_copies(self):
        print("\n=====================================")
        for char, copies in self.COPIES_DICT.items():
            if char == CHAR_DICT[GET_LIMITED]:
                print("\nSSRs:\n==============")
            elif char == CHAR_DICT[SSR_CHARS + 1]:
                print("\nSRs:\n==============")
            if copies > 0:
                print(f"{char}: {copies}")
        print("=====================================")
        
    def single_pull(self, is_limited: bool=True):
        if self.limited_stars == self.star_goal:
            return ALREADY_MAXED

        # gets a % chance between 0 to 100
        rolled_chance = roll_p()

        self.num_pulls += 1
        self.num_chips += 1
        self.sr_pity += 1
        self.ssr_pity += 1
        
        # hard pity
        if self.ssr_pity == HARD_PITY:
            obtained_char = self.choose_limited() if is_limited else self.choose_standard()
            
            self.num_ssr += 1
            self.ssr_pity = 0
            
            # if also sr pity, reset sr pity (rip lol)
            if self.sr_pity == SOFT_PITY:
                self.sr_pity = 0
                
                
            # if ssr is limited, add 1 star
            if obtained_char == GET_LIMITED:
                self.limited_stars += 1
            
        else:   # off pity
            # gets ssr
            if 0 < rolled_chance <= 0.75:
                self.num_ssr += 1
                self.num_ssr_off_pity += 1
                obtained_char = self.choose_limited() if is_limited else self.choose_standard()
                
                # if ssr is limited, add 1 star
                if obtained_char == GET_LIMITED:
                    self.limited_stars += 1
                    
                else:   # if ssr is not limited, it belongs to standard 
                    standard_ssr = randint(1, SSR_CHARS)
                    
                    # if dupe, get 10 chips
                    is_dupe = (standard_ssr <= self.num_a6_standard)
                    if is_dupe:
                        self.num_chips += 10
                        
            # gets sr
            elif 0.75 < rolled_chance <= 1.75 or self.sr_pity == SOFT_PITY:
                self.sr_pity = 0
                    
                self.num_sr += 1
                self.num_chips += 1
                
                obtained_char = self.choose_sr()
            
            # gets r
            else:
                obtained_char = GET_TRASH        
        
        # add to history if not trash
        if obtained_char != GET_TRASH:
            self.add_history(obtained_char)
            print(f"Pull {self.num_pulls}: {CHAR_DICT[obtained_char]}") if self.is_print else None
        
        # update and print if limited
        if obtained_char == GET_LIMITED:
            self.num_limited += 1
            print(f"    {self.limited_name} now at A{self.limited_stars}") if self.is_print else None
            
        
        # buy all possible copies up to needed for A6
        if self.num_chips >= PURCHASE_COST and \
                self.limited_stars < self.star_goal:
            # buy 1 copy
            self.num_chips -= PURCHASE_COST
            self.limited_stars += 1
            self.num_bought += 1
            self.pull_history.append((-1, self.limited_name))
            print(f"Bought 1 copy of {self.limited_name}, now at A{self.limited_stars}") if self.is_print else None
        
        # update copies dict
        self.COPIES_DICT[CHAR_DICT[obtained_char]] += 1
        
        return obtained_char
    
    
    def add_history(self, obtained_char):
        char_str = CHAR_DICT[obtained_char]
        self.pull_history.append((self.num_pulls, char_str))
    
    
    @staticmethod
    def choose_limited():
        # choose which ssr obtained
        # limiteds have 50% chance of rolling
        # the other 9 ssr share remaining roll chance equally
        
        rolled_chance = uniform(0, 100)
        
        if rolled_chance >= 50:
            return GET_LIMITED
        else:
            rolled_standard_ssr = randint(1, SSR_CHARS)
            return rolled_standard_ssr
        
        
    @staticmethod
    def choose_standard():
        # choose which ssr obtained
        # 9 ssr share roll chance equally
        rolled_standard_ssr = randint(1, SSR_CHARS)
        return rolled_standard_ssr


    @staticmethod
    def choose_sr():
        # choose which sr obtained
        rolled_standard_sr = randint(1, SR_CHARS) + SSR_CHARS
        return rolled_standard_sr
    


# helper functions
    
def roll_p():
    # outputs chance as percentage
    return uniform(0.0, 100.0)


if __name__ == '__main__':
    is_print = True
    